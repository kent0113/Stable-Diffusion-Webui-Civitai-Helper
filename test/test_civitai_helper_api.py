import os
from unittest import TestCase
from api import civitai_helper_api
from scripts.ch_lib import model


class Test(TestCase):

    def test_scan_models(self):
        model_type = ['ti', 'hyper', 'ckp', 'lora']
        download_max_size_preview = True
        skip_nsfw_preview = False
        civitai_helper_api.scan_models(model_type, download_max_size_preview, skip_nsfw_preview)

    def test_check_new_version(self):
        model_type = ['ti', 'hyper', 'ckp', 'lora']
        model_versions = civitai_helper_api.check_models_new_version(model_type, 0)
        print(model_versions)
        for model_version in model_versions:
            assert model_version.new_version is not None
            assert model_version.new_version.model_path is not None
            assert model_version.new_version.model_id is not None
            assert model_version.new_version.model_name is not None
            assert model_version.new_version.new_version_id is not None
            assert model_version.new_version.new_version_name is not None
            assert model_version.new_version.download_url is not None
        assert len(model_versions) == 2

    def test(self):
        root_path = "/Users/bytedance/Dev/aweminds/graviti-stable-diffusion-webui/models"
        model.folders = {
            "ti": os.path.join(root_path, "public", "embeddings"),
            "hyper": os.path.join(root_path, "public", "hypernetworks"),
            "ckp": os.path.join(root_path, "public", "Stable-diffusion"),
            "lora": os.path.join(root_path, "public", "Lora"),
        }

        name = model.load_model_info(
            "/Users/bytedance/Dev/aweminds/graviti-stable-diffusion-webui/models/public/embeddings/an9.civitai.info")
        print("------")
        print(name)
