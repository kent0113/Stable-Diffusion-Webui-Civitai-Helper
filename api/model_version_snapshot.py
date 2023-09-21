import random
import string

from api import utils
from api.model import Model


class ModelVersionSnapshot:
    def __init__(self, time, count, models: list[Model]):
        self.code = ''.join(random.sample(string.ascii_letters + string.digits, 8))
        self.time = time
        self.count = count
        self.models = models
