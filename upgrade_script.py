import os

import dotenv

from api import civitai_helper_api
from scripts.ch_lib import util

dotenv.load_dotenv()


def main():
    civitai_api_key = os.getenv('CIVITAI_API_KEY')
    util.civitai_api_key = civitai_api_key
    util.def_headers["Authorization"] = f"Bearer {civitai_api_key}"

    print("###############   init   ################ ")
    print(f"has_api_key: {True if civitai_api_key else False}")

    model_types = [
        "ti",
        "hyper",
        "ckp",
        "lora"
    ]
    print("############## scan models ############## ")
    civitai_helper_api.scan_models(model_types, False, False)
    print("############## check model version ############## ")
    new_version = civitai_helper_api.check_models_new_version(model_types, 1)
    if len(new_version) == 0:
        return

    _snapshot_list = civitai_helper_api.get_new_model_version()
    if len(_snapshot_list) == 0:
        return

    _code = _snapshot_list[0].code
    print("############## upgrade model ##############")
    civitai_helper_api.upgrade_models(_code, model_types)


main()
