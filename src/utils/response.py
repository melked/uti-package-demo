from copy import deepcopy
from components.GrayCompare.src.models.PackageModel import (
    Compare, CompareOutputs, CompareResponse, DiffImage,
    Gray, GrayOutputs, GrayResponse,
    ConfigExecutor, PackageConfigs, PackageModel
)
from sdks.novavision.src.helper.package import PackageHelper

def build_response(context, diff_image=None, second_image=None, is_compare=False):
    """
    context: executor objesi
    diff_image: Image objesi (compare için diff resmi)
    second_image: Image objesi (compare için ikinci input resmi)
    is_compare: bool, True ise compare, False ise gray output oluşturulur
    """

    if is_compare:

        diff_img_output = DiffImage(value=diff_image)
        compare_outputs = CompareOutputs(
            outputFirstImage=diff_img_output,
            outputSecondImage=second_image
        )
        compare_response = CompareResponse(outputs=compare_outputs)
        compare = Compare(value=compare_response)
        config_executor = ConfigExecutor(value=compare)

    else:
        output_image = GrayOutputs(outputFirstImage=context.image)
        gray_response = GrayResponse(outputs=output_image)
        gray = Gray(value=gray_response)
        config_executor = ConfigExecutor(value=gray)

    package_configs = PackageConfigs(executor=config_executor)
    package = PackageHelper(packageModel=PackageModel, packageConfigs=package_configs)
    package_model = package.build_model(context)

    return package_model
