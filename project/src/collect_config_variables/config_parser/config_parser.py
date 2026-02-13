from dataclasses import dataclass
from pathlib import Path
from typing import Dict, Tuple
from src.collect_config_variables.error_handlers import ConfigError
import sys
RD = "\033[91m"
R = "\033[0m"


@dataclass(frozen=True)
class ConfigParser:
    width: int
    height: int
    entry: Tuple[int, int]
    exit: Tuple[int, int]
    seed: int
    output_file: Path
    perfect: bool

    @classmethod
    def from_file(cls, path: str) -> "ConfigParser":
        values = cls._parse_file(path)
        return cls._validate_and_build(values)

    def _parse_file(path: str) -> Dict[str, str]:
        data: Dict[str, str] = {}

        try:
            with open(path, "r", encoding="utf-8") as file:
                for line_number, raw_line in enumerate(file, start=1):
                    line = raw_line.strip()
                    if not line or line.startswith("#"):
                        continue

                    if "=" not in line:
                        raise ConfigError(
                            f"Line {line_number}: invalid format "
                            "(expected KEY=VALUE)"
                        )

                    key, value = line.split("=", 1)
                    key = key.strip().upper()
                    value = value.strip()

                    if not key or not value:
                        raise ConfigError(
                            f"Line {line_number}: empty key or value"
                        )

                    data[key] = value

        except FileNotFoundError:
            raise ConfigError(f"Configuration file not found: {path}")

        return data

    def _validate_and_build(values: Dict[str, str]) -> "ConfigParser":

        required = {"WIDTH", "HEIGHT", "ENTRY", "EXIT", "SEED",
                    "OUTPUT_FILE", "PERFECT"}
        missing = required - values.keys()

        try:
            if missing:
                raise ConfigError(f"Missing configuration keys: "
                                  f"{', '.join(sorted(missing))}")
            width = ConfigParser._parse_positive_int(values["WIDTH"], "WIDTH")
            if width < 5:
                raise ConfigError("width must be bigger than four.")
            height = ConfigParser._parse_positive_int(values["HEIGHT"],
                                                      "HEIGHT")
            if height < 5:
                raise ConfigError("height must be bigger than four.")
            entry = ConfigParser._parse_coordinates(values["ENTRY"], "ENTRY")
            exit_ = ConfigParser._parse_coordinates(values["EXIT"], "EXIT")
            seed = ConfigParser._parse_positive_int(values["SEED"], "SEED")
            output_file = Path(values["OUTPUT_FILE"])
            perfect = ConfigParser._parse_bool(values["PERFECT"], "PERFECT")

            ConfigParser._validate_bounds(entry, width, height, "ENTRY")
            ConfigParser._validate_bounds(exit_, width, height, "EXIT")

            if entry == exit_:
                raise ConfigError("ENTRY and EXIT must be different")

            return ConfigParser(
                width=width,
                height=height,
                entry=entry,
                exit=exit_,
                seed=seed,
                output_file=output_file,
                perfect=perfect,
            )
        except ConfigError as e:
            print(f"{RD}Error: {e}{R}")
            print(f"\n{RD}Please reconfigure your config file!{R}")
            sys.exit(1)

    def _parse_positive_int(value: str, name: str) -> int:
        try:
            result = int(value)
        except ValueError:
            raise ConfigError(f"{name} must be an integer")

        if result <= 0:
            raise ConfigError(f"{name} must be greater than 0")

        return result

    def _parse_coordinates(value: str, name: str) -> Tuple[int, int]:
        try:
            x_str, y_str = value.split(",", 1)
            return int(x_str), int(y_str)
        except ValueError:
            raise ConfigError(f"{name} must be in format x,y")

    def _parse_bool(value: str, name: str) -> bool:
        val = value.lower()
        if val == "true":
            return True
        if val == "false":
            return False
        raise ConfigError(f"{name} must be True or False")

    def _validate_bounds(
        coord: Tuple[int, int],
        width: int,
        height: int,
        name: str,
    ) -> None:

        x, y = coord
        if not (0 <= x < width and 0 <= y < height):
            raise ConfigError(f"{name} is outside maze bounds")

    @staticmethod
    def config_parser_output_into_dict(cls) -> dict[str,
                                                    bool | int | float | str]:
        return dict(vars(cls))


# def print_dict(dictionary: dict) -> None:
#     if isinstance(dictionary, dict):
#         for key, value in dictionary.items():
#             print(f"{key}:\t{value}".expandtabs(16))


# def config_parser_test() -> None:

#     path_to_config_file = "config.txt"

#     try:
#         config = ConfigParser.from_file(path_to_config_file)
#         config = config.config_parser_output_into_dict(config)
#     except (IndexError, ConfigError) as error:
#         print(f"Error:\t{error}")
#         return
#     print_dict(config)
#     print()
#     print(config)


# def main() -> None:
#     config_parser_test()


# if __name__ == "__main__":
#     main()
