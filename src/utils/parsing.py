from pathlib import Path
from pydantic import BaseModel, ValidationError, Field, field_validator
import json
import sys


class Setup(BaseModel):
    highscore_filename: str = Field(default="highscore.json")
    level: int = 10
    width: int = 30
    height: int = 30
    lives: int = 3
    pacgum: int = 42
    points_per_pacgum: int = 10
    points_per_super_pacgum: int = 50
    points_per_ghost: int = 200
    seed: int = 42
    level_max_time: int = 90

    @field_validator("highscore_filename", mode="before")
    @classmethod
    def highscore_file_check(cls, value: str):
        if not isinstance(value, str) or not value.endswith(".json"):
            print(
                "invalid data for highscore_filename using default path",
                file=sys.stderr)
            return "highscore.json"
        return value

    @field_validator("level", mode="before")
    @classmethod
    def level_check(cls, value: int):
        if not isinstance(value, int):
            print("invalid data for number of level using default value 10",
                  file=sys.stderr)
            return 10
        elif value < 10:
            print("level value to low using default value 10")
            return 10
        return value

    @field_validator("width", "height", mode="before")
    @classmethod
    def size_check(cls, value: int):
        if not isinstance(value, int):
            print("invalid data for height or width, using default value 30",
                  file=sys.stderr)
            return 30
        elif value < 5:
            print("height or width value to low using default value 30")
            return 30
        return value

    @field_validator("lives", mode="before")
    @classmethod
    def num_life_check(cls, value: int):
        if not isinstance(value, int):
            print("invalid data for number of life, using default value 3",
                  file=sys.stderr)
            return 3
        elif value < 1:
            print("number of life value to low using default value 3")
            return 3
        return value

    @field_validator("pacgum", mode="before")
    @classmethod
    def pacgum_check(cls, value: int):
        if not isinstance(value, int):
            print("invalid data for number of"
                  " pacgum value, using default value 42",
                  file=sys.stderr)
            return 42
        elif value < 1:
            print("pacgum value to low using default value 42")
            return 42
        return value

    @field_validator("points_per_pacgum",
                     mode="before")
    @classmethod
    def points_per_pacgum_check(cls, value: int):
        if not isinstance(value, int):
            print("invalid data for point per pacgum,"
                  " using default value 10",
                  file=sys.stderr)
            return 10
        elif value < 1:
            print("point per pacgum value to low using default value 3")
            return 3
        return value

    @field_validator("points_per_super_pacgum",
                     mode="before")
    @classmethod
    def points_per_super_pacgum_check(cls, value: int):
        if not isinstance(value, int):
            print("invalid data for point per super pacgum,"
                  " using default value 50",
                  file=sys.stderr)
            return 50
        elif value < 1:
            print("point per super pacgum value to low using default value 50")
            return 50
        return value

    @field_validator("points_per_ghost",
                     mode="before")
    @classmethod
    def points_per_ghost_check(cls, value: int):
        if not isinstance(value, int):
            print("invalid data for point per ghost,"
                  " using default value 200",
                  file=sys.stderr)
            return 200
        elif value < 1:
            print("point per ghost value to low using default value 200")
            return 200
        return value

    @field_validator("seed",
                     mode="before")
    @classmethod
    def seed_check(cls, value: int):
        if not isinstance(value, int):
            print("invalid data for seed,"
                  " using default value 42",
                  file=sys.stderr)
            return 42
        elif value < 0:
            print("seed value must be positive, using default value 42")
            return 42
        return value

    @field_validator("level_max_time",
                     mode="before")
    @classmethod
    def lvl_time_check(cls, value: int):
        if not isinstance(value, int):
            print("invalid data for seed,"
                  " using default value 90",
                  file=sys.stderr)
            return 90
        elif value < 0:
            print("time value must be greater than 30, using default value 90")
            return 90
        return value


class JsonCleaning:
    def __init__(self, filename: str) -> None:
        self.path = Path(filename)

    def open_file(self) -> Setup:
        forbiden_char = ("#", "//")

        clean_json = []
        try:
            with open(self.path, "r", encoding="utf-8") as f:
                lines = f.read()
                for line in lines:
                    if line.strip().startswith(forbiden_char):
                        continue
                    else:
                        clean_json.append(line)
            conf = "".join(clean_json)
            final_json = eval(conf)

            config = json.load(final_json)
            data = Setup(**config)
            return data
        except FileNotFoundError as e:
            print(f"File {self.path} not found {e}")
            sys.exit(1)
