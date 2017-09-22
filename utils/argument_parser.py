import argparse

from setting.CONFIG import GROUPED_CONFIG, LIST_OF_MUTUAL_GROUPS


def parse_arguments():
    arguments_parser = argparse.ArgumentParser()
    add_positional_arguments(arguments_parser)
    add_optional_arguments(arguments_parser)
    parsed_arguments = arguments_parser.parse_args()
    arguments_filtered_dict = {k: v for k, v in vars(parsed_arguments).items() if v is not False and v is not None}
    names_of_method_type = [x['key'] for x in LIST_OF_MUTUAL_GROUPS]
    method_type = [x for x in arguments_filtered_dict.keys() if x in names_of_method_type][0]
    auth = {'fullname': arguments_filtered_dict['fullname'], "password": arguments_filtered_dict['password']}
    return {'method_type': method_type, 'auth': auth, "args": arguments_filtered_dict}


def add_positional_arguments(arguments_parser):
    arguments_parser.add_argument('fullname', type=str)
    arguments_parser.add_argument('password', type=str)


def add_optional_arguments(arguments_parser):
    mutual_group = arguments_parser.add_mutually_exclusive_group(required=True)
    for mutual_arg in LIST_OF_MUTUAL_GROUPS:
        mutual_group.add_argument(mutual_arg['name'], help=mutual_arg['help'], action="store_true")

    for group_config in GROUPED_CONFIG:
        group = arguments_parser.add_argument_group(group_config['name'], group_config['description'])
        for argument_config in group_config['args']:
            group.add_argument(
                *argument_config['positional'],
                **argument_config['optional'],
            )
