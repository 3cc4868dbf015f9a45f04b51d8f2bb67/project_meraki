# modules
import os
import json
import logging
from pathlib import Path
from typing import Union, Dict, List
import google.generativeai as neural_network
from google.generativeai import GenerationConfig
from random import choice

# consts
gemini_api: str = choice(json.load(open('src/data/credentials.json', 'r'))['gemini_api_list'])
system_prompt: str = open('src/data/system_instructions.info', 'r').read()