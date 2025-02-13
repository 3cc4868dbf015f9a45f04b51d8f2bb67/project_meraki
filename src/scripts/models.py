import json
import itertools
import re
from pathlib import Path
from typing import List, Optional, Dict

import google.generativeai as genai
from better_profanity import profanity

from src.scripts.logger import logHandler

class geminiMeraki:
    memoryPath = Path("src/data/memory.json")
    
    class MessageContent:
        def __init__(self):
            self.error: Optional[str] = None
            self.thought: Optional[str] = None
            self.bugFound: bool = True
            self.exploits_found: Dict[int, dict] = {}

    def __init__(self, tokens: List[str], logger: logHandler, reset_mem: Optional[bool]):
        self.logger = logger
        self.cycleKey = itertools.cycle(tokens)
        self.curKey = next(self.cycleKey)
        genai.configure(api_key=self.curKey)
        prompt_path = Path('src/data/.prompt')
        try:
            with prompt_path.open('r', encoding='utf-8') as f:
                system_instruction = f.read()
        except Exception as e:
            logger.error(f"Failed to read prompt file: {e}")
            system_instruction = ""
        
        self.model = genai.GenerativeModel(
            model_name="gemini-2.0-flash",
            generation_config=genai.GenerationConfig(
                temperature=1.95,
                top_p=0.95,
                top_k=40,
                max_output_tokens=8192,
            ),
            system_instruction=system_instruction,
        )
        self.memory = []
        if self.memoryPath.exists():
            try:
                with self.memoryPath.open('r', encoding='utf-8') as f:
                    self.memory = json.load(f)
            except json.JSONDecodeError:
                self.logger.error("Invalid memory.json, starting fresh")
                self.memory = []
        if reset_mem:
            try:
                with self.memoryPath.open('r', encoding='utf-8') as f:
                    json.dump([], f)
            except Exception:
                self.logger.error("Invalid memory.json, starting fresh")
                self.memory = []
        self.ChatSession = self.model.start_chat(history=self.memory)

    def save_memory(self):
        self.memoryPath.parent.mkdir(parents=True, exist_ok=True)
        with self.memoryPath.open('w', encoding='utf-8') as f:
            json.dump(self.memory, f, indent=2)

    def respond(self, script: str) -> MessageContent:
        msgCont = self.MessageContent()
        try:
            cycle_chars = itertools.cycle('%$!#')
            censored_text = ''.join(next(cycle_chars) if c == '*' else c for c in profanity.censor(script))
            response = self.ChatSession.send_message(censored_text)
            self.memory.extend([
                {"role": "user", "parts": censored_text},
                {"role": "model", "parts": [{"text": response.text}]}
            ])
            self.save_memory()
            thought_match = re.search(r'<think>(.*?)</think>', response.text, re.DOTALL)
            if thought_match:
                msgCont.thought = thought_match.group(1).strip()
            bug_matches = re.findall(r"!bugFound\(\[(low|medium|high)\], \[([^\]]+)\], \[(.*?)\], \[(.*?)\]\)", response.text)
            for i, match in enumerate(bug_matches, start=1):
                severity, risk_rating, analysis, execution = match
                try:
                    risk = float(risk_rating)
                except ValueError:
                    risk = 0.0
                msgCont.exploits_found[i] = {
                    'severity': severity,
                    'risk_rating': risk,
                    'analysis': analysis,
                    'execution': execution
                }
            if "!bugNotFound()" in response.text:
                msgCont.bugFound = False
            return msgCont
        except Exception as e:
            self.logger.error(f"Response error: {e}")
            error_str = str(e)
            if any(k in error_str for k in ('safety_rating', 'quota')):
                if 'safety_rating' in error_str:
                    msgCont.error = "Message flagged by safetyFilter! ⚠️"
                elif 'quota' in error_str:
                    msgCont.error = "Ran out of Quota!"
                    self.logger.debug("Changing API key ♻️")
                    self.curKey = next(self.cycleKey)
                    genai.configure(api_key=self.curKey)
                else:
                    msgCont.error = error_str
            else:
                msgCont.error = f"Processing error: {error_str}"
            return msgCont

if __name__ == '__main__':
    pass
