import os, logging, datetime, asyncio, json, shutil
from pathlib import Path

logPath = os.path.join("logs")
timestamp = datetime.datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
fileName = "main.live" 
log_file_path = f"{logPath}/{fileName}.log"
new_log_file_path = f"{logPath}/{timestamp}.live.log"

os.makedirs(logPath, exist_ok=True)

logFormatter = logging.Formatter("%(asctime)s [%(threadName)-12.12s] [%(levelname)-5.5s]  %(message)s")
rootLogger = logging.getLogger()
rootLogger.setLevel(logging.DEBUG)

fileHandler = logging.FileHandler(log_file_path)
fileHandler.setFormatter(logFormatter)
rootLogger.addHandler(fileHandler)

consoleHandler = logging.StreamHandler()
consoleHandler.setFormatter(logFormatter)
rootLogger.addHandler(consoleHandler)

async def handle_log_limit():
    localFileHandler = fileHandler
    if os.path.isfile(log_file_path):
        try:
            with open(log_file_path, "r") as file:
                current_line = sum(1 for _ in file)

            if current_line >= 500:
                logging.error("LOG FILE REACHED 500 LINES!")
                rootLogger.removeHandler(localFileHandler)
                localFileHandler.close()

                os.rename(log_file_path, new_log_file_path)
                with open(new_log_file_path, "a") as new_file:
                    new_file.write(f"[WARNING!!!]: Limit reached! Line Count: {current_line}. Rotating log files.\n")
                
                open(log_file_path, "w").close()
                
                localFileHandler = logging.FileHandler(log_file_path)
                localFileHandler.setFormatter(logFormatter)
                rootLogger.addHandler(localFileHandler)

                logging.info(f"Log file rotated. New log file created: {Path(new_log_file_path)}")
        except Exception as e:
            logging.error(f"Error handling log limit: {e}")

async def clear_empty_memories(memories_path: str = "logs"):
    for memory_folder in os.listdir(memories_path):
        try:
            memory_path = os.path.join(memories_path, memory_folder)
            if os.path.isdir(memory_path):
                for item in os.listdir(memory_path):
                    file_path = os.path.join(memory_path, item)
                    if 'conversation' in item and open(file_path, 'r+').read() == '[]':
                            with open(file_path, "r") as f:
                                content = f.readline().strip()
                                if content == "[]":
                                    f.close()
                                    shutil.rmtree(Path(memory_path))
        except Exception as e:
            print(f"Error processing {memory_folder}: {e}")


asyncio.run(clear_empty_memories())