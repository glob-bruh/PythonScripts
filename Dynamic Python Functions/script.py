
import os

all_entries = os.listdir("module")

for x in all_entries: 
        dirName = x
        files = os.listdir("module/" + x)
        for y in files:
            if y.split(".")[1] == "config":
                with open("module/" + x + "/" + y) as f: 
                    configContent = f.read()

targPath = "module/" + dirName + "/" + configContent.split("=")[1].strip()
print(targPath)