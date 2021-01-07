from gui_radon import *
import sys
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import numpy as np

import matplotlib.pyplot as plt

from image_utils import ImageFrame, Oval, cv2, iradon, np, plt, radon
import random

class MplCanvas(FigureCanvas):

    def __init__(self, parent=None, width=5, height=4, dpi=100):
        fig = Figure(figsize=(width, height), dpi=dpi)
        self.axes = fig.add_subplot(111)
        super(MplCanvas, self).__init__(fig)
        self.setParent(parent)

def elipseToOvals(Intensidad,SemiEjeX,SemiEjeY,CentroX,CentroY,Inclinacion):
    return Oval(Intensidad, Inclinacion, SemiEjeX, SemiEjeY, CentroX, CentroY)

class elipse():    
    def __init__(self,Intensidad = None,SemiEjeX=None,SemiEjeY=None,CentroX=None,CentroY=None,Inclinacion=None):
        self.Intensidad = Intensidad  
        self.SemiEjeX = SemiEjeX      
        self.SemiEjeY = SemiEjeY      
        self.CentroX = CentroX        
        self.CentroY = CentroY        
        self.Inclinacion = Inclinacion

    def str_with_params(self):
        return (f"I:{self.Intensidad},X:{self.SemiEjeX},Y:{self.SemiEjeY},CX:{self.CentroX},CY:{self.CentroY},A:{self.Inclinacion}")


class radon_params():    
    def __init__(self = None,RadonDesde = None,RadonPaso = None,RadonHasta = None,RadonAngulo = None):
        self.RadonDesde = RadonDesde
        self.RadonPaso = RadonPaso
        self.RadonHasta = RadonHasta
        self.RadonAngulo = RadonAngulo

class iradon_params():    
    def __init__(self = None,iRadonDesde = None,iRadonPaso = None,iRadonHasta = None,iRadonAngulo = None):
        self.iRadonDesde = iRadonDesde
        self.iRadonPaso = iRadonPaso
        self.iRadonHasta = iRadonHasta
        self.iRadonAngulo = iRadonAngulo


