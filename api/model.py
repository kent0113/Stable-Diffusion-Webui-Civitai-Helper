import os

from api import utils
from api.model_version import ModelVersion
from scripts.ch_lib import civitai
from scripts.ch_lib import model


class Model:

    def __init__(self, new_version: ModelVersion | None, model_path: str):
        self.model_id = None
        self.model_name = None
        self.model_type = None
        self.model_type_abbr = None
        self.base_model = None
        self.version_name = None
        self.model_file_name = None
        self.download_url = None
        self.create_at = None
        self.model_path = model_path
        self.new_version = new_version

        self._load_model_info()

    def _load_model_info(self):
        info_file_path = self._get_info_file_path()
        if not info_file_path:
            return

        model_info_dict = model.load_model_info(info_file_path)
        if model_info_dict.get("modelId") is None:
            # 如果info文件内容为空，则设置为others
            self.model_type_abbr = "others"
            return

        self.model_id = model_info_dict.get("modelId")
        self.version_name = model_info_dict.get("name")
        self.create_at = model_info_dict.get("createdAt")
        self.model_name = model_info_dict.get("model").get("name")
        self.model_type = model_info_dict.get("model").get("type")
        type_ = utils.model_type_mapping[self.model_type]
        self.model_type_abbr = type_ if type_ else "others"
        self.base_model = model_info_dict.get("baseModel")
        self.download_url = model_info_dict.get("downloadUrl")
        self.model_file_name = model_info_dict.get("files")[0].get("name")

    def _get_info_file_path(self) -> str | None:

        if not self.model_path:
            print("model_path is Empty")
            return None

        base, ext = os.path.splitext(self.model_path)
        model_info_base = base
        if base[:1] == "/":
            model_info_base = base[1:]

        model_info_filename = model_info_base + civitai.suffix + civitai.model.info_ext
        model_info_filepath = os.path.join("/", model_info_filename)

        if not os.path.isfile(model_info_filepath):
            print("Can not find model info file: " + model_info_filepath)
            return None

        return model_info_filepath
