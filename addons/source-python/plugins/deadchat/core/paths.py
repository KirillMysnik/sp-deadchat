# =============================================================================
# >> IMPORTS
# =============================================================================
# Source.Python
from paths import PLUGIN_PATH, PLUGIN_DATA_PATH

# DeadChat
from ..info import info


# =============================================================================
# >> GLOBAL VARIABLES
# =============================================================================
DEADCHAT_DATA_PATH = PLUGIN_DATA_PATH / info.name
GAME_SPECIFIC_MODULES_PATH = PLUGIN_PATH / info.name / "games"