class MainWindow(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self, *args, **kwargs):
        QtWidgets.QMainWindow.__init__(self, *args, **kwargs)
        self.setupUi(self)
        
        self.elipse_list = []
        self.displayed_elipse = elipse()
        self.image_frame = ImageFrame()

        self.displayed_radon = radon_params()
        self.displayed_iradon = iradon_params()
        
        self.canvas = MplCanvas(self, width=3, height=3, dpi=100)
        self.canvas.move(350,25)
        
        self.canvas_radon = MplCanvas(self, width=3, height=3, dpi=100)
        self.canvas_radon.move(850,25)

        self.canvas_iradon = MplCanvas(self, width=3, height=3, dpi=100)
        self.canvas_iradon.move(850,325)


        #asignamos la funcion asociada al evento textChanged
        self.lineEditIntensidad.textChanged.connect(self.textChangedIntensidad) # double
        self.lineEditIntensidad.setValidator(QtGui.QDoubleValidator(1.0,-1.0,4,notation=QtGui.QDoubleValidator.StandardNotation))
        
        self.lineEditSemiEjeX.textChanged.connect(self.textChangedSemiEjeX)
        self.lineEditSemiEjeX.setValidator(QtGui.QIntValidator(-1000,1000))
        
        self.lineEditSemiEjeY.textChanged.connect(self.textChangedSemiEjeY)
        self.lineEditSemiEjeY.setValidator(QtGui.QIntValidator(-1000,1000))

        
        self.lineEditCentroX.textChanged.connect(self.textChangedCentroX)
        self.lineEditCentroX.setValidator(QtGui.QIntValidator(-1000,1000))

        
        self.lineEditCentroY.textChanged.connect(self.textChangedCentroY)
        self.lineEditCentroY.setValidator(QtGui.QIntValidator(-1000,1000))


        self.lineEditInclinacion.textChanged.connect(self.textChangedInclinacion) # double
        self.lineEditInclinacion.setValidator(QtGui.QDoubleValidator(1.0,-1.0,4,notation=QtGui.QDoubleValidator.StandardNotation))


        self.lineEditRadonDesde.textChanged.connect(self.textChangedRadonDesde)
        self.lineEditRadonDesde.setValidator(QtGui.QIntValidator(0,360))

        self.lineEditRadonPaso.textChanged.connect(self.textChangedRadonPaso) # float
        self.lineEditRadonPaso.setValidator(QtGui.QDoubleValidator(0.0,360.0,4,notation=QtGui.QDoubleValidator.StandardNotation))
        
        self.lineEditRadonHasta.textChanged.connect(self.textChangedRadonHasta)
        self.lineEditRadonHasta.setValidator(QtGui.QIntValidator(0,360))

        self.lineEditRadonAngulo.textChanged.connect(self.textChangedRadonAngulo) # float
        self.lineEditRadonAngulo.setValidator(QtGui.QDoubleValidator(0.0,360.0,4,notation=QtGui.QDoubleValidator.StandardNotation))

        self.lineEditiRadonDesde.textChanged.connect(self.textChangediRadonDesde)
        self.lineEditiRadonDesde.setValidator(QtGui.QIntValidator(0,360))

        self.lineEditiRadonPaso.textChanged.connect(self.textChangediRadonPaso) # float
        self.lineEditRadonAngulo.setValidator(QtGui.QDoubleValidator(0.0,360.0,4,notation=QtGui.QDoubleValidator.StandardNotation))

        self.lineEditiRadonHasta.textChanged.connect(self.textChangediRadonHasta)
        self.lineEditiRadonHasta.setValidator(QtGui.QIntValidator(0,360))


        self.comboBoxInterpolacion.addItems(['linear', 'nearest', 'cubic'])
        self.comboBoxInterpolacion.currentIndexChanged.connect(self.selectionchangeInterpolacion)

        self.comboBoxFiltro.addItems(['ramp', 'shepp-logan', 'cosine', 'hamming', 'hann'])
        self.comboBoxFiltro.currentIndexChanged.connect(self.selectionchangeFiltro)

        #asignamos la funcion asociada al evento clicked en push buttons
        self.pushButtonAgregar.clicked.connect(self.onClickAgregar)
        self.pushButtonBorrar.clicked.connect(self.onClickBorrar)
        
        self.pushButtonRadonCalcular.clicked.connect(self.onClickRadonCalcular)
        self.pushButtoniRadonCalcular.clicked.connect(self.onClickiRadonCalcular)
          
        self.pushButtonAngulo.clicked.connect(self.onClickRadonAngulo)

    def onClickRadonAngulo(self):
        theta = self.displayed_radon.RadonAngulo #np.arange(self.displayed_radon.RadonDesde, self.displayed_radon.RadonHasta,self.displayed_radon.RadonPaso)
        aux_float_image = self.image_frame.image.astype(np.float64)
        projections  = radon(aux_float_image, theta=[theta])
        plt.plot(projections)
        plt.show()
  
        # projections  = radon(aux_float_image, theta=[theta])
        # self.canvas_radon.axes.cla()
        # self.canvas_radon.axes.imshow(projections)
        # self.canvas_radon.draw()

    def selectionchangeInterpolacion(self,i):
        pass
#        print("Items in the list are :")
            
#        for count in range(self.comboBoxInterpolacion.count()):
#            print(self.comboBoxInterpolacion.itemText(count))
#        print("Current index",i,"selection changed ",self.comboBoxInterpolacion.currentText())

    def selectionchangeFiltro(self,i):
        pass
