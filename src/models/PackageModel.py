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
    def set_type(cls, value, values):
        value = values.get("value")
        if isinstance(value, Image):
            return "object"
        elif isinstance(value, list):
            return "list"

    class Config:
        title = "First Image"


class InputSecondImage(Input):
    name: Literal["inputSecondImage"] = "inputSecondImage"
    value: Union[List[Image], Image]
    type: str = "object"

    @validator("type", pre=True, always=True)
    def set_type(cls, value, values):
        value = values.get("value")
        if isinstance(value, Image):
            return "object"
        elif isinstance(value, list):
            return "list"

    class Config:
        title = "Second Image"



class OutputFirstImage(Output):
    name: Literal["outputFirstImage"] = "outputFirstImage"
    value: Union[List[Image], Image]
    type: str = "object"

    @validator("type", pre=True, always=True)
    def set_type(cls, value, values):
        value = values.get("value")
        if isinstance(value, Image):
            return "object"
        elif isinstance(value, list):
            return "list"

    class Config:
        title = "Gray Output"


class OutputSecondImage(Output):
    name: Literal["outputSecondImage"] = "outputSecondImage"
    value: Union[List[Image], Image]
    type: str = "object"

    @validator("type", pre=True, always=True)
    def set_type(cls, value, values):
        value = values.get("value")
        if isinstance(value, Image):
            return "object"
        elif isinstance(value, list):
            return "list"

    class Config:
        title = "Second Output"


class OutputDiffImage(Output):
    name: Literal["outputDiffImage"] = "outputDiffImage"
    value: Union[List[Image], Image]
    type: str = "object"

    @validator("type", pre=True, always=True)
    def set_type(cls, value, values):
        value = values.get("value")
        if isinstance(value, Image):
            return "object"
        elif isinstance(value, list):
            return "list"

    class Config:
        title = "Diff Image"



class Degree(Config):
    name: Literal["Degree"] = "Degree"
    value: int = Field(ge=-359, le=359, default=0)
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


class KeepSide(Config):
    name: Literal["KeepSide"] = "KeepSide"
    value: Union[KeepSideTrue, KeepSideFalse]
    type: Literal["object"] = "object"
    field: Literal["dropdownlist"] = "dropdownlist"

    class Config:
        title = "Keep Sides"



class GrayInputs(Inputs):
    inputFirstImage: InputFirstImage


class GrayOutputs(Outputs):
    outputFirstImage: OutputFirstImage


class GrayConfigs(Configs):
    Degree: Degree
    KeepSide: KeepSide


class GrayRequest(Request):
    inputs: Optional[GrayInputs]
    configs: GrayConfigs

    class Config:
        json_schema_extra = {"target": "configs"}


class GrayResponse(Response):
    outputs: GrayOutputs


class Gray(Config):
    name: Literal["Gray"] = "Gray"
    value: Union[GrayRequest, GrayResponse]
    type: Literal["object"] = "object"
    field: Literal["option"] = "option"

    class Config:
        title = "Gray"
        json_schema_extra = {"target": {"value": 0}}



class CompareModeSSIM(Config):
    name: Literal["SSIM"] = "SSIM"
    value: Literal["SSIM"] = "SSIM"
    type: Literal["string"] = "string"
    field: Literal["option"] = "option"

    class Config:
        title = "SSIM"


class CompareMode(Config):
    name: Literal["CompareMode"] = "CompareMode"
    value: Union[CompareModeSSIM]
    type: Literal["object"] = "object"
    field: Literal["dropdownlist"] = "dropdownlist"

    class Config:
        title = "Comparison Method"



class CompareInputs(Inputs):
    inputFirstImage: InputFirstImage
    inputSecondImage: InputSecondImage


class CompareOutputs(Outputs):
    outputDiffImage: OutputDiffImage
    outputSecondImage: OutputSecondImage


class CompareConfigs(Configs):
    CompareMode: CompareMode


class CompareRequest(Request):
    inputs: Optional[CompareInputs]
    configs: CompareConfigs

    class Config:
        json_schema_extra = {"target": "configs"}


class CompareResponse(Response):
    outputs: CompareOutputs


class Compare(Config):
    name: Literal["Compare"] = "Compare"
    value: Union[CompareRequest, CompareResponse]
    type: Literal["object"] = "object"
    field: Literal["option"] = "option"

    class Config:
        title = "Compare"
        json_schema_extra = {"target": {"value": 0}}



class ConfigExecutor(Config):
    name: Literal["ConfigExecutor"] = "ConfigExecutor"
    value: Union[Gray, Compare]
    type: Literal["executor"] = "executor"
    field: Literal["dependentDropdownlist"] = "dependentDropdownlist"

    class Config:
        title = "Gray or Compare Executor"



class PackageConfigs(Configs):
    executor: ConfigExecutor


class PackageModel(Package):
    configs: PackageConfigs
    type: Literal["component"] = "component"
    name: Literal["GrayCompare"] = "GrayCompare"