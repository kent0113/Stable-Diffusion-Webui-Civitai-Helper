from typing import Tuple, Dict, List, Any

from api.model import Model


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
        if model_type is None:
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
