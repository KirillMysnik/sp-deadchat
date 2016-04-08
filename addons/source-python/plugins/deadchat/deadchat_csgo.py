from core import PLATFORM
from engines.server import engine_server
from filters.players import PlayerIter
from filters.recipients import RecipientFilter
from memory import Convention, DataType, get_object_pointer, make_object
from memory.hooks import PreHook
from messages import UserMessage
from _messages import ProtobufMessage


if PLATFORM == "windows":
    SEND_USER_MESSAGE_INDEX = 45
else:
    SEND_USER_MESSAGE_INDEX = 45


saytext2_index = UserMessage(RecipientFilter(), 'SayText2').message_index


# virtual void SendUserMessage( IRecipientFilter &filter, int message, const google::protobuf::Message &msg ) = 0;
send_user_message = get_object_pointer(engine_server).make_virtual_function(
    SEND_USER_MESSAGE_INDEX,
    Convention.THISCALL,
    [DataType.POINTER, DataType.POINTER, DataType.INT, DataType.POINTER],
    DataType.VOID
)


@PreHook(send_user_message)
def pre_send_user_message(args):
    if args[2] != saytext2_index:
        return
    
    recipient_filter = make_object(RecipientFilter, args[1])
    buffer = make_object(ProtobufMessage, args[3])
    msg_name = buffer.get_string('msg_name')

    if msg_name in ("Cstrike_Chat_AllDead", "Cstrike_Chat_AllSpec"):
        recipient_filter.add_all_players()

    elif msg_name == "Cstrike_Chat_T_Dead":
        recipient_filter.update(PlayerIter('t'))

    elif msg_name == "Cstrike_Chat_CT_Dead":
        recipient_filter.update(PlayerIter('ct'))
