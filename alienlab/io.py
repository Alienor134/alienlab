
import os
import sys
cwd = os.getcwd()

def create_folder_if(directory):
    if not os.path.exists(directory):
        os.makedirs(directory)

def catch_file(direc = cwd ):
    """Opens a dialog window to select a file. Default directory: current directory
    direc [str]: directory to open (default: current directory)
    """
    
    from PyQt5 import QtWidgets, QtGui
    app = QtWidgets.QApplication(sys.argv)
    fname = QtWidgets.QFileDialog.getOpenFileName(None, directory=direc, caption = "Select a video file...",
                                                  filter="All files (*)")
    return fname[0]
