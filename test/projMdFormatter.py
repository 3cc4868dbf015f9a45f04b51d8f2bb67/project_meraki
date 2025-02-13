def create_md_file(file_name: str, thoughts: str, exploits_found: dict, error: str) -> None:
    with open(file_name, 'w') as f:
        if title:
            f.write(f"# {file_name}'s Vulnerability Report\n\n")
        
        f.write("## Exploits Found\n")
        if exploits_found:
            for i, (key, value) in enumerate(exploits_found.items(), start=1):
                f.write(f"Exploit {key}:\n")
                f.write("```\n")
                f.write(f"{value}\n")
                f.write("```\n\n")
                f.write("\n")
        else:
            f.write("No exploits found.\n\n")
        
        f.write("## Reasoning\n")
        f.write("```\n")
        f.write(f"{thoughts}\n")
        f.write("```\n\n")
        
        if error:
            f.write("\n")
            f.write("## ERROR\n")
            f.write("```\n")
            f.write(f"{error}\n")
            f.write("```\n")

if __name__ == "__main__":
    file_name = "report.md"
    title = "Security Report"
    thoughts = "The system has several vulnerabilities that need immediate attention."
    exploits_found = {
        "1": "SQL Injection vulnerability in the login module.",
        "2": "Cross-Site Scripting (XSS) in the comment section."
    }
    error = "Error: Some exploits may not be reported due to incomplete scanning."

    create_md_file(file_name, title, thoughts, exploits_found, error)
    print(f"Markdown file '{file_name}' has been created.")
