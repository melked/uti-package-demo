def build_response(context, diff_image=None, is_compare=False):
    """
    context: component context, context.image en azından olmalı
    diff_image: Image objesi, sadece compare için
    is_compare: bool, False ise Gray, True ise Compare output oluşturulur
    """

    if is_compare:
        diff_img_output = DiffImage(value=diff_image)
        compare_outputs = CompareOutputs(outputFirstImage=diff_img_output, outputSecondImage=diff_img_output)
        compare_response = CompareResponse(outputs=compare_outputs)
        compare = Compare(value=compare_response)
        config_executor = ConfigExecutor(value=compare)

    else:
        output_image = OutputFirstImage(value=context.image)
        gray_outputs = GrayOutputs(outputFirstImage=output_image)
        gray_response = GrayResponse(outputs=gray_outputs)
        gray = Gray(value=gray_response)
        config_executor = ConfigExecutor(value=gray)

    package_configs = PackageConfigs(executor=config_executor)
    package = PackageHelper(packageModel=PackageModel, packageConfigs=package_configs)
    package_model = package.build_model(context)

    return package_model
