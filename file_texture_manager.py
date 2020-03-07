"""
A module containing helpful house keeping utilities for managing textures.
"""
import os.path
import shutil
import logging
import maya.cmds as mc

logger = logging.getLogger(__name__)


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
        file_node (string): Name of the file node
    Returns:
        dict: A dictionary of atttribtue name and value pairs ({attr:value})
    '''
    logging.debug('file_node: {}'.format(file_node))
    # TODO: Check file_node type and assert if not type fileNode

    # Create dictionary of attributes from the maya file node
    file_texture_attribues = dict({
                            'name': file_node,
                            'file_texture_name': mc.getAttr('{}.fileTextureName'.format(file_node)),
                            'file_exists': False,
                            'new_file_path': None,
                            'needs_move': False
                            })

    # TODO: Possibly add other useful data such as connections to other nodes
    logging.debug('file_texture_attribues: {}'.format(file_texture_attribues))

    return file_texture_attribues

# Ryan
def is_file_append(path, exist_list, lost_list):
    '''
    validate if a single path exists and append it to a list
    '''
    if os.path.isfile(path):
        exist_list.append(path)
        return True
    else:
        lost_list.append(path)
        return False

def file_exist(paths):
    '''
    validate input file paths
    '''
    paths_exist = list()
    paths_lost = list()
    # if multiple paths in a list
    if isinstance(paths, list):
        for path in paths:
            is_file_append(path, paths_exist, paths_lost)
    # if it is a single path
    else:
        is_file_append(path, paths_exist, paths_lost)
    return (paths_exist, paths_lost)

def get_project_path():
    '''
    return current project path
    '''
    project_path = mc.workspace(query=True, rootDirectory=True)
    return project_path


#Ji
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

def copy_texture(source):
    '''
    Description:
        Copy textures to the destination.
    Parameters:
        source is the class object dictionary
    Returns:
        dict: Update Information on dictionary
    '''
    file_texture_attribues = source

    file_name = file_texture_attribues['name']
    file_path = file_texture_attribues['file_texture_name']
    file_existance = file_texture_attribues['file_exists']
    new_destination = file_texture_attribues['new_file_path']
    needs_move = file_texture_attribues['needs_move']

    if file_existance == 'False':
        logging.info('The file has been lost. : {}'.format(file_name))
    else:
        #If the file exists, and has relative path.
        if new_destination is None:
            logging.info('The file already exists. : {}'.format(file_name))
        else:
            dirname = os.path.dirname(new_destination)
            path_exist = os.path.isdir(dirname)

            #If the new path is not valid.
            if path_exist == False:
                logging.info('The new file path doesn\'t exist. : {}.'.format(new_destination))

            else:
                #If the file exists, but it has absolute path.
                if needs_move is False:
                    logging.info('The file already exists. : {}.'.format(file_name))
                #If the file exists, and needs to be copied.
                else:
                    shutil.copy(file_path, new_destination)
                    logging.info('The file has been copied from {} to {}.'.format(file_path, new_destination))


### update paths on texture nodes (mike)
# sourceimages/fileName.tga
# directory = "Z:/temp"
# dirs = os.listdir(directory)
# os.listdir(os.path.join(directory, dirs[0]))
#
# sid = 'sourceImages'
# path = 'z:/temp/sourceImages'
#
# if sid in path:
#     print path

### print out log of all edits (mike)

# Test code to run when calling module
# example:
#   execfile('/Users/tmeade/Documents/python/maya/tools/file_texture_manager.py')
if __name__ == "__main__":
    # Get a list of all file texture nodes
    file_texture_nodes = get_file_textures()

    # Build a list of dictionary that each contain attribte:value pairs on each node.
    file_texture_attributes = list()
    for node in file_texture_nodes:
        file_texture_attributes.append(get_file_texture_attributes(node))

    # Validate the file path on each node.  I suggest taking the file_texture_attributes
    # list and adding a 'file_exists' attribute to the dict and setting it True or False.
    # file_exist(file_texture_attributes)
    # file_exists(dict)
    # if exists, set file_exists attr to True
    #
    # is_in_sourceImages()
    # # check that it IS in the project's sourceImages dir
    # # check the path and if absolute, set new_file_path to relative
    #
    # not_in_sourceImages()
    # # Set needs_moved
