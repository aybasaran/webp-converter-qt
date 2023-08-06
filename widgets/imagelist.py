from typing import List, Dict
from PyQt6 import QtGui
from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import (
    QListWidget,
    QWidget,
)

from PyQt6.QtGui import QDragEnterEvent


class ImageListWidget(QListWidget):
    def __init__(self, parent: QWidget):
        super().__init__(parent=parent)
        self.parent = parent
        self.addedImages: List[Dict] = []
        self.selectedImage: Dict = {}

        self.itemSelectionChanged.connect(self.selectImage)

        self.initUi()

    def initUi(self):
        self.setAcceptDrops(True)
        self.setDragEnabled(True)
        self.acceptDrops()
        self.setDropIndicatorShown(False)

    def selectImage(self):
        if self.selectedItems():
            self.selectedImage = self.addedImages[self.currentRow()]
        else:
            self.selectedImage = {}

    def handleRemoveSelected(self):
        if self.selectedImage:
            self.addedImages.remove(self.selectedImage)
            self.updateList()

    def updateList(self):
        self.clear()
        for img in self.addedImages:
            self.addItem(img["name"])

    def dragEnterEvent(self, event: QDragEnterEvent) -> None:
        for url in event.mimeData().urls():
            ext = url.fileName().split(".")[-1]
            if ext in ["png", "jpg", "jpeg"]:
                event.acceptProposedAction()

                if url.fileName() not in [img["name"] for img in self.addedImages]:
                    self.addedImages.append(
                        {"name": url.fileName(), "path": url.path()}
                    )
                    self.addItem(url.fileName())
