#!env python
import sys
import PyQt4.QtCore as QtCore
import PyQt4.QtGui as QtGui


class SliderWindow(QtGui.QWidget):
    count = 0
    def __init__(self, parent=None):
        QtGui.QWidget.__init__(self, parent=parent)
                              
        self.sliders = QtGui.QWidget(parent=self)
        self.locater = QtGui.QWidget(parent=self)
        self.TextEdit = QtGui.QTextEdit(parent=self)

        self.init_sliders()

        self.locater.setFixedSize(300,300)
        self.locater.setGeometry(0, 0, 280, 270)


        layout1 = QtGui.QHBoxLayout()
        layout1.addWidget(self.locater)
        layout1.addWidget(self.sliders)

        layout = QtGui.QVBoxLayout()
        layout.addLayout(layout1)
        layout.addWidget(self.TextEdit)

        self.setLayout(layout) 


    def init_sliders(self):
        self.setSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Expanding)

        self.Param = {'count':0, 'rad1': 0, 'rad2':50, 'dia':50, 'space':0}
        self.timerId = self.startTimer(5)

        slider_layout = QtGui.QVBoxLayout()

        slider_rad1 = QtGui.QSlider(QtCore.Qt.Horizontal, self)
        #slider_rad1.setFocusPolicy(QtCore.Qt.NoFocus)
        slider_rad1.valueChanged.connect(self.changeValue_rad1)

        slider_rad2 = QtGui.QSlider(QtCore.Qt.Horizontal, self)
        slider_rad2.valueChanged.connect(self.changeValue_rad2)
        
        slider_diam = QtGui.QSlider(QtCore.Qt.Horizontal, self)
        slider_diam.valueChanged.connect(self.changeValue_diam)
        
        slider_space = QtGui.QSlider(QtCore.Qt.Horizontal, self)
        slider_space.valueChanged.connect(self.changeValue_space)

        self.label_rad1 = QtGui.QLabel(self)
        self.label_rad1.setText('rad1: '+'0') 
        self.label_rad2 = QtGui.QLabel(self)
        self.label_rad2.setText('rad2: '+'0') 
        self.label_diam = QtGui.QLabel(self)
        self.label_diam.setText('diam: '+'0')
        self.label_space = QtGui.QLabel(self)
        self.label_space.setText('space: '+'0')
        hbox1 = QtGui.QHBoxLayout()
        hbox1.addWidget(self.label_rad1)
        hbox1.addWidget(slider_rad1)
        hbox2 = QtGui.QHBoxLayout()
        hbox2.addWidget(self.label_rad2)
        hbox2.addWidget(slider_rad2)
        hbox3 = QtGui.QHBoxLayout()
        hbox3.addWidget(self.label_diam)
        hbox3.addWidget(slider_diam)
        hbox4 = QtGui.QHBoxLayout()
        hbox4.addWidget(self.label_space)
        hbox4.addWidget(slider_space)
        slider_layout.addLayout(hbox1)
        slider_layout.addLayout(hbox2)
        slider_layout.addLayout(hbox3)
        slider_layout.addLayout(hbox4)

        self.sliders.setLayout(slider_layout)

        self.repaint()


    def changeValue_rad1(self, value):
        self.label_rad1.setText('rad1: '+str(value))
        self.Param['rad1'] = value
        self.generateRMCode()
        self.repaint()

    def changeValue_rad2(self, value):
        self.label_rad2.setText('rad2: '+str(value))
        self.Param['rad2'] = value
        self.generateRMCode()
        self.repaint()

    def changeValue_diam(self, value):
        self.label_diam.setText('diam: '+str(value))
        self.Param['dia'] = value
        self.generateRMCode()
        self.repaint()

    def changeValue_space(self, value):
        self.label_space.setText('space: '+str(value))
        self.Param['space'] = value
        self.generateRMCode()
        self.repaint()
        
    def generateRMCode(self):
        self.TextEdit.setText(self.gen_TeamSpacingModifier() + self.gen_PlaceCircular() + self.gen_PlacementSection())

    def gen_TeamSpacingModifier(self):
        f_to = 1
        f_from = 0
        prm = round(self.Param['space']/100.0 * (f_to - f_from) + f_from, 2)
        return '   rmSetTeamSpacingModifier('+str(prm)+');\n'

    def gen_PlacementSection(self):
        f_to = 1.0
        f_from = 0.0
        cprm1 = round(self.Param['rad1']/100.0 * (f_to - f_from) + f_from, 2)
        cprm2 = round(self.Param['rad2']/100.0 * (f_to - f_from) + f_from, 2)
        prm_2_1 = cprm1
        prm_2_2 = cprm2
        prm_4_1 = cprm1 - 0.025
        prm_4_2 = cprm2 + 0.025
        prm_6_1 = cprm1 - 0.05
        prm_6_2 = cprm2 + 0.05
        
        return '''    if ( cNumberNonGaiaPlayers < 3){
        rmSetPlacementSection('''+str(prm_2_1)+ ', '+str(prm_2_2)+''');
    }else if (cNumberNonGaiaPlayers < 5){
        rmSetPlacementSection('''+str(prm_4_1)+ ', '+str(prm_4_2)+''');
    }else{
        rmSetPlacementSection('''+str(prm_6_1)+ ', '+str(prm_6_2)+''');
    }\n'''

    def gen_PlaceCircular(self):
        f_to = 0.5
        f_from = 0.1
        prm = round(self.Param['dia']/100.0 * (f_to - f_from) + f_from, 2)
        return '    rmPlacePlayersCircular('+str(prm)+', '+str(prm)+', 0);\n'


    def paintEvent(self, event):
        painter = QtGui.QPainter()
        painter.begin(self)
        self.locater.paintEvent(event)
        self.draw_locater(event, painter)
        painter.end()

    def draw_locater(self, event, painter):
        h = self.locater.height()
        w = self.locater.width()
        csize = 230 * ( self.Param['dia'] / 200.0  + 0.5 )
        psize = 20

        # draw initialising
        brush = QtGui.QBrush(QtGui.QColor(0,120,0)) #green
        painter.translate(QtCore.QPoint(h/2, h/2))
        painter.setPen(QtGui.QPen(brush , 1))
        painter.setRenderHint(QtGui.QPainter.Antialiasing)
        painter.save()
        painter.drawEllipse(-csize/2, -csize/2, csize, csize)

        # Blue Team 1
        brush = QtGui.QBrush(QtGui.QColor(0,0,self.grow(120,255)))
        painter.setPen(QtGui.QPen(brush , 1))
        painter.setRenderHint(QtGui.QPainter.Antialiasing)
        painter.rotate(-45.0)
        painter.rotate(self.Param['rad1'] * 360 / 100.0)
        rot1 = 40 * self.Param['space'] /100.0
        for i in range(3):
            painter.drawEllipse((-csize-psize)/2, (-psize)/2, psize, psize)
            painter.rotate(rot1)

        # Red Team 2
        painter.restore()
        painter.save()
        brush = QtGui.QBrush(QtGui.QColor(self.grow(120,255),0,0))
        painter.setPen(QtGui.QPen(brush , 1))
        painter.setRenderHint(QtGui.QPainter.Antialiasing)
        painter.rotate(135.0)
        painter.rotate(self.Param['rad2'] * 360 / 100.0)
        rot2 = 40 * self.Param['space'] /100.0
        for i in range(3):
            painter.drawEllipse((-csize-psize)/2, (-psize)/2, psize, psize)
            painter.rotate(rot2)

        # picture background
        painter.restore()
        brush = QtGui.QBrush(QtGui.QColor(200,200,200))
        painter.setPen(QtGui.QPen(brush , 0.5))
        painter.setRenderHint(QtGui.QPainter.Antialiasing)
        painter.rotate(self.Param['rad1'] * 7 % 360)
        rot = 0
        while rot < 360.0:
            painter.drawEllipse(-125, -40, 150, 80) 
            painter.rotate(5.0)
            rot += 5.0


    # TODO: draw grow() with lambda
    def grow(self, minv, maxv):
        dev = self.count % (2 * (maxv-minv))
        if dev > (maxv - minv):
            return 2 * (maxv - minv) - dev + minv
        else:
            return dev + minv

    def timerEvent(self, event):
        self.count = self.count + 1
        self.repaint()


def main():
    app = QtGui.QApplication(sys.argv)
    
    panel = QtGui.QWidget()

    slider_widget = SliderWindow(parent=panel) 

    panel_layout = QtGui.QVBoxLayout()
    panel_layout.addWidget(slider_widget)
    panel.setLayout(panel_layout)
    panel.setFixedSize(600, 600)

    main_window = QtGui.QMainWindow()
    main_window.setWindowTitle("AoE3 Random Map Tool")
    main_window.setCentralWidget(panel)

    main_window.show()

    sys.exit(app.exec_())

if __name__ == "__main__":
    main()