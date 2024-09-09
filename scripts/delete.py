# Dev Script to run to avoid committing local generated plots/pages to the repo (to keep main clean)
import os
import shutil

os.chdir("..")
if os.path.isdir(f"{os.getcwd()}/docs/_posts"):
    shutil.rmtree(f"{os.getcwd()}/docs/_posts")

if os.path.isdir(f"{os.getcwd()}/docs/static/assets"):
    shutil.rmtree(f"{os.getcwd()}/docs/static/assets")

if os.path.isdir(f"{os.getcwd()}/docs/static/plots"):
    shutil.rmtree(f"{os.getcwd()}/docs/static/plots")
