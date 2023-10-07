import os
from unittest import TestCase
from api import utils
from scripts.ch_lib import civitai


class Test(TestCase):
    def test_get_file_path(self):
        model_path = "DEMO"

        info_path = utils.get_file_path(model_path, civitai.suffix + civitai.model.info_ext)
        png_path = utils.get_file_path(model_path, utils.png_ext)
        preview_png_path = utils.get_file_path(model_path, utils.preview_ext)

        print("--------------")
        print(info_path)
        print(png_path)
        print(preview_png_path)

    def test_get_model_folder_path(self):
        model_path = "/stable-diffusion-webui/models/public/Lora/SDXL/edgMamaLuba_DollLikeness.safetensors"
        folder = os.path.dirname(model_path)
        assert folder == "/stable-diffusion-webui/models/public/Lora/SDXL"
