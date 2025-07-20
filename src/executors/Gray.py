
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

        self.cartoon_mode = self.request.get_param("CartoonMode")             
        self.cartoon_output_type = self.request.get_param("CartoonOutputType") 

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
        """Tek kanal gri -> 3 kanala geri döndür (UI/codec uyumu için)."""
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        return cv2.cvtColor(gray, cv2.COLOR_GRAY2BGR)

    def _cartoon(self, image: np.ndarray, invert: bool = False) -> np.ndarray:
   
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

        if invert:
            cartoon = cv2.bitwise_not(cartoon)

        return cartoon

    def run(self):

        img_obj = Image.get_frame(img=self.image, redis_db=self.redis_db)
        np_img = self._ensure_uint8(img_obj.value)

        mode = self.photo_type_mode if isinstance(self.photo_type_mode, str) else "Gray"

        if mode == "Cartoon":
            invert = (self.cartoon_mode == "Invert")
            out_np = self._cartoon(np_img, invert=invert)
        else:
            out_np = self._to_gray3(np_img)

        img_obj.value = out_np
        out_img = Image.set_frame(img=img_obj, package_uID=self.uID, redis_db=self.redis_db)

        self.context["photoTypeMode"] = mode
        if mode == "Cartoon":
            self.context["cartoonMode"] = self.cartoon_mode
            self.context["cartoonOutputType"] = self.cartoon_output_type

       
        package_model = build_response(
            context=self,
            image=out_img  
        )
        return package_model


if __name__ == "__main__":
    Executor(sys.argv[1]).run()
