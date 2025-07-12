
from sdks.novavision.src.helper.package import PackageHelper
from components.Gray.src.models.PackageModel import (PackageModel, PackageConfigs,
ConfigExecutor, Gray,GrayResponse,GrayOutputs,OutputImage)


def build_response(context):
    outputImage = OutputImage(value=context.image)
    grayOutputs = GrayOutputs(outputImage=outputImage)
    grayResponse=GrayResponse(outputs=grayOutputs)
    gray=Gray(value=grayResponse)
    configExecutor=ConfigExecutor(value= gray)
    packageConfigs = PackageConfigs(executor=configExecutor)
    package = PackageHelper(packageModel=PackageModel, packageConfigs=packageConfigs)
    packageModel = package.build_model(context)
    return packageModel