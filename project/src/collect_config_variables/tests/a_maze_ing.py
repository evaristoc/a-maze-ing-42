import sys
from config_parser.config_parser import ConfigParser, ConfigError


def print_dict(dictionary: dict):
    if isinstance(dictionary, dict):
        for key, value in dictionary.items():
            print(f"{key}: {value}")


def config_parser_test():

    try:
        config = ConfigParser.from_file(sys.argv[1])
        config = config.config_parser_output_into_dict(config)
    except (IndexError, ConfigError) as error:
        print(f"Error:\t{error}")
        return
    print_dict(config)
    print()
    print(config)


def main() -> None:
    config_parser_test()


if __name__ == "__main__":
    main()
