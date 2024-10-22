# MediaSimple
Batch resize images and videos, with all code contained in a single file. Supported file formats include: png, jpeg, gif, webp, mp4

#### Introduction
MediaSimple is based on the cross-platform GUI library [Kivy](http://https://kivy.org/) for Python


#### Install
##### PreInstall
1.  install Python 3.x and the pip tool
2.  install setuptools and virtualenv

    `python -m pip install --upgrade pip setuptools virtualenv`
##### Create virtual environment
1.  Create a virtual environment named kivy_venv in the current directory.
    `python -m venv kivy_venv`
2.  Every time you open a new terminal or command prompt, you will need to activate the virtual environment to use it
    Windows cmd  `kivy_venv\Scripts\activate`
    Windows bash `source kivy_venv/Scripts/activate`   
    Linux or macOS  `source kivy_venv/bin/activate`
    After the environment is activated, the name of the virtual environment name (kivy_venv) will be displayed at the beginning of the path in the command line.
##### Install python lib 
    `pip install moviepy pillow piexif imghdr`

#### Run
1.  Run
    `python main.py`
2.  Drag the files that need to be compressed into the program window.
3.  After the files are compressed, a new file with '_opt' appended to the original filename will be generated in the same folder.
