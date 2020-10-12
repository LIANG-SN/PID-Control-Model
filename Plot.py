from pyqtgraph.Qt import QtGui, QtCore
import numpy as np
import pyqtgraph as pg
import math
import Model
import PID


# main strucure of window
app = QtGui.QApplication([])
# Enable antialiasing for prettier plots
pg.setConfigOptions(antialias=True)

mainWindow = QtGui.QMainWindow()
mainWindow.setWindowTitle('PID Tunning Simulator')
mainWindow.resize(800, 800)
layout = pg.LayoutWidget()
mainWindow.setCentralWidget(layout)
mainWindow.show()  # show window

# update model variables
model = Model.Model(100, 0)
pid = PID.PID(0, 0, 0)
setPoint = 100
# param tunning
spinP=pg.SpinBox(value = pid.p, decimals = 4, step = 0.5)
spinI=pg.SpinBox(value = pid.i, decimals = 4, step = 0.5)
spinD=pg.SpinBox(value = pid.d, decimals = 4, step = 0.5)
spinSP = pg.SpinBox(value = setPoint, step = 0.5)

spins = [
    ("Propotional", 
    spinP),
    ("Integration",
     spinI),
    ("Derivative",
     spinD),
    ("Set Point",
     spinSP)
]
colCount = 0
for text, spin in spins:
    label = QtGui.QLabel(text)
    layout.addWidget(label, row = 1, col=colCount)
    colCount+=1
    layout.addWidget(spin, row = 1, col=colCount)
    colCount+=1

# plotting

# graph feature
refreshPeriod = 0.01
totalTime = 10
dataLength = (int)(totalTime / refreshPeriod)

plotWidget = pg.PlotWidget(name="system status", background='default')
plotWidget.setTitle('System Status')
plotWidget.addLegend()
plotWidget.setYRange(0,100)
plotWidget.setXRange(-10, 0)
plotWidget.setLabel('bottom', text='time', units='s')  # add units
plotWidget.showGrid(x=True, y=False, alpha=1)
layout.addWidget(plotWidget, row=3, col=0, colspan=8)

# misc widgets
updatingLabel = QtGui.QLabel()
timeLabel = QtGui.QLabel()
errLabel = QtGui.QLabel()
runCheck = QtGui.QCheckBox('Run')
runCheck.setChecked(False)
layout.addWidget(runCheck, row = 0, colspan=1)
layout.addWidget(updatingLabel, row = 0, colspan=2)
layout.addWidget(timeLabel, row = 0, colspan=2)
layout.addWidget(errLabel, row = 0, colspan=2)

pidOutputCheck = QtGui.QCheckBox('pid output')
actualValueCheck = QtGui.QCheckBox('actual value')
setPointCheck = QtGui.QCheckBox('set point')
actualValueCheck.setChecked(True)
setPointCheck.setChecked(True)

layout.addWidget(pidOutputCheck, row = 2,col = 0, colspan=2,)
layout.addWidget(actualValueCheck, row = 2,col = 2, colspan=2)
layout.addWidget(setPointCheck, row=2, col = 4, colspan=2)
# data
xValue = np.linspace(-totalTime, 0, dataLength, False)
pidOutputArr = np.zeros(dataLength, dtype=float)
actualValueArr = np.zeros(dataLength, dtype=float)
setPointArr = np.zeros(dataLength, dtype=float)
nullArr = np.empty(dataLength)
nullArr[:] = np.nan
# nullArr = np.zeros(dataLength)

def updateModel():
    global model, pid, pidOutputArr, actualValueArr, setPointArr, xValue, spinP, spinI, spinD
    pid.p = (float)(spinP.value())
    pid.i = (float)(spinI.value())
    pid.d = (float)(spinD.value())
    setPoint = (float)(spinSP.value()) #  modify set point to check robustness

    pidOutput = pid.update(setPoint, model.actualValue,
                           actualValueArr[(dataLength - 1) - 1])
    delayTime = 0.3
    model.update(pidOutputArr[dataLength - 1 - (int)(delayTime / refreshPeriod)])
    for i in range(0, dataLength - 1):
        xValue[i] += refreshPeriod
        pidOutputArr[i] = pidOutputArr[i + 1]
        actualValueArr[i] = actualValueArr[i + 1]
        setPointArr[i] = setPointArr[i + 1]
    xValue[dataLength - 1] += refreshPeriod
    pidOutputArr[dataLength - 1] = (float)(pidOutput)
    actualValueArr[dataLength - 1] = model.actualValue
    setPointArr[dataLength - 1] = setPoint
 

# graphs
pidOutputCurve = plotWidget.plot(
    y=pidOutputArr, x=xValue, pen='r', name='pid output', connect = 'finite')
actualValueCurve = plotWidget.plot(
    y=actualValueArr, x=xValue, pen='y', name='actual value', connect = 'finite')
setPointCurve = plotWidget.plot(
    y=setPointArr, x=xValue, pen='g', name='set point', connect = 'finite')


count = 0
def update():
    global pidOutputCurve, actualValueCurve, setPointCurve, count, plotWidget, actualValueArr, setPointArr
    if runCheck.isChecked():
        updateModel()
        # plot data
        plotWidget.setXRange(xValue[0], xValue[0] + totalTime)
        if pidOutputCheck.isChecked():
            pidOutputCurve.setData(x=xValue, y=pidOutputArr)
        else:
            pidOutputCurve.setData(x=xValue, y=nullArr)
        if actualValueCheck.isChecked():
            actualValueCurve.setData(x=xValue, y=actualValueArr)
        else:
            actualValueCurve.setData(x=xValue, y=nullArr)
        if setPointCheck.isChecked():
            setPointCurve. setData(x=xValue, y=setPointArr)
        else:
            setPointCurve.setData(x=xValue, y=nullArr)
        if count == 0:
            # stop auto-scaling after the first data set is plotted
            plotWidget.enableAutoRange('xy', False)
        count += 1
        updatingLabel.setText('updating: %i samples' % count)
        time = count * refreshPeriod
        timeLabel.setText('Time: %f' % time)
        error = actualValueArr[dataLength-1] - setPointArr[dataLength-1]
        errLabel.setText('Error: %f' % error)
    else:
        updatingLabel.setText('suspended')


timer = QtCore.QTimer()
timer.timeout.connect(update)
timer.start(1000 * refreshPeriod)


# Start Qt event loop unless running in interactive mode or using pyside.
if __name__ == '__main__':
    import sys
    if (sys.flags.interactive != 1) or not hasattr(QtCore, 'PYQT_VERSION'):
        QtGui.QApplication.instance().exec_()
