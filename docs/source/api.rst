API
===

About tunnels
~~~~~~~~~~~~~

.. function:: tunnel (tunnel_type)

    Digs a tunnel via ngrok, depending on tunnel_type

    Usage:
    
        tunnel tunnel_type

    Creates a tunnel, and if such tunnel is already created just
    passes said open tunnel.

    To know which tunnel types are supported use get_tunnel_types
    command.

.. function:: close_tunnel (tunnel_type)

    Closes ngrok tunnel

    Usage:
        
        close_tunnel tunnel_type


Informational
~~~~~~~~~~~~~

.. function:: get_tunnel_types
    
        Gives info about tunnel types

.. function:: jupyter_advice
    
        Gives advice on sharing jupyter notebooks
