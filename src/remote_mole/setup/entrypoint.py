import argparse
import configparser
import os

import questionary


PROJECT_NAME = 'remote_mole'

AVAILABLE_BOTS = [
    'Discord',
]

CONFIG_PATH = os.path.join(
    os.path.expanduser('~'),
    f'.config/{PROJECT_NAME}/config.toml',
)

SYSD_SERVICE_PATH = os.path.join(
    os.path.expanduser('~'),
    f'.config/systemd/user/{PROJECT_NAME}.service'
)

PY_EXEC_PATH = '/usr/bin/python3'


def _create_file_with_content(filename, config):
    dirname = os.path.dirname(filename)
    os.mkdir
    try:
        os.makedirs(dirname)
    except FileExistsError:
        pass

    with open(filename, "w") as f:
        config.write(f)


def register():
    platform_config = configparser.ConfigParser()
    try:
        bot_token = questionary.text('Discord bot token').unsafe_ask()
        bot_keyword = questionary.text(
            'To what keyword should the bot listen',
        ).unsafe_ask()
        platform_config['Discord'] = {
            'token': bot_token,
            'keyword': bot_keyword,
        }

        auth_ngrok = questionary.confirm(
            'Do you want to set up a ngrok token (recommended)',
            auto_enter=False,
        ).unsafe_ask()

        ngrok_data = {}
        if auth_ngrok:
            ngrok_token = questionary.text('ngrok token').unsafe_ask()
            ngrok_data['ngrok_token'] = ngrok_token

        ngrok_region = questionary.select(
            'ngrok region',
            choices=[
                {'name': 'South America', 'value': 'sa'},
                {'name': 'United States', 'value': 'us'},
                {'name': 'Europe', 'value': 'eu'},
                {'name': 'Asia or Pacific', 'value': 'ap'},
                {'name': 'Australia', 'value': 'au'},
                {'name': 'Japan', 'value': 'jp'},
                {'name': 'India', 'value': 'in'},
            ]
        ).unsafe_ask()

    except KeyboardInterrupt:
        print("Cancelled by user")
        return

    ngrok_data['region'] = ngrok_region
    platform_config['ngrok'] = ngrok_data

    _create_file_with_content(
        CONFIG_PATH,
        platform_config,
    )


def start():
    config = configparser.ConfigParser()
    config.optionxform = str
    config.read(CONFIG_PATH)

    sysd_file = configparser.ConfigParser()
    sysd_file.optionxform = str

    this_file = os.path.realpath(__file__)
    pkg_dir = os.path.dirname(os.path.dirname(this_file))

    if 'Discord' in config.sections():
        daemon_path = os.path.join(
            pkg_dir,
            '_internal/platforms/discord/daemon.py'
        )
    else:
        raise EnvironmentError('No platforms are configured!')

    sysd_file['Unit'] = {
        'Description': PROJECT_NAME,
        'After': 'network-online.target',
        'Wants': 'network-online.target systemd-networkd-wait-online.service',
    }
    sysd_file['Service'] = {
        'ExecStart': f'{PY_EXEC_PATH} {daemon_path}',
        'Restart': 'on-failure',
        'Environment': 'PYTHONUNBUFFERED=1',
    }
    sysd_file['Install'] = {
        'WantedBy': 'default.target',
    }

    _create_file_with_content(
        SYSD_SERVICE_PATH,
        sysd_file,
    )
    os.system('systemctl --user daemon-reload')

    os.system(f'systemctl --user start {PROJECT_NAME}')


def stop():
    os.system(f'systemctl --user stop {PROJECT_NAME}')


def status():
    os.system(f'systemctl --user status {PROJECT_NAME}')


def main():
    parser = argparse.ArgumentParser(
        description=PROJECT_NAME
    )
    parser.add_argument(
        '-register', action='store_true',
        help='Register or overwrite mole configuration',
    )
    parser.add_argument(
        '-start', action='store_true',
        help='Start the mole daemon',
    )
    parser.add_argument(
        '-stop', action='store_true',
        help='Stop the mole daemon',
    )
    parser.add_argument(
        '-status', action='store_true',
        help='Get service status from systemctl',
    )
    args = parser.parse_args()

    if args.register:
        register()
        return 0

    if args.start:
        start()
        return 0

    if args.stop:
        stop()
        return 0

    if args.status:
        status()
        return 0


if __name__ == "__main__":
    main()
