import os
import cv2
import sys
import numpy as np

sys.path.append(os.path.join(os.path.dirname(__file__), "../../../../"))

from sdks.novavision.src.media.image import Image
from sdks.novavision.src.base.component import Component
from sdks.novavision.src.helper.executor import Executor

from components.GrayCompare.src.utils.response import build_response
from components.GrayCompare.src.models.PackageModel import PackageModel


class Gray(Component):
    def __init__(self, request, bootstrap):
        super().__init__(request, bootstrap)

        self.request.model = PackageModel(**self.request.data)


        self.image = self.request.get_param("inputFirstImage")


        self.photo_type_mode = self.request.get_param("PhotoTypeMode")
        self.gray_strength = self.request.get_param("GrayStrength")
        self.cartoon_strength = self.request.get_param("CartoonStrength")

        self.context = {}

    @staticmethod
    def bootstrap(config: dict) -> dict:
        return {}

    def _ensure_uint8(self, image: np.ndarray) -> np.ndarray:
        if image.dtype != np.uint8:
            if image.max() <= 1.0:
                image = (image * 255).astype(np.uint8)
            else:
                image = image.astype(np.uint8)
        return image

    def _to_gray3(self, image: np.ndarray) -> np.ndarray:
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        return cv2.cvtColor(gray, cv2.COLOR_GRAY2BGR)

    def _cartoon(self, image: np.ndarray) -> np.ndarray:
        img = self._ensure_uint8(image)
        color = cv2.bilateralFilter(img, d=9, sigmaColor=75, sigmaSpace=75)
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        gray_blur = cv2.medianBlur(gray, 5)
        if gray_blur.dtype != np.uint8:
            gray_blur = gray_blur.astype(np.uint8)
        edges = cv2.adaptiveThreshold(
            gray_blur,
            255,
            cv2.ADAPTIVE_THRESH_MEAN_C,
            cv2.THRESH_BINARY,
            blockSize=9,
            C=2
        )
        edges_colored = cv2.cvtColor(edges, cv2.COLOR_GRAY2BGR)
        cartoon = cv2.bitwise_and(color, edges_colored)
        return cartoon

    def _percent(self, value, default=100):
        if value is None:
            return default
        try:
            v = int(value)
        except Exception:
            v = default
        return max(0, min(v, 100))

    def _blend(self, original_bgr, processed_bgr, percent):
        """percent: 0-100"""
        alpha = percent / 100.0
        return cv2.addWeighted(processed_bgr, alpha, original_bgr, 1.0 - alpha, 0)

    def run(self):

        img_obj = Image.get_frame(img=self.image, redis_db=self.redis_db)
        src_np = self._ensure_uint8(img_obj.value)


        mode = self.photo_type_mode if isinstance(self.photo_type_mode, str) else "Gray"

        if mode == "Cartoon":
            processed_np = self._cartoon(src_np)
            p = self._percent(self.cartoon_strength, default=100)
        else:
            processed_np = self._to_gray3(src_np)
            p = self._percent(self.gray_strength, default=100)

        out_np = self._blend(src_np, processed_np, p)

        img_obj.value = out_np
        out_img = Image.set_frame(img=img_obj, package_uID=self.uID, redis_db=self.redis_db)

        self.image = out_img
        self.context["photoTypeMode"] = mode
        self.context["strengthPercent"] = p

        package_model = build_response(context=self, is_compare=False)
        return package_model


if __name__ == "__main__":
    Executor(sys.argv[1]).run()
