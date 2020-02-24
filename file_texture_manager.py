"""
A module containing helpful house keeping utilities for managing textures.
"""
import os.path
import os.shutil
import logging
import maya.cmds as mc

_logger = logging.getLogger(__name__)


def get_file_textures():
    '''
    Description:
        Gets all file textures in a Maya scene
    Parameters: None
    Returns:
        list: A list of all file testures.
    '''
    return mc.ls(type='file')


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
    # TODO: Check file_node type and assert if not type fileNode

    # Create dictionary of attributes from the maya file node
    file_texture_attribues = dict({
                            'name': file_node,
                            'file_texture_name': mc.getAttr('{}.fileTextureName'.format(file_node))
                            })

    # Possibly add other useful data such as connections to other nodes

    return file_texture_attribues

### validate file path (does texture file exist?)  (Ryan)
#import os.path
#os.path.isfile(fname)

### get current project (Ryan)
#mc.file() ??

### warn before copy files (Ji)

### copy files os.shutil.copy(source, dest) (Ji)

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
