# P3 Explorer Documentation
All instructions assume you are using a windows machine

## Dependencies
contourpy==1.2.1
cssselect==1.2.0
cycler==0.12.1
fonttools==4.53.0
kiwisolver==1.4.5
lxml==5.2.2
matplotlib==3.9.1
numpy==2.0.0
packaging==24.1
pandas==2.2.2
pillow==10.4.0
pyparsing==3.1.2
python-dateutil==2.9.0.post0
pytz==2024.1
six==1.16.0
tzdata==2024.1
Jinja2==3.1.4

Place into file called requirements.txt
run python -m pip install -r requirements.txt

P3 can't be installed using pip, clone the [repo](https://github.com/intel/p3-analysis-library)
then cd into the cloned repo and run python -m pip install .

## General Directory structure 
| Folder  | Purpose |
| ------------- | ------------- |
| /  | Contains miscellaneous files as well as the script which handles the building of the site |
| /.github | GitHub Actions workflows are stored in here  |
| /docs  | The folder the jekyll site is built from  |
| /scripts  | Where all the files with the logic to generate the plots and pages is stored  |
| /submissions  | Data repository where all the submitted data is stored  |

## Overview of functionality
Upon a push to the main branch the scripts.yml GitHub actions workflow runs. This action switches to and updates the github-pages branch with the contents of main (e.g. new submissions), submissionHandler.py is then ran to create all the plots & pages for all submitted data this is then pushed to the github-pages branch.
Upon the push to the github-pages the workflow site-branch-build-deploy.yml runs to build the contents of the docs folder and then deploys it to pages.
The updates site is then live at the url: [https://p3-explorer.github.io/](https://p3-explorer.github.io/)
Comments and doc-Strings are provided within the code and workflows to provide more specific explanations of each stage of the process described above.


