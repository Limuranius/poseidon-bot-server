from os import path

__SRC_DIR = path.dirname(__file__)

ROOT = f"{__SRC_DIR}/.."
CONFIGS_FOLDER = f"{ROOT}/configs"
BOT_CONFIG_PATH = f"{CONFIGS_FOLDER}/botconfig.json"
USER_DATA_PATH = f"{CONFIGS_FOLDER}/user_data.json"

LOGS_FOLDER = f"{ROOT}/logs"
LOG_FILE_PATH = f"{LOGS_FOLDER}/log.txt"
SCHEDULE_PATH = f"{LOGS_FOLDER}/schedule.json"
SCHEDULE_LOGS_PATH = f"{LOGS_FOLDER}/schedule_logs"

KV_FILE_PATH = f"{__SRC_DIR}/ui.kv"
