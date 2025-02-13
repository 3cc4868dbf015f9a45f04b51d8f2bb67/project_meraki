# Project Meraki

![](https://sm.mashable.com/t/mashable_me/article/y/youtube-ce/youtube-celebrates-international-cat-day-with-a-fur-tastic-p_ux9y.1248.jpg)

Project Meraki is a tool I created as a side project to help identify vulnerabilities on websites. 
Originally, I used it to pinpoint weaknesses in network gateways. Also- in the future, I’m considering developing an improved version in javascript with a more user-friendly GUI.

## Table of Contents
- [Overview](#overview)
- [Features](#features)
- [Dependencies](#dependencies)
- [Installation](#installation)
- [Usage](#usage)
- [License](#license)
- [Contributing](#contributing)
- [Acknowledgements](#acknowledgements)

## Overview
This project processes command-line arguments to configure a language model (using either Gemini or OpenAI) and scrapes the target website. It then analyzes the collected data to detect potential vulnerabilities. Reports are generated in Markdown format, separating files with detected bugs from those that are deemed safe.

## Features
- **Custom CLI:** Uses a tailored argparse help formatter with colored output.
- **Scraping & Analysis:** Automatically scrapes the website and sorts content into “bugs” or “safe” directories.
- **LLM Integration:** Leverages language models (Gemini or OpenAI) to analyze content and respond with vulnerability assessments.
- **Logging:** Provides detailed logging and error handling for smooth operation.
- **Modular Design:** Easy to maintain and extend, with future improvements planned.

## Dependencies

| Dependency      | Version/Link                                                 |
|-----------------|--------------------------------------------------------------|
| **Python**      | [3.13.2](https://www.python.org/downloads/)                  |
| **Gemini Token**| [Gemini API Key](https://aistudio.google.com/apikey)           |
| **Other Packages** | See [`requirements.txt`](./requirements.txt)              |

## Installation
1. **Clone the Repository:**
```bash
git clone https://github.com/yourusername/project-meraki.git
cd project-meraki
```

2. **Setup your environment**
   - **Using Pipenv**
   ```bash
   pipenv shell
   pipenv install -r requirements.txt
   ```

   - **Using Conda**
   ```bash
   conda create -n project-meraki python=3.13.2
   conda activate project-meraki
   pip install -r requirements.txt
   ```

## Usage
Open your terminal (or PowerShell) and navigate to the directory containing main.py. Run the script with the following command:

```bash
py main -llm [GEMINI | OPENAI] -tokens TOKEN1 TOKEN2 TOKEN3 ... -url https://example.com -m [TRUE | FALSE]
```

- -llm: Choose the language model (GEMINI or OPENAI).
- -tokens: Provide one or more tokens for the selected language model.
- -url: Specify the target website URL (must start with http:// or https://).
- -m: (Optional) Include to reset the model's memory (set to TRUE or FALSE). Omit if not needed.

## License
Project Meraki is distributed under terms outlined in the [LICENSE.md](license.md) file.

Contributions are welcome! Please open an issue or submit a pull request if you’d like to suggest improvements.

Thanks for checking this out! If you use or reference this tool, please credit me, Mu.rpy. Your support and feedback are greatly appreciated.