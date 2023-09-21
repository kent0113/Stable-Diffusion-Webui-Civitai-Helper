from fastapi import FastAPI
from pydantic import BaseModel

from api import civitai_helper_api
from api import utils

app = FastAPI()


class ModelVersionQueryParam(BaseModel):
    model_types: list
    delay_second: int | None
    max_size_preview: bool | None
    skip_nsfw_preview: bool | None


class ModelResponse:
    size: int
    models: list | None

    def __init__(self, size: int, models: list):
        self.size = size
        self.models = models


@app.get("/status")
async def status():
    return {"status": "UP"}


@app.post("/api/models")
async def scan_models(query_param: ModelVersionQueryParam):
    model_types = query_param.model_types
    max_size_preview = query_param.max_size_preview
    skip_nsfw_preview = query_param.skip_nsfw_preview
    models = civitai_helper_api.scan_models(model_types, max_size_preview, skip_nsfw_preview)

    model_group, sizes = utils.group_by_model_type(models)
    # return models
    return {"sizes": sizes, "models": model_group}


@app.post("/api/models/new_version")
async def check_version(query_param: ModelVersionQueryParam):
    model_types = query_param.model_types

    model_snapshot_list = civitai_helper_api.get_new_model_version(model_types)

    return model_snapshot_list


@app.post("/api/model/check_version")
async def check_version(query_param: ModelVersionQueryParam):
    model_types = query_param.model_types
    delay_second = query_param.delay_second

    models = civitai_helper_api.check_models_new_version(model_types, delay_second)

    model_group, sizes = utils.group_by_model_type(models)

    return {"size": sizes, "models": model_group}
