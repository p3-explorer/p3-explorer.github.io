import matplotlib.pyplot as plt
import pandas as pd
import p3analysis as p3
import os
from datetime import datetime
import numpy as np
import warnings
import tomllib as toml

warnings.filterwarnings("ignore")


class csvToPlot:
    """csvToPlot contains all the logic to create the P3 plots and save them in the appropiate place"""

    def __init__(self, outputFolder):
        """Constructor

        Parameters:
        targets(list): List of the file paths for a submission eg readme,coverage etc
        outputFolder(String): The name of the folder plots should be saved in within the assets folder

        """
        # Destination path where the plots will be saved
        self.destinationPath = rf"{os.getcwd()}/docs/static/assets/{outputFolder}"

    def createPlots(self, targets):
        """Calls the functions to create each plot and manages any exceptions that may arise

        Parameters:
        targets(dict): List of the file paths for a submission eg readme,coverage etc

        returns:
        boolean: returns false if the plots could not be generated, true otherwise

        """

        self.targets = targets
        print(f'Targets: {self.targets}')
        infoPath = open(self.targets.get("info"), "rb")
        infoData = toml.load(infoPath)
        self.fom = infoData.get("fom")

        if self.fom is None:
            self.fom = "Figure of Merit (FoM)"

        # Creation of directory for the plots to be saved into
        os.makedirs(rf"{self.destinationPath}", exist_ok=True)

        # Calling methods to create plots
        performanceData = pd.read_csv(self.targets.get("performance"))
        try:
            performanceData = self._autoProject(performanceData)
            performanceData.sort_values("application")

            coveragePath = self.targets.get("coverage")
            # Only attempting to create nav chart if coverage data is present
            if coveragePath is not None:
                coverageData = pd.read_csv(coveragePath)
                self.createNav(performanceData, coverageData)
            self.createCascade(performanceData)
            self.createBarChart(performanceData)
        except Exception as e:
            print(f"Generating the plots errored: {e}")
            return False
        return True

    def _maintainOrder(self, df):
        """Given a dataframe it returns the unique elements in the order they appear in the dataframe

        Parameters:
        df(DataFrame): Performance dataframe as it was loaded from the CSV

        Returns:
        List: Elements in the order they appear in the dataframe

        """
        return df.drop_duplicates().values.tolist()

    def _autoProject(self, df):
        """Converts columns of the performance data to P3 library accepted columns

        Parameters:
        df(DataFrame): Performance dataframe as it was loaded from the CSV

        Returns:
        DataFrame: Performance data with columns P3 accepts
        """
        if set(["problem", "application", "platform", "fom"]).issubset(set(df.columns)):
            projectedDf = p3.data.projection(
                df,
                problem=["problem"],
                platform=["platform"],
                application=["application"],
            )
            return projectedDf
        if set(["problem", "model", "platform", "fom"]).issubset(set(df.columns)):
            projectedDf = p3.data.projection(
                df, problem=["problem"], platform=["platform"], application=["model"]
            )
            return projectedDf
        if set(["name", "arch", "language", "fom"]).issubset(set(df.columns)):
            projectedDf = p3.data.projection(
                df, problem=["name"], platform=["arch"], application=["language"]
            )
            return projectedDf

        raise Exception("Data not of one of the required forms")

    def createBarChart(self, performanceData):
        """Creates the bar chart and saves it into datapages folder within the assets folder

        Parameters:
        performance(dataFrame): pandas dataframe containing the performance data

        """
        print("Creating bar chart")

        platforms = performanceData["platform"].unique()
        applications = performanceData["application"].unique()

        dataToPlot = {}
        for app in applications:
            byApp = performanceData[performanceData["application"] == app]
            values = []
            for platform in platforms:
                if byApp[byApp["platform"] == platform].empty:
                    values.append(0)
                else:
                    values.append(byApp[byApp["platform"] == platform]["fom"].values[0])

            dataToPlot.update({app: values})

        values = np.array([dataToPlot[app] for app in applications])

        num_applications = len(applications)
        num_platforms = len(platforms)
        platform_indices = np.arange(num_platforms)
        bar_width = 0.1

        cmap = plt.get_cmap("tab10")
        cmap = cmap.resampled(len(applications))
        colors = cmap(np.linspace(0, 1, len(applications)))
        appColours = {app: color for app, color in zip(applications, colors)}

        fig, ax = plt.subplots(figsize=(12, 5))
        for i, app in enumerate(applications):
            ax.bar(
                platform_indices + i * bar_width,
                values[i],
                bar_width,
                label=app,
                color=appColours.get(app),
            )

        ax.set_xlabel("Platforms")
        ax.set_ylabel(self.fom)
        ax.set_title(f"{self.fom} for application grouped by platform")
        ax.set_xticks(platform_indices + bar_width * (num_applications - 1) / 2)
        ax.set_xticklabels(platforms)
        ax.legend(title="Application", loc="upper left", ncol=3)

        plt.savefig(
            rf"{self.destinationPath}/barChart.png",
            bbox_inches="tight",
        )

    def createCascade(self, performance):
        """Creates the Csacade plot and saves it into datapages folder within the assets folder

        Parameters:
        performance(dataFrame): pandas dataframe containing the performance data

        """
        print("Creating cascade")

        performanceData = performance

        performanceData = p3.metrics.application_efficiency(performanceData)
        performanceData.sort_values("application")

        fig = plt.figure(figsize=(6, 5))
        ax = p3.plot.cascade(performanceData)

        plt.savefig(
            rf"{self.destinationPath}/cascade.png",
            bbox_inches="tight",
        )

        cascadeTex = p3.plot.cascade(performanceData, backend="pgfplots")
        cascadeTex.save(rf"{self.destinationPath}/cascade.tex")

    def createNav(self, performance, coverage):
        """Creates the Nav Chart and saves it into datapages folder within the assets folder

        Parameters:
        performance(dataFrame): pandas dataframe containing the performance data
        coverage(dataFrame): pandas dataframe containing the coverage data

        """
        print("Creating Navchart")

        # Checking whether coverage data is coverage or divergence data
        if set(["problem", "application", "divergence"]).issubset(set(coverage.columns)):
            div = coverage
        else:
            # Making sure the coverage_key column is present in performance data otherwise the navchart can't be created
            if not "coverage_key" in performance.columns:
                print(f'coverage_key column not found in performance data, cannot create nav chart')
                return
            div = p3.metrics.divergence(performance, coverage)
            

        effs = p3.metrics.application_efficiency(performance)
        
        pp = p3.metrics.pp(effs)

        fig = plt.figure(figsize=(5, 5))
        ax = p3.plot.navchart(pp, div)
        plt.savefig(
            rf"{self.destinationPath}/navChart.png",
            bbox_inches="tight",
        )
        navTex = p3.plot.navchart(pp, div, backend="pgfplots")
        navTex.save(rf"{self.destinationPath}/navChart.tex")


