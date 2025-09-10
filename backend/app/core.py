import logging
from logging.handlers import TimedRotatingFileHandler
from pathlib import Path
from slowapi import Limiter
from slowapi.util import get_remote_address

# --- Ensure logs directory exists ---
log_dir = Path("logs")
log_dir.mkdir(exist_ok=True)

# --- Rotating file handler (new log file every day, keep 7 days) ---
file_handler = TimedRotatingFileHandler(
    filename=log_dir / "maps_assistant.log",
    when="midnight",      # rotate at midnight
    interval=1,           # every 1 day
    backupCount=7,        # keep last 7 days of logs
    encoding="utf-8"
)

# --- Console handler (still prints to stdout) ---
console_handler = logging.StreamHandler()

# --- Logging setup ---
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[file_handler, console_handler]
)

logger = logging.getLogger("maps-assistant")

# --- Rate limiter setup ---
limiter = Limiter(key_func=get_remote_address)
