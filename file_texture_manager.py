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


# TODO: Create object to store attributes
def get_file_texture_attributes(file_node):
    '''
    Description:
        Gets node and file name from file node.
    Parameters:
        file_node (string): Name of the file node.
    Returns:
        dict: A dictionary of atttribtue name and value pairs ({attr:value}).
    '''
    logging.debug('file_node: {}'.format(file_node))
    # TODO: Check file_node type and assert if not type fileNode

    # Create dictionary of attributes from the maya file node
    file_texture_attributes = dict({
                            'name': file_node,
                            'file_texture_name': mc.getAttr('{}.fileTextureName'.format(file_node)),
                            'file_exists': False,
                            'new_file_path': None,
                            'needs_move': False
                            })

    # TODO: Possibly add other useful data such as connections to other nodes
    logging.debug('file_texture_attributes: {}'.format(file_texture_attributes))

    return file_texture_attributes


# Ryan
def validate_path_location(dict_attr):
    '''
    Description:
        validate if the file is relatively in sourceimages folder.
    Parameters:
        dict_attr (dict): file_texture_attributes.
    Returns:
        dict: A dictionary of atttribtue name and value pairs ({attr:value}).
    '''
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


def validate_path_exist(dict_attr):
    '''
    Description:
        validate if a single path exists and update dict_attr.
    Parameters:
        dict_attr (dict): file_texture_attributes.
    Returns:
        boolean: file exists or does not exist.
    '''
    # query the path from the dict
    path = dict_attr['file_texture_name']
    # if the path exists, update dict_attr
    if os.path.isfile(path):
        dict_attr['file_exists'] = True
    else:
        dict_attr['file_exists'] = False
    logging.debug('{}\nfile_exists: {}'.format(path, dict_attr['file_exists']))

    return dict_attr


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


# Ji
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


def copy_texture(dict_attr):
    '''
    Description:
        Copy textures to the destination.
    Parameters:
        dict_attr is the class object dictionary
    Returns:
        dict: Update Information on dictionary
    '''
    file_texture_attribues = dict_attr

    file_name = file_texture_attribues['name']
    file_path = file_texture_attribues['file_texture_name']
    file_existance = file_texture_attribues['file_exists']
    new_destination = file_texture_attribues['new_file_path']
    needs_move = file_texture_attribues['needs_move']

    if file_existance == False:
        logging.debug('The file has been lost. : {}'.format(file_name))
        return

    #If the file has relative path.
    if new_destination is None:
        logging.debug('The file already exists. : {}'.format(file_name))
        return


    #If the file exists, but it has absolute path.
    if needs_move is False:
        logging.info('The file already exists. : {}.'.format(file_name))
        return


    #If the file exists, and needs to be copied.
    new_destination = '{}/{}'.format(get_project_path(), new_destination)
    logging.debug('The file will be copied to the new_destination: {}.'.format(new_destination))
    shutil.copy(file_path, new_destination)
    logging.info('The file has been copied from {} to {}.'.format(file_path, new_destination))


def update_node_path(dict_attr):
    file_texture_attribues = dict_attr

    file_name = file_texture_attribues['name']
    file_existance = file_texture_attribues['file_exists']
    new_destination = file_texture_attribues['new_file_path']

    if file_existance == False:
        logging.info('The file has been lost. : {}'.format(file_name))
        return

    #If the file has relative path.
    if new_destination is None:
        logging.info('The file already exists. : {}'.format(file_name))
        return

    mc.setAttr('{}.{}'.format(file_name, 'fileTextureName'), new_destination, type='string')

    return new_destination

def log_summary(dict_attr):
    if dict_attr['needs_move'] is True:
        logger.info('File {} was COPIED to {}'.format(dict_attr['file_texture_name'], dict_attr['new_file_path']))

    if dict_attr['file_exist'] is False:
        logger.info('File {} in node {} was not found.'.format(dict_attr['file_texture_name'], dict_attr['name']))

    if dict_attr['new_file_path'] is not None:
        logger.info('File {} has been updated to use a relative path: {}'.format(dict_attr['file_texture_name'], dict_attr['new_file_path']))


# Test code to run when calling module
# example:
#   execfile('/Users/tmeade/Documents/python/maya/tools/file_texture_manager.py')
if __name__ == "__main__":
    # Get a list of all file texture nodes
    file_texture_nodes = ftm.get_file_textures()

    # Build a list of dictionary that each contain attribte:value pairs on each node.
    file_texture_attributes = list()
    for node in file_texture_nodes:
        file_texture_attributes.append(ftm.FileNode(node))

    validated_attributes = list()
    for attributes in file_texture_attributes:
        ftm.validate_path_location(attributes)
        validated_attributes.append(ftm.validate_path_exist(attributes))

    files_to_copy = list()
    for attributes in validated_attributes:
        if attributes['needs_move'] is True:
            files_to_copy.append(attributes)

    if files_to_copy:
        ftm.warn_copy()

    for attributes in files_to_copy:
        ftm.copy_texture(attributes)

    for attributes in validated_attributes:
        ftm.update_node_path(attributes)

    for attributes in :
        ftm.log_summary(attributes)
