from pydantic import Field, validator, root_validator
from typing import List, Optional, Union, Literal
from sdks.novavision.src.base.model import (
    Package, Image, Inputs, Configs, Outputs, Response, Request, Output, Input, Config
)


class InputImage(Input):
    name: Literal["inputImage"] = "inputImage"
    value: Union[List[Image], Image]
    type: str = "object"

    @validator("type", pre=True, always=True)
    def set_type_based_on_value(cls, v, values):
        value = values.get('value')
        if isinstance(value, Image):
            return "object"
        elif isinstance(value, list):
            return "list"
        return "object"

    class Config:
        title = "Image"


class OutputImage(Output):
    name: Literal["outputImage"] = "outputImage"
    value: Union[List[Image], Image]
    type: str = "object"

    @validator("type", pre=True, always=True)
    def set_type_based_on_value(cls, v, values):
        value = values.get('value')
        if isinstance(value, Image):
            return "object"
        elif isinstance(value, list):
            return "list"
        return "object"

    class Config:
        title = "Image"

# ------------------------------
# Gray Executor
# ------------------------------

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

class Degree(Config):
    name: Literal["Degree"] = "Degree"
    value: int = Field(ge=-359, le=359, default=0)
    type: Literal["number"] = "number"
    field: Literal["textInput"] = "textInput"
    class Config:
        title = "Angle"

class GrayInputs(Inputs):
    inputImage: InputImage

class GrayConfigs(Configs):
    degree: Degree
    drawBBox: KeepSideBBox

class GrayRequest(Request):
    inputs: Optional[GrayInputs]
    configs: GrayConfigs

class GrayOutputs(Outputs):
    outputImage: OutputImage

class GrayResponse(Response):
    outputs: GrayOutputs

class Gray(Config):
    name: Literal["Gray"] = "Gray"
    value: Union[GrayRequest, GrayResponse]
    type: Literal["object"] = "object"
    field: Literal["option"] = "option"
    class Config:
        title = "GrayExecutor"


class InputImage1(Input):
    name: Literal["inputImage1"] = "inputImage1"
    value: Union[List[Image], Image]
    type: str = "object"
    @validator("type", pre=True, always=True)
    def set_type_based_on_value(cls, v, values):
        value = values.get('value')
        if isinstance(value, Image):
            return "object"
        elif isinstance(value, list):
            return "list"
        return "object"

class InputImage2(Input):
    name: Literal["inputImage2"] = "inputImage2"
    value: Union[List[Image], Image]
    type: str = "object"
    @validator("type", pre=True, always=True)
    def set_type_based_on_value(cls, v, values):
        value = values.get('value')
        if isinstance(value, Image):
            return "object"
        elif isinstance(value, list):
            return "list"
        return "object"

class CompareInputs(Inputs):
    inputImage1: InputImage1
    inputImage2: InputImage2

class CompareConfigs(Configs):
    drawBBox: KeepSideBBox

class CompareRequest(Request):
    inputs: Optional[CompareInputs]
    configs: CompareConfigs

class SimilarityScore(Output):
    name: Literal["similarityScore"] = "similarityScore"
    value: float
    type: Literal["number"] = "number"

class DiffImage(Output):
    name: Literal["diffImage"] = "diffImage"
    value: Union[List[Image], Image]
    type: str = "object"
    @validator("type", pre=True, always=True)
    def set_type_based_on_value(cls, v, values):
        value = values.get('value')
        if isinstance(value, Image):
            return "object"
        elif isinstance(value, list):
            return "list"
        return "object"

class CompareOutputs(Outputs):
    similarityScore: SimilarityScore
    diffImage: DiffImage

class CompareResponse(Response):
    outputs: CompareOutputs

class Compare(Config):
    name: Literal["Compare"] = "Compare"
    value: Union[CompareRequest, CompareResponse]
    type: Literal["object"] = "object"
    field: Literal["option"] = "option"
    class Config:
        title = "CompareExecutor"



class ExecutorSelector(Config):
    name: Literal["ExecutorSelector"] = "ExecutorSelector"
    selected_executor: Literal["Gray", "Compare"]
    executor: Union[Gray, Compare] = Field(..., discriminator="name")

    class Config:
        title = "Executor Selector"

    @root_validator(pre=True)
    def check_executor_matches_selection(cls, values):
        sel = values.get("selected_executor")
        exe = values.get("executor")
        if sel == "Gray" and exe.get("name") != "Gray":
            raise ValueError("selected_executor 'Gray' seçildi ama executor Gray değil")
        if sel == "Compare" and exe.get("name") != "Compare":
            raise ValueError("selected_executor 'Compare' seçildi ama executor Compare değil")
        return values


class PackageConfigs(Configs):
    executor_selector: ExecutorSelector

class PackageModel(Package):
    configs: PackageConfigs
    type: Literal["component"] = "component"
    name: Literal["Gray"] = "Gray"
