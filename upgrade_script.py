from api import civitai_helper_api
from scripts.ch_lib import util


def main():
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
