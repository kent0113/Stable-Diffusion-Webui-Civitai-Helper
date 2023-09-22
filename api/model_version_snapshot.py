from datetime import datetime
import random
import string

from api import utils
from api.model import Model


class ModelVersionSnapshot:
    def __init__(self, models: list[Model]):
        self.code = ''.join(random.sample(string.ascii_letters + string.digits, 8))
        self.time = datetime.now().strftime("%Y-%m-%d, %H:%M:%S"),
        model_group, size = utils.group_by_model_type(models)
        self.size = size
        self.models = models
