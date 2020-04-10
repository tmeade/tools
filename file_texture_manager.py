"""
A module containing helpful house keeping utilities for managing textures.
"""
import os.path
import shutil
import logging
import maya.cmds as mc
import pymel.core as pm

logger = logging.getLogger(__name__)


# Thomas
class MayaNode(object):
    def __init__(self, node=None):
        if node:
            self.node = node
            self.get_attributes()
            self.data = self.__dict__

    def __repr__(self):
        return "MayaNode('{}')".format(self.node)

    def __str__(self):
        return str(self.data)

    def get_attributes(self):
        for attribute in mc.listAttr(self.node, hasData=True):
            try:
                value = mc.getAttr('{}.{}'.format(self.node, attribute))
                setattr(self, attribute, value)
            except:
                pass

    def set_maya_attributes(self, attribute=None, value=None):
        if attribute:
            get_type_and_set_attribute(self.node, attribute, value)
        else:
            for attribute, value in self.data.items():
                get_type_and_set_attribute(self.node, attribute, value)



class FileNode(MayaNode):
    def __init__(self, node=None):
        super(FileNode, self).__init__(node)
        self.file_exists = False
        self.needs_move = False
        self.new_file_path = None
        self.old_path = self.fileTextureName
    # Ryan
    def validate_path_location(self):
        '''
        Description:
            validate if the file is relatively in sourceimages folder.
        Returns:
            tuple: self.new_file_path and self.needs_move
        '''

        file_name = os.path.basename(self.old_path)
        path_relative = 'sourceimages/{}'.format(file_name)
        path_absolute = '/{}'.format(path_relative)

        # if the path is not relative
        if self.old_path is not path_relative:
            self.new_file_path = path_relative
            # if the file is not in sourceimages
            if path_absolute not in self.old_path:
                self.needs_move = True
        logging.debug('{}\nnew_file_path: {}\nneeds_move:{}'.format(self.old_path, self.new_file_path,
                        self.needs_move))

        return (self.new_file_path, self.needs_move)

    # Ryan
    def validate_path_exist(self):
        '''
        Description:
            validate if a single path exists and update file_texture_object.
        Returns:
            boolean: file exists or does not exist.
        '''

        # if the path exists, update file_texture_object
        if os.path.isfile(self.old_path):
            self.file_exists = True
        else:
            self.file_exists = False
        logging.debug('{}\nfile_exists: {}'.format(self.old_path, self.file_exists))

        return self.file_exists

    # Ji
    def copy_texture(self):
        '''
        Description:
            Copy textures to the destination.
        Parameters:
            file_texture_object is the class object dictionary
        Returns:
            dict: Update Information on dictionary
        '''
        # Copy the file to the destination
        msg = 'The file will be copied to the new_destination'
        logging.debug('{} : {}.'.format(msg, self.new_file_path))
        new_destination = '{}/{}'.format(get_project_path(), self.new_file_path)
        shutil.copy(self.old_path, new_destination)

        msg = 'The file has been copied from'
        logging.debug('{} {} to {}.'.format(msg, self.old_path, self.new_file_path))

# Mike
    def log_summary(self):
        if self.needs_move is True:
            logger.info('File {} was COPIED to {}'.format(
                self.fileTextureName,
                self.new_file_path))

        if self.file_exists is False:
            logger.info('File {} in node {} was not found.'.format(
                self.fileTextureName,
                self.node))

        if self.new_file_path is not None:
            logger.info('File {} has been updated to use a relative path: {}'.format(
                self.fileTextureName,
                self.new_file_path))


def get_file_textures():
    '''
    Description:
        Gets all file textures in a Maya scene
    Parameters: None
    Returns:
        list: A list of all file textures.
    '''
    file_texture_nodes = mc.ls(type='file')
    logging.debug('file_texture_nodes: {}'.format(file_texture_nodes))

    return file_texture_nodes


def warn_copy():
    '''
    Description:
        Warn the possible huge folder capacity.
    Parameters:
        None
    Returns:
        string(Yes/No)
    '''
    answer = mc.confirmDialog(title='Confirm Copying Files',
        message='Please, check your memory capacity is enough for files.\nDo you want to proceed?',
        button=['Yes','No'], defaultButton='Yes', cancelButton='No', dismissString='No')
    return answer


def get_project_path():
    '''
    Description:
        get current project path
    Parameters:
        None
    Returns:
        string: current project path
    '''
    project_path = mc.workspace(query=True, rootDirectory=True)
    return project_path


def get_type_and_set_attribute(node, attribute, value):
    node_obj = pm.PyNode(node)

    # try if attr exists in node or a custom attr
    try:
        # create a PyNode attribute obj
        attr_obj = node_obj.attr(attribute)
    except AttributeError as err:
        logging.info(err)
        return

    # check if attr_obj can be modified
    if (not attr_obj.isFreeToChange()) or (not attr_obj.isSettable()):
        logging.debug('{} cannot be modified'.format(attribute))
        return

    # check if attr value is a list
    if isinstance(value, list):
        value = value[0]

    # try setting attr value
    try:
        attr_obj.set(value)
    except RuntimeError as err:
        logging.info(err)
        return


def manage_file_textures():
    '''
    Description:
        Validates all file nodes in current scene, copies all files to current project and sets all
        existing absolute paths to relative paths.
    Parameters:
        None
    Returns:
        list: validated file texture objects
    '''

    # Get a list of all file texture nodes
    file_texture_nodes = get_file_textures()

    # Wrap each file node in an object
    file_texture_objects = list()
    for node in file_texture_nodes:
        print 'Node: ', node
        file_texture_objects.append(FileNode(node))

    validated_objects = list()
    for object in file_texture_objects:
        object.validate_path_location()
        if object.validate_path_exist():
            validated_objects.append(object)

    files_to_copy = list()
    for object in validated_objects:
        if object.needs_move is True:
            files_to_copy.append(object)

    if files_to_copy:
        warn_copy()

    for object in files_to_copy:
        object.copy_texture()

    for object in validated_objects:
        object.set_maya_attributes()  # 'fileTextureName', object.new_file_path)

    for object in validated_objects:
        object.log_summary()

    return validated_objects


if __name__ == "__main__":
    manage_file_textures()
