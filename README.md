# cod_bootstrap

Attempt to use service numbers as starting point to "bootstrap" an OCR model to read the whole document.


## Plan

Initial steps:

* enchange image; and/or
* work out how to find the service number in the doc first, then enchance
* do the rest (tbc)


## Enhancement techniques

TODO

Winning candidate:
```
{25: {'params': {'denoise': True, 'dilate': True, 'open': None, 'resize': 4},
      'service_no': '27354\n',
      'surname': 'HONNOH\n',
      'unit': '15th PaLtetson ——,\n'},
```
## Random stuff I found at the start

https://github.com/idea-fasoc/datasheet-scrubber - the datasheet scrubber project which started this iteration. Also https://www.sciencedirect.com/science/article/pii/S2590005622000595 which I think put me on to it.

https://github.com/ROBINADC/Neural-Enhanced-Live-Streaming - A real-time streaming framework that utilizes neural network-based super-resolution to enhance live video quality

https://keras.io/examples/nlp/ner_transformers/ - NER with Keras

https://pyimagesearch.com/2024/06/10/automatic-license-plate-reader-using-ocr-in-python/ - new article about a new OCR technique I have not seen before. TODO try this out?

https://pyimagesearch.com/2021/04/28/opencv-morphological-operations/ - various techiques for enhancing text

https://medium.com/@relaxandplanttrees/upscale-cropand-add-text-to-images-with-python-04f37638b968 - upscaling with torchvision