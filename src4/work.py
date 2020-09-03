import re
key = "  [ [  "
print(len(re.findall(r'\w+', key).s))
print(key.strip())