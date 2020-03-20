"""
A module containing helpful house keeping utilities for managing textures.
"""
import os.path
import shutil
import logging
import maya.cmds as mc

logger = logging.getLogger(__name__)


# Thomas
class MayaNode(object):
    def __init__(self, node=None):
        if node:
            self.node = node
            self.get_attributes(node)
            self.data = self.__dict__

    def __repr__(self):
        return "MayaNode('{}')".format(self.node)

    def __str__(self):
        return str(self.data)

    def get_attributes(self, node):
        for attribute in mc.listAttr(node, hasData=True):
            try:
                value = mc.getAttr('{}.{}'.format(node, attribute))
                setattr(self, attribute, value)
            except:
                pass

    def set_maya_attribute(self, attr=None, value=None):
        if attr:
            mc.setAttr(attr, value)
        else:
            for k, v in self.data.items():
                mc.setAttr(k, v)


class FileNode(MayaNode):
    def __init__(self, node=None):
        super(FileNode, self).__init__(node)
        self.file_exists = False
        self.needs_move = False
        self.new_file_path = None

    # Ryan
    def validate_path_location(self):
        '''
        Description:
            validate if the file is relatively in sourceimages folder.
        Parameters:
            dict_attr (dict): file_texture_objects.
        Returns:
            dict: A dictionary of atttribtue name and value pairs ({attr:value}).
        '''
        #global name 'dict_attr' is not defined
        path = dict_attr['file_texture_name']
        file_name = os.path.basename(path)
        path_relative = 'sourceimages/{}'.format(file_name)
        path_absolute = '/{}'.format(path_relative)

        # if the path is not relative
        if path is not path_relative:
            dict_attr['new_file_path'] = path_relative
            # if the file is not in sourceimages
            if path_absolute not in path:
                dict_attr['needs_move'] = True
        logging.debug('{}\nnew_file_path: {}\nneeds_move:{}'.format(path, dict_attr['new_file_path'],
                        dict_attr['needs_move']))

        return dict_attr

    # Ryan
    def validate_path_exist(self):
        '''
        Description:
            validate if a single path exists and update file_texture_object.
        Parameters:
            file_texture_object (dict): file_texture_objects.
        Returns:
            boolean: file exists or does not exist.
        '''
        # query the path from the dict
        path = file_texture_object['file_texture_name']
        # if the path exists, update file_texture_object
        if os.path.isfile(path):
            file_texture_object['file_exists'] = True
        else:
            file_texture_object['file_exists'] = False
        logging.debug('{}\nfile_exists: {}'.format(path, file_texture_object['file_exists']))

        return file_texture_object

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
        new_destination = self.new_file_path
        logging.debug('The file will be copied to the new_destination: {}.'.format(new_destination))
        shutil.copy(self, new_destination)
        logging.info('The file has been copied from {} to {}.'.format(file_path, new_destination))

# Mike
def log_summary(dict_attr):
    if dict_attr['needs_move'] is True:
        logger.info('File {} was COPIED to {}'.format(dict_attr['file_texture_name'], dict_attr['new_file_path']))

    if dict_attr['file_exist'] is False:
        logger.info('File {} in node {} was not found.'.format(dict_attr['file_texture_name'], dict_attr['name']))

    if dict_attr['new_file_path'] is not None:
        logger.info('File {} has been updated to use a relative path: {}'.format(dict_attr['file_texture_name'], dict_attr['new_file_path']))


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
        validated_objects.append(validate_path_exist(object))

    files_to_copy = list()
    for object in validated_objects:
        if object.needs_move is True:
            files_to_copy.append(object)

    if files_to_copy:
        warn_copy()

    for object in files_to_copy:
        object.copy_texture()

    for object in validated_objects:
        object.update_node_path()

    for object in validated_objects:
        log_summary(object)

    return validated_objects


if __name__ == "__main__":
    manage_file_textures()
