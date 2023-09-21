import os
from typing import Tuple, Dict, List, Any

from api.model import Model
from scripts.ch_lib import civitai

model_type_mapping = {
    "TextualInversion": "ti",
    "Hypernetwork": "hyper",
    "Checkpoint": "ckp",
    "LORA": "lora"
}

png_ext = ".png"
preview_ext = ".preview.png"


def group_by_model_type(models: list[Model]) -> tuple[dict, dict]:
    model_group = {
        "TextualInversion": [],
        "Hypernetwork": [],
        "Checkpoint": [],
        "LORA": [],
        "others": []
    }

    for model in models:
        model_type = model.model_type
        if model_type != "TextualInversion" and model_type != "Hypernetwork" and model_type != "Checkpoint" and model_type != "LORA":
            model_group["others"].append(model)
        else:
            model_group[model_type].append(model)

    sizes = {
        "totel": len(models),
        "ti": len(model_group["TextualInversion"]),
        "hyper": len(model_group["Hypernetwork"]),
        "ckp": len(model_group["Checkpoint"]),
        "lora": len(model_group["LORA"]),
        "others": len(model_group["others"]),
    }

    return model_group, sizes


def get_file_path(model_path: str, file_ext: str) -> str:
    base, ext = os.path.splitext(model_path)
    model_info_base = base
    if base[:1] == "/":
        model_info_base = base[1:]

    model_path = model_info_base + file_ext
    return os.path.join("/", model_path)
