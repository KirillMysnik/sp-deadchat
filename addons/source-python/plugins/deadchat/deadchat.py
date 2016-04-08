from core import GAME_NAME

import info


PROTOBUF_GAMES = ("csgo", )
USING_PROTOBUF = GAME_NAME in PROTOBUF_GAMES


if USING_PROTOBUF:
    from . import deadchat_csgo
else:
    from . import deadchat_css
