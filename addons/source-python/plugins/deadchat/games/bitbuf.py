# =============================================================================
# >> IMPORTS
# =============================================================================
# Source.Python
from filters.players import PlayerIter
from filters.recipients import RecipientFilter
from memory import make_object
from memory.hooks import PreHook
from memory.manager import TypeManager

# DeadChat
from ..core.paths import DEADCHAT_DATA_PATH
from ..deadchat import is_hltv_message


# =============================================================================
# >> GLOBAL VARIABLES
# =============================================================================
type_manager = TypeManager()
utils = type_manager.create_pipe_from_file(
    DEADCHAT_DATA_PATH / "bitbuf" / "UTIL.ini")


# =============================================================================
# >> HOOKS
# =============================================================================
@PreHook(utils.say_text2_filter)
def pre_say_text2_filter(args):
    recipient_filter = make_object(RecipientFilter, args[0])
    if is_hltv_message(recipient_filter):
        return

    msg_name = args[3]

    if msg_name in ("Cstrike_Chat_AllDead", "Cstrike_Chat_AllSpec"):
        recipient_filter.add_all_players()

    elif msg_name == "Cstrike_Chat_T_Dead":
        recipient_filter.update(PlayerIter('t'))

    elif msg_name == "Cstrike_Chat_CT_Dead":
        recipient_filter.update(PlayerIter('ct'))
