remote-mole
===========

|pypi-v| |pypi-l| |gitlab-ci| |coverage|

.. |pypi-v| image:: https://img.shields.io/pypi/v/remote-mole.svg
    :target: https://pypi.python.org/pypi/remote-mole

.. |pypi-l| image:: https://img.shields.io/pypi/l/remote-mole.svg
    :target: https://pypi.python.org/pypi/remote-mole

.. |gitlab-ci| image:: https://gitlab.com/acesrg/remote-ninja/badges/master/pipeline.svg
   :target: https://gitlab.com/acesrg/remote-ninja/-/commits/master

.. |coverage| image:: https://gitlab.com/acesrg/remote-ninja/badges/master/coverage.svg
    :target: https://gitlab.com/acesrg/remote-ninja/-/jobs/artifacts/master/file/htmlcov/index.html?job=unittest

``remote-mole`` is a CLI helper that sets up a bot that digs ngrok tunnels for you. The bots can be commanded via discord.

This way you can share a remote device with friends or colleagues, connecting to it via ``ssh`` or hosting ``jupyter notebooks`` there, and accessing them through an url in your browser.

.. toctree::
   :maxdepth: 3
   :caption: Contents:

How to install it (CLI-API)
---------------------------
Add a mole to your server!

.. image:: _static/example.gif

.. toctree::
   :maxdepth: 3

   getting_started

How to use ir (Discord API)
---------------------------
All the stuff a mole can do for you.

.. toctree::
   :maxdepth: 3

   api
