# Python Script to check that all Toml files within the submission folder are valid
import os
import tomllib as toml

source = "submissions/"

allApplications = os.listdir(source)
# Terminating the script if the submissions folder is empty (No applications present)
if len(allApplications) == 0:
    print("No submissions to process...")
    quit()


def checkToml(path):
    if os.path.basename(path).split(".")[1] == "toml":
        try:
            f = open(path, "rb")
            info = toml.load(f)
        except Exception as e:
            return False

    return True


allTomlsValid = True
for app in allApplications:
    if not checkToml(f"{source}{app}/readme.toml"):
        print(f"Invalid toml file: {source}{app}/readme.toml")
        allTomlsValid = False

    dataFolder = os.listdir(f"{source}{app}/data")
    for dataFile in dataFolder:
        if not checkToml(f"{source}{app}/data/{dataFile}"):
            print(f"Invalid toml file: {source}{app}/data/{dataFile}")
            allTomlsValid = False

if not allTomlsValid:
    quit(1)
