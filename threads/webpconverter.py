import logging
import os

from PIL import Image
from PyQt6.QtCore import QObject, pyqtSignal

logging.basicConfig(format="%(message)s", level=logging.INFO)


class WebpConverter(QObject):
    finished = pyqtSignal()

    def convert(self, imgDict, save_path):
        imgPath = imgDict["path"]
        imgName = imgDict["name"]
        try:
            if imgPath.startswith("/"):
                imgPath = imgPath[1:]

            if os.path.isfile(imgPath):
                openedImg = Image.open(imgPath).convert("RGB")
                openedImg.save(
                    os.path.join(save_path, imgName.split(".")[0] + ".webp"),
                    "webp",
                )

            self.finished.emit()

        except Exception as e:
            logging.error(e)
