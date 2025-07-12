"""
    It is one of the preprocessing components in which the image is rotated.
"""

import os
import cv2
import sys
sys.path.append(os.path.join(os.path.dirname(__file__), '../../../../'))

from sdks.novavision.src.media.image import Image
from sdks.novavision.src.base.component import Component
from sdks.novavision.src.helper.executor import Executor
from components.Gray.src.utils.response import build_response
from components.Gray.src.models.PackageModel import PackageModel


class Gray(Component):
    def __init__(self, request, bootstrap):
        super().__init__(request, bootstrap)
        self.request.model = PackageModel(**(self.request.data))
        self.rotation_degree = self.request.get_param("Degree")
        self.keep_side = self.request.get_param("KeepSide")
        self.image = self.request.get_param("inputImage")

    @staticmethod
    def bootstrap(config: dict) -> dict:
        return {}

    import cv2

    def cartoonify(self, image):

        if image.dtype != cv2.CV_8U and image.max() <= 1.0:
            image = (image * 255).astype('uint8')

        color = cv2.bilateralFilter(image, d=9, sigmaColor=75, sigmaSpace=75)

        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

        gray_blur = cv2.medianBlur(gray, 5)

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

    def run(self):
        img = Image.get_frame(img=self.image, redis_db=self.redis_db)
        img.value = self.cartoonify(img.value)
        self.image = Image.set_frame(img=img, package_uID=self.uID, redis_db=self.redis_db)
        packageModel = build_response(context=self)
        return packageModel




if "__main__" == __name__:
    Executor(sys.argv[1]).run()
