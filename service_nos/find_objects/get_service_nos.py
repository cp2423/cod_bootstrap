from dataclasses import dataclass
from numpy import ndarray
import cv2

@dataclass
class Result:
    service_no: ndarray
    surname: ndarray


def get_source_images():
    pass


def get_service_no():
    pass


def get_surname():
    pass

def upscale(img):
    pass


def save_result(service_no, surname):
    pass


def store_result():
    pass


# iterate through source images
sources = get_source_images()
for img in sources:
    # identify bouding box around service no
    service_no_orig = get_service_no()
    # identify bound boxing around surname
    surname_orig = get_surname()
    # upscale both
    service_no_upscaled = upscale()
# save and store