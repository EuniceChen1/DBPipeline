import os
import sys
from PySide.QtCore import *
from PySide import QtGui, QtUiTools
from createUi import Ui_MainWindow
import csv


class Window(QtGui.QMainWindow,Ui_MainWindow):
    def __init__(self,parent=None):
        super(Window, self).__init__(parent)
        loader = QtUiTools.QUiLoader()
        uifile = QFile(r"D:\Pipeline\createCSV.ui")
        uifile.open(QFile.ReadOnly)
        self.ui = loader.load(uifile,self)
        uifile.close()
        self.setupUi(self)
        self.setGeometry( 500,500,383,430 )
        self.setWindowTitle("PITA")
        self.setWindowIcon(QtGui.QIcon(r'C:\Pipeline\icons\favicon.ico')) 
        
        self.numOfSeqBox.returnPressed.connect(self.sequenceTree)
        
        self.addSelectedBt.clicked.connect(self.addSelBt)

        self.removeBt.clicked.connect(self.clearBt)

        self.submitBt.clicked.connect(self.makeCSV)
    
    def sequenceTree(self):
        self.sqList = []
        self.seqNum = self.numOfSeqBox.text()
        assert self.seqNum.isdigit(), "Must be a number!!"
        self.sqName=[]
        for q in xrange(int(self.seqNum)):
            q = q+1
            self.sqList.append(os.path.join('sc'+'%03d'%q))
            self.sqName.append(QtGui.QTreeWidgetItem(self.seqTree,['%03d'%q]))
            
        self.seqTree.expandItem(QtGui.QTreeWidgetItem(self.sqName))
        self.seqTree.addTopLevelItems(self.sqName)

    def addSelBt(self):
        self.noSubItem = self.subItemBox.text()
        assert self.noSubItem.isdigit(), "Must be a number!!"
        selectedItems = self.seqTree.selectedItems()
        scnName = []
        shtName = []
        if selectedItems[0].childCount() == 0:
            if len(selectedItems) > 0:
                
                for i in xrange(int(self.noSubItem)):
                    i = i+1
                    
                    if "sc" not in selectedItems[0].text(0):
                        selectedItems[0].addChild(QtGui.QTreeWidgetItem([('sc'+'%03d'%i)]))
                        continue
                        
                    else:
                        QtGui.QTreeWidgetItem(selectedItems[0],[('sh'+'%03d'%i)])
            else:
                assert (len(selectedItems) > 0), "Nothing is selected!"
                
        else:
            if len(selectedItems) > 0:
                for j in xrange(int(self.noSubItem)):
                    k = j + int((selectedItems[0].child(j).text(0))[-1])
                    k = k + 1
                    if "sc" not in selectedItems[0].text(0):
                        selectedItems[0].addChild(QtGui.QTreeWidgetItem([('sc'+'%03d'%k)]))
                        continue
                    else:
                        
                        QtGui.QTreeWidgetItem(selectedItems[0],[('sh'+'%03d'%k)])
            else:
                assert (len(selectedItems) > 0), "Nothing is selected!"

    def clearBt(self):
        selectedRemove = self.seqTree.selectedItems()
        if len(selectedRemove) > 0:
            #self.seqTree.clearSelection()
            selectedRemove[0].takeChildren()
        else:
            assert (len(selectedRemove) > 0), "Nothing is selected!"

    def makeCSV(self):
        outputFileA = os.path.join("D:\\"+"temp"+".csv")
        header = ["Sequence","Scene","Shot"]
        with open(outputFileA,'wb') as g:
            fieldnames = ["Sequence","Scene","Shot"]
            wr = csv.DictWriter(g,fieldnames=fieldnames)
            wr.writeheader()

##            keep_running = True
##            while(keep_running):
##            for i in self.sqList:
##                print i.items()
            
            print self.seqTree.itemWidget(0,QtGui.QTreeWidgetItem.child(0))
                
              

if __name__ == "__main__":
    app = QtGui.QApplication(sys.argv)
    myGUI = Window()
    myGUI.show()
    sys.exit(app.exec_())

