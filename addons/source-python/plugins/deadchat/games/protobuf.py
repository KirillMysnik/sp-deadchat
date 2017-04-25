# =============================================================================
# >> IMPORTS
# =============================================================================
# Source.Python
from engines.server import engine_server
from filters.players import PlayerIter
from filters.recipients import RecipientFilter
from memory import get_object_pointer, make_object
from memory.hooks import PreHook
from memory.manager import TypeManager
from _messages import ProtobufMessage
from messages import get_message_index

# DeadChat
from ..core.paths import DEADCHAT_DATA_PATH
from ..deadchat import is_hltv_message


# =============================================================================
# >> GLOBAL VARIABLES
# =============================================================================
say_text2_index = get_message_index('SayText2')
engine_server_ptr = get_object_pointer(engine_server)

type_manager = TypeManager()
engine_server_type = type_manager.create_type_from_file(
    'CVEngineServer', DEADCHAT_DATA_PATH / "protobuf" / "CVEngineServer.ini")

engine_server = make_object(engine_server_type, engine_server_ptr)


# =============================================================================
# >> HOOKS
# =============================================================================
@PreHook(engine_server.send_user_message)
def pre_send_user_message(args):
    if args[2] != say_text2_index:
        return

    recipient_filter = make_object(RecipientFilter, args[1])
    if is_hltv_message(recipient_filter):
        return

    buffer = make_object(ProtobufMessage, args[3])
    msg_name = buffer.get_string('msg_name')

    if msg_name in ("Cstrike_Chat_AllDead", "Cstrike_Chat_AllSpec"):
        recipient_filter.add_all_players()

    elif msg_name == "Cstrike_Chat_T_Dead":
        recipient_filter.update(PlayerIter('t'))

    elif msg_name == "Cstrike_Chat_CT_Dead":
        recipient_filter.update(PlayerIter('ct'))
