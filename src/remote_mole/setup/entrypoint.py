from __future__ import print_function, unicode_literals

import argparse
import os

from PyInquirer import prompt
import toml


AVAILABLE_BOTS = [
    'Discord',
]

CONFIG_PATH = os.path.join(
    os.path.expanduser('~'),
    '.config/remote_mole/config.toml',
)


def _create_file_with_content(filename, content):
    basename = os.path.basename(filename)
    dirname = os.path.dirname(filename)
    os.mkdir
    try:
        os.makedirs(dirname)
    except FileExistsError:
        pass

    with open(filename, "w") as f:
        f.write(content)


def register():
    questions = [
        {
            'type': 'rawlist',
            'name': 'platform',
            'message': 'Where will you talk to the bot from',
            'choices': ['Discord'],
        },
        {
            'type': 'confirm',
            'name': 'ngrok',
            'message': 'Will you use ngrok',
        },
        {
            'type': 'confirm',
            'name': 'ngrok_auth',
            'message': 'Do you want to set up a ngrok token (recommended)',
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

    if answers['ngrok']:
        ngrok_questions = [
            {
                'type': 'input',
                'name': 'region',
                'message': 'Ngrok region:',
            },
        ]
        if answers['ngrok_auth']:
            ngrok_questions.append(
                {
                    'type': 'input',
                    'name': 'ngrok_token',
                    'message': 'ngrok token: ',
                },
            )
        platform_answers['ngrok'] = prompt(ngrok_questions)

    _create_file_with_content(
        CONFIG_PATH,
        toml.dumps(platform_answers),
    )


def main():
    parser = argparse.ArgumentParser(
        description="remote_mole"
    )
    parser.add_argument(
        '-register', action='store_true',
        help='Register or overwrite mole configuration',
    )
    parser.add_argument(
        '-start', action='store_true',
        help='Start the mole daemon',
    )
    args = parser.parse_args()

    if args.register:
        register()
        return 0

    if args.run:
        run()
        return 0


if __name__ == "__main__":
    main()
