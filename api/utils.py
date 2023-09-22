import os
from typing import Tuple, Dict, List, Any

from api.model import Model
from scripts.ch_lib import civitai

model_type_mapping = {
    "TextualInversion": "ti",
    "Hypernetwork": "hyper",
    "Checkpoint": "ckp",
    "LORA": "lora",
    "LoCon": "lora"
}

png_ext = ".png"
preview_ext = ".preview.png"


def group_by_model_type(models: list[Model]) -> tuple[dict, dict]:
    model_group = {
        "ti": [],
        "hyper": [],
        "ckp": [],
        "lora": [],
        "others": []
    }

    for model in models:
        model_type = model.model_type_abbr
        model_group[model_type].append(model)

    sizes = {
        "totel": len(models),
        "ti": len(model_group["ti"]),
        "hyper": len(model_group["hyper"]),
        "ckp": len(model_group["ckp"]),
        "lora": len(model_group["lora"]),
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
