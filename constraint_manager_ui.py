from PySide2 import QtUiTools, QtWidgets, QtCore
import shiboken2
import logging
logger = logging.getLogger(__name__)

import maya.cmds as mc
import tools.constraint_manager as cm

try:
    from maya import OpenMayaUI as omui
except Exception as e:
    logging.error(e)


def get_main_window():
    try:
        mayaMainWindowPtr = omui.MQtUtil.mainWindow()
        mayaMainWindow = shiboken2.wrapInstance(long(mayaMainWindowPtr), QtWidgets.QMainWindow)
    except Exception:
        mayaMainWindow = None
    return mayaMainWindow


class ConstraintManagerUI(QtWidgets.QDialog):
    def __init__(self, parent=get_main_window(), constraint_data=None):
        super(ConstraintManagerUI, self).__init__(parent)
        self.constraint_data = constraint_data

        #self.windowTitle = 'Publish Animation'
        self.setWindowFlags(self.windowFlags() | QtCore.Qt.WindowStaysOnTopHint)
        self.main_layout = QtWidgets.QVBoxLayout()
        self.setLayout(self.main_layout)
        self.create_ui()

    def create_ui(self):
        self.ui = QtUiTools.QUiLoader().load('/Users/tmeade/Documents/python/maya/tools/constraint_manager.ui')
        self.main_layout.addWidget(self.ui)
        self.ui.create_new_constraint_PB.clicked.connect(self.slot_new_contrain_clicked)
        self.ui.delete_constraint_PB.clicked.connect(self.slot_delete_constraint_clicked)
        self.ui.add_target_PB.clicked.connect(self.slot_add_target_clicked)
        self.ui.close_PB.clicked.connect(self.slot_close)

        for constraint in self.constraint_data:
            # item_widget = QtWidgets.QListWidgetItem()
            # item_widget.text(constraint.constraint_name)
            self.ui.constraints_LW.addItem(constraint.constraint_name)

    def slot_new_contrain_clicked(self):
        print 'slot_new_contrain_clicked'

    def slot_delete_constraint_clicked(self):
        print 'slot_delete_contstraint_clicked'

    def slot_add_target_clicked(self):
        print 'slot_add_target_clicked'

    def slot_close(self):
        self.close()


def get_super_constraints():
    super_constraints = list()
    for item in mc.ls(type='blendMatrix'):
        if mc.attributeQuery('superConstraint', node=item, exists=True):
            super_constraints.append(item)

    logging.info('super_constraints: {}'.format(super_constraints))

    return super_constraints


def build_super_constraint_data(super_constraints):
    super_constraint_data = list()
    for constraint in super_constraints:
        super_constraint_data.append(cm.SuperConstraint(constraint_name=constraint))

    logging.info('super_constraint_data: {}'.format(super_constraint_data))

    return super_constraint_data


def show_constraint_window(super_constraint_data):
    try:
        win.close()
    except Exception as e:
        logging.debug('{}.  Window has not previously initialized.'.format(e))
    logging.info('Launching window....')

    window = ConstraintManagerUI(constraint_data=super_constraint_data)
    window.setAttribute(QtCore.Qt.WA_DeleteOnClose)
    window.show()

    return window


def build_publish():
    constraint_data = None
    try:
        constraint_data = build_super_constraint_data(get_super_constraints())
    except:
        logging.info('Cannot import maya.cmds')

    logging.info('constraint_data: {}'.format( constraint_data))
    show_constraint_window(constraint_data)




if __name__ == '__main__':
    build_publish()
