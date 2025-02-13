from better_profanity import profanity
import re, time, itertools

## censoring curse words
# le = itertools.cycle('%$!#')
# print(''.join(next(le) if c == '*' else c for c in profanity.censor("*** for *** in range(***)")))

text: str = """
<think>
thought process... 1...
thought process.... 2...
thought process..... 3...
</think>

!bugFound([high], [6.9], [This is a zeroday bc...], [Step 1, run vscode, step 2, choose assembly as language, step 3...])
"""

exploits_found: dict = {}
for i, match in enumerate(re.findall(r"!bugFound\(\[(low|medium|high)\], \[([^\]]+)\], \[(.*?)\], \[(.*?)\]\)", text)):
    x, y, z, gg = match
    exploits_found[i+1] = {'severity': x, 'risk_rating': float(y), 'analysis': z, 'execution': gg}

for y in exploits_found.values():
    print(y)