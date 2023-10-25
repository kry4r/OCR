from paddleocr import PaddleOCR, draw_ocr
import matplotlib.pyplot as plt
from ocrui import Ui_MainWindow
import sys
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication, QMainWindow, QFileDialog, QGraphicsScene, QGraphicsPixmapItem
from PyQt5.QtGui import QImage, QPixmap, QIcon
from PIL import Image
import time



class MainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.setWindowIcon(QIcon("icon.png"))
        self.setWindowTitle("街景识别 2020215446,2020213394,2020213398")
        self.img_b.clicked.connect(self.open_image)
        self.rec_b.clicked.connect(self.open_rec)
        self.det_b.clicked.connect(self.open_det)
        self.clr_b.clicked.connect(self.open_cls)
        self.PrimaryPushButton.clicked.connect(self.start)
        self.PrimaryPushButton_2.clicked.connect(self.saveas)

    
    def open_rec(self):
        self.rec_v = QFileDialog().getExistingDirectory()
        self.rec.setText(self.rec_v)

    def open_det(self):
        self.det_v = QFileDialog().getExistingDirectory()
        self.det.setText(self.det_v)

    def open_cls(self):
        self.cls_v = QFileDialog().getExistingDirectory()
        self.clr.setText(self.cls_v)

    def open_image(self):
        image = QFileDialog().getOpenFileName()
        self.image.setText(image[0])
        self.img_path = image[0]
    
    def start(self):
        self.pocr = PaddleOCR(use_angle_cls=True, lang="ch", det_model_dir=self.det_v, rec_model_dir=self.rec_v,
                              cls_model_dir=self.cls_v)
        result = self.pocr.ocr(self.img_path, cls=True)
        result = result[0]
        image = Image.open(self.img_path).convert('RGB')
        boxes = [line[0] for line in result]
        txts = [line[1][0] for line in result]
        scores = [line[1][1] for line in result]
        im_show = draw_ocr(image, boxes, txts, scores, font_path='doc/fonts/simfang.ttf')
        im_show = Image.fromarray(im_show)
        im_show.save('result.jpg')
        
        self.pixmap = QPixmap('result.jpg')
        self.label.setPixmap(self.pixmap)
        self.label.setScaledContents(True)
        
    def saveas(self):
        file_path, _=QFileDialog.getSaveFileName(self,"result",'',"Image(*.jpg *.gif *.png)")
        if not file_path: return

        pixmap = self.pixmap
        pixmap.save(file_path)


if __name__ == '__main__':
    QApplication.setHighDpiScaleFactorRoundingPolicy(Qt.HighDpiScaleFactorRoundingPolicy.PassThrough)
    QApplication.setAttribute(Qt.AA_EnableHighDpiScaling)
    QApplication.setAttribute(Qt.AA_UseHighDpiPixmaps)
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())