# AMLFinalProject

After cloning the repository, it is necessary to setup the data repoistory in the correct place in order
for each script to run.

For [COW_CNN.ipynb](https://github.com/amunkharel/AMLFinalProject/blob/main/COW_CNN.ipynb):

If running in google drive / from google colab, ensure that the os.chdir() value is set to the same level as the data directory in your drive.
There is an example of what that would look like in the first cell of the notebook.

If running locally, do the same but remove the google drive mounting imports.

For [preprocess.py](https://github.com/amunkharel/AMLFinalProject/blob/main/preprocess.py) and [ImageAnalysis.py](https://github.com/amunkharel/AMLFinalProject/blob/main/ImageAnalysis.py):

If running locally, plz do the following steps:
- Change the 2nd line (where os.chdir is set) to point to the same directory the data directory is stored in.
- Change the line 30-32 and line 49-50 as comments shown in .py file.
- Then try "python preprocess.py" to run preprocess.py.
- Then try "python ImageAnalysis.py D1" to run ImageAnalysis.py.


Once this is done each python script / notebook will run as intended.
