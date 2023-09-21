import os
import time
from datetime import datetime

import scripts.ch_lib.model as model
from api import utils
from api.model import Model
from api.model_version import ModelVersion
from api.model_version_snapshot import ModelVersionSnapshot
from scripts.ch_lib import civitai
from scripts.ch_lib import util
from scripts.ch_lib import downloader

root_path = os.getenv('MODEL_BASE_PATH')

model.folders = {
    "ti": os.path.join(root_path, "public", "embeddings"),
    "hyper": os.path.join(root_path, "public", "hypernetworks"),
    "ckp": os.path.join(root_path, "public", "Stable-diffusion"),
    "lora": os.path.join(root_path, "public", "Lora"),
}

model_version_snapshot_list = []


def scan_models(scan_model_types: list, max_size_preview: bool, skip_nsfw_preview: bool):
    util.printD("Start scan_model")
    output = ""

    # check model types
    if not scan_model_types:
        output = "Model Types is None, can not scan."
        util.printD(output)
        return output

    model_types = []
    # check type if it is a string
    if type(scan_model_types) == str:
        model_types.append(scan_model_types)
    else:
        model_types = scan_model_types

    model_count = 0
    image_count = 0

    _models = []
    # scan_log = ""
    for model_type, model_folder in model.folders.items():
        if model_type not in model_types:
            continue

        util.printD("Scanning path: " + model_folder)
        for root, dirs, files in os.walk(model_folder, followlinks=True):
            for filename in files:
                # check ext
                item = os.path.join(root, filename)
                base, ext = os.path.splitext(item)
                if ext in model.exts:
                    # ignore vae file
                    if len(base) > 4:
                        if base[-4:] == model.vae_suffix:
                            # find .vae
                            util.printD("This is a vae file: " + filename)
                            continue

                    # find a model
                    # get info file
                    info_file = base + civitai.suffix + model.info_ext
                    # check info file
                    if not os.path.isfile(info_file):
                        util.printD("Creating model info for: " + filename)
                        # get model's sha256
                        hash = util.gen_file_sha256(item)

                        if not hash:
                            output = "failed generating SHA256 for model:" + filename
                            util.printD(output)
                            continue

                        # use this sha256 to get model info from civitai
                        model_info = civitai.get_model_info_by_hash(hash)

                        # delay 1 second for ti
                        if model_type == "ti":
                            util.printD("Delay 1 second for TI")
                            time.sleep(1)

                        if model_info is None:
                            output = "Connect to Civitai API service failed. Wait a while and try again"
                            util.printD(output + ", check console log for detail")
                            continue

                        # write model info to file
                        model.write_model_info(info_file, model_info)

                    model_version = Model(None, item)
                    _models.append(model_version)

                    # set model_count
                    model_count = model_count + 1

                    # check preview image
                    civitai.get_preview_image_by_model_path(item, max_size_preview, skip_nsfw_preview)
                    image_count = image_count + 1

    # scan_log = "Done"

    output = f"Done. Scanned {model_count} models, checked {image_count} images"

    util.printD(output)

    return _models


# def scan_models(model_type, download_max_size_preview, skip_nsfw_preview):
#     model_action_civitai.scan_model(model_type, download_max_size_preview, skip_nsfw_preview)


def get_new_model_version(model_type: list):
    return model_version_snapshot_list


def check_models_new_version(model_type: list, delay_second: int) -> list:
    new_versions = civitai.check_models_new_version_by_model_types(model_type, delay_second)

    _models = []

    if not new_versions:
        print("No model has new version")
    else:
        for new_version in new_versions:
            model_path, model_id, model_name, new_version_id, new_version_name, description, download_url, img_url = new_version

            new_model_version = ModelVersion(model_path, model_id, model_name, new_version_id, new_version_name,
                                             description, download_url, img_url)

            _model = Model(new_model_version, model_path)
            _models.append(_model)

    snapshot = ModelVersionSnapshot(datetime.now().strftime("%Y-%m-%d, %H:%M:%S"), len(_models), _models)
    model_version_snapshot_list.insert(0, snapshot)

    return _models


def upgrade_models(snapshot_code: str) -> tuple[bool, list]:
    new_model_paths = []

    snapshot = None
    for _snapshot in model_version_snapshot_list:
        if _snapshot.code == snapshot_code:
            snapshot = _snapshot

    if snapshot is None:
        return False, new_model_paths

    for _model in snapshot.models:
        new_version = _model.new_version
        if not new_version:
            continue
        url = new_version.download_url
        model_type = _model.model_type

        if model_type != "TextualInversion" and model_type != "Hypernetwork" and model_type != "Checkpoint" and model_type != "LORA":
            model_type = "Checkpoint"

        folder = model.folders[utils.model_type_mapping[model_type]]

        old_version_path = _model.model_path
        delete_file(old_version_path)

        downloader_dl = downloader.dl(url, folder, None, None)
        new_model_paths.append(downloader_dl)

    return True, new_model_paths


def delete_file(file_path: str) -> bool:
    png_file_path = utils.get_file_path(file_path, utils.png_ext)
    preview_png_file_path = utils.get_file_path(file_path, utils.preview_ext)
    info_path = utils.get_file_path(file_path, civitai.suffix + civitai.model.info_ext)

    if os.path.exists(file_path):
        util.printD("Deleting model from: " + file_path)
        os.remove(file_path)
        util.printD("Deleted model from: " + file_path)

    if os.path.exists(info_path):
        util.printD("Deleting info file from: " + info_path)
        os.remove(info_path)
        util.printD("Deleted info file from: " + info_path)

    if os.path.exists(png_file_path):
        util.printD("Deleting png from: " + png_file_path)
        os.remove(png_file_path)
        util.printD("Deleted png from: " + png_file_path)

    if os.path.exists(preview_png_file_path):
        util.printD("Deleting preview png from: " + preview_png_file_path)
        os.remove(preview_png_file_path)
        util.printD("Deleted preview png from: " + preview_png_file_path)

    return True
