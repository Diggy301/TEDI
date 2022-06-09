from multiprocessing.sharedctypes import Value
import os
from matplotlib import pyplot as plt
import random 
import numpy as np

import chipwhisperer as cw
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import Qt
from matplotlib.backends.backend_qt5agg import FigureCanvas, NavigationToolbar2QT

from pandasmodel import PandasModel
from leakagemodels import get_leakage_model
from analysis import Analysis
from helper_windows import HelpSubWindow



class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        
        self.default_sad_resync_window_min_value = 0
        self.default_sad_resync_window_max_value = 300
        self.default_sad_resync_max_shift_value = 1000
        self.default_dtw_resync_radius_value = 1
        self.current_proj  = None
        self.current_analysis_model = None
        self.sad_window_min_value = self.default_sad_resync_window_min_value
        self.sad_window_max_value = self.default_sad_resync_window_max_value
        self.sad_max_shift_value = self.default_sad_resync_max_shift_value
        self.dtw_radius_value = self.default_dtw_resync_radius_value
        self.current_proj_key = None
        self.plaintext_option_data = None

        self.help_subwindow = HelpSubWindow()

        self.setStyleSheet("background-color: #606060;")
        # Continental orange: #FFA500
        self.setupUi()
        self.setFixedSize(1200, 900) # fixed size
        #self.resize(1200, 900)
        self.center()
        self.show()


    def setupUi(self):
        #validator for only-number-inputs
        self.is_number_validator = QtGui.QIntValidator()
        
        #logo
        self.ces_logo_label = QtWidgets.QLabel(self)
        self.ces_logo_label.move(1050, 850)
        self.ces_logo = QtGui.QPixmap('logo.png')
        self.ces_logo_label.setPixmap(self.ces_logo)
        self.ces_logo_label.setGeometry(QtCore.QRect(1028, 864 ,self.ces_logo.width(), self.ces_logo.height()))

        #table widget
        self.table_widget = QtWidgets.QWidget(self)
        self.table_widget.setGeometry(QtCore.QRect(330, 550, 800, 300))
        self.table_grid_layout_widget = QtWidgets.QGridLayout(self.table_widget)
        self.table_grid_layout_widget.setContentsMargins(0, 0, 0, 0)
        self.table_view = QtWidgets.QTableView(self.table_widget)
        vheader = self.table_view.verticalHeader()
        vheader.setSectionResizeMode(QtWidgets.QHeaderView.Stretch)
        self.table_view.setContentsMargins(0, 0, 0, 0)
        self.table_view.horizontalHeader().setSectionResizeMode(1)
        self.table_grid_layout_widget.addWidget(self.table_view, 0, 0, 1, 1)

        #plot widget
        self.plot_frame = QtWidgets.QFrame(self)
        self.plot_frame.setGeometry(QtCore.QRect(330, 0, 800, 500))
        self.plot_frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.plot_frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.vertical_layout_plot_widget = QtWidgets.QWidget(self.plot_frame)
        self.vertical_layout_plot_widget.setGeometry(QtCore.QRect(0, 0, 800, 500))
        self.vertical_layout_plot = QtWidgets.QVBoxLayout(self.vertical_layout_plot_widget)
        self.vertical_layout_plot.setContentsMargins(0, 0, 0, 0)
        self.plot_figure = plt.figure()
        self.plot_axe = self.plot_figure.add_subplot(111)
        self.plot_figure.set_facecolor('#808080')
        self.plot_axe.set_facecolor('silver')
        self.plot_canvas = FigureCanvas(self.plot_figure)
        self.vertical_layout_plot.addWidget(NavigationToolbar2QT(self.plot_canvas, self.vertical_layout_plot_widget), alignment=Qt.AlignVCenter)
        self.vertical_layout_plot.addWidget(self.plot_canvas)

        #Tab widget
        #tab1
        self.tab_widget = QtWidgets.QTabWidget(self)
        self.tab_widget.setGeometry(QtCore.QRect(15, 20, 300, 462))
        self.tab1 = QtWidgets.QWidget()
        self.tab_widget.addTab(self.tab1, "New Project")
        self.tab1.setStyleSheet("border-color: blue;")
        #self.tab1.setStyleSheet("background-color: #FFA500;")
        self.tab1_group_box = QtWidgets.QGroupBox(self.tab1)
        self.tab1_group_box.setStyleSheet('color: white;')
        self.tab1_group_box.setEnabled(True)
        self.tab1_group_box.setGeometry(QtCore.QRect(28, 30, 244, 390))
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.tab1_group_box.sizePolicy().hasHeightForWidth())
        self.tab1_group_box.setSizePolicy(sizePolicy)
        self.tab1_group_box.setMaximumSize(QtCore.QSize(400, 16777215))

        
        self.tab1_group_box.setAlignment(QtCore.Qt.AlignCenter)
        self.tab1_vertical_layout = QtWidgets.QVBoxLayout(self.tab1_group_box)
        self.number_traces_label = QtWidgets.QLabel(self.tab1_group_box)

        self.tab1_vertical_layout.addWidget(self.number_traces_label)
        self.number_traces_data = QtWidgets.QLineEdit(self.tab1_group_box)
        self.number_traces_data.setStyleSheet('color: white;')
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.number_traces_data.sizePolicy().hasHeightForWidth())
        self.number_traces_data.setSizePolicy(sizePolicy)
        self.number_traces_data.setMaximumSize(QtCore.QSize(16777215, 16777215))
        
        self.number_traces_data.setValidator(self.is_number_validator)
        self.tab1_vertical_layout.addWidget(self.number_traces_data)
        self.number_points_label = QtWidgets.QLabel(self.tab1_group_box)

        self.tab1_vertical_layout.addWidget(self.number_points_label)
        self.number_points_data = QtWidgets.QLineEdit(self.tab1_group_box)
        self.number_points_data.setStyleSheet('color: white;')
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.number_points_data.sizePolicy().hasHeightForWidth())
        self.number_points_data.setSizePolicy(sizePolicy)
        self.number_points_data.setMaximumSize(QtCore.QSize(16777215, 16777215))
        self.number_points_data.setInputMethodHints(QtCore.Qt.ImhDigitsOnly)
        self.number_points_data.setValidator(self.is_number_validator)
        self.tab1_vertical_layout.addWidget(self.number_points_data)
        self.scope_offset_label = QtWidgets.QLabel(self.tab1_group_box)
        self.tab1_vertical_layout.addWidget(self.scope_offset_label)
        self.scope_offset_data = QtWidgets.QLineEdit(self.tab1_group_box)
        self.scope_offset_data.setStyleSheet('color: white;')
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.scope_offset_data.sizePolicy().hasHeightForWidth())
        self.scope_offset_data.setSizePolicy(sizePolicy)
        self.scope_offset_data.setMaximumSize(QtCore.QSize(16777215, 16777215))
        
        self.scope_offset_data.setValidator(self.is_number_validator)
        self.tab1_vertical_layout.addWidget(self.scope_offset_data)
        self.scope_trigger_label = QtWidgets.QLabel(self.tab1_group_box)

        self.tab1_vertical_layout.addWidget(self.scope_trigger_label)
        self.scope_trigger_options = QtWidgets.QComboBox(self.tab1_group_box)
        self.scope_trigger_options.setStyleSheet('color: white;')
        self.scope_trigger_options.setIconSize(QtCore.QSize(16, 16))
        self.scope_trigger_options.addItem("Rx")
        self.scope_trigger_options.addItem("Tx")
        self.scope_trigger_options.addItem("GPIO 4")
        self.tab1_vertical_layout.addWidget(self.scope_trigger_options)

        self.key_len_label = QtWidgets.QLabel(self.tab1_group_box)

        self.tab1_vertical_layout.addWidget(self.key_len_label)
        self.key_len_options = QtWidgets.QComboBox(self.tab1_group_box)
        self.key_len_options.setStyleSheet('color: white;')
        self.key_len_options.setIconSize(QtCore.QSize(16, 16))
        self.key_len_options.addItem("128")
        self.key_len_options.addItem("256")
        self.tab1_vertical_layout.addWidget(self.key_len_options)
        self.plaintext_options_label = QtWidgets.QLabel(self.tab1_group_box)

        self.tab1_vertical_layout.addWidget(self.plaintext_options_label)
        self.plaintext_options = QtWidgets.QComboBox(self.tab1_group_box)
        self.plaintext_options.activated[str].connect(self.change_plaintext_options)
        self.plaintext_options.setStyleSheet('color: white;')
        self.plaintext_options.setIconSize(QtCore.QSize(16, 16))
        self.plaintext_options.addItem("Random")
        self.plaintext_options.addItem("Provided")
        self.tab1_vertical_layout.addWidget(self.plaintext_options)

        self.capture_traces_button = QtWidgets.QPushButton(self.tab1_group_box)
        self.capture_traces_button.setStyleSheet('background-color : #454548; color: white')

        self.capture_traces_button.setGeometry(QtCore.QRect(28, 400, 50, 25))
        self.capture_traces_button.clicked.connect(self.capture_traces)
        self.tab1_vertical_layout.addWidget(self.capture_traces_button)
        #
        
        #tab2
        self.tab2 = QtWidgets.QWidget()
        self.tab_widget.addTab(self.tab2, "Load Project")
        #tab2 load proj label
        self.tab2_load_proj_label = QtWidgets.QLabel(self.tab2)
        self.tab2_load_proj_label.setGeometry(QtCore.QRect(10, 50, 50, 25))
        #tab2 load proj textedit
        self.tab2_load_proj_textbox = QtWidgets.QTextBrowser(self.tab2)
        self.tab2_load_proj_textbox.setStyleSheet('color: white;')
        self.tab2_load_proj_textbox.setGeometry(QtCore.QRect(55, 50, 170, 25))
        self.tab2_load_proj_textbox.setWordWrapMode(QtGui.QTextOption.NoWrap)
        self.tab2_load_proj_textbox.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        #tab2 load proj button
        self.tab2_load_proj_button = QtWidgets.QPushButton(self.tab2)
        self.tab2_load_proj_button.setStyleSheet('background-color : #454548;color: white;')
        self.tab2_load_proj_button.setGeometry(QtCore.QRect(235, 50, 50, 25))
        self.tab2_load_proj_button.clicked.connect(self.set_project_path)
        #tab2 choose model label
        self.tab2_encryption_model_label = QtWidgets.QLabel(self.tab2)
        self.tab2_encryption_model_label.setGeometry(QtCore.QRect(10, 95, 100, 25))
        #tab2 choose model options
        self.tab2_encryption_model_options = QtWidgets.QComboBox(self.tab2)
        self.tab2_encryption_model_options.setStyleSheet('color: white;')
        self.tab2_encryption_model_options.setGeometry(QtCore.QRect(120, 95, 70, 25))
        self.tab2_encryption_model_options.setIconSize(QtCore.QSize(16, 16))
        self.tab2_encryption_model_options.addItem("ECB")
        self.tab2_encryption_model_options.addItem("CBC")
        self.tab2_encryption_model_options.addItem("CFB")
        self.tab2_encryption_model_options.addItem("OFB")
        self.tab2_encryption_model_options.addItem("CTR")
        self.tab2_encryption_model_options.setCurrentIndex(-1) # define default option
        self.tab2_encryption_model_options.activated[str].connect(self.set_project_model)
        #radio buttons for circumventing countermeasures 
        self.resync_button_group = QtWidgets.QButtonGroup(self.tab2)
        self.resync_button_group.setExclusive(False) #
        self.resync_button_group.buttonClicked.connect(self.resync_status_update)

        self.sad_resync_button = QtWidgets.QRadioButton(self.tab2)
        self.sad_resync_button.setStyleSheet('color: white;')
        self.sad_resync_button.setGeometry(QtCore.QRect(25, 140, 150, 40))
        self.sad_resync_button.clicked.connect(self.pressed_sad_button)
        self.resync_button_group.addButton(self.sad_resync_button)
        self.sad_tooltip_label = QtWidgets.QLabel(self.tab2)
        self.sad_tooltip_label.setFont(QtGui.QFont('Arial', 15))
        self.sad_tooltip_label.setGeometry(QtCore.QRect(120, 140, 150, 40))
        
        
        self.sad_resync_window_label = QtWidgets.QLabel(self.tab2)
        self.sad_resync_window_label.setGeometry(QtCore.QRect(20, 180, 80, 25))
        
        self.sad_resync_max_shift_label = QtWidgets.QLabel(self.tab2)
        self.sad_resync_max_shift_label.setGeometry(QtCore.QRect(20, 220, 80, 25))
        

        self.sad_resync_window_min_data = QtWidgets.QLineEdit(self.tab2)
        self.sad_resync_window_min_data.setStyleSheet('color: white;')
        self.sad_resync_window_min_data.setValidator(self.is_number_validator)
        self.sad_resync_window_min_data.setGeometry(QtCore.QRect(100, 180, 50, 20))
        self.sad_resync_window_min_data.textChanged.connect(self.update_resync_data)

        self.sad_resync_window_max_data = QtWidgets.QLineEdit(self.tab2)
        self.sad_resync_window_max_data.setStyleSheet('color: white;')
        self.sad_resync_window_max_data.setValidator(self.is_number_validator)
        self.sad_resync_window_max_data.setGeometry(QtCore.QRect(160, 180, 50, 20))
        self.sad_resync_window_max_data.textChanged.connect(self.update_resync_data)

        self.sad_resync_max_shift_data = QtWidgets.QLineEdit(self.tab2)
        self.sad_resync_max_shift_data.setStyleSheet('color: white;')
        self.sad_resync_max_shift_data.setValidator(self.is_number_validator)
        self.sad_resync_max_shift_data.setGeometry(QtCore.QRect(100, 220, 50, 20))
        self.sad_resync_max_shift_data.textChanged.connect(self.update_resync_data)


        self.dtw_resync_button = QtWidgets.QRadioButton(self.tab2)
        self.dtw_resync_button.setStyleSheet('color: white;')
        self.dtw_resync_button.setGeometry(QtCore.QRect(25, 270, 150, 40))
        self.dtw_tooltip_label = QtWidgets.QLabel(self.tab2)
        self.dtw_tooltip_label.setFont(QtGui.QFont('Arial', 15))
        self.dtw_tooltip_label.setGeometry(QtCore.QRect(120, 270, 150, 40))
        
        self.resync_button_group.addButton(self.dtw_resync_button)
        self.dtw_resync_radius_label = QtWidgets.QLabel(self.tab2)
        self.dtw_resync_radius_label.setGeometry(QtCore.QRect(20, 310, 80, 20))
        
        self.dtw_resync_radius_data = QtWidgets.QLineEdit(self.tab2)
        self.dtw_resync_radius_data.setStyleSheet('color: white;')
        self.dtw_resync_radius_data.textChanged.connect(self.update_resync_data)
        self.dtw_resync_radius_data.setValidator(self.is_number_validator)
        self.dtw_resync_radius_data.setGeometry(QtCore.QRect(100, 310, 50, 25))
        self.dtw_resync_radius_data.textChanged.connect(self.update_resync_data)
        #tab2 export plaintext and ciphertext button
        self.tab2_export_ptct_button = QtWidgets.QPushButton(self.tab2)
        self.tab2_export_ptct_button.setStyleSheet('background-color : #454548;color: white;')
        self.tab2_export_ptct_button.setGeometry(QtCore.QRect(75, 370, 150, 40))
        self.tab2_export_ptct_button.clicked.connect(self.export_ptct)
        #


        #use default key checkbox
        self.use_default_key_checkbox = QtWidgets.QCheckBox(self)
        self.use_default_key_checkbox.move(380,510)
        self.use_default_key_checkbox.clicked.connect(self.set_default_key)
        self.use_default_key_label = QtWidgets.QLabel(self)
        self.use_default_key_label.move(400, 510)
        #start analysis button 
        self.start_analysis_button = QtWidgets.QPushButton(self)
        self.start_analysis_button.setStyleSheet("background-color : #FFA500;")
        self.start_analysis_button.move(695,510)
        self.start_analysis_button.clicked.connect(self.start_analysis)
        #analysis status label
        self.analysis_status_label = QtWidgets.QLabel(self)
        self.analysis_status_label.move(970, 520)
        self.analysis_status_label.setFixedWidth(200)
        #table data tooltip
        self.table_tooltip_label = QtWidgets.QLabel(self)
        self.table_tooltip_label.setFont(QtGui.QFont('Arial', 20))
        self.table_tooltip_label.move(800, 505)       


        #textbrowser for current project
        self.current_project_info_group_box = QtWidgets.QGroupBox(self)
        self.current_project_info_group_box.setAlignment(QtCore.Qt.AlignCenter)
        self.current_project_info_group_box.setStyleSheet('color: white;')
        self.current_project_info_group_box.setTitle('Current Project Settings')
        self.current_project_info_group_box.setGeometry(QtCore.QRect(15, 550, 300, 250))
        self.current_project_info = QtWidgets.QTextBrowser(self.current_project_info_group_box)
        self.current_project_info.setStyleSheet('border-width: 0px; border-style: solid; color: white;')
        self.current_project_info.setGeometry(QtCore.QRect(15, 15, 270, 220))

        self.plot_trace_button = QtWidgets.QPushButton(self)
        self.plot_trace_button.setStyleSheet('color: white;')
        self.plot_trace_button.setGeometry(90, 810, 150, 40)
        self.plot_trace_button.clicked.connect(self.plot_trace)
        self.plot_trace_button.setStyleSheet("background-color : #FFA500")

        self.help_button = QtWidgets.QPushButton(self)
        self.help_button.setText("Help")
        self.help_button.setGeometry(QtCore.QRect(1145, 5, 50, 25))
        self.help_button.clicked.connect(self.help_subwindow.show)

        self.setTexts()
        QtCore.QMetaObject.connectSlotsByName(self)

    def setTexts(self):
        self.setWindowTitle("Power Analysis Tool")
        self.start_analysis_button.setText('Start Analysis')
        ### Tab 1
        self.tab1_group_box.setTitle('General Settings')
        self.number_traces_label.setText('<font color="white">Number of Traces')
        self.number_traces_data.setText('1000')
        self.number_points_label.setText('<font color="white">Number of points')
        self.number_points_data.setText('1000')
        self.scope_offset_label.setText('<font color="white">Scope offset')
        self.scope_offset_data.setText('0')
        self.scope_trigger_label.setText('<font color="white">Scope Trigger')
        self.key_len_label.setText('<font color="white">Key Length')
        self.plaintext_options_label.setText('<font color="white">Plaintext')
        self.capture_traces_button.setText('Capture Traces')
        ### Tab 2
        self.tab2_load_proj_label.setText('<font color="white">Project: ')
        self.tab2_load_proj_button.setText('Choose')
        self.tab2_encryption_model_label.setText('<font color="white">Encryption Model: ')
        self.tab2_export_ptct_button.setText('Export Plaintext/CipherText')
        self.sad_resync_button.setText('SAD resync')
        #self.sad_tooltip_label.setText('<font color="white">\U0001F6C8')
        #self.sad_tooltip_label.setToolTip('Resynchronizing Traces with Sum of Absolute Difference')
        self.sad_resync_window_label.setText('<font color="white">SAD window')
        self.sad_resync_max_shift_label.setText('<font color="white">SAD max shift')
        self.sad_resync_window_min_data.setText(str(self.default_sad_resync_window_min_value))
        self.sad_resync_window_max_data.setText(str(self.default_sad_resync_window_max_value))
        self.sad_resync_max_shift_data.setText(str(self.default_sad_resync_max_shift_value))
        self.dtw_resync_button.setText('DTW resync')
        #self.dtw_tooltip_label.setText('<font color="white">\U0001F6C8')
        #self.dtw_tooltip_label.setToolTip('Resynchronizing Traces with Dynamic Time Warp')
        self.dtw_resync_radius_label.setText('<font color="white">DTW radius')
        self.dtw_resync_radius_data.setText(str(self.default_dtw_resync_radius_value))
        ###proj info
        self.plot_trace_button.setText('Plot Random Trace')
        self.use_default_key_label.setText('<font color="white">Use default key')
        #self.use_default_key_label.setToolTip('File should be named "defaultkey.txt" and placed in the path of this App.\nThe bytes of the key should be written as integers and separated by spaces')
        #self.table_tooltip_label.setText('<font color="white">\U0001F6C8')
        #self.table_tooltip_label.setToolTip('Upper value indicates the Byte value in Hex\nLower value indicates the correlation value')


    def change_plaintext_options(self, text):
        if text == "Random":
            self.plaintext_option_data = None
            self.number_traces_data.setEnabled(True)
        else: # "Provided"
            try:
                default_key_filename = 'plaintext.txt'
                with open(default_key_filename, 'r') as f:
                    lines = f.readlines()
                    self.plaintext_option_data = []

                    for lineindex, line in enumerate(lines):
                        linedata_str = line.strip().split(" ")
                        linedata = []
                        
                        for value in linedata_str:
                            try:
                                value_ = int(value)
                                if value_ < 0 or value_ > 255:
                                    raise ValueError(f"Invalid input number: {value_}")
                                linedata.append(value_)
                            except ValueError as e:
                                self.popup_error(f"{str(e)} in line {lineindex+1}")
                                self.plaintext_option_data = None
                                return
                        self.plaintext_option_data.append(linedata)
                self.number_traces_data.setText(str(len(self.plaintext_option_data)))
                self.number_traces_data.setEnabled(False)
            except FileNotFoundError as e:
                self.popup_error(str(e))
            
            


    def pressed_sad_button(self):
        self.plot_trace(0)


    def center(self):
        qr = self.frameGeometry()
        cp = QtWidgets.QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

    def update_current_project_text(self):
        if self.current_proj:
            text1 = f"Current project path: {self.current_proj.get_filename()}"
            text2 = f"Number of traces: {len(self.current_proj.waves)}"
            text3 = f"Number of points in a trace: {len(self.current_proj.waves[0])}"
            text4 = f"Key length: {len(self.current_proj.keys[0])} bytes"
            txt = "\n\n".join([text1, text2, text3, text4])
            self.current_project_info.setText(txt)

    def set_default_key(self):
        if self.use_default_key_checkbox.isChecked():
            try:
                default_key_filename = 'defaultkey.txt'
                with open(default_key_filename, 'r') as f:
                    key_str = f.readline()
                    self.current_proj_key = [int(a) for a in key_str.split(" ")]
            except FileNotFoundError as e:
                self.popup_error(str(e))
        else:
            self.current_proj_key = None
        

    def set_project_path(self):
        filefilter = 'Project files (*.cwp)'
        response = QtWidgets.QFileDialog.getOpenFileName(parent=self, caption="captoin here", directory=os.getcwd(), filter = filefilter)
        proj_path = response[0]
        if proj_path:
            self.tab2_load_proj_textbox.setText(proj_path)
            self.current_proj = cw.open_project(proj_path)

            self.update_current_project_text()
        else:
            self.popup_error("Missing project path information")

    def set_project_model(self, model):
        self.current_analysis_model = get_leakage_model(model)  
        if self.current_analysis_model is None:
            self.popup_error("Missing encryption model information")


    def start_analysis(self):
        if self.current_proj and self.current_analysis_model:
            self.start_analysis_button.setEnabled(False)
            self.analysis_thread = QtCore.QThread()
            
            self.analysis_worker = Analysis(self.current_proj, self.current_analysis_model, self.sad_window_min_value, 
                                            self.sad_window_max_value,self.sad_max_shift_value,self.dtw_radius_value, self.current_proj_key)

            self.analysis_worker.apply_sad_resync_flag = self.sad_resync_button.isChecked()
            self.analysis_worker.apply_dtw_resync_flag = self.dtw_resync_button.isChecked()
            if self.tab2_encryption_model_options.currentText() == 'CTR':
                self.analysis_worker.key_from_round10 = True
            else:
                self.analysis_worker.key_from_round10 = False

            self.analysis_worker.moveToThread(self.analysis_thread)
            self.analysis_thread.started.connect(self.analysis_worker.run_analysis)
            self.analysis_worker.finished.connect(self.analysis_thread.quit)
            self.analysis_worker.finished.connect(self.stop_analysis)
            self.analysis_thread.finished.connect(self.analysis_thread.deleteLater)
            self.analysis_worker.updated_results_table.connect(self.update_table)
            self.analysis_worker.update_status_table.connect(self.update_table_label)
            self.analysis_thread.start()
        else:
            self.popup_error("Missing analysis information")

    def stop_analysis(self):
        self.analysis_worker.deleteLater()
        self.start_analysis_button.setEnabled(True)
        # reactivate button


    def update_table(self, data):
        self.table_view.setModel(PandasModel(data, self.current_proj_key))

    
    def update_table_label(self, data):
        self.analysis_status_label.setText(data)
    

    def plot_trace(self, traceindex=None):
        if self.current_proj is None:
            self.popup_error("Load a project first")
            return 
        
        if traceindex is False:
            traceindex = random.randint(0, len(self.current_proj.waves))

        wave = self.current_proj.waves[traceindex]
        self.plot_axe.clear()
        self.plot_axe.plot(wave)
        self.plot_axe.set_title("Power Trace View")
        self.plot_axe.set_xlabel("Samples")
        self.plot_axe.set_ylabel("Data")
        self.plot_canvas.draw()
        
    def export_ptct(self):
        if self.current_proj is None:
            self.popup_error("Load a project first")
            return 
        pt = list(self.current_proj.textins)
        np.savetxt("plaintext.txt", pt, fmt="%d")

        ct = list(self.current_proj.textouts)
        np.savetxt("ciphertext.txt", ct, fmt="%d")

    def update_resync_data(self):
        # if empty, fill with default values
        if not self.sad_resync_window_min_data.text():
            self.sad_resync_window_min_data.setText(str(self.default_sad_resync_window_min_value))
        if not self.sad_resync_window_max_data.text():
            self.sad_resync_window_max_data.setText(str(self.default_sad_resync_window_min_value))
        if not self.sad_resync_max_shift_data.text():
            self.sad_resync_max_shift_data.setText(str(self.default_sad_resync_window_min_value))
        if not self.dtw_resync_radius_data.text():
            self.dtw_resync_radius_data.setText(str(self.default_sad_resync_window_min_value))
        if int(self.sad_resync_window_max_data.text()) < int(self.sad_resync_window_min_data.text()):
            self.sad_resync_window_max_data.setText(str(int(self.sad_resync_window_min_data.text())+1))
        
        self.sad_window_min_value = int(self.sad_resync_window_min_data.text())
        self.sad_window_max_value = int(self.sad_resync_window_max_data.text())
        self.sad_max_shift_value = int(self.sad_resync_max_shift_data.text())
        self.dtw_radius_value = int(self.dtw_resync_radius_data.text())


    def resync_status_update(self, button):
        ## allow to uncheck radio button
        for btn in self.resync_button_group.buttons():
            if btn is not button:
                btn.setChecked(False)
        ##
        
    def popup_error(self, msg):
        popup_box = QtWidgets.QMessageBox()
        popup_box.setWindowTitle("Error")
        popup_box.setIcon(QtWidgets.QMessageBox.Critical)
        popup_box.setText(msg)
        x = popup_box.exec_()  # this will show our messagebox

        
    def capture_traces(self):
        target, scope = self.detect_chipwhisperer()
        if target is None and scope is None:
            return

        # to key in proj, set usekey=True
        self.current_proj = self.read_traces(scope, target)
        
        path = os.getcwd() + "\\current_project.cwp"

        self.set_project_path(path)

        self.exit_cw_connection(scope, target)

    
    def detect_chipwhisperer(self):
        while True:
            try:
                if not scope.connectStatus:
                    scope.con()
            except NameError:
                try:
                    scope = cw.scope()
                    break
                except:
                    self.popup_error("couldnt find ChipWhisperer, try again")
                    return None, None
                    
        try:
            if SS_VER == "SS_VER_2_1":
                target_type = cw.targets.SimpleSerial2
            elif SS_VER == "SS_VER_2_0":
                raise OSError("SS_VER_2_0 is deprecated. Use SS_VER_2_1")
            else:
                target_type = cw.targets.SimpleSerial
        except:
            SS_VER="SS_VER_1_1"
            target_type = cw.targets.SimpleSerial

        try:
            target = cw.target(scope, target_type)
        except:
            print("INFO: Caught exception on reconnecting to target - attempting to reconnect to scope first.")
            print("INFO: This is a work-around when USB has died without Python knowing. Ignore errors above this line.")
            scope = cw.scope()
            target = cw.target(scope, target_type)

        return target, scope
    
    def read_traces(self, scope, target, usekey=False):
          
        ktp = cw.ktp.Basic()

        proj = cw.create_project("current_project.cwp", overwrite=True)
        scope.adc.samples = int(self.number_points_data.text())
        scope.adc.offset = int(self.scope_offset_data.tex())

        trigg = self.get_trigger()
        if trigg is not None:
            scope.trigger.triggers = trigg

        N = int(self.number_traces_data.text())

        for i in range(N):

            key, text = ktp.next()
            if not usekey:
                key = None
            if self.plaintext_option_data is not None:
                text = self.plaintext_option_data[i]

            trace = cw.capture_trace(scope, target, text, key)
            if not trace:
                continue
    
            proj.traces.append(trace)
        proj.save()
        return proj


    def get_trigger(self):
        value = self.scope_trigger_options.currentText()
        if value == 'Rx':
            return 'tio1'
        if value == 'Tx':
            return 'tio2'
        return None


    def exit_cw_connection(self, scope, target):
        scope.dis()
        target.dis()

        

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    
    mw = MainWindow()

    sys.exit(app.exec_())