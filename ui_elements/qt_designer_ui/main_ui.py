# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '.\main_window.ui'
#
# Created by: PyQt5 UI code generator 5.15.9
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(800, 600)
        self.central_widget = QtWidgets.QWidget(MainWindow)
        self.central_widget.setObjectName("central_widget")
        MainWindow.setCentralWidget(self.central_widget)
        self.menu_bar = QtWidgets.QMenuBar(MainWindow)
        self.menu_bar.setGeometry(QtCore.QRect(0, 0, 800, 26))
        self.menu_bar.setObjectName("menu_bar")
        self.menu_area = QtWidgets.QMenu(self.menu_bar)
        self.menu_area.setObjectName("menu_area")
        self.menu_bottom_profile = QtWidgets.QMenu(self.menu_area)
        self.menu_bottom_profile.setObjectName("menu_bottom_profile")
        self.menu_source = QtWidgets.QMenu(self.menu_bar)
        self.menu_source.setObjectName("menu_source")
        self.menu_new_source = QtWidgets.QMenu(self.menu_source)
        self.menu_new_source.setObjectName("menu_new_source")
        self.menu_marigrams = QtWidgets.QMenu(self.menu_bar)
        self.menu_marigrams.setObjectName("menu_marigrams")
        self.menu_select_points = QtWidgets.QMenu(self.menu_marigrams)
        self.menu_select_points.setObjectName("menu_select_points")
        self.menu_calculations = QtWidgets.QMenu(self.menu_bar)
        self.menu_calculations.setObjectName("menu_calculations")
        self.menu_visualisation = QtWidgets.QMenu(self.menu_bar)
        self.menu_visualisation.setObjectName("menu_visualisation")
        self.menu_set_contour_lines_levels = QtWidgets.QMenu(self.menu_visualisation)
        self.menu_set_contour_lines_levels.setObjectName("menu_set_contour_lines_levels")
        MainWindow.setMenuBar(self.menu_bar)
        self.status_bar = QtWidgets.QStatusBar(MainWindow)
        self.status_bar.setObjectName("status_bar")
        MainWindow.setStatusBar(self.status_bar)
        self.action_size = QtWidgets.QAction(MainWindow)
        self.action_size.setObjectName("action_size")
        self.action_steps = QtWidgets.QAction(MainWindow)
        self.action_steps.setObjectName("action_steps")
        self.action_source_parameters = QtWidgets.QAction(MainWindow)
        self.action_source_parameters.setObjectName("action_source_parameters")
        self.action_calculate_most = QtWidgets.QAction(MainWindow)
        self.action_calculate_most.setObjectName("action_calculate_most")
        self.action_heatmap = QtWidgets.QAction(MainWindow)
        self.action_heatmap.setEnabled(False)
        self.action_heatmap.setObjectName("action_heatmap")
        self.action_3d_heatmap = QtWidgets.QAction(MainWindow)
        self.action_3d_heatmap.setEnabled(False)
        self.action_3d_heatmap.setObjectName("action_3d_heatmap")
        self.action_wave_profile_bar_chart = QtWidgets.QAction(MainWindow)
        self.action_wave_profile_bar_chart.setEnabled(False)
        self.action_wave_profile_bar_chart.setObjectName("action_wave_profile_bar_chart")
        self.action_marigrams = QtWidgets.QAction(MainWindow)
        self.action_marigrams.setEnabled(False)
        self.action_marigrams.setObjectName("action_marigrams")
        self.action_calculation_parameters = QtWidgets.QAction(MainWindow)
        self.action_calculation_parameters.setObjectName("action_calculation_parameters")
        self.actionArea = QtWidgets.QAction(MainWindow)
        self.actionArea.setObjectName("actionArea")
        self.action_show_area = QtWidgets.QAction(MainWindow)
        self.action_show_area.setObjectName("action_show_area")
        self.action_heatmap_contour = QtWidgets.QAction(MainWindow)
        self.action_heatmap_contour.setEnabled(False)
        font = QtGui.QFont()
        self.action_heatmap_contour.setFont(font)
        self.action_heatmap_contour.setObjectName("action_heatmap_contour")
        self.action_heatmap_with_contour = QtWidgets.QAction(MainWindow)
        self.action_heatmap_with_contour.setEnabled(False)
        self.action_heatmap_with_contour.setObjectName("action_heatmap_with_contour")
        self.action_load_existing_results = QtWidgets.QAction(MainWindow)
        self.action_load_existing_results.setObjectName("action_load_existing_results")
        self.action_select_points_on_area = QtWidgets.QAction(MainWindow)
        self.action_select_points_on_area.setObjectName("action_select_points_on_area")
        self.action_select_points_on_heatmap = QtWidgets.QAction(MainWindow)
        self.action_select_points_on_heatmap.setEnabled(False)
        self.action_select_points_on_heatmap.setObjectName("action_select_points_on_heatmap")
        self.action_default = QtWidgets.QAction(MainWindow)
        self.action_default.setObjectName("action_default")
        self.action_draw_wave_profile = QtWidgets.QAction(MainWindow)
        self.action_draw_wave_profile.setEnabled(False)
        self.action_draw_wave_profile.setObjectName("action_draw_wave_profile")
        self.action_static = QtWidgets.QAction(MainWindow)
        self.action_static.setObjectName("action_static")
        self.action_set_contour_lines_levels_for_MOST = QtWidgets.QAction(MainWindow)
        self.action_set_contour_lines_levels_for_MOST.setObjectName("action_set_contour_lines_levels_for_MOST")
        self.action_set_contour_lines_levels_for_STATIC = QtWidgets.QAction(MainWindow)
        self.action_set_contour_lines_levels_for_STATIC.setObjectName("action_set_contour_lines_levels_for_STATIC")
        self.action_change_source = QtWidgets.QAction(MainWindow)
        self.action_change_source.setEnabled(False)
        self.action_change_source.setObjectName("action_change_source")
        self.action_calculate_most_static = QtWidgets.QAction(MainWindow)
        self.action_calculate_most_static.setEnabled(False)
        self.action_calculate_most_static.setObjectName("action_calculate_most_static")
        self.action_elliptical_source = QtWidgets.QAction(MainWindow)
        self.action_elliptical_source.setObjectName("action_elliptical_source")
        self.action_static_source = QtWidgets.QAction(MainWindow)
        self.action_static_source.setObjectName("action_static_source")
        self.action_show_static = QtWidgets.QAction(MainWindow)
        self.action_show_static.setEnabled(False)
        self.action_show_static.setObjectName("action_show_static")
        self.menu_bottom_profile.addAction(self.action_default)
        self.menu_area.addAction(self.menu_bottom_profile.menuAction())
        self.menu_area.addSeparator()
        self.menu_area.addAction(self.action_size)
        self.menu_area.addSeparator()
        self.menu_area.addAction(self.action_show_area)
        self.menu_new_source.addAction(self.action_elliptical_source)
        self.menu_new_source.addAction(self.action_static_source)
        self.menu_source.addAction(self.menu_new_source.menuAction())
        self.menu_source.addSeparator()
        self.menu_source.addAction(self.action_show_static)
        self.menu_select_points.addAction(self.action_select_points_on_area)
        self.menu_select_points.addAction(self.action_select_points_on_heatmap)
        self.menu_marigrams.addAction(self.menu_select_points.menuAction())
        self.menu_calculations.addAction(self.action_calculation_parameters)
        self.menu_calculations.addAction(self.action_calculate_most)
        self.menu_calculations.addSeparator()
        self.menu_calculations.addAction(self.action_load_existing_results)
        self.menu_set_contour_lines_levels.addAction(self.action_set_contour_lines_levels_for_MOST)
        self.menu_set_contour_lines_levels.addAction(self.action_set_contour_lines_levels_for_STATIC)
        self.menu_visualisation.addAction(self.action_heatmap)
        self.menu_visualisation.addAction(self.action_heatmap_with_contour)
        self.menu_visualisation.addAction(self.action_3d_heatmap)
        self.menu_visualisation.addAction(self.action_wave_profile_bar_chart)
        self.menu_visualisation.addSeparator()
        self.menu_visualisation.addAction(self.action_marigrams)
        self.menu_visualisation.addSeparator()
        self.menu_visualisation.addAction(self.menu_set_contour_lines_levels.menuAction())
        self.menu_visualisation.addAction(self.action_draw_wave_profile)
        self.menu_bar.addAction(self.menu_area.menuAction())
        self.menu_bar.addAction(self.menu_source.menuAction())
        self.menu_bar.addAction(self.menu_marigrams.menuAction())
        self.menu_bar.addAction(self.menu_calculations.menuAction())
        self.menu_bar.addAction(self.menu_visualisation.menuAction())

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "ITMS"))
        self.menu_area.setTitle(_translate("MainWindow", "Area"))
        self.menu_bottom_profile.setTitle(_translate("MainWindow", "Bottom profile..."))
        self.menu_source.setTitle(_translate("MainWindow", "Source"))
        self.menu_new_source.setTitle(_translate("MainWindow", "New tsunami source..."))
        self.menu_marigrams.setTitle(_translate("MainWindow", "Marigrams"))
        self.menu_select_points.setTitle(_translate("MainWindow", "Select points..."))
        self.menu_calculations.setTitle(_translate("MainWindow", "Calculations"))
        self.menu_visualisation.setTitle(_translate("MainWindow", "Visualisation"))
        self.menu_set_contour_lines_levels.setTitle(_translate("MainWindow", "Set contour lines levels..."))
        self.action_size.setText(_translate("MainWindow", "Size..."))
        self.action_steps.setText(_translate("MainWindow", "Steps..."))
        self.action_source_parameters.setText(_translate("MainWindow", "Change elliptical source parameters..."))
        self.action_calculate_most.setText(_translate("MainWindow", "Run and plot MOST"))
        self.action_heatmap.setText(_translate("MainWindow", "Heatmap"))
        self.action_3d_heatmap.setText(_translate("MainWindow", "3D heatmap"))
        self.action_wave_profile_bar_chart.setText(_translate("MainWindow", "Wave profile"))
        self.action_marigrams.setText(_translate("MainWindow", "Marigrams"))
        self.action_calculation_parameters.setText(_translate("MainWindow", "Calculation parameters..."))
        self.actionArea.setText(_translate("MainWindow", "Area"))
        self.action_show_area.setText(_translate("MainWindow", "Show Area"))
        self.action_heatmap_contour.setText(_translate("MainWindow", "Heatmap with contour lines"))
        self.action_heatmap_with_contour.setText(_translate("MainWindow", "Heatmap with contour lines"))
        self.action_load_existing_results.setText(_translate("MainWindow", "Load existing MOST results..."))
        self.action_select_points_on_area.setText(_translate("MainWindow", "On area"))
        self.action_select_points_on_heatmap.setText(_translate("MainWindow", "On heatmap"))
        self.action_default.setText(_translate("MainWindow", "Default"))
        self.action_draw_wave_profile.setText(_translate("MainWindow", "Draw wave profile"))
        self.action_static.setText(_translate("MainWindow", "Run STATIC"))
        self.action_set_contour_lines_levels_for_MOST.setText(_translate("MainWindow", "For MOST"))
        self.action_set_contour_lines_levels_for_STATIC.setText(_translate("MainWindow", "For STATIC"))
        self.action_change_source.setText(_translate("MainWindow", "Switch source to STATIC"))
        self.action_calculate_most_static.setText(_translate("MainWindow", "Run MOST with STATIC source"))
        self.action_elliptical_source.setText(_translate("MainWindow", "Elliptical..."))
        self.action_static_source.setText(_translate("MainWindow", "STATIC..."))
        self.action_show_static.setText(_translate("MainWindow", "Show STATIC heatmap"))
