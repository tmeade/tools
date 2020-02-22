"""
A module containing helpful house keeping utilities for managing textures.
"""
import os.path
import os.shutil
import logging
import maya.cmds as mc

### Get all file textures (TOM)
# mc.ls(type='fileTexture')

### get path (TOM)
# getAttr(<node>.imageName)

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
