import os
import sys
import cv2
import numpy as np
from copy import deepcopy
from skimage.metrics import structural_similarity as ssim

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../../../"))
if BASE_DIR not in sys.path:
    sys.path.insert(0, BASE_DIR)

from sdks.novavision.src.media.image import Image
from sdks.novavision.src.base.component import Component
from sdks.novavision.src.helper.executor import Executor

from components.GrayCompare.src.models.PackageModel import PackageModel
from components.GrayCompare.src.utils.response import build_response


class Compare(Component):

    def __init__(self, request, bootstrap):
        super().__init__(request, bootstrap)

        self.request.model = PackageModel(**self.request.data)

        self.compare_mode = self.request.get_param("CompareMode")
        self.compare_output_type = self.request.get_param("CompareOutputType")

        self.image1 = self.request.get_param("inputFirstImage")
        self.image2 = self.request.get_param("inputSecondImage")

        self.context = {}

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

    def _resize_pair(self, img1: np.ndarray, img2: np.ndarray, size=(256, 256)) -> tuple[np.ndarray, np.ndarray]:
        """SSIM/PixelDiff hesaplamasını sabit boyutta yapmak için yardımcı."""
        return cv2.resize(img1, size), cv2.resize(img2, size)

    def _compare_ssim(self, img1: np.ndarray, img2: np.ndarray) -> tuple[float, np.ndarray]:
        img1_r, img2_r = self._resize_pair(img1, img2, size=(256, 256))
        gray1 = cv2.cvtColor(img1_r, cv2.COLOR_BGR2GRAY)
        gray2 = cv2.cvtColor(img2_r, cv2.COLOR_BGR2GRAY)
        score, diff = ssim(gray1, gray2, full=True)
        diff = (diff * 255).astype(np.uint8)
        diff_colored = cv2.cvtColor(diff, cv2.COLOR_GRAY2BGR)

        diff_colored = cv2.resize(diff_colored, (img2.shape[1], img2.shape[0]))
        return float(score), diff_colored

    def _compare_pixeldiff(self, img1: np.ndarray, img2: np.ndarray) -> tuple[None, np.ndarray]:
        """
        Doğrudan piksel farkı. Boyut eşitlemek için 2. görüntü boyutuna resize ediyoruz.
        """
        if img1.shape[:2] != img2.shape[:2]:
            img1 = cv2.resize(img1, (img2.shape[1], img2.shape[0]))
        diff = cv2.absdiff(img1, img2)
        return None, diff

    def _make_overlay(self, base_img: np.ndarray, diff_img: np.ndarray) -> np.ndarray:
        """
        Diff görüntüsünü kırmızı highlight olarak base_img üzerine bindir.
        """

        gray = cv2.cvtColor(diff_img, cv2.COLOR_BGR2GRAY)

        _, mask = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY)
        mask_col = cv2.cvtColor(mask, cv2.COLOR_GRAY2BGR)

        red = np.zeros_like(base_img)
        red[:, :] = (0, 0, 255)

        red_masked = cv2.bitwise_and(red, mask_col)
        overlay = cv2.addWeighted(base_img, 1.0, red_masked, 0.6, 0)
        return overlay

    def run(self):

        img1 = Image.get_frame(img=self.image1, redis_db=self.redis_db)
        img2 = Image.get_frame(img=self.image2, redis_db=self.redis_db)

        np1 = self.ensure_uint8(img1.value)
        np2 = self.ensure_uint8(img2.value)

        mode = (self.compare_mode or "SSIM") if isinstance(self.compare_mode, str) else "SSIM"
        out_mode = (self.compare_output_type or "DiffOnly") if isinstance(self.compare_output_type, str) else "DiffOnly"

        if mode == "PixelDiff":
            similarity, diff_np = self._compare_pixeldiff(np1, np2)
        else:
            similarity, diff_np = self._compare_ssim(np1, np2)

        diff_image_obj = deepcopy(img1)
        diff_image_obj.value = diff_np
        diff_img = Image.set_frame(img=diff_image_obj, package_uID=self.uID, redis_db=self.redis_db)

        if out_mode == "DiffAndOverlay":
            overlay_np = self._make_overlay(np2, diff_np)
            overlay_obj = deepcopy(img2)
            overlay_obj.value = overlay_np
            second_output = Image.set_frame(img=overlay_obj, package_uID=self.uID, redis_db=self.redis_db)
        else:

            second_output = Image.set_frame(img=img2, package_uID=self.uID, redis_db=self.redis_db)

        self.context["similarityScore"] = similarity
        self.context["compareMode"] = mode
        self.context["compareOutputType"] = out_mode
        self.context["diffImage"] = diff_img

        package_model = build_response(
            context=self,
            diff_image=diff_img,
            second_image=second_output,
            is_compare=True
        )
        return package_model


if __name__ == "__main__":
    Executor(sys.argv[1]).run()
