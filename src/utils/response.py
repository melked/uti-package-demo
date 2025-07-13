from components.Gray.src.models.PackageModel import (
    PackageModel, PackageConfigs, ConfigExecutor,
    Gray, GrayResponse, GrayOutputs, OutputImage,
    Compare, CompareResponse, CompareOutputs, SimilarityScore, DiffImage
)
from sdks.novavision.src.helper.package import PackageHelper


def build_response(context, similarity_score=None, diff_image=None, is_compare=False):
    """
    context: component context, context.image en azından olmalı
    similarity_score: float, sadece compare için
    diff_image: Image objesi, sadece compare için
    is_compare: bool, False ise Gray, True ise Compare output oluşturulur
    """

    if is_compare:
        # Compare için response oluştur
        sim_score = SimilarityScore(value=similarity_score if similarity_score is not None else 0.0)
        diff_img_output = DiffImage(value=diff_image)
        compare_outputs = CompareOutputs(similarityScore=sim_score, diffImage=diff_img_output)
        compare_response = CompareResponse(outputs=compare_outputs)
        compare = Compare(value=compare_response)
        config_executor = ConfigExecutor(value=compare)

    else:
        # Gray için response oluştur
        output_image = OutputImage(value=context.image)
        gray_outputs = GrayOutputs(outputImage=output_image)
        gray_response = GrayResponse(outputs=gray_outputs)
        gray = Gray(value=gray_response)
        config_executor = ConfigExecutor(value=gray)

    package_configs = PackageConfigs(executor=config_executor)
    package = PackageHelper(packageModel=PackageModel, packageConfigs=package_configs)
    package_model = package.build_model(context)

    return package_model
