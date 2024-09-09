---
layout: default
title: About
nav_enabled: True
nav_order: 3
---
# About

Data is submitted through pull requests to the GitHub repo, steps for how to submit are as follows:
1. Navigate to the submissions folder.
2. If the app you are submitting data for is present skip to step 6.
3. Create folder with your app as the name.
4. Create a readme.toml within the folder, this should contain a short description of the application as well as the app domain (schema can be found below).
5. Within your folder create another folder named data.
6. Place all files for your submission in the data folder within your chosen apps folder.
7. Required files are a CSV containing performance data and a TOML  file containing information about the submission, coverage data in a CSV is required for the Navchart plot however all other plots will work without it.
- These files should be named as per the convention outlined at the bottom of this page. 
- The schema for the TOML file can also be found below.
- A visual representation of the directory structure for submissions can also be found below. 
- The structure of the CSV files can be found below.
8. Once you are ready, submit a pull request to the repository you will automatically be told whether your submission can be accepted or not.
9. All submissions will be subject to review to ensure they are of appropiate standard, we aim to complete this in a reasonable amount of time so please be patient!

## TOML Format
### Data
<img src="static/tomlTemplate.png" alt="Image of Template">
<a href="static/2024-07-example.toml" download>Download Example</a>
<a href="static/template.toml" download> Download Schema</a>

### App
<a href="static/readMe.toml" download>Download Example</a>
(Note the name of the app is taken from the app's folder name)
### Format of Submission Files
<img src="static/submissionFormat.png" alt="Image of Submission Format">

### Directory Structure
<img src="static/directoryStructure.png" alt="Image of Submission Format">

## Data CSV Format
### Performance 
Columns: fom, problem, application, platform, coverage_key* <br>
*Only required if coverage data provided
### Coverage
Columns: coverage_key, coverage
Coverage data can be sourced from the schema
