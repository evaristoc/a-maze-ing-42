from dataclasses import dataclass
from pathlib import Path
from typing import Dict, Tuple

from collect_config_variables.error_handlers import ConfigError


@dataclass(frozen=True)
class ConfigParser:
    width: int
    height: int
    entry: Tuple[int, int]
    exit: Tuple[int, int]
    seed: int
    output_file: Path
    perfect: bool
    music_file: bool
    color_walls: int
    color_background: int
    color_fourtytwo: int
    color_entry: int
    color_exit: int
    color_menutext: int
    cell_size: int
    perc_wall: float
    perc_padding: float

    @classmethod
    def from_file(cls, path: str) -> "ConfigParser":
        values = cls._parse_file(path)
        return cls._validate_and_build(values)

    @staticmethod
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

    @staticmethod
    def _validate_and_build(values: Dict[str, str]) -> "ConfigParser":
        required = {
            "WIDTH", "HEIGHT", "ENTRY", "EXIT",
            "SEED", "OUTPUT_FILE", "PERFECT",
        }
        missing = required - values.keys()
        if missing:
            raise ConfigError(
                f"Missing configuration keys: "
                f"{', '.join(sorted(missing))}"
            )
        width = ConfigParser._parse_positive_int(
            values["WIDTH"], "WIDTH"
        )
        if width < 5:
            raise ConfigError("width must be bigger than four.")
        height = ConfigParser._parse_positive_int(
            values["HEIGHT"], "HEIGHT"
        )
        if height < 5:
            raise ConfigError("height must be bigger than four.")
        entry = ConfigParser._parse_coordinates(
            values["ENTRY"], "ENTRY"
        )
        exit_ = ConfigParser._parse_coordinates(
            values["EXIT"], "EXIT"
        )
        seed = ConfigParser._parse_positive_int(
            values["SEED"], "SEED"
        )
        output_file = Path(values["OUTPUT_FILE"])
        perfect = ConfigParser._parse_bool(
            values["PERFECT"], "PERFECT"
        )
        ConfigParser._validate_bounds(entry, width, height, "ENTRY")
        ConfigParser._validate_bounds(exit_, width, height, "EXIT")
        if entry == exit_:
            raise ConfigError("ENTRY and EXIT must be different")
        music_file = ConfigParser._parse_bool(
            values["MUSIC_FILE"], "MUSIC_FILE"
        )
        color_walls = ConfigParser._parse_hex_color(
            values["COLOR_WALLS"], "COLOR_WALLS"
        )
        color_background = ConfigParser._parse_hex_color(
            values["COLOR_BACKGROUND"], "COLOR_BACKGROUND"
        )
        color_fourtytwo = ConfigParser._parse_hex_color(
            values["COLOR_FOURTYTWO"], "COLOR_FOURTYTWO"
        )
        color_entry = ConfigParser._parse_hex_color(
            values["COLOR_ENTRY"], "COLOR_ENTRY"
        )
        color_exit = ConfigParser._parse_hex_color(
            values["COLOR_EXIT"], "COLOR_EXIT"
        )
        color_menutext = ConfigParser._parse_hex_color(
            values["COLOR_MENUTEXT"], "COLOR_MENUTEXT"
        )
        cell_size = ConfigParser._parse_positive_int(
            values["CELL_SIZE"], "CELL_SIZE"
        )
        perc_wall = ConfigParser._parse_percentage(
            values["PERC_WALL"], "PERC_WALL"
        )
        perc_padding = ConfigParser._parse_percentage(
            values["PERC_PADDING"], "PERC_PADDING"
        )
        return ConfigParser(
            width=width,
            height=height,
            entry=entry,
            exit=exit_,
            seed=seed,
            output_file=output_file,
            perfect=perfect,
            music_file=music_file,
            color_walls=color_walls,
            color_background=color_background,
            color_fourtytwo=color_fourtytwo,
            color_entry=color_entry,
            color_exit=color_exit,
            color_menutext=color_menutext,
            cell_size=cell_size,
            perc_wall=perc_wall,
            perc_padding=perc_padding,
        )

    @staticmethod
    def _parse_positive_int(value: str, name: str) -> int:
        try:
            result = int(value)
        except ValueError:
            raise ConfigError(f"{name} must be an integer")
        if result <= 0:
            raise ConfigError(f"{name} must be greater than 0")
        return result

    @staticmethod
    def _parse_coordinates(value: str, name: str) -> Tuple[int, int]:
        try:
            x_str, y_str = value.split(",", 1)
            return int(x_str), int(y_str)
        except ValueError:
            raise ConfigError(f"{name} must be in format x,y")

    @staticmethod
    def _parse_bool(value: str, name: str) -> bool:
        val = value.lower()
        if val == "true":
            return True
        if val == "false":
            return False
        raise ConfigError(f"{name} must be True or False")

    @staticmethod
    def _parse_hex_color(value: str, name: str) -> int:
        if not value.startswith("0x"):
            raise ConfigError(f"{name} must start with 0x")
        try:
            result = int(value, 16)
        except ValueError:
            raise ConfigError(f"{name} must be a valid hexadecimal value")
        if result < 0 or result > 0xFFFFFFFF:
            raise ConfigError(
                f"{name} must be in ARGB hex format 0xAARRGGBB"
            )
        return result

    @staticmethod
    def _parse_percentage(value: str, name: str) -> float:
        try:
            result = float(value)
        except ValueError:
            raise ConfigError(f"{name} must be a float")
        if result < 0 or result >= 1:
            raise ConfigError(
                f"{name} must be equal to or greater "
                "than 0 and smaller than 1"
            )
        return result

    @staticmethod
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
    def config_parser_output_into_dict(
        cls: "ConfigParser",
    ) -> dict[str, bool | int | float | str]:
        return dict(vars(cls))
