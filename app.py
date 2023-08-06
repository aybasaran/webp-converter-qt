import logging

from PyQt6.QtCore import QDir, QThread
from PyQt6.QtWidgets import (
    QApplication,
    QFileDialog,
    QHBoxLayout,
    QLabel,
    QMainWindow,
    QMessageBox,
    QPushButton,
    QVBoxLayout,
    QWidget,
)

from threads.webpconverter import WebpConverter
from widgets.imagelist import ImageListWidget

logging.basicConfig(format="%(message)s", level=logging.INFO)


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi()
        self.threads = []
        self.doneJobs = 0
        self.savingDir = ""

    def setupUi(self):
        self.setWindowTitle("Webp Converter")
        self.resize(400, 300)
        self.centralWidget = QWidget()
        self.setCentralWidget(self.centralWidget)

        self.saveDirLabel = QLabel("Save Dir: ")

        convertBtn = QPushButton("Conver to Webp 📸")
        convertBtn.clicked.connect(self.startThreads)
        selectSaveDirBtn = QPushButton("Select Save Directory 📂")
        selectSaveDirBtn.clicked.connect(self.selectSaveDir)

        delSelectedImgBtn = QPushButton("❌")
        delSelectedImgBtn.clicked.connect(self.removeAddedImage)

        self.imageList = ImageListWidget(self)

        mainLayout = QVBoxLayout()
        mainLayout.addWidget(self.saveDirLabel)

        listAndActionsLayout = QHBoxLayout()

        actionsSidebarLayout = QVBoxLayout()
        listAndActionsLayout.addLayout(actionsSidebarLayout)
        listAndActionsLayout.addWidget(self.imageList)
        actionsSidebarLayout.addWidget(delSelectedImgBtn)

        bottomActionsLayout = QHBoxLayout()
        bottomActionsLayout.addWidget(convertBtn)
        bottomActionsLayout.addWidget(selectSaveDirBtn)
        mainLayout.addLayout(listAndActionsLayout)
        mainLayout.addLayout(bottomActionsLayout)

        self.centralWidget.setLayout(mainLayout)

    def removeAddedImage(self):
        self.imageList.handleRemoveSelected()

    def createThread(self, img):
        thread = QThread()
        worker = WebpConverter()
        worker.moveToThread(thread)
        thread.started.connect(lambda: worker.convert(img, self.savingDir))
        worker.finished.connect(self.threadMadeHisJob)
        worker.finished.connect(thread.quit)
        worker.finished.connect(worker.deleteLater)
        thread.finished.connect(thread.deleteLater)
        return thread

    def startThreads(self):
        if self.imageList.addedImages and self.savingDir != "":
            self.threads.clear()
            self.threads = [
                self.createThread(img) for img in self.imageList.addedImages
            ]
            for thread in self.threads:
                thread.start()

    def selectSaveDir(self):
        dlg = QFileDialog()
        dlg.setFileMode(QFileDialog.FileMode.Directory)
        dlg.setFilter(QDir.Filter.AllDirs)
        dlg.setOption(QFileDialog.Option.ShowDirsOnly, True)

        if dlg.exec():
            selected = dlg.selectedFiles()
            self.saveDirLabel.setText("Save Dir: " + selected[0])
            self.savingDir = selected[0]

    def showMessage(self, msg: str):
        msgBox = QMessageBox(self)
        msgBox.setIcon(QMessageBox.Icon.Information)
        msgBox.setText(msg)
        msgBox.setWindowTitle("Info")
        msgBox.setStandardButtons(QMessageBox.StandardButton.Ok)
        returnValue = msgBox.exec()
        if returnValue == QMessageBox.StandardButton.Ok:
            self.imageList.clear()
            self.imageList.addedImages = []
            self.imageList.selectedImage = {}
            self.doneJobs = 0

    def threadMadeHisJob(self):
        self.doneJobs += 1
        if self.doneJobs == len(self.imageList.addedImages):
            self.showMessage("All images converted to webp")


if __name__ == "__main__":
    app = QApplication([])
    window = MainWindow()
    window.show()
    app.exec()
