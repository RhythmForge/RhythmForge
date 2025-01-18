<p align="center">
<img src="https://github.com/RhythmForge/RhythmForge-Server/blob/c38d7501e04d1390f999d7f28d30256c4b518330/.github/images/RHYTHMFORGE_LOGO_FINAL_256x256.jpg" alt="RhythmForge"/>
</p>

# RhythmForge-Server

[![Python 3.11+](https://img.shields.io/badge/python-3.11+-blue.svg)](https://www.python.org/downloads/)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/ambv/black)
[![pre-commit.ci status](https://results.pre-commit.ci/badge/github/osuAkatsuki/bancho.py/master.svg)](https://results.pre-commit.ci/latest/github/osuAkatsuki/bancho.py/master)
[![Discord](https://discordapp.com/api/guilds/748687781605408908/widget.png?style=shield)](https://discord.gg/ShEQgUx)

RhythmForge-Server runs on bancho.py-ex, which is an in-progress osu! server implementation for developers of all levels of experience interested in hosting their own osu private server instance(s).

the project is developed primarily by the Akatsuki team, and our aim is to create the most easily maintainable, reliable, and feature-rich osu! server implementation available.

the main developer of bancho.py-ex is osuNoLimits

If you are interested in running or contributing to bancho.py, you should head over to the bancho.py wiki.

## Extra features 
- 🧩 Redis pubsubs for: [(wiki)](https://github.com/osu-NoLimits/bancho.py-ex/wiki/Pubsubs) 
    - Ranking beatmaps
    - Un/restricting users
    - Wipe users
    - Send a alert to online players
    - Give donator
    - Add or remove priv
- 🧩 Prometheus metric support (when enabled)
- 🧩 First place webhook (when enabled)
- 🧩 2016 client support

## License

**bancho.py-ex** is licensed under the [MIT License](https://opensource.org/license/mit/). Please see the [LICENSE](https://github.com/osuAkatsuki/bancho.py/blob/master/LICENSE) file for more information.
