import re, os, logging, datetime, asyncio
from pathlib import Path

logPath = Path("src/data/logs")
logPath.mkdir(parents=True, exist_ok=True)
log_file_path = logPath / "live.log"
new_log_file_path = logPath / f"{datetime.datetime.now().strftime('[%Y-%m-%d %Hh_%Mm_%Ss]')}.log"

RESET = "\033[0m"
HIGHLIGHT_COLOR = "\033[1;36m"
REQUEST_HIGHLIGHT = "\033[1;38;5;115m"
COLORS = {
    "THINKING": "\033[1;96m",
    "TEST": "\033[1;96m",
    "MERAKI": "\033[1;38;5;115m",
    "INFO": "\033[1;38;5;111m",
    "WARNING": "\033[1;38;5;111m",
    "ERROR": "\033[1;38;5;111m",
    "DEBUG": "\033[1;38;5;111m",
    "EXCEPTION": "\033[1;38;5;111m",
    "CRITICAL": "\033[1;38;5;111m",
}

KEYWORDS = [
    re.escape('meraki'),
    re.escape('<think>'),
    re.escape('</think>'),
    re.escape('!bugNotFound()'),
    r"!bugFound\(\[(low|medium|high)\], \[([^\]]+)\], \[(.*?)\], \[(.*?)\]\)",
]
def add_levels(levels={'THINKING': 25, 'TEST': 35, "MERAKI": 45}):
    for name, level in levels.items():
        logging.addLevelName(level, name)
        def custom(self, message, *args, _level=level, **kwargs):
            if self.isEnabledFor(_level):
                self._log(_level, message, args, **kwargs)
        setattr(logging.Logger, name.lower(), custom)

class CustomFormatter(logging.Formatter):
    def formatTime(self, record, datefmt=None):
        asctime = super().formatTime(record, datefmt)
        return f"\033[1;38;5;159m{asctime}{RESET}"
    def format(self, record):
        record.threadName = f"\033[1;38;5;141m{record.threadName}{RESET}"
        color = COLORS.get(record.levelname, RESET)
        record.levelname = f"{color}{record.levelname}{RESET}"
        message = record.msg
        message = re.sub(r'\b(?:\d{1,3}\.){3}\d(?:\d{1,3}\.){3}\b', f'{HIGHLIGHT_COLOR}\\g<0>{RESET}', message)
        message = re.sub(r'\b\d+\.\d+\b', f'{HIGHLIGHT_COLOR}\\g<0>{RESET}', message)
        keywords_pattern = re.compile("|".join(KEYWORDS), flags=re.IGNORECASE)
        message = keywords_pattern.sub(lambda m: f'{REQUEST_HIGHLIGHT}{m.group(0)}{RESET}', message)
        record.msg = message
        return super().format(record)

class CustomFileFormatter(logging.Formatter):
    LEVEL_MAP = {
        "THINKING": "INFO",
        "TEST": "CRITICAL",
        "MERAKI": "CRITICAL",
    }
    
    def format(self, record):
        clean_level = re.sub(r'\x1b\[[0-9;]*m', '', record.levelname)
        record.levelname = self.LEVEL_MAP.get(clean_level, clean_level)
        record.msg = re.sub(r'\x1b\[[0-9;]*m', '', record.msg)
        record.threadName = re.sub(r'\x1b\[[0-9;]*m', '', record.threadName)
        return super().format(record)

async def logHandler() -> logging.Logger:
    add_levels()
    logger = logging.getLogger()
    logger.setLevel(logging.DEBUG)
    
    stream_handler = logging.StreamHandler()
    stream_handler.setFormatter(
        CustomFormatter("[%(asctime)s] [%(threadName)s] [%(levelname)s]: %(message)s")
    )
    
    file_handler = logging.FileHandler(log_file_path)
    file_handler.setFormatter(
        CustomFileFormatter("[%(asctime)s] [%(threadName)s] [%(levelname)s]: %(message)s")
    )

    logger.addHandler(stream_handler)
    logger.addHandler(file_handler)
    
    try:
        with log_file_path.open() as f:
            current_line = sum(1 for _ in f)
    except FileNotFoundError:
        current_line = 0

    if current_line >= 500:
        for handler in logger.handlers[:]:
            if isinstance(handler, logging.FileHandler):
                logger.removeHandler(handler)
                handler.close()
        os.rename(log_file_path, new_log_file_path)
        with new_log_file_path.open("a") as new_file:
            new_file.write(
                f"[{datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] [CRITICAL]: "
                f"Log rotated. Line Count: {current_line}\n"
            )
        log_file_path.touch()
        new_file_handler = logging.FileHandler(log_file_path)
        new_file_handler.setFormatter(
            CustomFileFormatter("[%(asctime)s] [%(threadName)s] [%(levelname)s]: %(message)s")
        )
        logger.addHandler(new_file_handler)
    
    return logger

if __name__ == "__main__":
    sampleMsg: str = """
<think>
Thought process...
Thought process....
Thought process.....
Thought process......
</think>

!bugFound([high], [6.9], [This is a zeroday bc...], [Step 1, run vscode, step 2, choose assembly as language, step 3...])
"""
    
    logger = asyncio.run(logHandler())
    logger.info("Request from 192.168.2.1 handled in 33.100 ms")
    logger.thinking("This is a custom THINKING level log.")
    logger.test("This is a test level log")
    logger.meraki("[Event.Handler] Bug has been found!")
    logger.info(sampleMsg)
    logger.meraki('No bug found in script')