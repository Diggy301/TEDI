
from PyQt5.QtWidgets import QWidget, QTreeWidget, QTreeWidgetItem, QScrollArea
from PyQt5.QtCore import Qt, QRect, QSize




class HelpSubWindow(QWidget):
    def __init__(self):
        super(HelpSubWindow, self).__init__()
        self.setFixedSize(600, 500)
        self.setWindowTitle("Help")


        self.scrollArea = QScrollArea(self)
        self.scrollArea.setGeometry(QRect(0, 0, 600, 500))
        self.scrollArea.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        self.scrollArea.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.scrollAreaWidgetContents = QWidget(self)
        self.scrollAreaWidgetContents.setGeometry(QRect(0, 0, 600, 1000))
        self.scrollArea.setWidget(self.scrollAreaWidgetContents)


        self.treeWidget = QTreeWidget(self.scrollAreaWidgetContents)
        self.treeWidget.setGeometry(QRect(0, 0, 600, 1000))
        self.treeWidget.setObjectName("treeWidget")
        #self.treeWidget.headerItem().setText(0, "")
        self.treeWidget.header().setVisible(False)

        self.treeWidget.setColumnCount(1)
        tab1_table = QTreeWidgetItem(["New Project", ])
        self.treeWidget.addTopLevelItem(tab1_table)

        tab1_branch1 = QTreeWidgetItem(["Required Hardware"])
        tab1_branch1_subbranch1 = QTreeWidgetItem(["ChipWhisperer Lite"])
        tab1_branch1.addChild(tab1_branch1_subbranch1)
        tab1_branch1_subbranch2 = QTreeWidgetItem(["20 Pin connector"])
        tab1_branch1.addChild(tab1_branch1_subbranch2)
        tab1_branch1_subbranch3 = QTreeWidgetItem(["SMA to BNC connector"])
        tab1_branch1.addChild(tab1_branch1_subbranch3)
        tab1_branch1_subbranch4 = QTreeWidgetItem(["Oscilloscope probe"])
        tab1_branch1.addChild(tab1_branch1_subbranch4)
        tab1_table.addChild(tab1_branch1)

        tab1_branch2 = QTreeWidgetItem(["Number of traces"])
        tab1_branch2_subbranch1 = QTreeWidgetItem(["The number of traces to be captured by the ChipWhisperer Lite"])
        tab1_branch2.addChild(tab1_branch2_subbranch1)
        tab1_table.addChild(tab1_branch2)

        tab1_branch3 = QTreeWidgetItem(["Number of points"])
        tab1_branch3_subbranch1 = QTreeWidgetItem(["The number of measurements to be captured in a trace"])
        tab1_branch3.addChild(tab1_branch3_subbranch1)
        tab1_table.addChild(tab1_branch3)

        tab1_branch4 = QTreeWidgetItem(["Scope Offset"])
        tab1_branch4_subbranch1 = QTreeWidgetItem(["Delay the capture of ADC data a certain number of points"])
        tab1_branch4.addChild(tab1_branch4_subbranch1)
        tab1_table.addChild(tab1_branch4)
        
        tab1_branch5 = QTreeWidgetItem(["Scope Trigger"])
        tab1_branch5_subbranch1 = QTreeWidgetItem(["Method for triggering the start of capture"])
        tab1_branch5.addChild(tab1_branch5_subbranch1)
        tab1_table.addChild(tab1_branch5)
        
        tab1_branch6 = QTreeWidgetItem(["Key Length"])
        tab1_branch6_subbranch1 = QTreeWidgetItem(["Length of the key in bits"])
        tab1_branch6.addChild(tab1_branch6_subbranch1)
        tab1_table.addChild(tab1_branch6)
        
        tab1_branch7 = QTreeWidgetItem(["Plain Text"])
        tab1_branch7_subbranch1 = QTreeWidgetItem(['Option Box to select if the plaintext to be used in the capture of traces should be random or \nprovided. Provided plaintext should be placed in the path of this App. On each line of the file \nthe bytes should be writted as integers and separated by spaces.\nNOTE - if chosen "provide" option, the number of traces will be changed to the lengh \nof the provided plaintext'])
        tab1_branch7.addChild(tab1_branch7_subbranch1)
        tab1_table.addChild(tab1_branch7)

        tab1_branch8 = QTreeWidgetItem(["Capture Traces"])
        tab1_branch8_subbranch1 = QTreeWidgetItem(["Creates a ChipWhisperer Project (.cwp) in the current directory with the captured traces, along \nwith the plaintext sent and the cipher text received. Also updates the currently loaded project."])
        tab1_branch8.addChild(tab1_branch8_subbranch1)
        tab1_table.addChild(tab1_branch8)

        tab2_table = QTreeWidgetItem(["Load Project", ])
        self.treeWidget.addTopLevelItem(tab2_table)

        tab2_branch1 = QTreeWidgetItem(["Choose a Project"])
        tab2_branch1_subbranch1 = QTreeWidgetItem(["Select an existing ChipWhisperer Project (.cwp)"])
        tab2_branch1.addChild(tab2_branch1_subbranch1)
        tab2_table.addChild(tab2_branch1)

        tab2_branch2 = QTreeWidgetItem(["Encryption Model"])
        tab2_branch2_subbranch1 = QTreeWidgetItem(["Choose the encryption model to be used in the analysis. For more information on the existing \nmodels check: https://en.wikipedia.org/wiki/Block_cipher_mode_of_operation"])
        tab2_branch2.addChild(tab2_branch2_subbranch1)
        tab2_table.addChild(tab2_branch2)

        tab2_branch3 = QTreeWidgetItem(["Resynchronizing Traces with Sum of Absolute Difference"])
        tab2_branch3_subbranch1 = QTreeWidgetItem(["Algorithm used to overcome jitter-based countermeasures by resynchronizing the traces. \nWhen Radio button is checked the first trace of the project is ploted"])
        tab2_branch3.addChild(tab2_branch3_subbranch1)
        tab2_table.addChild(tab2_branch3)

        tab2_branch4 = QTreeWidgetItem(["Sum of Absolute Difference Window"])
        tab2_branch4_subbranch1 = QTreeWidgetItem(['Establish bounds for subset of the first trace of the project (reference trace). \nIdeally chosen to be "fairly unique".'])
        tab2_branch4.addChild(tab2_branch4_subbranch1)
        tab2_table.addChild(tab2_branch4)
        
        tab2_branch5 = QTreeWidgetItem(["Sum of Absolute Difference Max Shift"])
        tab2_branch5_subbranch1 = QTreeWidgetItem(["SAD algorithm will discard a trace if it needs to be shifted more than this value"])
        tab2_branch5.addChild(tab2_branch5_subbranch1)
        tab2_table.addChild(tab2_branch5)
        
        tab2_branch6 = QTreeWidgetItem(["Resynchronizing Traces with Dynamic Time Warp"])
        tab2_branch6_subbranch1 = QTreeWidgetItem(["Algorithm used to overcome the adition of jitter and random delays by resynchronizing \nthe traces. \nFor more information check: https://en.wikipedia.org/wiki/Dynamic_time_warping"])
        tab2_branch6.addChild(tab2_branch6_subbranch1)
        tab2_table.addChild(tab2_branch6)
        
        tab2_branch7 = QTreeWidgetItem(["Dynamic Time Warp Radius"])
        tab2_branch7_subbranch1 = QTreeWidgetItem(['Variable for the DTW Algorithm. Higher radii will generally give a better synchronization, but at \nthe cost of a higher processing time'])
        tab2_branch7.addChild(tab2_branch7_subbranch1)
        tab2_table.addChild(tab2_branch7)

        tab2_branch8 = QTreeWidgetItem(["Export plaintext / ciphertext"])
        tab2_branch8_subbranch1 = QTreeWidgetItem(["Simple button to export the plaintext and the cipher text found in the currently loaded project. \nText files will be created in the current path"])
        tab2_branch8.addChild(tab2_branch8_subbranch1)
        tab2_table.addChild(tab2_branch8)

        plot = QTreeWidgetItem(["Plot Widget"])
        self.treeWidget.addTopLevelItem(plot)
        plot_branch = QTreeWidgetItem(["On the top contains a default Matplotlib figure toolbar. The bottom portion contains a canvas."])
        plot.addChild(plot_branch)

        textbox = QTreeWidgetItem(["Plot Random Trace Button"])
        self.treeWidget.addTopLevelItem(textbox)
        text = QTreeWidgetItem(["Button which plots on the canvas a random point of the currently loaded project."])
        textbox.addChild(text)

        textbox = QTreeWidgetItem(["Current Project Settings"])
        self.treeWidget.addTopLevelItem(textbox)
        text = QTreeWidgetItem(["Contains a regular textbox which is filled when the information of the currently \nloaded project"])
        textbox.addChild(text)

        analysistable = QTreeWidgetItem(["Analysis Table"])
        self.treeWidget.addTopLevelItem(analysistable)
        tabletext = QTreeWidgetItem(["Start Analysis button begins the analysis of the currently loaded project with the selected \nencryption model. \nThe table is updated in real time with the results of the analysis at that time. \nThe upper value in a cell indicates the value of the byte in hexadecimal form. \nThe lower one indicates the correlation value with the traces of the project"])
        analysistable.addChild(tabletext)

        defaultkeybranch = QTreeWidgetItem(["Use default Key"])
        defaultkeysubbranch = QTreeWidgetItem(['When pressed, it locates a "defaultkey.txt" in the path of this App. In this file, the bytes of the key \nshould be written as integers and separated by spaces.'])
        defaultkeybranch.addChild(defaultkeysubbranch)
        analysistable.addChild(defaultkeybranch)


