from sources.locations import IMAGE_PARENT_FOLDER
import os
import tarfile

# grab as list else iterator will break as we extract files since this adds to the dir
paths = list(os.scandir(IMAGE_PARENT_FOLDER))
for p in paths:
    if p.name.endswith(".tar.xz"):
        vol = p.name.split(".")[0]
        if tarfile.is_tarfile(p):
            try:
                print("Extracting", p)
                tar = tarfile.open(p)
                tar.extractall(path=IMAGE_PARENT_FOLDER)
                print("... done")
                os.remove(p)
            except Exception as e:
                print(e, p)
