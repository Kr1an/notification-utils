LIST_OF_MUTUAL_GROUPS = [
    {
        "name": "--add",
        "key": "add",
        "help": "Activate <add> commands",
    },
    {
        "name": "--get",
        "key": "get",
        "help": "Activate <get> commands",
    },
    {
        "name": "--find",
        "key": "find",
        "help": "Activate <find> commands",
    },
    {
        "name": "--update",
        "key": "update",
        "help": "Activate <update> commands",
    },
    {
        "name": "--delete",
        "key": "delete",
        "help": "Activate <delete> commands",
    },
    {
        "name": "--create_user",
        "key": "create_user",
        "help": "Activate <create-user> commands",
    },
]
GROUPED_CONFIG = [
    {
        "name": "Add Note",
        "description": "Creation of a new note.",
        "args": [
            {
                "method": "add",
                "positional": [
                    "--add_with_title",
                ],
                "optional": {
                    "help": "Title of new note.",
                },
            },
            {
                "method": "add",
                "positional": [
                    "--add_with_text",
                ],
                "optional": {
                    "help": "Text of new note.",
                },
            },
            {
                "method": "add",
                "positional": [
                    "--add_with_files",
                ],
                "optional": {
                    "help": "File(s) of new note.",
                    "nargs": "+",
                },
            },
            {
                "method": "add",
                "positional": [
                    "--add_with_tags",
                ],
                "optional": {
                    "help": "File(s) of new note.",
                    "nargs": "+",
                },
            },
        ],
    },
    {
        "name": "Delete Note(s)",
        "description": "Deleting note(s).",
        "args": [
            {
                "method": "delete",
                "positional": [
                    "--delete_by_id",
                ],
                "optional": {
                    "help": "Specify deleting note id.",
                },
            },
            {
                "method": "delete",
                "positional": [
                    "--delete_all",
                ],
                "optional": {
                    "help": "Delete all notes.",
                    "action": "store_true",
                },
            },
        ],
    },
    {
        "name": "Update Note",
        "description": "Updating note(s).",
        "args": [
            {
                "method": "update",
                "positional": [
                    "--update_by_id",
                ],
                "optional": {
                    "help": "Specify updating note id.",
                },
            },
            {
                "method": "update",
                "positional": [
                    "--update_with_title",
                ],
                "optional": {
                    "help": "Specify updating title.",
                },
            },
            {
                "method": "update",
                "positional": [
                    "--update_with_text",
                ],
                "optional": {
                    "help": "Specify updating text.",
                },
            },
            {
                "method": "update",
                "positional": [
                    "--update_with_files",
                ],
                "optional": {
                    "help": "Specify new files.",
                    "nargs": "+",
                },
            },
        ],
    },
    {
        "name": "Find Note(s)",
        "description": "Finding note(s).",
        "args": [
            {
                "method": "find",
                "positional": [
                    "--find_by_id",
                ],
                "optional": {
                    "help": "Specify finding note id.",
                },
            },
            {
                "method": "find",
                "positional": [
                    "--find_by_title",
                ],
                "optional": {
                    "help": "Specify finding note title.",
                },
            },
            {
                "method": "find",
                "positional": [
                    "--find_by_text",
                ],
                "optional": {
                    "help": "Specify finding note text.",
                },
            },
            {
                "method": "find",
                "positional": [
                    "--find_by_tag",
                ],
                "optional": {
                    "help": "Specify finding note tag.",
                },
            },
            {
                "method": "find",
                "positional": [
                    "--find_by_date",
                ],
                "optional": {
                    "help": "Specify finding note date.",
                },
            },
        ],
    },
]
