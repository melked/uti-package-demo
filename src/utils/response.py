from sdks.novavision.src.helper.package import PackageHelper

from components.GrayCompare.src.models.PackageModel import (
    Gray, GrayOutputs, GrayResponse,
    Compare, CompareOutputs, CompareResponse,
    OutputFirstImage, OutputDiffImage, OutputSecondImage,
    ConfigExecutor, PackageConfigs, PackageModel
)


def build_response(context, diff_image=None, second_image=None, is_compare=False):
    """
    :param context: Component objesi
    :param diff_image: SSIM sonucu fark görüntüsü (Image)
    :param second_image: Karşılaştırılan ikinci görüntü (Image)
    :param is_compare: Compare executor çalışıyorsa True, Gray ise False
    """

    if is_compare:

        diff_output = OutputDiffImage(value=diff_image)
        second_output = OutputSecondImage(value=second_image)
        compare_outputs = CompareOutputs(
            outputDiffImage=diff_output,
            outputSecondImage=second_output
        )
        compare_response = CompareResponse(outputs=compare_outputs)
        executor_model = Compare(value=compare_response)

    else:

        gray_output = OutputFirstImage(value=context.image)
        gray_outputs = GrayOutputs(outputFirstImage=gray_output)
        gray_response = GrayResponse(outputs=gray_outputs)
        executor_model = Gray(value=gray_response)


    config_executor = ConfigExecutor(value=executor_model)
    package_configs = PackageConfigs(executor=config_executor)
    package = PackageHelper(packageModel=PackageModel, packageConfigs=package_configs)
    package_model = package.build_model(context)

    return package_model
