from unittest import TestCase

from api import civitai_helper_api


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

    def test_upgrade_models(self):
        model_types = [
            "hyper",
            "ckp"
        ]
        result1 = "ti" in model_types
        result2 = "hyper" in model_types

        assert result1 is False
        assert result2 is True