#        print("Items in the list are :")        
#        for count in range(self.comboBoxFiltro.count()):
#            print(self.comboBoxFiltro.itemText(count))
#        print("Current index",i,"selection changed ",self.comboBoxFiltro.currentText())
        


    def onClickRadonCalcular(self):
        # print(self.displayed_radon.RadonAngulo)
        theta = np.arange(self.displayed_radon.RadonDesde, self.displayed_radon.RadonHasta,self.displayed_radon.RadonPaso)
        aux_float_image = self.image_frame.image.astype(np.float64)
        sinogram = radon(aux_float_image, theta=theta, circle=True)
        self.canvas_radon.axes.cla()
        self.canvas_radon.axes.imshow(sinogram, cmap=plt.cm.Greys_r,extent=(0, 180, 0, sinogram.shape[0]), aspect='auto')
        self.canvas_radon.draw()

    def onClickiRadonCalcular(self):
        theta = np.arange(self.displayed_iradon.iRadonDesde, self.displayed_iradon.iRadonHasta, self.displayed_iradon.iRadonPaso)
        aux_float_image = self.image_frame.image.astype(np.float64) 
        sinogram = radon(aux_float_image, theta=theta, circle=True)
        reconstruction_fbp = iradon(sinogram, theta=theta, filter_name = self.comboBoxFiltro.currentText() ,interpolation =self.comboBoxInterpolacion.currentText(),circle=True )
        error = reconstruction_fbp - self.image_frame.image
        self.canvas_iradon.axes.cla()
        self.canvas_iradon.axes.imshow(reconstruction_fbp, cmap=plt.cm.Greys_r)
        self.canvas_iradon.draw()
    

    def update_plot(self,image):
        self.canvas.axes.cla()  # Clear the canvas.
        self.canvas.axes.imshow(image, cmap='gray')
        # Trigger the canvas to update and redraw.
        self.canvas.draw()

    def areAllParamsDisplayedValid(self):
        if(self.validateNumberIntensidad() and self.validateNumberSemiEjeX() and self.validateNumberSemiEjeY()
        and self.validateNumberCentroX() and self.validateNumberCentroY() and self.validateNumberInclinacion()):
            return True
        else:
            return False
            
        #escribimos la funcion asociada al evento clicked en push buttons

    def updateElipseGraphics(self):
        for e in self.elipse_list:
           currOval = elipseToOvals(e.Intensidad,e.SemiEjeX,e.SemiEjeY,e.CentroX,e.CentroY,e.Inclinacion)
           self.image_frame.add_oval(currOval)
        self.image_frame.apply_ovals()

    def onClickAgregar(self):
        if self.areAllParamsDisplayedValid():
            Intensidad = self.displayed_elipse.Intensidad
            SemiEjeX = self.displayed_elipse.SemiEjeX
            SemiEjeY = self.displayed_elipse.SemiEjeY
            CentroX = self.displayed_elipse.CentroX
            CentroY = self.displayed_elipse.CentroY
            Inclinacion = self.displayed_elipse.Inclinacion
            new_elipse = elipse(Intensidad,SemiEjeX,SemiEjeY,CentroX,CentroY,Inclinacion)
            self.elipse_list.append(new_elipse)
            self.update_text()

            self.updateElipseGraphics()
            self.update_plot(self.image_frame.image)
        else:
            print("error en alguno de los parametros")

    def onClickBorrar(self):
        if len(self.elipse_list) > 0:
            self.elipse_list.pop()
            self.update_text()
        else:
            #que no haga nada cuando esta vacia
            pass

    def update_text(self):
        tableStr = ""
        for elip in self.elipse_list:
            tableStr+= elip.str_with_params()+ "\n"
        self.textEditParametersChart.setText(tableStr)

    #escribimos la validacion del numero de la funcion asociada al evento textChanged
    def validateNumberIntensidad(self):
        if self.displayed_elipse.Intensidad is not None:
            if  -1.0 <=self.displayed_elipse.Intensidad <= 1.0:
                return True
            else:
                print("rango invalido de Intensidad")
                return False
        else:
            return False
    def validateNumberSemiEjeX(self):
        #sobreescribir con rango
        if self.displayed_elipse.SemiEjeX is not None:
            return True
        else:
            return False
    def validateNumberSemiEjeY(self):
        #sobreescribir con rango
        if self.displayed_elipse.SemiEjeY is not None:
            return True
        else:
            return False
    def validateNumberCentroX(self):
        #sobreescribir con rango
        if self.displayed_elipse.CentroX is not None:
            return True
        else:
            return False
    def validateNumberCentroY(self):
        #sobreescribir con rango
        if self.displayed_elipse.CentroY is not None:
            return True
        else:
            return False
    def validateNumberInclinacion(self):
        #sobreescribir con rango
        if self.displayed_elipse.Inclinacion is not None:
            return True
        else:
            return False

    #escribimos la funcion asociada al evento textChanged
    def textChangedIntensidad(self):
        if(self.lineEditIntensidad.text()=='.'):
            self.displayed_elipse.Intensidad = 0
        else:
            if(len(self.lineEditIntensidad.text())!=0):
                input_number = float(self.lineEditIntensidad.text())
                self.displayed_elipse.Intensidad = input_number
    def textChangedSemiEjeX(self):
        if(self.lineEditSemiEjeX.text()=='.'):
            self.displayed_elipse.SemiEjeX = 0
        else:
            if(len(self.lineEditSemiEjeX.text())!=0):
                input_number = int(self.lineEditSemiEjeX.text())
                self.displayed_elipse.SemiEjeX = input_number
    def textChangedSemiEjeY(self):
        if(self.lineEditSemiEjeY.text()=='.'):
            self.displayed_elipse.SemiEjeY = 0
        else:
            if(len(self.lineEditSemiEjeY.text())!=0):
                input_number = int(self.lineEditSemiEjeY.text())
                self.displayed_elipse.SemiEjeY = input_number
    def textChangedCentroX(self):
        if(self.lineEditCentroX.text()=='.'):
            self.displayed_elipse.CentroX = 0
        else:
            if(len(self.lineEditCentroX.text())!=0):
                input_number = int(self.lineEditCentroX.text())
                self.displayed_elipse.CentroX = input_number
    def textChangedCentroY(self):
        if(self.lineEditCentroY.text()=='.'):
            self.displayed_elipse.CentroY = 0
        else:
            if(len(self.lineEditCentroY.text())!=0):
                input_number = int(self.lineEditCentroY.text())
                self.displayed_elipse.CentroY = input_number
    def textChangedInclinacion(self):
        if(self.lineEditInclinacion.text()=='.'):
            self.displayed_elipse.Inclinacion = 0
        else:
            if(len(self.lineEditInclinacion.text())!=0):
                input_number = float(self.lineEditInclinacion.text())
                self.displayed_elipse.Inclinacion = input_number


    def textChangedRadonDesde(self):
        if(self.lineEditRadonDesde.text()=='.'):
            self.displayed_radon.RadonDesde = 0
        else:
            if(len(self.lineEditRadonDesde.text())!=0):
                input_number = int(self.lineEditRadonDesde.text())
                self.displayed_radon.RadonDesde = input_number
    def textChangedRadonPaso(self):
        if(self.lineEditRadonPaso.text()=='.'):
            self.displayed_radon.RadonPaso = 0
        else:
            if(len(self.lineEditRadonPaso.text())!=0):
                input_number = float(self.lineEditRadonPaso.text())
                self.displayed_radon.RadonPaso = input_number
    def textChangedRadonHasta(self):
        if(self.lineEditRadonHasta.text()=='.'):
            self.displayed_radon.RadonHasta = 0
        else:
            if(len(self.lineEditRadonHasta.text())!=0):
                input_number = int(self.lineEditRadonHasta.text())
                self.displayed_radon.RadonHasta = input_number
    def textChangedRadonAngulo(self):
        if(self.lineEditRadonAngulo.text()=='.'):
            self.displayed_radon.RadonAngulo = 0
        else:
            if(len(self.lineEditRadonAngulo.text())!=0):
                input_number = float(self.lineEditRadonAngulo.text())
                self.displayed_radon.RadonAngulo = input_number
    def textChangediRadonDesde(self):
        if(self.lineEditiRadonDesde.text()=='.'):
            self.displayed_iradon.iRadonDesde = 0
        else:
            if(len(self.lineEditiRadonDesde.text())!=0):
                input_number = int(self.lineEditiRadonDesde.text())
                self.displayed_iradon.iRadonDesde = input_number
    def textChangediRadonPaso(self):
        if(self.lineEditiRadonPaso.text()=='.'):
            self.displayed_iradon.iRadonPaso = 0
        else:
            if(len(self.lineEditiRadonPaso.text())!=0):
                input_number = float(self.lineEditiRadonPaso.text())
                self.displayed_iradon.iRadonPaso = input_number
    def textChangediRadonHasta(self):
        if(self.lineEditiRadonHasta.text()=='.'):
            self.displayed_iradon.iRadonHasta = 0
        else:
            if(len(self.lineEditiRadonHasta.text())!=0):
                input_number = int(self.lineEditiRadonHasta.text())
                self.displayed_iradon.iRadonHasta = input_number
        
if __name__ == "__main__":
    app = QtWidgets.QApplication([])
    window = MainWindow()
    window.show()
    app.exec_()