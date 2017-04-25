# =============================================================================
# >> IMPORTS
# =============================================================================
# Python
from importlib import import_module

# Source.Python
from core import GAME_NAME
from events import Event
from filters.players import PlayerIter
from messages import UserMessage
from players.entity import Player

# DeadChat
from .core.paths import GAME_SPECIFIC_MODULES_PATH
from .info import info


# =============================================================================
# >> FUNCTIONS
# =============================================================================
def is_hltv_message(recipient_filter):
    """Return whether the recipient filter was created for HLTV bot.

    https://github.com/Source-Python-Dev-Team/Source.Python/issues/185
    """
    if hltv_index is None:
        return False

    return len(recipient_filter) == 1 and recipient_filter[0] == hltv_index


# =============================================================================
# >> GLOBAL VARIABLES
# =============================================================================
hltv_index = None


# =============================================================================
# >> GAME-SPECIFIC IMPORTS
# =============================================================================
if (GAME_SPECIFIC_MODULES_PATH / (GAME_NAME + ".py")).isfile():
    import_module('.'.join((info.name, 'games', GAME_NAME)))

else:
    if UserMessage.is_protobuf():
        from .games import protobuf
    else:
        from .games import bitbuf


# =============================================================================
# >> EVENTS
# =============================================================================
@Event('player_spawn')
def on_player_spawn(game_event):

    # We refresh HLTV index every time in case somebody kicks that poor guy
    player = Player.from_userid(game_event['userid'])
    if not player.is_hltv():
        return

    global hltv_index
    hltv_index = player.index


def load():

    # Hot plug stuff
    for player in PlayerIter():
        if not player.is_hltv():
            continue

        global hltv_index
        hltv_index = player.index
        return
