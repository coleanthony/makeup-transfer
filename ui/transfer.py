
import sys
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
import qtawesome
import os
from utils.makeuptransfer import *
from utils.Dynamic_Processing_Graph import *

class MakeupTransfer(QWidget):
    def __init__(self, parent=None):
        super(MakeupTransfer, self).__init__(parent)
        self.resize(1200,400)
        layout = QGridLayout()

        self.beautygan=BeautyGAN()
        self.nonemkup=None
        self.mkup=None
        self.img=None

        self.take = DP_Graph()

        self.btn = QPushButton()
        self.btn.clicked.connect(self.loadFile)
        self.btn.setText("上传原图")
        layout.addWidget(self.btn,1,0)

        self.btn6 = QPushButton()
        self.btn6.clicked.connect(self.take.takephoto)
        self.btn6.setText("在线拍照")
        layout.addWidget(self.btn6, 2, 0)

        self.btn2 = QPushButton()
        self.btn2.clicked.connect(self.loadmakeupfile)
        self.btn2.setText("上传彩妆照片")
        layout.addWidget(self.btn2,1,1)

        self.btn4 = QPushButton()
        self.btn4.clicked.connect(self.process)
        self.btn4.setText("合成")
        layout.addWidget(self.btn4,1,2)

        self.btn3 = QPushButton()
        self.btn3.clicked.connect(self.close)
        self.btn3.setText("返回")
        layout.addWidget(self.btn3, 2, 1)

        self.btn5 = QPushButton()
        self.btn5.clicked.connect(self.downloadfile)
        self.btn5.setText("下载迁移完成图像")
        layout.addWidget(self.btn5, 2, 2)

        self.label = QLabel()
        layout.addWidget(self.label,0,0)
        self.label2 = QLabel()
        layout.addWidget(self.label2, 0, 1)
        self.label3 = QLabel()
        layout.addWidget(self.label3, 0, 2)

        self.setWindowTitle("彩妆迁移")
        self.setLayout(layout)
        self.beautify()

    def beautify(self):
        self.setWindowOpacity(0.95)

        palette = QPalette()
        path = os.path.join('tools', 'win.jpg')
        palette.setBrush(QPalette.Background, QBrush(QPixmap(path)))
        self.setPalette(palette)

        iconpath = os.path.join('tools', 'amg.jpg')
        self.setWindowIcon(QIcon(iconpath))
        spin_icon = qtawesome.icon('fa.book', color='black')
        spin_icon2 = qtawesome.icon('fa.comment', color='black')
        spin_icon3 = qtawesome.icon('fa5s.ban', color='black')
        spin_icon4 = qtawesome.icon('fa.star', color='black')
        spin_icon5 = qtawesome.icon('fa.download', color='black')
        spin_icon6 = qtawesome.icon('fa.photo', color='black')

        self.btn.setIcon(spin_icon)
        self.btn2.setIcon(spin_icon2)
        self.btn3.setIcon(spin_icon3)
        self.btn4.setIcon(spin_icon4)
        self.btn5.setIcon(spin_icon5)
        self.btn6.setIcon(spin_icon6)

        self.btn.setStyleSheet('''QPushButton{border:none;}
                       QPushButton:hover{color:white;
                                   border:2px solid #F3F3F5;
                                   border-radius:35px;
                                   background:darkGray;}''')

        self.btn2.setStyleSheet('''QPushButton{border:none;}
                               QPushButton:hover{color:white;
                                           border:2px solid #F3F3F5;
                                           border-radius:35px;
                                           background:darkGray;}''')

        self.btn3.setStyleSheet('''QPushButton{border:none;}
                               QPushButton:hover{color:white;
                                           border:2px solid #F3F3F5;
                                           border-radius:35px;
                                           background:darkGray;}''')

        self.btn4.setStyleSheet('''QPushButton{border:none;}
                                       QPushButton:hover{color:white;
                                                   border:2px solid #F3F3F5;
                                                   border-radius:35px;
                                                   background:darkGray;}''')

        self.btn5.setStyleSheet('''QPushButton{border:none;}
                                               QPushButton:hover{color:white;
                                                           border:2px solid #F3F3F5;
                                                           border-radius:35px;
                                                           background:darkGray;}''')

        self.btn6.setStyleSheet('''QPushButton{border:none;}
                                                       QPushButton:hover{color:white;
                                                                   border:2px solid #F3F3F5;
                                                                   border-radius:35px;
                                                                   background:darkGray;}''')

    def loadFile(self):
        self.nonemkup, _ = QFileDialog.getOpenFileName(self, '选择图片', 'c:\\', 'Image files(*.jpg *.gif *.png)')
        self.label.setPixmap(QPixmap(self.nonemkup))

    def loadmakeupfile(self):
        self.mkup, _2 = QFileDialog.getOpenFileName(self, '选择图片', 'c:\\', 'Image files(*.jpg *.gif *.png)')
        self.label2.setPixmap(QPixmap(self.mkup))

    def process(self):
        if self.nonemkup!=None or self.mkup!=None:
            self.beautygan.process(self.nonemkup,self.mkup)
            with open('Res/result.jpg', 'rb') as f:
                self.img = f.read()
            self.imagex = QImage.fromData(self.img)
            pixmap = QPixmap.fromImage(self.imagex)
            self.label3.setPixmap(QPixmap(pixmap))
        else:
            QMessageBox.about(QWidget(), '提示', '未上传原图或化妆图')

    def downloadfile(self):
        '''
         downloadfile
        :return:None
        '''
        if self.img==None:
            QMessageBox.about(QWidget(), '提示', '无合成图像')
        else:
            savename, type = QFileDialog.getSaveFileName(self, '保存图片', 'c:\\', 'Image files(*.jpg *.gif *.png)')
            if savename=='':
                QMessageBox.about(QWidget(), '提示', '取消保存')
            else:
                with open(savename, 'wb') as f:
                    f.write(self.img)
                    QMessageBox.about(QWidget(), '提示', '保存成功')

