from pyngrok import conf, ngrok

_type_description = {
    'ssh': {
        'port': 22,
        'proto': 'tcp',
    },
    'jupyter': {
        'port': 8888,
        'proto': 'http',
    },
}
HOST = 'localhost'


def _get_addr_from_url(url):
    return url.split("//")[-1].split(":")[0]


def _get_port_from_url(url):
    return url.split("//")[-1].split(":")[1]


class TunnelAlredyOpenError(Exception):
    pass


class Tunnel:
    @staticmethod
    def _is_already_open(tunnel_type):
        PORT = str(_type_description[tunnel_type]['port'])

        if _type_description[tunnel_type]['proto'] == 'tcp':
            this_tunnel_config = f'{HOST}:{PORT}'
        elif _type_description[tunnel_type]['proto'] == 'http':
            this_tunnel_config = f'http://{HOST}:{PORT}'
        else:
            raise ValueError('Unexpected tunnel type')

        tunnels = ngrok.get_tunnels()
        if tunnels is None:
            return False
        for tunnel in tunnels:
            if tunnel.config['addr'] == this_tunnel_config:
                return True
        return False

    def __init__(self, tunnel_type):
        ngrok.get_tunnels()
        if Tunnel._is_already_open(tunnel_type):
            raise TunnelAlredyOpenError(
                "Such tunnel is already open"
            )
        self.ngrok_tunnel = ngrok.connect(
            _type_description[tunnel_type]['port'],
            _type_description[tunnel_type]['proto'],
        )
        self.address = _get_addr_from_url(self.ngrok_tunnel.public_url)
        if tunnel_type == 'ssh':
            self.port = _get_port_from_url(self.ngrok_tunnel.public_url)

    def is_still_open(self):
        tunnels = ngrok.get_tunnels()
        for tunnel in tunnels:
            if tunnel.public_url == self.ngrok_tunnel.public_url:
                return True
        return False

    def close(self):
        ngrok.disconnect(self.ngrok_tunnel.public_url)


def authenticate(token):
    ngrok.set_auth_token(token)


def set_region(region):
    conf.get_default().region = region
