# Code in here calls all the other scripts in under to process the data then moves the finished product into the appropiate folder on the website


import os
import shutil
import re

source = "submissions/"
# Handling exceptions that might arise if the submission folder is missing
try:
    allApplications = os.listdir(source)
except Exception as e:
    print(f"Error getting contents of {source} directory: {e}")
    quit(1)

# Terminating the script if the submissions folder is empty (No applications present)
if len(allApplications) == 0:
    print("No submissions to process...")
    quit()

directoryStatus = True

# Validating that submissions follow the correct file structure and naming conventions
rejectedApps = []  # All apps that don't match the format are added to this list
for app in allApplications:
    appFolders = os.listdir(f"{source}/{app}")

    # Checking to make sure each app folder has 2 items
    if len(appFolders) != 2:
        rejectedApps.append(app)
        print(f"Rejected App: {app} as {len(appFolders)} folders found expected 2.")
        directoryStatus = False
        continue
    # Checking to make sure thosr 2 folders are 'data' and 'readme.toml'
    if "data" not in appFolders or "readme.toml" not in appFolders:
        rejectedApps.append(app)
        print(
            f'Rejected App: {app} as required folder "data" or file "readme.toml" is missing.'
        )
        directoryStatus = False
        continue

    appData = os.listdir(f"{source}/{app}/data")

    # Making sure the data folder has 2 or more files in
    if len(appData) < 2:
        rejectedApps.append(app)
        print(
            f'Rejected App: {app} as "data" folder has insufficent number of files: {len(appData)}'
        )
        directoryStatus = False
        continue

    # Checking to make sure all files in the data folder follow the naming convention
    acceptableFileNames = re.compile(
        r"(([0-9][0-9][0-9][0-9]-(([0][0-9])|([1][0-2]))-[a-z]+.((toml)|(csv)))|([0-9][0-9][0-9][0-9]-(([0][0-9])|([1][0-2]))-[a-z]+-coverage.csv))",
        re.IGNORECASE,
    )

    incorrectFileName = False
    for file in appData:
        if acceptableFileNames.match(file) is None:
            print(f"{file} in data folder of {app} doesn't match the naming convention")
            rejectedApps.append(app)
            incorrectFileName = True
            directoryStatus = False

# Getting the list of apps which match the correct format
acceptedApps = list(set(allApplications) - set(rejectedApps))


# Creates a dictionary containing the paths of the files to be processed within the data folder
def getInfo(app):

    # Adding app name and read me path to the dict
    appPaths = {"name": app}
    appPaths.update({"readMe": rf"{source}{app}/readme.toml"})

    # Adding the contents of the datafolder to the dict
    dataPath = rf"{source}{app}/data"
    allData = os.listdir(dataPath)
    appData = []
    for data in allData:
        appData.append(rf"{dataPath}/{data}")

    appPaths.update({"data": appData})
    appDataFiles = appPaths.get("data")

    # Grouping the files for each submission together based on the naming convention
    groupedFiles = []
    for fileToProcess in appDataFiles:
        fileName = os.path.basename(fileToProcess).split(".")[0]
        fileName = fileName.replace("-coverage", "")
        group = []
        for comparisonFile in appDataFiles:
            comparisonFileName = os.path.basename(comparisonFile).split(".")[0]
            if fileName in comparisonFileName:
                group.append(comparisonFile)

        # Method counts files multiple times this line stops repeats being added to the list
        if sorted(group) in groupedFiles:
            continue
        groupedFiles.append(sorted(group))
    appPaths.update({"individualSubmissions": groupedFiles})

    return appPaths


# Loop that generates the pages for all the apps and creates pages for each of the data points
for app in acceptedApps:

    # loading a dictionary with the app info
    appInfo = getInfo(app)

    # Iterating through each submission and generating plots and a data page for it
    for data in appInfo.get("individualSubmissions"):

        # Dict to store the identified paths for each of performance,coverage and meta data
        targets = {}

        # Identifying which files in each submission are which (e.i performance, coverage etc)
        for i in range(len(data)):
            if os.path.basename(data[i]).split(".")[1] == "toml":
                targets.update({"info": data[i]})
            if "coverage" in str(data[i]):
                targets.update({"coverage": data[i]})
                continue
            if os.path.basename(data[i]).split(".")[1] == "csv":
                targets.update({"performance": data[i]})

        dataFileName = (
            os.path.basename(data[0]).split(".")[0].replace("-coverage", "")
        )  # The yyyy-mm-author of the submission
        # If no info file is present then the submission is skipped
        if targets.get("info") is None:
            print(f"No toml file found for {dataFileName} this data will be rejected")
            directoryStatus = False

        # If no performance data is present the submission is skipped
        if targets.get("performance") is None:
            print(
                f"No performance csv file found for {dataFileName} this data will be rejected"
            )
            directoryStatus = False


if not directoryStatus:
    quit(1)
