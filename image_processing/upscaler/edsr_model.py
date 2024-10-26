from cv2 import dnn_superres
from importlib.resources import path
from numpy import ndarray

BINARY_FILENAME = "EDSR_x4.pb"
NAME = "edsr"
SCALE_FACTOR = 4

# absolute nonsense to simply read a file from within a module
with path(__name__, BINARY_FILENAME) as path:
    MODEL_FILEPATH = str(path)


class SuperRes:
    def __init__(self):
        self.sr = dnn_superres.DnnSuperResImpl_create()
        self.sr.readModel(MODEL_FILEPATH)
        self.sr.setModel(NAME, SCALE_FACTOR)

    def upscale(self, img) -> ndarray:
        return self.sr.upsample(img)