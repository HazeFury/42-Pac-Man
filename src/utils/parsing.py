import json
import random
import sys
from pathlib import Path
from typing import Any, cast

from pydantic import (
    BaseModel,
    Field,
    ValidationError,
    ValidationInfo,
    ValidatorFunctionWrapHandler,
    field_validator,
)

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
    "level_max_time": "[Error] level_max_time value wrong",
}


class LevelConfig(BaseModel):
    width: int = Field(default_factory=lambda: random.randint(10, 35), ge=10)
    height: int = Field(default_factory=lambda: random.randint(10, 35), ge=10)
    pacgum: int = Field(default_factory=lambda: random.randint(1, 1), ge=0)
    seed: int = Field(default_factory=lambda: random.randint(0, 1000), ge=0)

    @field_validator("width", "height", "pacgum", "seed", mode="wrap")
    @classmethod
    def validate_level_field(
        cls,
        value: Any,
        handler: ValidatorFunctionWrapHandler,
        info: ValidationInfo,
    ) -> int:
        field_name = info.field_name or ""
        try:
            return cast(int, handler(value))
        except ValidationError:
            if field_name in ERROR_MESSAGE:
                print(ERROR_MESSAGE[field_name])
            field = cls.model_fields[field_name]
            return cast(int, field.get_default(call_default_factory=True))


def default_levels() -> dict[str, LevelConfig]:
    return {str(i): LevelConfig() for i in range(1, 11)}


class Setup(BaseModel):
    """
    Configuration schema and validation for game settings.
    """

    highscore_filename: str = Field(default="highscore.json")
    lives: int = Field(default=3, ge=1)
    points_per_pacgum: int = Field(default=10, ge=10)
    points_per_super_pacgum: int = Field(default=50, ge=10)
    points_per_ghost: int = Field(default=200, ge=10)
    level_max_time: int = Field(default=90, ge=10)
    levels: dict[str, LevelConfig] = Field(default_factory=default_levels)

    def get_level(self, level: int = 1) -> LevelConfig:
        """
        Returns the configuration for a specific level, falling back to
        default.
        """
        return self.levels.get(str(level), LevelConfig())

    def get_amount_of_level(self) -> int:
        return len(self.levels)

    @field_validator("highscore_filename", mode="before")
    @classmethod
    def highscore_file_check(cls, value: Any) -> str:
        """
        Validates the highscore file path, falling back to default if invalid.
        """
        if not isinstance(value, str) or not value.endswith(".json"):
            print(
                "invalid data for highscore_filename using default path",
                file=sys.stderr,
            )
            return "highscore.json"
        return value

    @field_validator(
        "lives",
        "points_per_pacgum",
        "points_per_super_pacgum",
        "points_per_ghost",
        "level_max_time",
        mode="wrap",
    )
    @classmethod
    def validate_field(
        cls,
        value: Any,
        handler: ValidatorFunctionWrapHandler,
        info: ValidationInfo,
    ) -> int:
        """
        Validates integer fields and falls back to the default value upon
        error.
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
        else:
            path = Path("config.json")
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

        return data


class Player_score(BaseModel):
    name: str = Field(max_length=10)
    score: int = Field(ge=0, le=9999, default=123)

    @field_validator("name", "score", mode="wrap")
    @classmethod
    def score_checker(cls, value: Any, handler: Any, info: ValidationInfo):
        try:
            return handler(value)
        except Exception:
            if info.field_name:
                return cls.model_fields[info.field_name].default
            return value


class Highscore(BaseModel):
    scores: list[Player_score] = Field(default_factory=list)


config = Setup.from_json_file()
