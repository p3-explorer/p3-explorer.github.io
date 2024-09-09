# Code in here calls all the other scripts in under to process the data then moves the finished product into the appropiate folder on the website


import os
import shutil
import re
from generatePlots import csvToPlot, page


source = "submissions/"
destination = "docs/"
os.chdir("..")
# Handling exceptions that might arise if the submission folder is missing
try:
    allApplications = os.listdir(source)
except Exception as e:
    print(f"Error getting contents of {source} directory: {e}")
    quit()

# Terminating the script if the submissions folder is empty (No applications present)
if len(allApplications) == 0:
    print("No submissions to process...")
    quit()

# Validating that submissions follow the correct file structure and naming conventions
rejectedApps = []  # All apps that don't match the format are added to this list
for app in allApplications:
    appFolders = os.listdir(f"{source}/{app}")

    # Checking to make sure each app folder has 2 items
    if len(appFolders) != 2:
        rejectedApps.append(app)
        print(f"Rejected App: {app} as {len(appFolders)} folders found expected 2.")
        continue
    # Checking to make sure thosr 2 folders are 'data' and 'readme.toml'
    if "data" not in appFolders or "readme.toml" not in appFolders:
        rejectedApps.append(app)
        print(
            f'Rejected App: {app} as required folder "data" or file "readme.toml" is missing.'
        )
        continue

    appData = os.listdir(f"{source}/{app}/data")

    # Making sure the data folder has 2 or more files in
    if len(appData) < 2:
        rejectedApps.append(app)
        print(
            f'Rejected App: {app} as "data" folder has insufficent number of files: {len(appData)}'
        )
        continue

    # Checking to make sure all files in the data folder follow the naming convention
    acceptableFileNames = re.compile(
        r"(([0-9][0-9][0-9][0-9]-(([0][0-9])|([1][0-2]))-[a-z]+.((toml)|(csv)))|([0-9][0-9][0-9][0-9]-(([0][0-9])|([1][0-2]))-[a-z]+-coverage.csv))",
        re.IGNORECASE,
    )

    incorrectFileName = False
    for file in appData:
        if acceptableFileNames.match(file) is None:
            print(
                f"Rejected App: {app} as {file} in data folder is of incorrect format"
            )
            rejectedApps.append(app)
            incorrectFileName = True
        if incorrectFileName:
            break

print(f"RejectedApps: {rejectedApps}")

# Getting the list of apps which match the correct format
acceptedApps = list(set(allApplications) - set(rejectedApps))
print(f"Moving: {acceptedApps} on to the processing stage")


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


# Removing all current posts/images in order to regenerate pages from scratch
if os.path.isdir(f"{os.getcwd()}/docs/_posts"):
    shutil.rmtree(f"{os.getcwd()}/docs/_posts")

if os.path.isdir(f"{os.getcwd()}/docs/static/assets"):
    shutil.rmtree(f"{os.getcwd()}/docs/static/assets")

if os.path.isdir(f"{os.getcwd()}/docs/static/plots"):
    shutil.rmtree(f"{os.getcwd()}/docs/static/plots")

# Loop that generates the pages for all the apps and creates pages for each of the data points
for app in acceptedApps:

    # loading a dictionary with the app info
    appInfo = getInfo(app)

    # Instantiating a page class to handle the creation of this apps pages
    appPage = page(appInfo)

    # Variable to keep track of how many data pages have successfully been created
    validData = 0

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
            continue

        # If no performance data is present the submission is skipped
        if targets.get("performance") is None:
            print(
                f"No performance csv file found for {dataFileName} this data will be rejected"
            )
            continue

        # Passing information into the plot creation class
        plots = csvToPlot(
            rf'{appInfo.get("name")}/{dataFileName}',
        )

        # Creating the plots, plotted is a boolean which stores whether this is successful or not
        plotted = plots.createPlots(targets)

        # If creating the plots was successful a datapage can be created
        if plotted:
            appPage.generateDataPost(dataFileName, targets.get("info"))
            print(rf'output folder: {appInfo.get("name")}/{dataFileName}')

            # Incrementing valid data as the data was plotted successfully
            validData += 1
    # If there is any valid data for the app the app page can be created
    if validData > 0:
        appPage.generateAppPage()

# Creating a zip file of the plots for the download link
os.chdir(f"{os.getcwd()}/docs/static")
allApps = os.listdir("assets/")

# Gets a list of all the apps from the assets folder as the list of accepted apps might contain apps for which plots haven't been generated
if len(allApps) > 0:
    # Iterating through all apps assets
    for app in allApps:
        allData = os.listdir(rf"assets/{app}")
        # Creating the zip file for each datapage's plots
        for data in allData:
            shutil.make_archive(
                f"plots/{app}/{data}/plots", "zip", rf"assets/{app}/{data}"
            )
