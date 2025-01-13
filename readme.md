# Project Meraki

Finding zero-day vulnerabilities with the help of AI.

**Warning:** This project is for educational purposes only! 
By using this project, you agree to the [Terms and Conditions](TERMS_AND_CONDITIONS.md).


---

## Table of Contents
- [Dependencies](#dependencies)
- [Setup Instructions](#setup-instructions)
- [License](#license)

---

## Dependencies

| Dependency     | Version  |
|----------------|----------|
| Conda          | 24.11.3  |
| Miniforge      | 1.5.9    |
| Python         | 3.13.1   |

You need a gemini API KEY for this!
Enter your API Keys into [credentials.json](src/data/credentials.json)

---

## Setup Instructions

1. **Download and Extract**
   - Download the project folder and extract its contents.

2. **Create and Activate a New Conda Environment**
   ```bash
   conda create --name env_name
   conda activate env_name
   ```

3. **Install Required Packages**
   - Install all necessary packages from the `requirements.txt` file:
     ```bash
     pip install -r requirements.txt
     ```

4. **Add Scripts to Scan**
   - Place the scripts you want to scan inside the `scripts` directory.

5. **Run the Main Script**
   - Execute the main script using the following command:
     ```bash
     & C:/Users/YOUR_USER/.conda/envs/ENV_NAME/python.exe main.py
     ```

   - The exploits will appear on the Exploits directory

---

## License

Project Meraki © 2025 by Mu.rpy is licensed under Creative Commons Attribution 4.0 International. To view a copy of this license, visit https://creativecommons.org/licenses/by/4.0/
