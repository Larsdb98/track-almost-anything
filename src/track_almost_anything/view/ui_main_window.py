# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'main_windowPOBUKI.ui'
##
## Created by: Qt User Interface Compiler version 6.8.0
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QAction, QBrush, QColor, QConicalGradient,
    QCursor, QFont, QFontDatabase, QGradient,
    QIcon, QImage, QKeySequence, QLinearGradient,
    QPainter, QPalette, QPixmap, QRadialGradient,
    QTransform)
from PySide6.QtWidgets import (QApplication, QCheckBox, QComboBox, QFrame,
    QGridLayout, QGroupBox, QHBoxLayout, QHeaderView,
    QLabel, QMainWindow, QMenu, QMenuBar,
    QPushButton, QScrollArea, QSizePolicy, QSlider,
    QSpacerItem, QSpinBox, QTabWidget, QTableView,
    QVBoxLayout, QWidget)

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.setEnabled(True)
        MainWindow.resize(1421, 1058)
        MainWindow.setMouseTracking(False)
        MainWindow.setStyleSheet(u"\n"
"/*-----QWidget-----*/\n"
"QWidget\n"
"{\n"
"	background-color: #232430;\n"
"	color: #000000;\n"
"	border-color: #000000;\n"
"\n"
"}\n"
"\n"
"\n"
"/*-----QLabel-----*/\n"
"QLabel\n"
"{\n"
"	/*background-color: #232430;*/\n"
"	background-color: transparent;\n"
"	color: #c1c1c1;\n"
"	/*border-color: #000000;*/\n"
"\n"
"}\n"
"\n"
"/*------QMenuBar------*/\n"
"\n"
"QMenuBar\n"
"{\n"
"	color: #ffffff;\n"
"}\n"
"\n"
"/*------QSlider-------*/\n"
"QSlider\n"
"{\n"
"	background-color: #2d2d37;\n"
"}\n"
"\n"
"\n"
"/*-----QCheckBox------*/\n"
"QCheckBox\n"
"{\n"
"	color: #c1c1c1;\n"
"	background-color: #2d2d37;\n"
"}\n"
"\n"
"/*------QComboBox-------*/\n"
"QComboBox\n"
"{\n"
"	background-color: #2d2d37;\n"
"	color: #c1c1c1;\n"
"}\n"
"\n"
"/*-------QSpinBox-------*/\n"
"QSpinBox\n"
"{\n"
"	color: #c1c1c1;\n"
"}\n"
"\n"
"\n"
"/*-----QPushButton-----*/\n"
"QPushButton\n"
"{\n"
"	background-color: #ff9c2b;\n"
"	color: #000000;\n"
"	font-weight: bold;\n"
"	border-style: solid;\n"
"	border-color: #000000;\n"
"	padding: 6px"
                        ";\n"
"\n"
"}\n"
"\n"
"\n"
"QPushButton::hover\n"
"{\n"
"	background-color: #ffaf5d;\n"
"\n"
"}\n"
"\n"
"\n"
"QPushButton::pressed\n"
"{\n"
"	background-color: #dd872f;\n"
"\n"
"}\n"
"\n"
"\n"
"/*-----QToolButton-----*/\n"
"QToolButton\n"
"{\n"
"	background-color: #ff9c2b;\n"
"	color: #000000;\n"
"	font-weight: bold;\n"
"	border-style: solid;\n"
"	border-color: #000000;\n"
"	padding: 6px;\n"
"\n"
"}\n"
"\n"
"\n"
"QToolButton::hover\n"
"{\n"
"	background-color: #ffaf5d;\n"
"\n"
"}\n"
"\n"
"\n"
"QToolButton::pressed\n"
"{\n"
"	background-color: #dd872f;\n"
"\n"
"}\n"
"\n"
"\n"
"/*-----QLineEdit-----*/\n"
"QLineEdit\n"
"{\n"
"	background-color: #38394e;\n"
"	color: #c1c1c1;\n"
"	border-style: solid;\n"
"	border-width: 1px;\n"
"	border-color: #4a4c68;\n"
"\n"
"}\n"
"\n"
"\n"
"/*-----QTableView-----*/\n"
"QTableView, \n"
"QHeaderView, \n"
"QTableView::item \n"
"{\n"
"	background-color: #232430;\n"
"	color: #c1c1c1;\n"
"	border: none;\n"
"\n"
"}\n"
"\n"
"\n"
"QTableView::item:selected \n"
"{ \n"
"    background-color"
                        ": #41424e;\n"
"    color: #c1c1c1;\n"
"\n"
"}\n"
"\n"
"\n"
"QHeaderView::section:horizontal \n"
"{\n"
"    background-color: #232430;\n"
"	border: 1px solid #37384d;\n"
"	padding: 5px;\n"
"\n"
"}\n"
"\n"
"\n"
"QTableView::indicator{\n"
"	background-color: #1d1d28;\n"
"	border: 1px solid #37384d;\n"
"\n"
"}\n"
"\n"
"\n"
"QTableView::indicator:checked{\n"
"	/*image:url(\"./ressources/check.png\"); /*To replace*/\n"
"	background-color: #1d1d28;\n"
"\n"
"}\n"
"\n"
"/*-----QTabWidget-----*/\n"
"QTabWidget::pane \n"
"{ \n"
"    border: none;\n"
"\n"
"}\n"
"\n"
"\n"
"QTabWidget::tab-bar \n"
"{\n"
"    left: 5px; \n"
"\n"
"}\n"
"\n"
"\n"
"QTabBar::tab \n"
"{\n"
"    color: #c1c1c1;\n"
"    min-width: 1px;\n"
"	padding: 5px;\n"
"    height: 28px;\n"
"	border: none;\n"
"\n"
"}\n"
"\n"
"\n"
"QTabBar::tab:selected \n"
"{\n"
"    color: #000000;\n"
"	font-weight: bold;\n"
"    height: 28px;\n"
"\n"
"	background-color: #ff9c2b;\n"
"	border-style: solid;\n"
"	border-width: 1px;\n"
"	border-color: #000000;\n"
"	border-top-lef"
                        "t-radius: 3px;\n"
"	border-top-right-radius: 3px;\n"
"	padding: 2px;\n"
"\n"
"}\n"
"\n"
"\n"
"\n"
"QTabBar::tab:!selected \n"
"{\n"
"    color: #c1c1c1;\n"
"	font-weight: bold;\n"
"    height: 28px;\n"
"\n"
"	background-color: #2d2d37; /*38394e*/\n"
"	border-style: solid;\n"
"	border-color: #3e3e48;\n"
"	border-width: 1px;\n"
"	border-top-left-radius: 3px;\n"
"	border-top-right-radius: 3px;\n"
"	padding: 2px\n"
"\n"
"}\n"
"\n"
"QTabBar::tab:top, QTabBar::tab:bottom \n"
"{\n"
"    min-width: 8ex;\n"
"    margin-right: -1px;\n"
"    padding: 1px 10px 1px 10px;\n"
"\n"
"}\n"
"\n"
"\n"
"QTabBar::tab:hover \n"
"{\n"
"    color: #DDD;\n"
"	background-color: #454545;\n"
"\n"
"}\n"
"\n"
"QTabBar::tab:selected:hover\n"
"{\n"
"	color: #000000;\n"
"	background-color: #ffaf5d;\n"
"}\n"
"\n"
"\n"
"/*-----QScrollBar-----*/\n"
"QScrollBar:horizontal \n"
"{\n"
"    background-color: transparent;\n"
"    height: 8px;\n"
"    margin: 0px;\n"
"    padding: 0px;\n"
"\n"
"}\n"
"\n"
"\n"
"QScrollBar::handle:horizontal \n"
"{\n"
"  "
                        "  border: none;\n"
"	min-width: 100px;\n"
"    background-color: #56576c;\n"
"\n"
"}\n"
"\n"
"\n"
"QScrollBar::add-line:horizontal, \n"
"QScrollBar::sub-line:horizontal,\n"
"QScrollBar::add-page:horizontal, \n"
"QScrollBar::sub-page:horizontal \n"
"{\n"
"    width: 0px;\n"
"    background-color: transparent;\n"
"\n"
"}\n"
"\n"
"\n"
"QScrollBar:vertical \n"
"{\n"
"    background-color: transparent;\n"
"    width: 8px;\n"
"    margin: 0;\n"
"\n"
"}\n"
"\n"
"\n"
"QScrollBar::handle:vertical \n"
"{\n"
"    border: none;\n"
"	min-height: 100px;\n"
"    background-color: #56576c;\n"
"\n"
"}\n"
"\n"
"\n"
"QScrollBar::add-line:vertical, \n"
"QScrollBar::sub-line:vertical,\n"
"QScrollBar::add-page:vertical, \n"
"QScrollBar::sub-page:vertical \n"
"{\n"
"    height: 0px;\n"
"    background-color: transparent;\n"
"\n"
"}\n"
"")
        self.action_save = QAction(MainWindow)
        self.action_save.setObjectName(u"action_save")
        self.action_save_as = QAction(MainWindow)
        self.action_save_as.setObjectName(u"action_save_as")
        self.action_quit = QAction(MainWindow)
        self.action_quit.setObjectName(u"action_quit")
        self.global_widget = QWidget(MainWindow)
        self.global_widget.setObjectName(u"global_widget")
        self.verticalLayout_3 = QVBoxLayout(self.global_widget)
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.tool_widget = QWidget(self.global_widget)
        self.tool_widget.setObjectName(u"tool_widget")
        self.tool_widget.setMinimumSize(QSize(0, 40))
        self.tool_widget.setMaximumSize(QSize(16777215, 40))
        self.horizontalLayout_2 = QHBoxLayout(self.tool_widget)
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.horizontalLayout_2.setContentsMargins(12, 0, -1, 0)
        self.label_source = QLabel(self.tool_widget)
        self.label_source.setObjectName(u"label_source")

        self.horizontalLayout_2.addWidget(self.label_source)

        self.comboBox_image_source = QComboBox(self.tool_widget)
        self.comboBox_image_source.setObjectName(u"comboBox_image_source")
        self.comboBox_image_source.setMinimumSize(QSize(200, 0))

        self.horizontalLayout_2.addWidget(self.comboBox_image_source)

        self.button_start = QPushButton(self.tool_widget)
        self.button_start.setObjectName(u"button_start")

        self.horizontalLayout_2.addWidget(self.button_start)

        self.button_pause = QPushButton(self.tool_widget)
        self.button_pause.setObjectName(u"button_pause")

        self.horizontalLayout_2.addWidget(self.button_pause)

        self.button_stop = QPushButton(self.tool_widget)
        self.button_stop.setObjectName(u"button_stop")

        self.horizontalLayout_2.addWidget(self.button_stop)

        self.button_load_video = QPushButton(self.tool_widget)
        self.button_load_video.setObjectName(u"button_load_video")

        self.horizontalLayout_2.addWidget(self.button_load_video)

        self.horizontalSpacer = QSpacerItem(776, 13, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_2.addItem(self.horizontalSpacer)


        self.verticalLayout_3.addWidget(self.tool_widget)

        self.line_2 = QFrame(self.global_widget)
        self.line_2.setObjectName(u"line_2")
        self.line_2.setFrameShape(QFrame.Shape.HLine)
        self.line_2.setFrameShadow(QFrame.Shadow.Sunken)

        self.verticalLayout_3.addWidget(self.line_2)

        self.tab_widget = QTabWidget(self.global_widget)
        self.tab_widget.setObjectName(u"tab_widget")
        self.tab_widget.setFocusPolicy(Qt.FocusPolicy.TabFocus)
        self.tab_widget.setContextMenuPolicy(Qt.ContextMenuPolicy.DefaultContextMenu)
        self.tab_widget.setTabPosition(QTabWidget.TabPosition.North)
        self.tab_widget.setTabShape(QTabWidget.TabShape.Rounded)
        self.tab_widget.setIconSize(QSize(16, 16))
        self.tab_widget.setElideMode(Qt.TextElideMode.ElideLeft)
        self.tab_widget.setUsesScrollButtons(False)
        self.tab_widget.setDocumentMode(False)
        self.tab_widget.setTabsClosable(False)
        self.tab_widget.setMovable(True)
        self.tab_widget.setTabBarAutoHide(False)
        self.tab_detection_tracking = QWidget()
        self.tab_detection_tracking.setObjectName(u"tab_detection_tracking")
        self.tab_detection_tracking.setMouseTracking(False)
        self.tab_detection_tracking.setAcceptDrops(False)
        self.horizontalLayout = QHBoxLayout(self.tab_detection_tracking)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.scroll_detection_options = QScrollArea(self.tab_detection_tracking)
        self.scroll_detection_options.setObjectName(u"scroll_detection_options")
        self.scroll_detection_options.setMinimumSize(QSize(300, 0))
        self.scroll_detection_options.setMaximumSize(QSize(300, 16777215))
        self.scroll_detection_options.setStyleSheet(u"")
        self.scroll_detection_options.setWidgetResizable(True)
        self.scroll_area_widget_contents = QWidget()
        self.scroll_area_widget_contents.setObjectName(u"scroll_area_widget_contents")
        self.scroll_area_widget_contents.setGeometry(QRect(0, 0, 293, 926))
        self.verticalLayout = QVBoxLayout(self.scroll_area_widget_contents)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.groupBox_detection_options = QGroupBox(self.scroll_area_widget_contents)
        self.groupBox_detection_options.setObjectName(u"groupBox_detection_options")
        self.groupBox_detection_options.setStyleSheet(u"")
        self.verticalLayout_5 = QVBoxLayout(self.groupBox_detection_options)
        self.verticalLayout_5.setObjectName(u"verticalLayout_5")
        self.verticalLayout_5.setContentsMargins(0, 0, 0, 0)
        self.label_detection_options = QLabel(self.groupBox_detection_options)
        self.label_detection_options.setObjectName(u"label_detection_options")
        self.label_detection_options.setMinimumSize(QSize(0, 40))
        self.label_detection_options.setMaximumSize(QSize(16777215, 40))

        self.verticalLayout_5.addWidget(self.label_detection_options)

        self.label_detection_algo = QLabel(self.groupBox_detection_options)
        self.label_detection_algo.setObjectName(u"label_detection_algo")
        self.label_detection_algo.setMaximumSize(QSize(16777215, 25))

        self.verticalLayout_5.addWidget(self.label_detection_algo)

        self.combo_detection_algo = QComboBox(self.groupBox_detection_options)
        self.combo_detection_algo.setObjectName(u"combo_detection_algo")

        self.verticalLayout_5.addWidget(self.combo_detection_algo)

        self.label_model_type = QLabel(self.groupBox_detection_options)
        self.label_model_type.setObjectName(u"label_model_type")

        self.verticalLayout_5.addWidget(self.label_model_type)

        self.combo_model_type = QComboBox(self.groupBox_detection_options)
        self.combo_model_type.setObjectName(u"combo_model_type")

        self.verticalLayout_5.addWidget(self.combo_model_type)

        self.groupBox_items_to_detect = QGroupBox(self.groupBox_detection_options)
        self.groupBox_items_to_detect.setObjectName(u"groupBox_items_to_detect")
        self.groupBox_items_to_detect.setMinimumSize(QSize(0, 80))
        self.groupBox_items_to_detect.setMaximumSize(QSize(16777215, 50))
        self.gridLayout = QGridLayout(self.groupBox_items_to_detect)
        self.gridLayout.setObjectName(u"gridLayout")
        self.gridLayout.setContentsMargins(12, 6, 12, 12)
        self.button_none = QPushButton(self.groupBox_items_to_detect)
        self.button_none.setObjectName(u"button_none")

        self.gridLayout.addWidget(self.button_none, 2, 2, 1, 1)

        self.button_all = QPushButton(self.groupBox_items_to_detect)
        self.button_all.setObjectName(u"button_all")

        self.gridLayout.addWidget(self.button_all, 2, 1, 1, 1)

        self.label_items_to_detect = QLabel(self.groupBox_items_to_detect)
        self.label_items_to_detect.setObjectName(u"label_items_to_detect")
        self.label_items_to_detect.setMinimumSize(QSize(0, 15))

        self.gridLayout.addWidget(self.label_items_to_detect, 1, 1, 1, 1)


        self.verticalLayout_5.addWidget(self.groupBox_items_to_detect)

        self.table_view_all_detectables = QTableView(self.groupBox_detection_options)
        self.table_view_all_detectables.setObjectName(u"table_view_all_detectables")
        self.table_view_all_detectables.setMinimumSize(QSize(0, 100))
        self.table_view_all_detectables.setMaximumSize(QSize(16777215, 150))

        self.verticalLayout_5.addWidget(self.table_view_all_detectables)

        self.active_detection_items_controller = QGroupBox(self.groupBox_detection_options)
        self.active_detection_items_controller.setObjectName(u"active_detection_items_controller")
        self.active_detection_items_controller.setMinimumSize(QSize(0, 55))
        self.active_detection_items_controller.setMaximumSize(QSize(16777215, 55))
        self.horizontalLayout_3 = QHBoxLayout(self.active_detection_items_controller)
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.button_move_to_active = QPushButton(self.active_detection_items_controller)
        self.button_move_to_active.setObjectName(u"button_move_to_active")

        self.horizontalLayout_3.addWidget(self.button_move_to_active)

        self.button_remove_active = QPushButton(self.active_detection_items_controller)
        self.button_remove_active.setObjectName(u"button_remove_active")

        self.horizontalLayout_3.addWidget(self.button_remove_active)


        self.verticalLayout_5.addWidget(self.active_detection_items_controller)

        self.label_active_detection_items = QLabel(self.groupBox_detection_options)
        self.label_active_detection_items.setObjectName(u"label_active_detection_items")
        self.label_active_detection_items.setMinimumSize(QSize(0, 15))
        self.label_active_detection_items.setMaximumSize(QSize(16777215, 15))

        self.verticalLayout_5.addWidget(self.label_active_detection_items)

        self.table_view_active_detections = QTableView(self.groupBox_detection_options)
        self.table_view_active_detections.setObjectName(u"table_view_active_detections")
        self.table_view_active_detections.setMinimumSize(QSize(0, 100))
        self.table_view_active_detections.setMaximumSize(QSize(16777215, 150))

        self.verticalLayout_5.addWidget(self.table_view_active_detections)

        self.groupBox_detection_confidence = QGroupBox(self.groupBox_detection_options)
        self.groupBox_detection_confidence.setObjectName(u"groupBox_detection_confidence")
        self.groupBox_detection_confidence.setMinimumSize(QSize(0, 70))
        self.groupBox_detection_confidence.setMaximumSize(QSize(16777215, 65))
        self.gridLayout_2 = QGridLayout(self.groupBox_detection_confidence)
        self.gridLayout_2.setObjectName(u"gridLayout_2")
        self.label_detection_confidence = QLabel(self.groupBox_detection_confidence)
        self.label_detection_confidence.setObjectName(u"label_detection_confidence")

        self.gridLayout_2.addWidget(self.label_detection_confidence, 0, 0, 1, 1)

        self.slider_detection_confidence = QSlider(self.groupBox_detection_confidence)
        self.slider_detection_confidence.setObjectName(u"slider_detection_confidence")
        self.slider_detection_confidence.setMinimumSize(QSize(0, 30))
        self.slider_detection_confidence.setMaximumSize(QSize(16777215, 40))
        self.slider_detection_confidence.setOrientation(Qt.Orientation.Horizontal)

        self.gridLayout_2.addWidget(self.slider_detection_confidence, 1, 0, 1, 2)

        self.label_value_detection_confidence = QLabel(self.groupBox_detection_confidence)
        self.label_value_detection_confidence.setObjectName(u"label_value_detection_confidence")

        self.gridLayout_2.addWidget(self.label_value_detection_confidence, 0, 1, 1, 1)


        self.verticalLayout_5.addWidget(self.groupBox_detection_confidence)

        self.groupBox_number_of_objects = QGroupBox(self.groupBox_detection_options)
        self.groupBox_number_of_objects.setObjectName(u"groupBox_number_of_objects")
        self.groupBox_number_of_objects.setMinimumSize(QSize(0, 42))
        self.horizontalLayout_6 = QHBoxLayout(self.groupBox_number_of_objects)
        self.horizontalLayout_6.setObjectName(u"horizontalLayout_6")
        self.horizontalLayout_6.setContentsMargins(6, 6, 6, 6)
        self.label_number_of_objects = QLabel(self.groupBox_number_of_objects)
        self.label_number_of_objects.setObjectName(u"label_number_of_objects")

        self.horizontalLayout_6.addWidget(self.label_number_of_objects)

        self.spinbox_number_of_objects = QSpinBox(self.groupBox_number_of_objects)
        self.spinbox_number_of_objects.setObjectName(u"spinbox_number_of_objects")

        self.horizontalLayout_6.addWidget(self.spinbox_number_of_objects)


        self.verticalLayout_5.addWidget(self.groupBox_number_of_objects)


        self.verticalLayout.addWidget(self.groupBox_detection_options)

        self.line = QFrame(self.scroll_area_widget_contents)
        self.line.setObjectName(u"line")
        self.line.setFrameShape(QFrame.Shape.HLine)
        self.line.setFrameShadow(QFrame.Shadow.Sunken)

        self.verticalLayout.addWidget(self.line)

        self.groupBox_tracking_options = QGroupBox(self.scroll_area_widget_contents)
        self.groupBox_tracking_options.setObjectName(u"groupBox_tracking_options")
        self.groupBox_tracking_options.setEnabled(True)
        self.groupBox_tracking_options.setMinimumSize(QSize(0, 155))
        self.groupBox_tracking_options.setMaximumSize(QSize(16777215, 16777215))
        self.verticalLayout_4 = QVBoxLayout(self.groupBox_tracking_options)
        self.verticalLayout_4.setObjectName(u"verticalLayout_4")
        self.label_tracking_options = QLabel(self.groupBox_tracking_options)
        self.label_tracking_options.setObjectName(u"label_tracking_options")
        self.label_tracking_options.setMinimumSize(QSize(0, 40))
        self.label_tracking_options.setMaximumSize(QSize(16777215, 40))

        self.verticalLayout_4.addWidget(self.label_tracking_options)

        self.checkbox_tracking_enabled = QCheckBox(self.groupBox_tracking_options)
        self.checkbox_tracking_enabled.setObjectName(u"checkbox_tracking_enabled")

        self.verticalLayout_4.addWidget(self.checkbox_tracking_enabled)

        self.groupBox_number_generations = QGroupBox(self.groupBox_tracking_options)
        self.groupBox_number_generations.setObjectName(u"groupBox_number_generations")
        self.groupBox_number_generations.setMinimumSize(QSize(0, 50))
        self.groupBox_number_generations.setMaximumSize(QSize(16777215, 50))
        self.horizontalLayout_4 = QHBoxLayout(self.groupBox_number_generations)
        self.horizontalLayout_4.setObjectName(u"horizontalLayout_4")
        self.horizontalLayout_4.setContentsMargins(0, 0, 0, 0)
        self.label_number_generations = QLabel(self.groupBox_number_generations)
        self.label_number_generations.setObjectName(u"label_number_generations")

        self.horizontalLayout_4.addWidget(self.label_number_generations)

        self.spinbox_number_generations = QSpinBox(self.groupBox_number_generations)
        self.spinbox_number_generations.setObjectName(u"spinbox_number_generations")
        self.spinbox_number_generations.setWrapping(False)
        self.spinbox_number_generations.setMaximum(29)
        self.spinbox_number_generations.setValue(5)

        self.horizontalLayout_4.addWidget(self.spinbox_number_generations)


        self.verticalLayout_4.addWidget(self.groupBox_number_generations)


        self.verticalLayout.addWidget(self.groupBox_tracking_options)

        self.verticalSpacer = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.verticalLayout.addItem(self.verticalSpacer)

        self.scroll_detection_options.setWidget(self.scroll_area_widget_contents)

        self.horizontalLayout.addWidget(self.scroll_detection_options)

        self.widget_view_video_feed = QWidget(self.tab_detection_tracking)
        self.widget_view_video_feed.setObjectName(u"widget_view_video_feed")
        self.verticalLayout_2 = QVBoxLayout(self.widget_view_video_feed)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.label_video_feed = QLabel(self.widget_view_video_feed)
        self.label_video_feed.setObjectName(u"label_video_feed")
        self.label_video_feed.setCursor(QCursor(Qt.CursorShape.CrossCursor))
        self.label_video_feed.setStyleSheet(u"background-color: rgb(15, 15, 15);")

        self.verticalLayout_2.addWidget(self.label_video_feed)

        self.widget_2 = QWidget(self.widget_view_video_feed)
        self.widget_2.setObjectName(u"widget_2")
        self.widget_2.setMaximumSize(QSize(16777215, 100))
        self.widget_2.setStyleSheet(u"background-color: rgb(95, 95, 95);")

        self.verticalLayout_2.addWidget(self.widget_2)


        self.horizontalLayout.addWidget(self.widget_view_video_feed)

        self.scrollArea = QScrollArea(self.tab_detection_tracking)
        self.scrollArea.setObjectName(u"scrollArea")
        self.scrollArea.setMinimumSize(QSize(300, 0))
        self.scrollArea.setMaximumSize(QSize(300, 16777215))
        self.scrollArea.setStyleSheet(u"/*background-color: rgb(95, 95, 95);*/")
        self.scrollArea.setWidgetResizable(True)
        self.scrollAreaWidgetContents = QWidget()
        self.scrollAreaWidgetContents.setObjectName(u"scrollAreaWidgetContents")
        self.scrollAreaWidgetContents.setGeometry(QRect(0, 0, 298, 878))
        self.verticalLayout_6 = QVBoxLayout(self.scrollAreaWidgetContents)
        self.verticalLayout_6.setObjectName(u"verticalLayout_6")
        self.groupBox_roi = QGroupBox(self.scrollAreaWidgetContents)
        self.groupBox_roi.setObjectName(u"groupBox_roi")
        self.groupBox_roi.setMinimumSize(QSize(0, 300))
        self.groupBox_roi.setMaximumSize(QSize(16777215, 300))
        self.verticalLayout_7 = QVBoxLayout(self.groupBox_roi)
        self.verticalLayout_7.setObjectName(u"verticalLayout_7")
        self.verticalLayout_7.setContentsMargins(0, 0, 0, 0)
        self.label_roi_title = QLabel(self.groupBox_roi)
        self.label_roi_title.setObjectName(u"label_roi_title")
        self.label_roi_title.setMinimumSize(QSize(0, 40))
        self.label_roi_title.setMaximumSize(QSize(16777215, 40))

        self.verticalLayout_7.addWidget(self.label_roi_title)

        self.label_roi_preview = QLabel(self.groupBox_roi)
        self.label_roi_preview.setObjectName(u"label_roi_preview")
        self.label_roi_preview.setStyleSheet(u"background-color: rgb(15, 15, 15);")

        self.verticalLayout_7.addWidget(self.label_roi_preview)

        self.groupBox_roi_control = QGroupBox(self.groupBox_roi)
        self.groupBox_roi_control.setObjectName(u"groupBox_roi_control")
        self.groupBox_roi_control.setMinimumSize(QSize(0, 55))
        self.groupBox_roi_control.setMaximumSize(QSize(16777215, 55))
        self.horizontalLayout_5 = QHBoxLayout(self.groupBox_roi_control)
        self.horizontalLayout_5.setObjectName(u"horizontalLayout_5")
        self.button_save_roi = QPushButton(self.groupBox_roi_control)
        self.button_save_roi.setObjectName(u"button_save_roi")

        self.horizontalLayout_5.addWidget(self.button_save_roi)

        self.button_clear_roi = QPushButton(self.groupBox_roi_control)
        self.button_clear_roi.setObjectName(u"button_clear_roi")
        self.button_clear_roi.setEnabled(False)

        self.horizontalLayout_5.addWidget(self.button_clear_roi)


        self.verticalLayout_7.addWidget(self.groupBox_roi_control)


        self.verticalLayout_6.addWidget(self.groupBox_roi)

        self.verticalSpacer_2 = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.verticalLayout_6.addItem(self.verticalSpacer_2)

        self.scrollArea.setWidget(self.scrollAreaWidgetContents)

        self.horizontalLayout.addWidget(self.scrollArea)

        self.tab_widget.addTab(self.tab_detection_tracking, "")
        self.tab_analysis = QWidget()
        self.tab_analysis.setObjectName(u"tab_analysis")
        self.tab_widget.addTab(self.tab_analysis, "")
        self.tab_settings = QWidget()
        self.tab_settings.setObjectName(u"tab_settings")
        self.tab_widget.addTab(self.tab_settings, "")
        self.tab_logs_reports = QWidget()
        self.tab_logs_reports.setObjectName(u"tab_logs_reports")
        self.tab_widget.addTab(self.tab_logs_reports, "")

        self.verticalLayout_3.addWidget(self.tab_widget)

        MainWindow.setCentralWidget(self.global_widget)
        self.menu_bar = QMenuBar(MainWindow)
        self.menu_bar.setObjectName(u"menu_bar")
        self.menu_bar.setGeometry(QRect(0, 0, 1421, 21))
        self.menu_file = QMenu(self.menu_bar)
        self.menu_file.setObjectName(u"menu_file")
        self.menu_edit = QMenu(self.menu_bar)
        self.menu_edit.setObjectName(u"menu_edit")
        self.menu_help = QMenu(self.menu_bar)
        self.menu_help.setObjectName(u"menu_help")
        self.menu_pesentation = QMenu(self.menu_bar)
        self.menu_pesentation.setObjectName(u"menu_pesentation")
        MainWindow.setMenuBar(self.menu_bar)
        QWidget.setTabOrder(self.tab_widget, self.comboBox_image_source)
        QWidget.setTabOrder(self.comboBox_image_source, self.button_start)
        QWidget.setTabOrder(self.button_start, self.button_pause)
        QWidget.setTabOrder(self.button_pause, self.button_stop)
        QWidget.setTabOrder(self.button_stop, self.button_load_video)
        QWidget.setTabOrder(self.button_load_video, self.scroll_detection_options)
        QWidget.setTabOrder(self.scroll_detection_options, self.button_all)
        QWidget.setTabOrder(self.button_all, self.button_none)
        QWidget.setTabOrder(self.button_none, self.button_move_to_active)
        QWidget.setTabOrder(self.button_move_to_active, self.button_remove_active)

        self.menu_bar.addAction(self.menu_file.menuAction())
        self.menu_bar.addAction(self.menu_edit.menuAction())
        self.menu_bar.addAction(self.menu_pesentation.menuAction())
        self.menu_bar.addAction(self.menu_help.menuAction())
        self.menu_file.addAction(self.action_save)
        self.menu_file.addAction(self.action_save_as)
        self.menu_file.addSeparator()
        self.menu_file.addAction(self.action_quit)

        self.retranslateUi(MainWindow)

        self.tab_widget.setCurrentIndex(0)


        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"Track Almost Anything", None))
        self.action_save.setText(QCoreApplication.translate("MainWindow", u"Save", None))
        self.action_save_as.setText(QCoreApplication.translate("MainWindow", u"Save As", None))
        self.action_quit.setText(QCoreApplication.translate("MainWindow", u"Quit", None))
        self.label_source.setText(QCoreApplication.translate("MainWindow", u"Source", None))
        self.button_start.setText(QCoreApplication.translate("MainWindow", u"Start", None))
        self.button_pause.setText(QCoreApplication.translate("MainWindow", u"Pause", None))
        self.button_stop.setText(QCoreApplication.translate("MainWindow", u"Stop", None))
        self.button_load_video.setText(QCoreApplication.translate("MainWindow", u"Load Video", None))
        self.label_detection_options.setText(QCoreApplication.translate("MainWindow", u"<html><head/><body><p align=\"center\"><span style=\" font-size:18pt;\">Detection Options</span></p></body></html>", None))
        self.label_detection_algo.setText(QCoreApplication.translate("MainWindow", u"Detection Algorithm", None))
        self.label_model_type.setText(QCoreApplication.translate("MainWindow", u"Model Type", None))
        self.button_none.setText(QCoreApplication.translate("MainWindow", u"None", None))
        self.button_all.setText(QCoreApplication.translate("MainWindow", u"All", None))
        self.label_items_to_detect.setText(QCoreApplication.translate("MainWindow", u"Items to Detect", None))
        self.button_move_to_active.setText(QCoreApplication.translate("MainWindow", u"Move to Active", None))
        self.button_remove_active.setText(QCoreApplication.translate("MainWindow", u"Remove Active", None))
        self.label_active_detection_items.setText(QCoreApplication.translate("MainWindow", u"Active", None))
        self.label_detection_confidence.setText(QCoreApplication.translate("MainWindow", u"Detection Confidence:", None))
        self.label_value_detection_confidence.setText(QCoreApplication.translate("MainWindow", u"VALUE", None))
        self.label_number_of_objects.setText(QCoreApplication.translate("MainWindow", u"Number of Objects", None))
        self.label_tracking_options.setText(QCoreApplication.translate("MainWindow", u"<html><head/><body><p align=\"center\"><span style=\" font-size:18pt;\">Tracking Options</span></p></body></html>", None))
        self.checkbox_tracking_enabled.setText(QCoreApplication.translate("MainWindow", u"Enabled", None))
        self.label_number_generations.setText(QCoreApplication.translate("MainWindow", u"Number of Generations", None))
        self.label_video_feed.setText(QCoreApplication.translate("MainWindow", u"<html><head/><body><p align=\"center\">Video Feed</p></body></html>", None))
        self.label_roi_title.setText(QCoreApplication.translate("MainWindow", u"<html><head/><body><p align=\"center\"><span style=\" font-size:18pt;\">Region of Interest (ROI) Tool</span></p></body></html>", None))
        self.label_roi_preview.setText(QCoreApplication.translate("MainWindow", u"<html><head/><body><p align=\"center\">ROI Preview</p></body></html>", None))
        self.button_save_roi.setText(QCoreApplication.translate("MainWindow", u"Save ROI", None))
        self.button_clear_roi.setText(QCoreApplication.translate("MainWindow", u"Clear ROI", None))
        self.tab_widget.setTabText(self.tab_widget.indexOf(self.tab_detection_tracking), QCoreApplication.translate("MainWindow", u"Detection and Tracking", None))
        self.tab_widget.setTabText(self.tab_widget.indexOf(self.tab_analysis), QCoreApplication.translate("MainWindow", u"Analysis", None))
        self.tab_widget.setTabText(self.tab_widget.indexOf(self.tab_settings), QCoreApplication.translate("MainWindow", u"Settings", None))
        self.tab_widget.setTabText(self.tab_widget.indexOf(self.tab_logs_reports), QCoreApplication.translate("MainWindow", u"Logs and Reports", None))
        self.menu_file.setTitle(QCoreApplication.translate("MainWindow", u"File", None))
        self.menu_edit.setTitle(QCoreApplication.translate("MainWindow", u"Edit", None))
        self.menu_help.setTitle(QCoreApplication.translate("MainWindow", u"Help", None))
        self.menu_pesentation.setTitle(QCoreApplication.translate("MainWindow", u"Presentation", None))
    # retranslateUi

