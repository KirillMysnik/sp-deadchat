from messages import UserMessage

from . import info


if UserMessage.is_protobuf():
    from . import deadchat_csgo
else:
    from . import deadchat_css
