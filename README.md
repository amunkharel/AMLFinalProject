# AMLFinalProject

After cloning the repository, it is necessary to setup the data repoistory in the correct place in order
for each script to run.

For COW_CNN.ipynb:

If running in google drive / from google colab, ensure that the os.chdir() value is set to the same level as the data directory in your drive.
There is an example of what that would look like in the first cell of the notebook.

If running locally, do the same but remove the google drive mounting imports.

For ImageAnalysis.py:

Change the 2nd line (where os.chdir is set) to point to the same directory the data directory is stored in.

Once this is done each python script / notebook will run as intended.
