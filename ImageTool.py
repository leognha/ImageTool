from cgi import print_form
import sys
import os
import fnmatch
import cv2
from ImageTool_ui import Ui_Dialog 
from PyQt6 import QtCore, QtGui, QtWidgets

class MainWindow(QtWidgets.QDialog, Ui_Dialog):
    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent=parent)
        self.setupUi(self)
        self._translate = QtCore.QCoreApplication.translate
        
        self.onlyInt = QtGui.QIntValidator()
        self.lineEdit.setValidator(self.onlyInt)
        self.lineEdit_2.setValidator(self.onlyInt)
        self.lineEdit_3.setValidator(self.onlyInt)
        
        self.lineEdit.setText("256")
        self.lineEdit_2.setText("256")
        self.lineEdit_3.setText("50")

        self.pushButton.clicked.connect(self.dir_msg)
        self.pushButton_2.clicked.connect(self.files_msg)
        
        self.buttonGroup=QtWidgets.QButtonGroup(self)
        self.buttonGroup.addButton(self.radioButton, 0)
        self.buttonGroup.addButton(self.radioButton_3, 1)
        
        self.buttonBox.accepted.connect(self.checkType)
        
        self.dir_file = ''
        self.dir_files = []
        self.included_extensions = ['jpg','jpeg', 'png']

    def dir_msg(self,Filepath):
        m = QtWidgets.QFileDialog.getExistingDirectory(None,"選取資料夾","./") # 起始路徑
        self.setWindowTitle(self._translate("Dialog", "圖片小工具 " + m))
        self.dir_files = None
        self.dir_folder = m
    
    def files_msg(self,Filepath):
        directory = QtWidgets.QFileDialog.getOpenFileNames(None, "選取多個檔案", "./","Image Files(*.png *.jpg *.jepg)") 
        self.setWindowTitle(self._translate("Dialog", "圖片小工具 已選取" + str(len(directory[0]))))
        print(directory[0])
        self.dir_files = directory[0]
        self.dir_folder = None
    
    def checkType(self):
        if self.checkChooseFiles() == False:
            self.msgBox("沒選檔案阿!!!")
            return
        if self.checkNoEmptyLineEdit() == False:
            self.msgBox("數字不能空且要大於0阿!!!")
            return
        
        self.folderpath = os.path.join('./', 'resize_output')
        try:
            os.makedirs(self.folderpath)
        # 檔案已存在的例外處理
        except FileExistsError:
            print("檔案已存在。")
            
        if self.buttonGroup.checkedId() == 0:
            self.resizeImageByFix()
        else:
            self.resizeImageByRate()
             
    def resizeImageByRate(self):
        rate = int(self.lineEdit_3.text())/100
        
        if self.dir_files:
            for url in self.dir_files:
                img = cv2.imread(url)
                file_name = url.split('/')[-1]
                height, width = img.shape[:2]
                print(height, width,img.shape)
                img_resize = cv2.resize(img, (int(width * rate), int(height * rate)), interpolation = cv2.INTER_AREA)
                cv2.imwrite(os.path.join(self.folderpath, file_name), img_resize)
                print(os.path.join(self.folderpath, file_name))
        else:
            file_names = [fn for fn in os.listdir(self.dir_folder) if any(fn.endswith(ext) for ext in self.included_extensions)]
            
            for file_name in file_names:
                img = cv2.imread(os.path.join(self.dir_folder, file_name))
                height, width = img.shape[:2]
                print(height, width,img.shape)
                img_resize = cv2.resize(img, (int(width * rate), int(height * rate)), interpolation = cv2.INTER_AREA)
                cv2.imwrite(os.path.join(self.folderpath, file_name), img_resize)
                print(os.path.join(self.folderpath, file_name))

    def resizeImageByFix(self):
        width = self.lineEdit.text()
        height = self.lineEdit_2.text()
        
        if self.dir_files:
            for url in self.dir_files:
                img = cv2.imread(url)
                file_name = url.split('/')[-1]
                img_resize = cv2.resize(img, (int(width), int(height)), interpolation = cv2.INTER_AREA)
                cv2.imwrite(os.path.join(self.folderpath, file_name), img_resize)
                print(os.path.join(self.folderpath, file_name))
        else:
            file_names = [fn for fn in os.listdir(self.dir_folder) if any(fn.endswith(ext) for ext in self.included_extensions)]
            
            for file_name in file_names:
                img = cv2.imread(os.path.join(self.dir_folder, file_name))
                img_resize = cv2.resize(img, (int(width), int(height)), interpolation = cv2.INTER_AREA)
                cv2.imwrite(os.path.join(self.folderpath, file_name), img_resize)
                print(os.path.join(self.folderpath, file_name))
    
    def checkNoEmptyLineEdit(self):
        result = True
        if self.buttonGroup.checkedId() == 0:
            if self.lineEdit_3.text() =='' or int(self.lineEdit_3.text()) <= 0:
                result = False
        else:
            if self.lineEdit_2.text() =='' or int(self.lineEdit_2.text()) <= 0:
                result = False
            if self.lineEdit.text() =='' or int(self.lineEdit.text()) <= 0:
                result = False
        return result
    
    def checkChooseFiles(self):
        if self.dir_file == '' and self.dir_files == []:
            return False
        else:
            return True
    def msgBox(self, msg):         
        reply = QtWidgets.QMessageBox()
        reply.setWindowTitle("出事啦!!!")
        reply.setIcon(QtWidgets.QMessageBox.Icon.Critical)
        reply.setText(msg)
        reply.setStandardButtons(QtWidgets.QMessageBox.StandardButton.Ok)
    
        reply.exec()

if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    mainWindow = MainWindow()
    mainWindow.show()
    sys.exit(app.exec())