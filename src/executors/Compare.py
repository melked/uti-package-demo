import os
import cv2
import sys
import numpy as np
from copy import deepcopy
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

        self.request.model = PackageModel(**self.request.data)

        self.compare_mode = self.request.get_param("CompareMode")
        self.image1 = self.request.get_param("inputFirstImage")
        self.image2 = self.request.get_param("inputSecondImage")

    @staticmethod
    def bootstrap(config: dict) -> dict:
        return {}

    def ensure_uint8(self, image: np.ndarray) -> np.ndarray:
        if image.dtype != np.uint8:
            if image.max() <= 1.0:
                image = (image * 255).astype(np.uint8)
            else:
                image = image.astype(np.uint8)
        return image

    def compare_images(self, img1: np.ndarray, img2: np.ndarray) -> tuple[float, np.ndarray]:
        img1_resized = cv2.resize(img1, (256, 256))
        img2_resized = cv2.resize(img2, (256, 256))

        gray1 = cv2.cvtColor(img1_resized, cv2.COLOR_BGR2GRAY)
        gray2 = cv2.cvtColor(img2_resized, cv2.COLOR_BGR2GRAY)

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

        # Burada deepcopy ile var olan Image objesini klonla, value olarak diff görüntüyü ver
        diff_image_obj = deepcopy(img1)
        diff_image_obj.value = diff_image
        diff_img = Image.set_frame(img=diff_image_obj, package_uID=self.uID, redis_db=self.redis_db)

        # İkinci görüntüyü de aynı şekilde kopyala (değişmeden)
        second_image_obj = deepcopy(img2)
        image2_output = Image.set_frame(img=second_image_obj, package_uID=self.uID, redis_db=self.redis_db)

        self.context["similarityScore"] = similarity

        package_model = build_response(
            context=self,
            diff_image=diff_img,
            second_image=image2_output,
            is_compare=True
        )

        return package_model


if __name__ == "__main__":
    Executor(sys.argv[1]).run()
