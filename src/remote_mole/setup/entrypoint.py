from __future__ import print_function, unicode_literals

import os

from PyInquirer import prompt
import toml


AVAILABLE_BOTS = [
    'Discord',
]
CONFIG_PATH = '/etc/remote_mole/config.toml'
TEMP_DIR = '/tmp'


def _create_file_with_content(filename, content):
    basename = os.path.basename(filename)
    dirname = os.path.dirname(filename)
    non_root_path = os.path.join(TEMP_DIR, basename)
    with open(non_root_path, "w") as f:
        f.write(content)

    are_we_root = os.getuid() == 0
    if are_we_root:
        root_exec = ''
    else:
        root_exec = 'sudo'
        print("remote_mole needs root access to write config files.")

    os.system(f'{root_exec} mkdir -p {dirname}')
    os.system(f'{root_exec} mv {non_root_path} {CONFIG_PATH}')
    print("...done, config was written")


def register():
    questions = [
        {
            'type': 'rawlist',
            'name': 'platform',
            'message': 'Where will you talk to the bot from',
            'choices': ['Discord'],
        },

    ]
    answers = prompt(questions)
    platform_answers = {}
    if answers['platform'] == 'Discord':
        discord_questions = [
            {
                'type': 'input',
                'name': 'token',
                'message': 'Discord bot token:',
            },
            {
                'type': 'input',
                'name': 'keyword',
                'message': 'To what keyword should the bot listen:',
            },
        ]
        platform_answers['Discord'] = prompt(discord_questions)

    _create_file_with_content(
        CONFIG_PATH,
        toml.dumps(platform_answers),
    )
