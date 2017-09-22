import json
import sys
import datetime
from utils import argument_parser, intermidiate


def datetime_handler(x):
    if isinstance(x, datetime.datetime):
        return x.isoformat()
    raise TypeError("Unknown type")


def main():
    options = argument_parser.parse_arguments()
    response = intermidiate.resolve_input(options)
    return json.dumps({"response": response}, default=datetime_handler)


if __name__ == "__main__":
    response = main()
    sys.stdout.write(response)
