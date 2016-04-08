from core import PLATFORM
from filters.players import PlayerIter
from filters.recipients import RecipientFilter
from memory import Convention, DataType, find_binary, make_object
from memory.hooks import PreHook


if PLATFORM == 'windows':
    SAYTEXT2_FILTER_IDENTIFIER = b"\x55\x89\xE5\x57\x56\x53\x83\xEC\x2C\x8B\x55\x14\x2A\x2A\x2A\x2A\x2A\x2A\x2A\x2A\x8B\x45\x0C\x8B\x7D\x18"
else:
    SAYTEXT2_FILTER_IDENTIFIER = "_Z19UTIL_SayText2FilterR16IRecipientFilterP11CBasePlayerbPKcS4_S4_S4_S4_"


server = find_binary('server')

# void UTIL_SayText2Filter( IRecipientFilter& filter, CBasePlayer *pEntity, bool bChat, const char *msg_name, const char *param1, const char *param2, const char *param3, const char *param4 )
saytext2_filter = server[SAYTEXT2_FILTER_IDENTIFIER].make_function(
    Convention.CDECL,
    [DataType.POINTER, DataType.POINTER, DataType.BOOL, DataType.POINTER, DataType.POINTER, DataType.POINTER, DataType.POINTER, DataType.POINTER],
    DataType.VOID,
)


@PreHook(saytext2_filter)
def pre_saytext2_filter(args):
    recipient_filter = make_object(RecipientFilter, args[0])
    msg_name = args[3].get_string_array()

    if msg_name in ("Cstrike_Chat_AllDead", "Cstrike_Chat_AllSpec"):
        recipient_filter.add_all_players()

    elif msg_name == "Cstrike_Chat_T_Dead":
        recipient_filter.update(*[player.index for player in PlayerIter('t')])

    elif msg_name == "Cstrike_Chat_CT_Dead":
        recipient_filter.update(*[player.index for player in PlayerIter('ct')])
