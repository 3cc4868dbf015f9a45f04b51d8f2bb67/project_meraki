from src.scripts.dependencies import *
from src.scripts.logger import *

class MessageContent:
    def __init__(self) -> None:
        self.text: str = None
        self.error: str = None

class AI:
    def __init__(self, name: str = '_renny'):
        self.name: str = name
        self.world: str = None
        self.mem_dir = Path("src/data")
        self.chat_session_file = self.mem_dir / "memory.json"
        self.mem_dir.mkdir(parents=True, exist_ok=True)

        neural_network.configure(api_key=gemini_api)
        self.memory: list = self.load_file(self.chat_session_file, default=[])
        self.generation_config = GenerationConfig(
            temperature=1.95,
            top_p=0.95,
            top_k=64,
            max_output_tokens=8192,
        )
        self.model = neural_network.GenerativeModel(
            model_name="gemini-1.5-flash",
            generation_config=self.generation_config,
            system_instruction=system_prompt.replace("$NAME", name),
        )
        self.chat_session = self.model.start_chat(history=self.memory)
        self.save_file(self.chat_session_file, self.memory)

    def load_file(self, file_path, default=None) -> Union[Dict, List]:
        file_path = Path(file_path)
        try:
            if file_path.exists():
                with open(file_path, 'r') as f:
                    return json.load(f)
        except (json.JSONDecodeError, FileNotFoundError) as e:
            logging.exception(f"Failed to load file {file_path}: {e}")
        return default

    @staticmethod
    def save_file(file_path, data) -> None:
        file_path = Path(file_path)
        file_path.parent.mkdir(parents=True, exist_ok=True)
        with open(file_path, 'w') as f:
            json.dump(data, f, indent=2)

    def respond(self, message: str) -> MessageContent:
        model_content = MessageContent()
        try:
            model_content.text = self.chat_session.send_message(message).text
            self.memory.extend([
                {"role": "user", "parts": [message]},
                {"role": "model", "parts": [model_content.text]},
            ])
            self.save_file(self.chat_session_file, self.memory)
        except Exception as e:
            logging.exception("Error in respond method:")
            model_content.error = str(e)
        return model_content

searcher: AI = AI()
scripts: dict = {}


def script_scan():
    global scripts
    scripts_dir = Path("scripts")
    scripts_dir.mkdir(parents=True, exist_ok=True)  # Ensure the directory exists
    for item in scripts_dir.iterdir():
        if item.suffix == ".js":
            with item.open("r") as f:
                scripts[item.name] = f.read()
                logging.info(f"Script {item.name} loaded successfully")
        else:
            logging.warning(f"Script {item.name} is not a JavaScript file")


def found_exploits() -> List[str]:
    exploits_dir = Path("Exploits")
    exploits_dir.mkdir(parents=True, exist_ok=True)  # Ensure the directory exists
    lel = [item.name for item in exploits_dir.iterdir() if item.is_file()]

    if not lel:
        logging.warning("No exploits found")
        return []

    logging.info(f"Found {len(lel)} exploits! :>")
    return lel


def main():
    script_scan()

    count: int = 0
    for item, value in scripts.items():
        count += 1
        tempt_msg = searcher.respond(f"SYSTEM: Your Script is: ```{value}```")

        if "!ZERODAYFOUND" in (tempt_msg.text or ""):
            logging.info(f"ZERO DAY FOUND IN [{item}]!")
            logging.info(f"```{value}```")

            exploit_path = Path(f"Exploits/exploit_{count}.md")
            exploit_path.parent.mkdir(parents=True, exist_ok=True)
            with exploit_path.open('w') as f:
                f.write(f"""
Script:
```\n{value}\n```

AI Response:
```\n{tempt_msg.text}\n```
                        """)
            logging.info(f"Exploit saved as exploit_{count}.md")
        
        else:
            logging.warning(f"No exploit found for {item}")

    found_exploits()


if __name__ == "__main__":
    main()