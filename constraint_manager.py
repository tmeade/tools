import maya.cmds as mc

class SuperConstraint(object):
    def __init__(self, constraint_name='superConstraint_0'):
        self.constraint_name = constraint_name
        self.targets = list()
        self.current_target = None
        self.driven_item = None
        self.current_offset_matrix = None
        self.blend_matrix_node = mc.createNode('blendMatrix', name=self.constraint_name+'_blendMatrix')

    # def set_keys(self, frame_offset=1):
    #     # Set keys on blend_matrix_node.weight attrs at current frame
    #     current_frame = mc.currentTime()
    #     for weight in blend_matrix_node.weights:
    #         if weight == 1:
    #             mc.setAttr(weight, 0)
    #         else:
    #             mc.setAttr(weight, 1)
    #
    #         mc.keyframe(current_frame-1, weight)
    #
    # def calcluate_offset_matrix(self):
    #     self.current_offset_matrix = getLocalOffset(self.current_target, self.driven_item)
    #
    # def create_contstraint():
    #     # connect targets world matrix to blendInputs
    #     # connect blend.outputMatrix to driven.offsetParentMatrix
    #     # set driven.offsetParentMatrix with self.current_offset_matrix
    #     pass
    #
    # def add_target(self, new_target):
    #     self.targets.append(new_target)
    #     #connect target to self.blend_matrix_node.input[]
    #
    # def set_target(self):
    #     # set self.blend_matrix_node.weight values to 1 for target, 0 for others
    #     for i in self.targets:
    #         if i is self.current_target:
    #             index = figure out index
    #             mc.setAttr('{}.weight[{}]'.format(blend_matrix_node, index), 1)
    #         else:
    #             mc.setAttr('{}.weight[{}]'.format(blend_matrix_node, index), 0)
    #
    #     #set offsetParentMatrix
    #     mc.setAttr('{}.offsetParentMatrix'.format(),
    #                     [self.current_offset_matrix(i, j)
    #                     for i in range(4) for j in range(4)], type="matrix")


import maya.OpenMaya as om

def getDagPath(node=None):
    sel = om.MSelectionList()
    sel.add(node)
    d = om.MDagPath()
    sel.getDagPath(0, d)
    return d

def getLocalOffset(parent, child):
    parentWorldMatrix = getDagPath(parent).inclusiveMatrix()
    childWorldMatrix = getDagPath(child).inclusiveMatrix()

    return childWorldMatrix * parentWorldMatrix.inverse()
