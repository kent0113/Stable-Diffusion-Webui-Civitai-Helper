from unittest import TestCase
from api.model import Model


class TestModelVersion(TestCase):

    def test_load_model_info(self):
        model_version = Model(None,
                              "DEMO")
        # model_version.load_model_info()

        assert model_version.model_id is not None
        assert model_version.model_name is not None
        assert model_version.model_type is not None
        assert model_version.base_model is not None
        assert model_version.version_name is not None
        assert model_version.model_file_name is not None
        assert model_version.model_path is not None
        assert model_version.download_url is not None
        print("---------model_info-----")
        print(model_version.model_id)
        print(model_version.model_name)
        print(model_version.version_name)
