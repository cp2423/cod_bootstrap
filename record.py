from image_processing import myocrfuncs
from image_processing.imgtypes import Img, Rect


class _RecordPage:
    def __init__(self, filepath: str):
        self.fp = filepath
        self.img = myocrfuncs.get_rgb_img(filepath)
        self.rects = myocrfuncs.get_rects(self.img)


class _RecordFrontPage(_RecordPage):
    def __init__(self, filepath: str):
        super().__init__(filepath)
        self.service_no_digits, self.service_no_all = self._get_service_no()
        print(self.service_no_digits, self.service_no_all)

    def _get_service_no(self) -> str:
        roi = _RegionOfImage(self, (180, 250), (35, 55))
        digits = roi._get_digits_only()
        text = roi._get_all_text()

        return digits, text


class _RecordBackPage(_RecordPage):
    pass


class Record:
    def __init__(self, front_filepath: str, back_filepath: str):
        self.front = _RecordFrontPage(front_filepath)
        self.back = _RecordBackPage(back_filepath)


class _RegionOfImage:
    def __init__(self, page: _RecordPage, x_range: tuple[int], y_range: tuple[int]):
        self._parent = page
        self._x_range = x_range
        self._y_range = y_range
        self.img = self._get_img()


    def _is_candidate(self, rect: Rect) -> bool:
        tests = [
            myocrfuncs.is_in_range(rect[0], self._x_range),
            myocrfuncs.is_in_range(rect[1], self._y_range),
            myocrfuncs.is_minimum(rect[2]),
            myocrfuncs.is_minimum(rect[3])
        ]

        return all(tests)

    def _get_img(self) -> Img:
        rects = [r for r in self._parent.rects if self._is_candidate(r)]
        candidates = [myocrfuncs.get_snipped(self._parent.img, r, padding=2) for r in rects]

        if len(candidates) == 0:
            return None
        elif len(candidates) == 1:
            return candidates[0]
        else:
            raise RuntimeWarning(f"more than one candidate found {candidates} in file {self._parent.fp}")

    def _get_digits_only(self):
        return myocrfuncs.read_text(self.img, myocrfuncs.DIGITS)

    def _get_capitals_only(self):
        return myocrfuncs.read_text(self.img, myocrfuncs.CAPITALS)

    def _get_all_text(self):
        return myocrfuncs.read_text(self.img)
