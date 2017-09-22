import json
from utils import argument_parser, intermidiate


def main():
    options = argument_parser.parse_arguments()
    response = intermidiate.resolve_input(options)
    return json.dumps({"response": response})


if __name__ == "__main__":
    main()