class page:
    """The page class contains all the logic to handle the creation of the pages for each application and study"""

    def __init__(self, appInfo):
        self.appInfo = appInfo
        self.appName = appInfo.get("name")

    def generateDataPost(self, filename, infoPath):
        """Loads and populates the app template then saves it in the Jekyll posts folder

        Parameters:
        fileName (string): The name of the datapost file & folder in which assets will be saved

        """

        # Loads info file into a dictionary
        self.info = self.parseInfo(infoPath)

        # Loads template and using find and replace to populate it with data
        with open("scripts/templates/dataTemplate.txt", "r") as f:
            fileContents = f.read()

            # Adding the title and the file path names
            fileContents = fileContents.replace(
                "$TITLE", str(self.info.get("title")).replace(":", "&#58;")
            )
            fileContents = fileContents.replace("$OUTPUTFOLDER", f"{self.appName}/{filename}")

            authors = ""
            for author in self.info.get("authors"):
                authors += author + ", "
            authors = authors[0 : len(authors) - 2]

            fileContents = fileContents.replace("$AUTHOR", authors)

            tags = ""
            for tag in self.info.get("tags"):
                tags += tag + ", "
            tags = tags[0 : len(tags) - 2]
            tags.replace("'", "")

            fileContents = fileContents.replace("$APPNAME", self.appName)
            fileContents = fileContents.replace("$TAGS", tags)
            fileContents += "\n"

            # Links are lists 0-What the link is,1-The link itself
            links = self.info.get("sources")
            for link in links:
                fileContents += f"[{link[0]}]({link[1]})<br>"

            fileContents = fileContents.replace(
                "$DATE", os.path.basename(infoPath).split(".")[0][0:7]
            )
            fileContents = fileContents.replace(
                "$DOI",
                f'[{self.info.get("doi")}](https://doi.org/{self.info.get("doi")})',
            )

            fileContents = fileContents.replace("$DESCRIPTION", self.info.get("description"))

            os.makedirs(rf"{os.getcwd()}/docs/_posts/{self.appName}", exist_ok=True)

            # Getting current date as jekyll requires posts have a date (also serves to see when the website was last built I guess)
            today = datetime.today()
            date = today.strftime("%Y-%m-%d")

            with open(
                f"{os.getcwd()}/docs/_posts/{self.appName}/{date}-D{filename}.md", "w+"
            ) as o:
                o.write(fileContents)
                o.close()
            print(f"Generated data post: {filename}")

    def generateAppPage(self):
        """Loads and populates the app template then saves it in the Jekyll posts folder"""

        with open("scripts/templates/appTemplate.txt", "r") as f:
            fileContents = f.read()

            # Adding the title and the file path names
            title = self.appName
            fileContents = fileContents.replace("$APPNAME", self.appName)

            j = open(self.appInfo.get("readMe"), "rb")
            readMe = toml.load(j)

            if readMe.get("title") is not None and readMe.get("title") != "":
                title = title + f": {readMe.get('title')}"
            fileContents = fileContents.replace("$FULLTITLE", title)

            appDomains = readMe.get("appDomain")
            formattedAppDomains = ""
            if len(appDomains) > 1:
                for domain in appDomains:
                    formattedAppDomains += f"{domain},"
                formattedAppDomains = formattedAppDomains[
                    0 : len(formattedAppDomains) - 1
                ]
            else:
                formattedAppDomains = (
                    str(appDomains).replace('"', "").replace("[", "").replace("]", "")
                )

            fileContents = fileContents.replace("$APPDOMAINS", formattedAppDomains)
            fileContents = fileContents.replace("$README", readMe.get("description"))

            links = readMe.get("sources")
            for link in links:
                fileContents += f"[{link[0]}]({link[1]})<br>"

            os.makedirs(rf"{os.getcwd()}/docs/_posts/apps", exist_ok=True)

            today = datetime.today()
            date = today.strftime("%Y-%m-%d")

            with open(
                rf"{os.getcwd()}/docs/_posts/apps/{date}-{self.appName}.md", "w+"
            ) as o:
                o.write(fileContents)
                o.close()
            print(f"Generated app page: {self.appName}")

    def parseInfo(self, path):
        """Loads the info TOML file into a dictionary

        Parameters:
        path(string): Path to the info file to be parsed

        Returns:
        dict: Dictionary of the files contents

        """
        print(f"Parsing {path}")
        f = open(path, "rb")
        info = toml.load(f)
        return info
