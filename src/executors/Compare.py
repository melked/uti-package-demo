"""
    It is a component that compares two images and returns a similarity score and a difference image.
"""

import os
import cv2
import sys
import numpy as np
from skimage.metrics import structural_similarity as ssim

sys.path.append(os.path.join(os.path.dirname(__file__), '../../../../'))

from sdks.novavision.src.media.image import Image
from sdks.novavision.src.base.component import Component
from sdks.novavision.src.helper.executor import Executor
from components.GrayCompare.src.utils.response import build_response
from components.GrayCompare.src.models.PackageModel import PackageModel


class Compare(Component):
    def __init__(self, request, bootstrap):
        super().__init__(request, bootstrap)
        self.request.model = PackageModel(**(self.request.data))
        self.image1 = self.request.get_param("inputImage1")
        self.image2 = self.request.get_param("inputImage2")

    @staticmethod
    def bootstrap(config: dict) -> dict:
        return {}

    def ensure_uint8(self, image):
        if image.dtype != np.uint8:
            if image.max() <= 1.0:
                return (image * 255).astype(np.uint8)
            else:
                return image.astype(np.uint8)
        return image

    def compare_images(self, img1, img2):
        img1 = cv2.resize(img1, (256, 256))
        img2 = cv2.resize(img2, (256, 256))

        gray1 = cv2.cvtColor(img1, cv2.COLOR_BGR2GRAY)
        gray2 = cv2.cvtColor(img2, cv2.COLOR_BGR2GRAY)

        score, diff = ssim(gray1, gray2, full=True)
        diff = (diff * 255).astype(np.uint8)
        diff_colored = cv2.cvtColor(diff, cv2.COLOR_GRAY2BGR)

        return float(score), diff_colored

    def run(self):
        img1 = Image.get_frame(img=self.image1, redis_db=self.redis_db)
        img2 = Image.get_frame(img=self.image2, redis_db=self.redis_db)

        img1.value = self.ensure_uint8(img1.value)
        img2.value = self.ensure_uint8(img2.value)

        similarity, diff_image = self.compare_images(img1.value, img2.value)

        diff_img = Image.set_frame(img=Image(value=diff_image), package_uID=self.uID, redis_db=self.redis_db)

        # Sadece JSON için context üzerinden return edilecek veriler
        self.context["similarityScore"] = similarity

        packageModel = build_response(
            context=self,
            image=diff_img  # bu diff görseli doğrudan output olarak döner
        )

        return packageModel


if __name__ == "__main__":
    Executor(sys.argv[1]).run()