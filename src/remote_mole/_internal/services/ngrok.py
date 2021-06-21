from pyngrok import conf, ngrok

_type_description = {
    'ssh': {
        'port': 22,
        'proto': 'tcp'
        },
    'jupyter': {
        'port': 8888,
        'proto': 'http'
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
    def __init__(self, tunnel_type):
        ngrok.get_tunnels()
        if _is_already_open(tunnel_type):
            raise TunnelAlredyOpenError(
                "Such tunnel is already open"
            )
        self.ngrok_tunnel = ngrok.connect(
            _type_description[tunnel_type]['port'],
            _type_description[tunnel_type]['proto'],
        )
        self.address = get_addr_from_url(self.ngrok_tunnel.public_url)
        self.port = get_port_from_url(self.ngrok_tunnel.public_url)

    @staticmethod
    def _is_already_open(tunnel_type):
        this_tunnel_config = HOST + str(_type_description[tunnel_type]['port'])
        tunnels = ngrok.get_tunnels()
        for tunnel in tunnels:
            if tunnel.config == this_tunnel_config:
                return True
        return False

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
