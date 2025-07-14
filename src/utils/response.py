from components.GrayCompare.src.models.PackageModel import (
    Compare, CompareOutputs, CompareResponse,
    Gray, GrayOutputs, GrayResponse,
    OutputFirstImage, OutputSecondImage, DiffImage,
    ConfigExecutor, PackageConfigs, PackageModel
)
from sdks.novavision.src.helper.package import PackageHelper


def build_response(context, diff_image=None, second_image=None, is_compare=False):
    """
    :param context: executor objesi (Gray ya da Compare sınıfı)
    :param diff_image: Image objesi (Compare için oluşturulan diff görüntüsü)
    :param second_image: Image objesi (Compare için ikinci input image)
    :param is_compare: Compare işlemi mi? (True/False)
    :return: PackageModel
    """

    if is_compare:
        # Compare için iki output oluşturuluyor
        diff_output = DiffImage(value=diff_image)
        second_output = OutputSecondImage(value=second_image)

        compare_outputs = CompareOutputs(
            outputFirstImage=diff_output,
            outputSecondImage=second_output
        )

        compare_response = CompareResponse(outputs=compare_outputs)
        executor_config = Compare(value=compare_response)

    else:
        # Gray işlemi için tek output
        output = OutputFirstImage(value=context.image)
        gray_outputs = GrayOutputs(outputFirstImage=output)
        gray_response = GrayResponse(outputs=gray_outputs)
        executor_config = Gray(value=gray_response)

    # Executor’ü package’a sarmala
    config_executor = ConfigExecutor(value=executor_config)
    package_configs = PackageConfigs(executor=config_executor)
    package = PackageHelper(packageModel=PackageModel, packageConfigs=package_configs)
    package_model = package.build_model(context)

    return package_model
