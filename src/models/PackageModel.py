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
        v = values.get("value")
        if isinstance(v, Image):
            return "object"
        elif isinstance(v, list):
            return "list"

    class Config:
        title = "First Image"


class InputSecondImage(Input):
    name: Literal["inputSecondImage"] = "inputSecondImage"
    value: Union[List[Image], Image]
    type: str = "object"

    @validator("type", pre=True, always=True)
    def set_type(cls, value, values):
        v = values.get("value")
        if isinstance(v, Image):
            return "object"
        elif isinstance(v, list):
            return "list"

    class Config:
        title = "Second Image"


class OutputFirstImage(Output):
    name: Literal["outputFirstImage"] = "outputFirstImage"
    value: Union[List[Image], Image]
    type: str = "object"

    @validator("type", pre=True, always=True)
    def set_type(cls, value, values):
        v = values.get("value")
        if isinstance(v, Image):
            return "object"
        elif isinstance(v, list):
            return "list"

    class Config:
        title = "Photo Output"


class OutputSecondImage(Output):
    name: Literal["outputSecondImage"] = "outputSecondImage"
    value: Union[List[Image], Image]
    type: str = "object"

    @validator("type", pre=True, always=True)
    def set_type(cls, value, values):
        v = values.get("value")
        if isinstance(v, Image):
            return "object"
        elif isinstance(v, list):
            return "list"

    class Config:
        title = "Second Output"


class OutputDiffImage(Output):
    name: Literal["outputDiffImage"] = "outputDiffImage"
    value: Union[List[Image], Image]
    type: str = "object"

    @validator("type", pre=True, always=True)
    def set_type(cls, value, values):
        v = values.get("value")
        if isinstance(v, Image):
            return "object"
        elif isinstance(v, list):
            return "list"

    class Config:
        title = "Diff Image"


class CartoonModeNormal(Config):
    name: Literal["Normal"] = "Normal"
    value: Literal["Normal"] = "Normal"
    type: Literal["string"] = "string"
    field: Literal["option"] = "option"
    class Config:
        title = "Normal Cartoon"


class CartoonModeInvert(Config):
    name: Literal["Invert"] = "Invert"
    value: Literal["Invert"] = "Invert"
    type: Literal["string"] = "string"
    field: Literal["option"] = "option"
    class Config:
        title = "Invert Cartoon"


class CartoonMode(Config):
    name: Literal["CartoonMode"] = "CartoonMode"
    value: Union[CartoonModeNormal, CartoonModeInvert]
    type: Literal["object"] = "object"
    field: Literal["dropdownlist"] = "dropdownlist"
    class Config:
        title = "Cartoon Mode"


class CartoonOutputSingle(Config):
    name: Literal["Single"] = "Single"
    value: Literal["Single"] = "Single"
    type: Literal["string"] = "string"
    field: Literal["option"] = "option"
    class Config:
        title = "Single Output"


class CartoonOutputMulti(Config):
    name: Literal["Multi"] = "Multi"
    value: Literal["Multi"] = "Multi"
    type: Literal["string"] = "string"
    field: Literal["option"] = "option"
    class Config:
        title = "Multi Output"


class CartoonOutputType(Config):
    name: Literal["CartoonOutputType"] = "CartoonOutputType"
    value: Union[CartoonOutputSingle, CartoonOutputMulti]
    type: Literal["object"] = "object"
    field: Literal["dropdownlist"] = "dropdownlist"
    class Config:
        title = "Cartoon Output Type"


class CartoonConfigEdit(Config):
    """Cartoon alt ayarlarını toplayan container. PhotoTypeMode->Cartoon seçilince açılır."""
    CartoonMode: CartoonMode
    CartoonOutputType: CartoonOutputType
    name: Literal["CartoonConfigEdit"] = "CartoonConfigEdit"
    value: Literal["CartoonConfigEdit"] = "CartoonConfigEdit"
    type: Literal["object"] = "object"
    field: Literal["group"] = "group"
    class Config:
        title = "Cartoon Settings"



class PhotoGray(Config):
    name: Literal["Gray"] = "Gray"
    value: str = Field(default="Gray")
    type: Literal["string"] = "string"
    field: Literal["option"] = "option"
    class Config:
        title = "Gray"


class PhotoCartoon(Config):
    configEdit: CartoonConfigEdit
    name: Literal["Cartoon"] = "Cartoon"
    value: str = Field(default="Cartoon")
    type: Literal["string"] = "string"
    field: Literal["option"] = "option"
    class Config:
        title = "Cartoon"


class PhotoTypeMode(Config):
    name: Literal["PhotoTypeMode"] = "PhotoTypeMode"
    value: Union[PhotoGray, PhotoCartoon]
    type: Literal["object"] = "object"
    field: Literal["dependentDropdownlist"] = "dependentDropdownlist"
    class Config:
        title = "Photo Type"


class GrayInputs(Inputs):
    inputFirstImage: InputFirstImage


class GrayOutputs(Outputs):
    outputFirstImage: OutputFirstImage


class GrayConfigs(Configs):
    PhotoTypeMode: PhotoTypeMode


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


class CompareModePixelDiff(Config):
    name: Literal["PixelDiff"] = "PixelDiff"
    value: Literal["PixelDiff"] = "PixelDiff"
    type: Literal["string"] = "string"
    field: Literal["option"] = "option"
    class Config:
        title = "Pixel Diff"


class CompareMode(Config):
    name: Literal["CompareMode"] = "CompareMode"
    value: Union[CompareModeSSIM, CompareModePixelDiff]
    type: Literal["object"] = "object"
    field: Literal["dropdownlist"] = "dropdownlist"
    class Config:
        title = "Comparison Method"


class CompareOutputDiffOnly(Config):
    name: Literal["DiffOnly"] = "DiffOnly"
    value: Literal["DiffOnly"] = "DiffOnly"
    type: Literal["string"] = "string"
    field: Literal["option"] = "option"
    class Config:
        title = "Diff Only"


class CompareOutputDiffAndOverlay(Config):
    name: Literal["DiffAndOverlay"] = "DiffAndOverlay"
    value: Literal["DiffAndOverlay"] = "DiffAndOverlay"
    type: Literal["string"] = "string"
    field: Literal["option"] = "option"
    class Config:
        title = "Diff + Overlay"


class CompareOutputType(Config):
    name: Literal["CompareOutputType"] = "CompareOutputType"
    value: Union[CompareOutputDiffOnly, CompareOutputDiffAndOverlay]
    type: Literal["object"] = "object"
    field: Literal["dropdownlist"] = "dropdownlist"
    class Config:
        title = "Output Type"


class CompareInputs(Inputs):
    inputFirstImage: InputFirstImage
    inputSecondImage: InputSecondImage


class CompareOutputs(Outputs):
    outputDiffImage: OutputDiffImage
    outputSecondImage: OutputSecondImage


class CompareConfigs(Configs):
    CompareMode: CompareMode
    CompareOutputType: CompareOutputType


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
