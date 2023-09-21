from unittest import TestCase
from api import utils
from scripts.ch_lib import civitai


class Test(TestCase):
    def test_get_file_path(self):
        model_path = "/Users/bytedance/Dev/aweminds/graviti-stable-diffusion-webui/models/public/embeddings/an9.pt"

        info_path = utils.get_file_path(model_path, civitai.suffix + civitai.model.info_ext)
        png_path = utils.get_file_path(model_path, utils.png_ext)
        preview_png_path = utils.get_file_path(model_path, utils.preview_ext)

        print("--------------")
        print(info_path)
        print(png_path)
        print(preview_png_path)

