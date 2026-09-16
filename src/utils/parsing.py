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
        field_name = info.field_name or ""
        try:
            return cast(int, handler(value))
        except ValidationError:
            print(ERROR_MESSAGE[field_name])
            return cast(int, cls.model_fields[field_name].default)


class JsonCleaning:
    def __init__(self, filename: str) -> None:
        self.path = Path(filename)
        self.open_file()

    def open_file(self) -> None:
        forbiden_char = ("#", "//", "*/", "/*")
        clean_json = []
        output = Path("test.json")

        try:
            with open(self.path, "r", encoding="utf-8") as f:
                lines = f.read().split("\n")
                print("read ok")
                for line in lines:
                    if line.strip().startswith(forbiden_char):
                        continue
                    else:
                        clean_json.append(line)
            print("clean ok")
            try:
                conf = "".join(clean_json)
                final_json = eval(conf)
                data = Setup(**final_json)
            except Exception:
                print("invalide json format using defaults value")
                data = Setup()

            output.write_text(
                data.model_dump_json(
                    indent=2), encoding="UTF-8")
        except FileNotFoundError as e:
            print(f"File {self.path} not found {e}")
            data = Setup()
            output.write_text(
                data.model_dump_json(
                    indent=2), encoding="UTF-8")


def main() -> None:
    JsonCleaning("config.json")
    print("ok")


if __name__ == "__main__":
    main()
