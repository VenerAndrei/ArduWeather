# -*- coding: utf-8 -*-
"""
Various methods of drawing scrolling plots.
"""
import pyqtgraph as pg
from pyqtgraph.Qt import QtCore, QtGui
import numpy as np
import serial
import datetime 

win = pg.GraphicsWindow()
win.setWindowTitle('Meteo Station')

ser = serial.Serial('COM4')

# 1) Simplest approach -- update data in the array such that plot appears to scroll
#    In these examples, the array size is fixed.

p1 = win.addPlot()
p2 = win.addPlot()

text_uv = pg.TextItem('UV')
text_temp = pg.TextItem('TEMPERATURA')
text_pres = pg.TextItem('PRESIUNE')
p1.addItem(text_uv)
p2.addItem(text_pres)

win.nextRow()
p3 = win.addPlot(colspan=2)
p3.addItem(text_temp)
data_t = np.ones(200)
data_p = np.ones(100)
data_uv = np.ones(100)
curve_t = p3.plot(data_t)
curve_p = p2.plot(data_p)
curve_uv = p1.plot(data_uv)
last_h,now_h = -1,-1
def update1():
    global data_t, curve_t, ptr1,last_h,now_h
    
    date_today = datetime.date.today()
    now = datetime.datetime.now()
    data_t[:-1] = data_t[1:]
    data_p[:-1] = data_p[1:]
    data_uv[:-1] = data_uv[1:]

    #curve_p.setData(data_t)
    #curve_p.setPos(ptr1, 0)
    ser.write(b"SEND")
    line = ser.readline()
    byte_data = line.decode("utf-8")
    data = byte_data.split(";")
    print("RX:\t"+"T : "+data[0] + "\t" + "P : "+data[1] + "\t" + "UV : "+data[2])
    data_t[-1] =  data[0]
    data_p[-1] =  data[1]
    data_uv[-1] =  data[2]
    #print("[!] SENDED")
    curve_t.setData(data_t)
    curve_p.setData(data_p)
    curve_uv.setData(data_uv)
    now_h = now.minute
    if(last_h != now_h):
        file_str = str(date_today)+".txt"
        f = open(file_str,"a")
        f.write(byte_data)
    last_h = now_h


# update all plots
def update():
    update1()
timer = pg.QtCore.QTimer()
timer.timeout.connect(update)
timer.start(5000)



## Start Qt event loop unless running in interactive mode or using pyside.
if __name__ == '__main__':
    import sys
    if (sys.flags.interactive != 1) or not hasattr(QtCore, 'PYQT_VERSION'):
        QtGui.QApplication.instance().exec_()
        ser.close()