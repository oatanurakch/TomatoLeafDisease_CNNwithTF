import sys
import os
import cv2

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from UI.ui_program import *
from datetime import datetime
from pathlib import Path

FILE = Path(__file__).resolve()
ROOT = FILE.parents[0]

# Load module predict image
from predictProcess import Predict
# Create object for used predict in program
predict = Predict(path = os.path.join(ROOT, 'Model', 'TomatoLeafDiseaseModel.h5'))

app = QtWidgets.QApplication(sys.argv)
MainWindow = QtWidgets.QMainWindow()

class ui_sub(Ui_MainWindow):
    def __init__(self):
        super().setupUi(MainWindow)
        # Set windows name
        MainWindow.setWindowTitle('Tomato leaf disease detection')
        # Set windows title
        try:
            MainWindow.setWindowIcon(QtGui.QIcon(os.path.join(ROOT, r'UI/elec.png')))
        except:
            pass
        # Set sized of windows
        MainWindow.setFixedHeight(650)
        MainWindow.setFixedWidth(1200)
        # Setup button in GUI
        self.SetUpButtonOnGUI()
        # Assign initial variable
        self.ImgPredict = None
           
    # Setup button
    def SetUpButtonOnGUI(self):
        self.LoadImageOnce.clicked.connect(self.SelectedImageForPrediction)

    # Selected image for predection with .h5
    def SelectedImageForPrediction(self):
        # Load image process
        try:
            height_srcImage = self.SourceImage.height()
            width_srcImage = self.SourceImage.width()
            # Load image for detection
            file, check = QFileDialog.getOpenFileName(None, 'Select image', '', 'Image files (*.jpg)')
            # if selected file, then show image in GUI
            if check:
                # Load image from path selected
                Img = cv2.imread(str(file))
                # convert color to RGB
                Img = cv2.cvtColor(Img, cv2.COLOR_BGR2RGB)
                # load shape of image
                h, w, ch = Img.shape
                # check size of image, if image size is bigger than srcimage labels size, then resize image
                if h > height_srcImage or w > width_srcImage:
                    Img = cv2.resize(Img, (width_srcImage, height_srcImage))
                    # check new shape of image
                    h, w, ch = Img.shape
                elif h < height_srcImage and w < width_srcImage:
                    Img = cv2.resize(Img, (int(w * 170 / 100), int(h * 170 / 100)))
                    h, w, ch = Img.shape
                qImg = QImage(Img.data, w, h, ch * w, QImage.Format_RGB888)
                # Set pixmap for show on GUI
                self.SourceImage.setPixmap(QPixmap.fromImage(qImg))
                # Predict process
                self.PredictProcess(imgPath = file)
        except:
            self.AleartBoxError(description = 'Can\'t load image !')
        
    # Predict process
    def PredictProcess(self, imgPath):
        # Call module for predict image
        predict_ret = predict.predict_process(path_img = imgPath)
        # Show result predict on GUI
        self.LoadResult(img = imgPath, predict_class = predict_ret)
    
    # Load result and put text in image
    def LoadResult(self, img, predict_class):
        height_srcImage = self.DisImage.height()
        width_srcImage = self.DisImage.width()
        # load image that selected
        Img = cv2.imread(img)
        # Load image that RGB mode
        Img = cv2.cvtColor(Img, cv2.COLOR_BGR2RGB)
        # load shape of image
        h, w, ch = Img.shape
        # check size of image, if image size is bigger than srcimage labels size, then resize image
        if h > height_srcImage or w > width_srcImage:
            Img = cv2.resize(Img, (width_srcImage, height_srcImage))
            # check new shape of image
            h, w, ch = Img.shape
        elif h < height_srcImage and w < width_srcImage:
            Img = cv2.resize(Img, (int(w * 170 / 100), int(h * 170 / 100)))
            h, w, ch = Img.shape
        # Add label to image
        self.ImgPredict = self.LabelShow(img = Img, label = predict_class)
        qImg = QImage(self.ImgPredict.data, w, h, ch * w, QImage.Format_RGB888)
        # Set pixmap for show on GUI
        self.DisImage.setPixmap(QPixmap.fromImage(qImg))
        
    # Label for show image
    def LabelShow(self, img, label):
        try:
            # check size of text
            p1, p2 = 5, 30
            # size of text string label
            w, h = cv2.getTextSize(label, 0, fontScale = 0.7, thickness = 1)
            # topleft border
            tl = (p1, p2 - w[1])
            # bottomright border
            btr = (p1 + w[0], p2 + 5)
            # Draw rectangle
            cv2.rectangle(img, tl, btr, (255, 255, 255), -1, cv2.LINE_AA) 
            # Add label class predict in Image
            cv2.putText(img, str(label), (p1, p2), 0, 0.7, (0, 0, 0), 1)
            # return image
            return img
        except:
            self.AleartBoxError(description = 'Can\'t draw box and text !')
            
    # ----- Aleart message -----
    def AleartBoxError(self, description):
        msg = QMessageBox()
        msg.setWindowTitle('Error')
        msg.setText(description)
        msg.setIcon(QMessageBox.Warning)
        msg.setStandardButtons(QMessageBox.Ok)
        msg.exec_()
            
            
if __name__ == '__main__':
    obj = ui_sub()
    MainWindow.show()
    sys.exit(app.exec_())
