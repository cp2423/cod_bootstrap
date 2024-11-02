from sources.locations import IMAGE_PARENT_FOLDER
import os
import tarfile


class SourceFolder:
    def __init__(self, path: os.DirEntry):
        if tarfile.is_tarfile(path):
            print(path)
            tar = tarfile.open(path)
            self._iter = tar.getnames()
        elif path.is_dir:
            self._iter = os.scandir(path)

    def __iter__(self):
        return self

    def __next__(self):
        return next(self._iter)


class SourceFolders:
    def __init__(self):
        self._paths = os.scandir(IMAGE_PARENT_FOLDER)

    def __iter__(self):
        return self

    def __next__(self):
        path = next(self._paths)
        return SourceFolder(path)


def get_all_folders() -> SourceFolders:
    return list(SourceFolders())

def get_all_images_from_folder(folder: SourceFolder):
    return SourceFolder()
