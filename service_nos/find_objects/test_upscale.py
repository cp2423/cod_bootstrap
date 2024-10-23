# src https://docs.opencv.org/4.x/d5/d29/tutorial_dnn_superres_upscale_image_single.html

import cv2
from cv2 import dnn_superres

# Create an SR object - only function that differs from c++ code
sr = dnn_superres.DnnSuperResImpl_create()

# Read image
image = cv2.imread('/Users/chris/Dev/cod_records/cod_bootstrap/service_nos/find_objects/roi/ROI.png')

# Read the desired model
path = "/Users/chris/Dev/cod_records/cod_bootstrap/service_nos/find_objects/EDSR_x4.pb"
sr.readModel(path)

# Set the desired model and scale to get correct pre- and post-processing
sr.setModel("edsr", 4)

# Upscale the image
result = sr.upsample(image)

# Save the image
cv2.imwrite("./upscaled.png", result)