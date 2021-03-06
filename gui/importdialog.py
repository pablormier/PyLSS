'''
@package importdialog.py

importdialog.py was writen by Giuseppe Marco Randazzo <gmrandazzo@gmail.com>
and is distributed under LGPL version 3

Geneve February 2015
'''

from PyQt4 import *
from PyQt4 import *
import sys

from gui_importdialog import Ui_ImportDialog
from os.path import isfile, basename
from utilities import *

class ImportDialog(QtGui.QDialog, Ui_ImportDialog):
    def __init__(self,parent=None):
        QtGui.QDialog.__init__(self,parent)
        self.setupUi(self)
        self.tablemodel = TableModel(self)
        self.tableView.setModel(self.tablemodel)
        self.openButton.clicked.connect(self.open_)
        self.closeButton.clicked.connect(self.close_)
        self.okButton.clicked.connect(self.ok_)
        self.splitlineby.currentIndexChanged.connect(self.preview)
        self.lineEdit.textChanged.connect(self.preview)
        self.firstcolobjname.stateChanged.connect(self.preview)

    def open_(self):
        fname = QtGui.QFileDialog.getOpenFileName(self, 'Open file')
        if fname and isfile(fname):
            self.lineEdit.setText(fname)
            self.lineEdit_2.setText(str.split(basename(str(fname)), ".")[0])
            self.preview()

    def close_(self):
        self.reject()

    def ok_(self):
        self.accept()

    def preview(self):
        f = open(self.lineEdit.text())
        self.tablemodel.clean()
        i = 0
        grad = []
        tg = []
        for line in f:
            if "dwell volume" in line.lower():
                self.dwelVolSpinBox.setValue(float(nsplit(line.strip(), ":")[-1]))
            elif "flow rate" in line.lower():
                self.flowrateSpinBox.setValue(float(nsplit(line.strip(), ":")[-1]))
            elif "time zero" in line.lower():
                self.t0SpinBox.setValue(float(nsplit(line.strip(), ":")[-1]))
            elif "gradient " in line.lower(): # Each line is a gradient column
                v = str.split(line.strip(), ":")[-1].strip()
                v = str.split(v, " ")
                tg.append(float(v[0]))
                grad.append([float(v[1])/100., float(v[2])/100.])
            else:
                v = nsplit(line.strip(), self.splitlineby.currentText())
                row = []
                if i < 10:
                    if i == 0:
                        header = []
                        header.append("Molecule")
                        for j in range(len(grad)):
                            header.append("%.1f%% %.1f%% %.1f min" % (round(grad[j][0]*100,1), round(grad[j][1]*100,1), tg[j]))
                        self.tablemodel.setHeader(header)
                        self.tableView.model().layoutChanged.emit()

                    if self.firstcolobjname.isChecked():
                        row.append(v[0])
                        for j in range(1, len(v)):
                            try:
                                row.append(float(v[j]))
                            except:
                                row.append(v[j])
                    else:
                        row.append("Molecule %d" % (i+1))
                        for item in v:
                            try:
                                row.append(float(item))
                            except:
                                row.append(item)
                    self.tablemodel.addRow(row)
                    self.tableView.model().layoutChanged.emit()
                    i += 1
                else:
                    row.append("...")
                    for j in range(len(v)):
                        row.append("...")
                    self.tablemodel.addRow(row)
                    self.tableView.model().layoutChanged.emit()
                    break
        f.close()

    def getdata(self):
        trdata = []
        molname = []
        grad = []
        tg = []
        f = open(self.lineEdit.text())
        self.tablemodel.clean()
        i = 0
        for line in f:
            if "dwell volume" in line.lower():
                self.dwelVolSpinBox.setValue(float(nsplit(line.strip(), ":")[-1]))
            elif "flow rate" in line.lower():
                self.flowrateSpinBox.setValue(float(nsplit(line.strip(), ":")[-1]))
            elif "time zero" in line.lower():
                self.t0SpinBox.setValue(float(nsplit(line.strip(), ":")[-1]))
            elif "gradient " in line.lower(): # Each line is a gradient column
                v = str.split(line.strip(), ":")[-1].strip()
                v = str.split(v, " ")
                tg.append(float(v[0]))
                grad.append([float(v[1])/100., float(v[2])/100.])
            else:
                v = nsplit(line.strip(), self.splitlineby.currentText())
                trdata.append(list())
                if self.firstcolobjname.isChecked():
                    molname.append(v[0])
                    for j in range(1, len(v)):
                        trdata[-1].append(float(v[j]))
                else:
                    molname.append("Molecule %d" % (i+1))
                    for item in v:
                        trdata[-1].append(float(item))
                i += 1
        f.close()

        return [self.lineEdit_2.text(), molname, trdata, grad, tg,
                self.dwelVolSpinBox.value(), self.t0SpinBox.value(),
                self.flowrateSpinBox.value()]
