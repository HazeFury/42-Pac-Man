from pathlib import Path
from pydantic import (
    BaseModel,
    Field,
    ValidationError,
    ValidationInfo,
    ValidatorFunctionWrapHandler,
    field_validator,
)
from typing import Any, cast
import sys
import json

ERROR_MESSAGE = {
    "level": "[Error] level value wrong",
    "width": "[Error] width value wrong",
    "height": "[Error] height value wrong",
    "lives": "[Error] lives value wrong",
    "pacgum": "[Error] pacgum value wrong",
    "points_per_pacgum": "[Error] points_per_pacgum value wrong",
    "points_per_super_pacgum": "[Error] points_per_super_pacgum value wrong",
    "points_per_ghost": "[Error] points_per_ghost value wrong",
    "seed": "[Error] seed value wrong",
    "level_max_time": "[Error] level_max_time value wrong"
}


class Setup(BaseModel):
    """
    Configuration schema and validation for game settings.
    """
    highscore_filename: str = Field(default="highscore.json")
    level: int = Field(default=10, ge=10)
    width: int = Field(default=30, ge=10)
    height: int = Field(default=30, ge=10)
    lives: int = Field(default=3, ge=1)
    pacgum: int = Field(default=42, ge=10)
    points_per_pacgum: int = Field(default=10, ge=10)
    points_per_super_pacgum: int = Field(default=50, ge=10)
    points_per_ghost: int = Field(default=200, ge=10)
    seed: int = Field(default=42, ge=0)
    level_max_time: int = Field(default=90, ge=10)

    @field_validator("highscore_filename", mode="before")
    @classmethod
    def highscore_file_check(cls, value: Any) -> str:
        """
        Validates the highscore file path, falling back to default if invalid.
        """
        if not isinstance(value, str) or not value.endswith(".json"):
            print(
                "invalid data for highscore_filename using default path",
                file=sys.stderr)
            return "highscore.json"
        return value

    @field_validator("level", "width", "height", "lives", "pacgum",
                     "points_per_pacgum", "points_per_super_pacgum",
                     "points_per_ghost", "seed", "level_max_time",
                     mode="wrap")
    @classmethod
    def validate_field(cls, value: Any,
                       handler: ValidatorFunctionWrapHandler,
                       info: ValidationInfo) -> int:
        """
        Validates integer fields and falls back to the default value upon error.
        """
        field_name = info.field_name or ""
        try:
            return cast(int, handler(value))
        except ValidationError:
            print(ERROR_MESSAGE[field_name])
            return cast(int, cls.model_fields[field_name].default)

    @classmethod
    def from_json_file(cls) -> "Setup":

        forbiden_char = ("#", "//", "*/", "/*")
        clean_json = []
        if len(sys.argv) > 1:
            path = Path(sys.argv[1])
            try:
                with open(path, "r", encoding="utf-8") as f:
                    lines = f.read().split("\n")
                    for line in lines:
                        if line.strip().startswith(forbiden_char):
                            continue
                        clean_json.append(line)

                try:
                    conf = "".join(clean_json)
                    final_json = json.loads(conf)
                    data = cls(**final_json)
                except Exception:
                    print("invalid json format using defaults value")
                    data = cls()

            except FileNotFoundError as e:
                print(f"File {path} not found {e}")
                data = cls()
        else:
            data = cls()
        return data


class Player_score(BaseModel):
    name: str = Field(max_length=10, default="AAA")
    score: int = Field(ge=0, le=9999, default=0)


class Highscore(BaseModel):
    scores: list[Player_score] = Field(default_factory=list)
