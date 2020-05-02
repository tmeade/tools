from PySide2 import QtUiTools, QtWidgets, QtCore
import shiboken2
import logging

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


class PublishAnimationUI(QtWidgets.QDialog):
    def __init__(self, parent=get_main_window(), publish_data=None):
        super(PublishAnimationUI, self).__init__(parent)
        self.publish_data = publish_data

        self.windowTitle('Publish Animation')
        self.setWindowFlags(self.windowFlags() | QtCore.Qt.WindowStaysOnTopHint)
        self.main_layout = QtWidgets.QVBoxLayout()
        self.setLayout(self.main_layout)
        self.create_ui()

    def create_ui(self):
        self.ui = QtUiTools.QUiLoader().load('/Users/tmeade/Documents/python/maya/tools/pubilsh_window.ui')
        self.main_layout.addWidget(self.ui)
        self.ui.publish_btn.clicked.connect(self.slot_publish_clicked)
        self.ui.close_btn.clicked.connect(self.slot_close)
        self.ui.char_lw.setSizeAdjustPolicy(QtWidgets.QListWidget.AdjustToContents)

        for data in self.publish_data:
            item_widget = QtWidgets.QListWidgetItem()
            self.ui.char_lw.addItem(item_widget)

            publish_widget = PublishItemWidget(publish_data=data)
            self.ui.char_lw.addItem(item_widget)
            self.ui.char_lw.setItemWidget(item_widget, publish_widget)
            item_widget.setSizeHint(publish_widget.sizeHint())

    def slot_publish_clicked(self):
        go_publish(self.publish_data)

    def slot_close(self):
        self.close()


class PublishItemWidget(QtWidgets.QWidget):
    def __init__(self, parent=None, publish_data=None):
        super(PublishItemWidget, self).__init__(parent=None)
        self.publish_data = publish_data
        self.setWindowTitle("Publish Item")

        self.main_layout = QtWidgets.QVBoxLayout()
        self.setLayout(self.main_layout)
        self.create_ui()

    def create_ui(self):
        self.horizontalLayout = QtWidgets.QHBoxLayout()

        self.char_name_cbox = QtWidgets.QCheckBox()
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        self.char_name_cbox.setSizePolicy(sizePolicy)
        self.char_name_cbox.setMinimumSize(QtCore.QSize(120, 0))
        self.char_name_cbox.setObjectName("char_name_cbox")
        self.char_name_cbox.setText(self.publish_data.asset_name)
        self.char_name_cbox.clicked.connect(self.slot_char_name_cbox_clicked)
        self.horizontalLayout.addWidget(self.char_name_cbox)

        self.start_frame_le = QtWidgets.QLineEdit()
        self.start_frame_le.setObjectName("start_frame_le")
        self.start_frame_le.setText(str(self.publish_data.start_frame))
        self.horizontalLayout.addWidget(self.start_frame_le)

        self.end_frame_le = QtWidgets.QLineEdit()
        self.end_frame_le.setObjectName("end_frame_le")
        self.end_frame_le.setText(str(self.publish_data.end_frame))
        self.horizontalLayout.addWidget(self.end_frame_le)

        self.version_le = QtWidgets.QLineEdit()
        self.version_le.setObjectName("version_le")
        self.version_le.setText(str(self.publish_data.rig_version))
        self.horizontalLayout.addWidget(self.version_le)

        self.main_layout.addLayout(self.horizontalLayout)
        self.main_layout.setSizeConstraint(QtWidgets.QLayout.SetFixedSize)

    def slot_char_name_cbox_clicked(self):
        if self.char_name_cbox.isChecked() is True:
            self.publish_data.publish = True
        else:
            self.publish_data.publish = False




if __name__ == '__main__':
    import maya.cmds as mc

    publishable_items = list()
    for item in mc.ls(type='locator'):
        if mc.attributeQuery('asset_name', node=item, exists=True):
            publishable_items.append(item)

    logging.info('publishable_items: {}'.format(publishable_items))

    publish_data = list()
    for item in publish_data:
        asset_name = mc.getAttr('{}.asset_name'.format(item))
        rig_version = mc.getAttr('{}.rig_version'.format(item))
        publish_data.append(PublishData(asset_name=asset_name, rig_version=rig_version))

    logging.info('publishable_data: {}'.format(publish_data))

    try:
        win.close()
    except:
        logging.info('Launching window....')

    win = PublishAnimationUI(publish_data=publish_data)
    win.setAttribute(QtCore.Qt.WA_DeleteOnClose)
    win.show()

# import maya.cmds as mc
# import random
#
# ASSETS = ['bilbo', 'frodo', 'gandalf', 'warg', 'aragorn']
# for asset in ASSETS:
#     loc = mc.createNode('locator', name=asset)
#     mc.addAttr(asset, dataType='string', longName='asset_name')
#     mc.setAttr('{}.asset_name'.format(asset), asset, type='string')
#     mc.addAttr(asset, dataType='string', longName='rig_version')
#     mc.setAttr('{}.rig_version'.format(asset), random.randint(1,50), type='string')
