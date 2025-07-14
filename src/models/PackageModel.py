from pydantic import Field, validator
from typing import List, Optional, Union, Literal
from sdks.novavision.src.base.model import (
    Package, Image, Inputs, Configs, Outputs, Response, Request,
    Output, Input, Config
)




class InputFirstImage(Input):
    name: Literal["inputFirstImage"] = "inputFirstImage"
    value: Union[List[Image], Image]
    type: str = "object"

    @validator("type", pre=True, always=True)
    def set_type_based_on_value(cls, value, values):
        value = values.get('value')
        if isinstance(value, Image):
            return "object"
        elif isinstance(value, list):
            return "list"
        return value

    class Config:
        title = "Image"


class InputSecondImage(Input):
    name: Literal["inputSecondImage"] = "inputSecondImage"
    value: Union[List[Image], Image]
    type: str = "object"

    @validator("type", pre=True, always=True)
    def set_type_based_on_value(cls, value, values):
        value = values.get('value')
        if isinstance(value, Image):
            return "object"
        elif isinstance(value, list):
            return "list"
        return value

    class Config:
        title = "Image"


class OutputFirstImage(Output):
    name: Literal["outputFirstImage"] = "outputFirstImage"
    value: Union[List[Image], Image]
    type: str = "object"

    @validator("type", pre=True, always=True)
    def set_type_based_on_value(cls, value, values):
        value = values.get('value')
        if isinstance(value, Image):
            return "object"
        elif isinstance(value, list):
            return "list"
        return value

    class Config:
        title = "Image"



class Degree(Config):
    name: Literal["Degree"] = "Degree"
    value: int = Field(ge=-359.0, le=359.0, default=0)
    type: Literal["number"] = "number"
    field: Literal["textInput"] = "textInput"

    class Config:
        title = "Rotation Degree"


class KeepSideFalse(Config):
    name: Literal["False"] = "False"
    value: Literal[False] = False
    type: Literal["bool"] = "bool"
    field: Literal["option"] = "option"

    class Config:
        title = "Disable"


class KeepSideTrue(Config):
    name: Literal["True"] = "True"
    value: Literal[True] = True
    type: Literal["bool"] = "bool"
    field: Literal["option"] = "option"

    class Config:
        title = "Enable"


class KeepSideBBox(Config):
    name: Literal["KeepSide"] = "KeepSide"
    value: Union[KeepSideTrue, KeepSideFalse]
    type: Literal["object"] = "object"
    field: Literal["dropdownlist"] = "dropdownlist"

    class Config:
        title = "Keep Sides"


class CompareModeSSIM(Config):
    name: Literal["SSIM"] = "SSIM"
    value: Literal["SSIM"] = "SSIM"
    type: Literal["string"] = "string"
    field: Literal["option"] = "option"

    class Config:
        title = "SSIM"


class CompareModeConfig(Config):
    name: Literal["CompareMode"] = "CompareMode"
    value: Union[CompareModeSSIM]
    type: Literal["object"] = "object"
    field: Literal["dropdownlist"] = "dropdownlist"

    class Config:
        title = "Comparison Method"



class GrayInputs(Inputs):
    inputFirstImage: InputFirstImage


class GrayConfigs(Configs):
    Degree: Degree
    KeepSide: KeepSideBBox


class GrayRequest(Request):
    inputs: Optional[GrayInputs]
    configs: GrayConfigs

    class Config:
        json_schema_extra = {
            "target": "configs"
        }


class GrayOutputs(Outputs):
    outputFirstImage: OutputFirstImage


class GrayResponse(Response):
    outputs: GrayOutputs


class Gray(Config):
    name: Literal["Gray"] = "Gray"
    value: Union[GrayRequest, GrayResponse]
    type: Literal["object"] = "object"
    field: Literal["option"] = "option"

    class Config:
        title = "Gray"
        json_schema_extra = {
            "target": {
                "value": 0
            }
        }



class CompareInputs(Inputs):
    inputFirstImage: InputFirstImage
    inputSecondImage: InputSecondImage


class CompareConfigs(Configs):
    CompareMode: CompareModeConfig


class CompareRequest(Request):
    inputs: Optional[CompareInputs]
    configs: CompareConfigs

    class Config:
        json_schema_extra = {
            "target": "configs"
        }


class CompareOutputs(Outputs):
    outputFirstImage: OutputFirstImage


class CompareResponse(Response):
    outputs: CompareOutputs


class Compare(Config):
    name: Literal["Compare"] = "Compare"
    value: Union[CompareRequest, CompareResponse]
    type: Literal["object"] = "object"
    field: Literal["option"] = "option"

    class Config:
        title = "Compare"
        json_schema_extra = {
            "target": {
                "value": 0
            }
        }




class ConfigExecutor(Config):
    name: Literal["ConfigExecutor"] = "ConfigExecutor"
    value: Union[Gray, Compare]
    type: Literal["executor"] = "executor"
    field: Literal["dependentDropdownlist"] = "dependentDropdownlist"

    class Config:
        title = "Type"


class PackageConfigs(Configs):
    executor: ConfigExecutor


class PackageModel(Package):
    configs: PackageConfigs
    type: Literal["component"] = "component"
    name: Literal["GrayCompare"] = "GrayCompare"



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

        sim_score = SimilarityScore(value=similarity_score if similarity_score is not None else 0.0)
        diff_img_output = DiffImage(value=diff_image)
        compare_outputs = CompareOutputs(similarityScore=sim_score, diffImage=diff_img_output)
        compare_response = CompareResponse(outputs=compare_outputs)
        compare = Compare(value=compare_response)
        config_executor = ConfigExecutor(value=compare)

    else:

        output_image = OutputImage(value=context.image)
        gray_outputs = GrayOutputs(outputImage=output_image)
        gray_response = GrayResponse(outputs=gray_outputs)
        gray = Gray(value=gray_response)
        config_executor = ConfigExecutor(value=gray)

    package_configs = PackageConfigs(executor=config_executor)
    package = PackageHelper(packageModel=PackageModel, packageConfigs=package_configs)
    package_model = package.build_model(context)

    return package_model
