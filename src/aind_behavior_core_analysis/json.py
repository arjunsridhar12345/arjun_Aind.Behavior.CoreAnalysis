import dataclasses
import json
import os
from typing import Generic, List, Optional, Type, TypeVar

import pandas as pd
import pydantic

from . import FilePathBaseParam


@dataclasses.dataclass
class JsonReaderParams:
    path: os.PathLike
    encoding: str = "UTF-8"


def json_reader(params: JsonReaderParams) -> dict[str, str]:
    with open(params.path, "r", encoding=params.encoding) as file:
        data = json.load(file)
    return data


@dataclasses.dataclass
class JsonWriterParams:
    path: os.PathLike
    indent: int = 4
    encoding: str = "UTF-8"


def json_writer(data: object, params: JsonWriterParams) -> None:
    with open(params.path, "w", encoding=params.encoding) as file:
        json.dump(data, file, indent=params.indent)


def multi_line_json_reader(params: JsonReaderParams) -> list[dict[str, str]]:
    with open(params.path, "r", encoding=params.encoding) as file:
        data = [json.loads(line) for line in file]
    return data


_TModel = TypeVar("_TModel", bound=pydantic.BaseModel)


@dataclasses.dataclass
class MultiLinePydanticModelReaderParams(FilePathBaseParam, Generic[_TModel]):
    model: Type[_TModel]
    encoding: str = "UTF-8"


def multi_line_pydantic_model_reader(params: MultiLinePydanticModelReaderParams[_TModel]) -> List[_TModel]:
    with open(params.path, "r", encoding=params.encoding) as file:
        model_ls = [params.model.model_validate_json(line) for line in file]
    return model_ls


@dataclasses.dataclass
class MultiLinePydanticModelDfReaderParams(FilePathBaseParam, Generic[_TModel]):
    model: Type[_TModel]
    encoding: str = "UTF-8"
    index: Optional[str] = None
    rename_columns: Optional[dict[str, str]] = None


def multi_line_pydantic_model_df_reader(params: MultiLinePydanticModelDfReaderParams[_TModel]) -> pd.DataFrame:
    with open(params.path, "r", encoding=params.encoding) as file:
        model_ls = pd.DataFrame([params.model.model_validate_json(line).model_dump() for line in file])
    if params.rename_columns is not None:
        model_ls.rename(columns=params.rename_columns, inplace=True)
    if params.index is not None:
        model_ls.set_index(params.index, inplace=True)
    return model_ls


@dataclasses.dataclass
class PydanticModelReaderParams(FilePathBaseParam, Generic[_TModel]):
    model: Type[_TModel]
    encoding: str = "UTF-8"


def pydantic_model_reader(params: PydanticModelReaderParams[_TModel]) -> _TModel:
    with open(params.path, "r", encoding=params.encoding) as file:
        return params.model.model_validate_json(file.read())
