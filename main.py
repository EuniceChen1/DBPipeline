import os
import sys
from PySide.QtCore import *
from PySide import QtGui, QtUiTools
from main_ui import Ui_MainWindow
import csv

class Window(QtGui.QMainWindow,Ui_MainWindow):
    def __init__(self,parent=None):
        super(Window, self).__init__(parent)
        self.setupUi(self)
        self.setGeometry( 500,500,383,430 )
        self.setWindowTitle("Sequence Handler")
        self.setWindowIcon(QtGui.QIcon(r'C:\Users\Eunice Chen\Pictures\pythonlogo.png'))
        #self.seqTree.setSelectionMode(QtGui.QAbstractItemView.ExtendedSelection)

        #DISABLE EVERYTHING UNLESS PROJECT NAME IS TYPED
        self.numOfSeqBox.setEnabled(0)
        self.addSelectedBt.setEnabled(0)
        self.removeBt.setEnabled(0)
        self.seqTree.setEnabled(0)
        self.submitBt.setEnabled(0)
        self.cancelBt.setEnabled(0)
        self.resetBt.setEnabled(0)
        
        #CONNECTIONS
        self.numOfSeqBox.returnPressed.connect(self.sequenceTree)
        self.addSelectedBt.clicked.connect(self.addSelBt)
        self.removeBt.clicked.connect(self.clearBt)
        self.submitBt.clicked.connect(self.onSubmit)
        self.cancelBt.clicked.connect(self.onCancel)
        self.resetBt.clicked.connect(self.onReset)
        self.projNameBox.textChanged.connect(self.projName)

    def projName(self):
        if len(self.projNameBox.text()) != 0:
            self.numOfSeqBox.setEnabled(1)
            self.addSelectedBt.setEnabled(1)
            self.removeBt.setEnabled(1)
            self.seqTree.setEnabled(1)
            self.submitBt.setEnabled(1)
            self.cancelBt.setEnabled(1)
            self.resetBt.setEnabled(1)
    
    def sequenceTree(self):
        
        self.sqList = []
        self.seqNum = self.numOfSeqBox.text()
        assert self.seqNum.isdigit(), "Must be a number!!"
        self.sqName=[]
        if self.seqNum != "0":
            if self.seqTree.topLevelItemCount() == 0:
                for q in xrange(int(self.seqNum)):
                    q = q+1
                    self.sqList.append(os.path.join('%03d'%q))
                    self.sqName.append(QtGui.QTreeWidgetItem(self.seqTree,['sq'+'%03d'%q]))
                    
                self.seqTree.expandItem(QtGui.QTreeWidgetItem(self.sqName))
                self.seqTree.addTopLevelItems(self.sqName)
                self.seqTree.sortItems(0,Qt.SortOrder(0))
            else:
                numOfTopLevelItems = self.seqTree.topLevelItemCount()
                for m in xrange(int(self.seqNum)):
                    topItem = m + numOfTopLevelItems
                    topItem = topItem + 1
                    self.sqName.append(QtGui.QTreeWidgetItem(self.seqTree,['sq'+'%03d'%topItem]))
                self.seqTree.expandItem(QtGui.QTreeWidgetItem(self.sqName))
                self.seqTree.addTopLevelItems(self.sqName)
                self.seqTree.sortItems(0,Qt.SortOrder(0))
            
        else:
            self.sqName.append(QtGui.QTreeWidgetItem(self.seqTree,['sq000']))
            self.seqTree.expandItem(QtGui.QTreeWidgetItem(self.sqName))
            self.seqTree.addTopLevelItems(self.sqName)
            self.seqTree.sortItems(0,Qt.SortOrder(0))

    def addSelBt(self):
        #self.scnName = []
        #self.shtName = []
        self.noSubItem = self.subItemBox.text()
        if self.noSubItem.isdigit() == False:
            self.mustBeDigit()
            assert (self.noSubItem.isdigit()), "Must be a number!!"
            
        selectedItems = self.seqTree.selectedItems()
        if selectedItems[0].childCount() == 0:
            if len(selectedItems) > 0:
                
                for i in xrange(int(self.noSubItem)):
                    i = i+1
                    if "sc" not in selectedItems[0].text(0) and "sh" not in selectedItems[0].text(0):
                        selectedItems[0].addChild(QtGui.QTreeWidgetItem([('sc'+'%03d'%i)]))
                        #self.scnName.append(QtGui.QTreeWidgetItem([('sc'+'%03d'%i)]).text(0))
                        continue
                        
                    else:
                        if "sh" not in selectedItems[0].text(0):
                            QtGui.QTreeWidgetItem(selectedItems[0],[('sh'+'%03d'%i)])
                        #self.shtName.append(QtGui.QTreeWidgetItem([('sh'+'%03d'%i)]).text(0))
            else:
                self.ntgSelected()
                assert (len(selectedItems) > 0), "Nothing is selected!"
                
        else:
            if len(selectedItems) > 0:
                numOfChild = selectedItems[0].childCount()
                for j in xrange(int(self.noSubItem)):
                    k = j + numOfChild #int((selectedItems[0].child(j).text(0))[-1])
                    k = k + 1
                    if "sc" not in selectedItems[0].text(0):
                        selectedItems[0].addChild(QtGui.QTreeWidgetItem([('sc'+'%03d'%k)]))
                        #self.scnName.append(QtGui.QTreeWidgetItem([('sc'+'%03d'%k)]).text(0))
                        continue
                    else:
                        QtGui.QTreeWidgetItem(selectedItems[0],[('sh'+'%03d'%k)])
                        #self.shtName.append(QtGui.QTreeWidgetItem(selectedItems[0],[('sh'+'%03d'%k)]))
            else:
                self.ntgSelected()
                assert (len(selectedItems) > 0), "Nothing is selected!"

    def clearBt(self):
        selectedRemove = self.seqTree.selectedItems()
        if len(selectedRemove) > 0:
            selectedRemove[0].takeChildren()
        else:
            self.ntgSelected()
            assert (len(selectedRemove) > 0), "Nothing is selected!"
            

    def makeCSV(self):
        sq=[]
        outputFileA = os.path.join("D:\\"+"temp"+".csv")
        with open(outputFileA,'wb') as g:
            fieldnames = ["Sequence","Scene","Shot"]
            wr = csv.DictWriter(g,fieldnames=fieldnames)
            wr.writeheader()

            for j in self.sqName:
                sq.append(j.text(0).split("q")[-1])
                if j.childCount() != 0:
                    for scItem in range(0,j.childCount()):
                        scItem = scItem + 1
                        if j.child(scItem-1).text(0) != None:
                            scene = j.child(scItem-1)
                            if scene.childCount() != 0:
                                for shItem in range(0,scene.childCount()):
                                    shItem = shItem + 1
                                    if scene.child(shItem-1).text(0) != None:
                                        shot = scene.child(shItem-1)

                                        wr.writerow({
                                                    fieldnames[0]:j.text(0).split("q")[-1],
                                                    fieldnames[1]:scene.text(0).split("c")[-1],
                                                    fieldnames[2]:shot.text(0)
                                                    })
                            else:
                                wr.writerow({
                                            fieldnames[0]:j.text(0).split("q")[-1],
                                            fieldnames[1]:scene.text(0).split("c")[-1],
                                            fieldnames[2]:""
                                            })
                else:
                    wr.writerow({
                                fieldnames[0]:j.text(0).split("q")[-1],
                                fieldnames[1]:"",
                                fieldnames[2]:""
                                })

                            
                                
        projName = self.projNameBox.text()
        outputFileB = os.path.join("D:\\"+projName+"_"+"tacticData"+".csv")
        
        with open(outputFileA,'r') as inf:
            with open(outputFileB,'wb') as outf:
                reader = inf.readlines()
                for ind, q in enumerate(reader):
                    if ind == 0:
                        reader[ind] = "Sq,"+q
                    else:
                        if ind-1 >= len(sq):
                            reader[ind] = ","+q
                        else:
                            reader[ind] = self.sqList[ind-1]+","+q

                    outf.write(reader[ind])
                    
        os.remove(outputFileA)

    def onSubmit(self):
        """
        Show Submit question message
        """
        msgBox = QtGui.QMessageBox()
        msgBox.setIcon(QtGui.QMessageBox.Question)
        msgBox.setWindowTitle("Confirm")
        msgBox.setText("Are you sure you want to submit?")
        msgBox.setStandardButtons(QtGui.QMessageBox.Yes | QtGui.QMessageBox.No)
        msgBox.setDefaultButton(QtGui.QMessageBox.Yes)
        response = msgBox.exec_()

        if response == QtGui.QMessageBox.Yes:
            self.makeCSV()
            msgBox = QtGui.QMessageBox()
            msgBox.setWindowTitle("Action is not available")
            msgBox.setIcon(QtGui.QMessageBox.Critical)
            msgBox.setText("Application is not accessible.")
            msgBox.setInformativeText("Access is denied.")
            msgBox.addButton(msgBox.Retry)
            retry = msgBox.exec_()
            if retry == QtGui.QMessageBox.Retry:
                replyBox = QtGui.QMessageBox()
                replyBox.setWindowTitle("Information")
                replyBox.setIcon(QtGui.QMessageBox.Information)
                replyBox.setText("Just Kidding ;)")
                replyBox.setInformativeText("Your data has been submitted. \n \n A CSV file has been generated in your local drive.")
                reply = replyBox.exec_()
            self.close()
            
        elif response == QtGui.QMessageBox.No:
            msgBox = QtGui.QMessageBox()
            msgBox.setWindowTitle("Warning")
            msgBox.setIcon(QtGui.QMessageBox.Warning)
            msgBox.setText("You're fired!")
            response = msgBox.exec_()
        else:
            print "Choose wisely" #This should not happen
            
    def onCancel(self):
        """
        Show Cancel question message
        """
        msgBox = QtGui.QMessageBox()
        msgBox.setIcon(QtGui.QMessageBox.Question)
        msgBox.setWindowTitle("Warning")
        msgBox.setText("Are you sure you want to quit?")
        msgBox.setStandardButtons(QtGui.QMessageBox.Yes | QtGui.QMessageBox.No)
        msgBox.setDefaultButton(QtGui.QMessageBox.Yes)
        response = msgBox.exec_()

        if response == QtGui.QMessageBox.Yes:
            msgBox = QtGui.QMessageBox()
            msgBox.setWindowTitle("Warning")
            msgBox.setIcon(QtGui.QMessageBox.Warning)
            msgBox.setText("You're fired for quitting!")
            response = msgBox.exec_()
            self.close()
            
        elif response == QtGui.QMessageBox.No:
            msgBox = QtGui.QMessageBox()
            msgBox.setWindowTitle("Warning")
            msgBox.setIcon(QtGui.QMessageBox.Warning)
            msgBox.setText("Wrong answer!")
            response = msgBox.exec_()
        else:
            print "Choose wisely" #This should not happen

    def onReset(self):
        self.seqTree.clear()

    def ntgSelected(self):
        """
        Show Nothing selected message
        """
        msgBox = QtGui.QMessageBox()
        msgBox.setIcon(QtGui.QMessageBox.Warning)
        msgBox.setWindowTitle("Alert!")
        msgBox.setText("Nothing is selected!!")
        response = msgBox.exec_()

    def mustBeDigit(self):
        """
        Show Nothing selected message
        """
        msgBox = QtGui.QMessageBox()
        msgBox.setIcon(QtGui.QMessageBox.Warning)
        msgBox.setWindowTitle("Alert!")
        msgBox.setText("Input must be a number!!")
        response = msgBox.exec_()
    

if __name__ == "__main__":
    app = QtGui.QApplication(sys.argv)
    myGUI = Window()
    myGUI.show()
    sys.exit(app.exec_())

