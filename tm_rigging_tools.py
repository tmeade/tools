import maya.cmds as mc
import maya.OpenMaya as om



def create_two_bone_ik(orient_to_world = False):

    #Check Selection
    #if len(mc.sl=1) == 0:
        
    #Get Joints
    root_joint = mc.ls(sl=1)[0]
    mid_joint = mc.listRelatives(root_joint, c=1)[0]
    end_joint = mc.listRelatives(mid_joint, c=1)[0]
    
    #TODO: Validate joint orientations
    
    #Determine primary orientation axis from end_joint (assumes uniform ornientation based on validation).
    translate_values = list(mc.getAttr('{}.translate'.format(end_joint))[0])
    orientation_vector = [0,0,0]
    ctrl_radius = 1
    for item, value in enumerate(translate_values):
        if int(value) != 0:
            orientation_vector[item] = 1
            ctrl_radius = value
           
    
    #Create ik
    ik_handle = mc.ikHandle(sj=root_joint, ee=end_joint)[0]
    
    #Create controls
    ik_ctrl = mc.ls(mc.circle(nr=tuple(orientation_vector), r=ctrl_radius/3), uuid=True)[0] 
    ctrl_grp = mc.ls(mc.group(em=True), uuid=True)[0]
    
    #Place controls in local or world
    for item in list([ik_ctrl, ctrl_grp]):
        if orient_to_world == True:
            mc.matchTransform(mc.ls(item)[0], end_joint, pos=True)
        else: 
            mc.matchTransform(mc.ls(item)[0], end_joint)
    
    #Setup Constraint is local 
    #TODO: This is sloppy
    if orient_to_world == False:
        mc.orientConstraint(mc.ls(ik_ctrl)[0], end_joint)
        
    #create control hierarchy
    mc.parent(mc.ls(ik_ctrl)[0], mc.ls(ctrl_grp)[0])
    mc.parent(ik_handle, mc.ls(ik_ctrl)[0])
    
    mc.rename(mc.ls(ik_ctrl)[0], '_ctrl')
    mc.rename(mc.ls(ctrl_grp)[0], '_ctrl_grp')
    
    ###Get pole vector position
    # Get vectors for postion of each joint
    start_vector = om.MVector(
        mc.xform(root_joint, q=True, ws=True, t=True)[0],
        mc.xform(root_joint, q=True, ws=True, t=True)[1],
        mc.xform(root_joint, q=True, ws=True, t=True)[2]
        )
    mid_vector = om.MVector(
        mc.xform(mid_joint, q=True, ws=True, t=True)[0],
        mc.xform(mid_joint, q=True, ws=True, t=True)[1],
        mc.xform(mid_joint, q=True, ws=True, t=True)[2]
        )
    end_vector = om.MVector(
        mc.xform(end_joint, q=True, ws=True, t=True)[0],
        mc.xform(end_joint, q=True, ws=True, t=True)[1],
        mc.xform(end_joint, q=True, ws=True, t=True)[2]
        )
    
    # Calculate vectors
    start_end = end_vector - start_vector 
    start_mid = mid_vector - start_vector
    
    dot_product =  start_mid * start_end
    
    proj = float(dot_product) / float(start_end.length())
    proj_vector = start_end.normal() * proj
    
    arrow_vector = start_mid - proj_vector
    
    # Add resulting vecotr to mid joint
    final_vector = arrow_vector + mid_vector
    
    #create pole vector and groups
    pv_ctrl = mc.ls(mc.spaceLocator(), uuid=True)
    mc.move(final_vector.x, final_vector.y, final_vector.z)
    pv_grp = mc.ls(mc.group(em=True), uuid=True)[0]
    mc.matchTransform(mc.ls(pv_grp)[0], mc.ls(pv_ctrl)[0])
    
    mc.rename(mc.ls(pv_ctrl)[0], '_pvCtrl')
    mc.rename(mc.ls(pv_grp)[0], '_pv_grp')
    
    mc.parent(mc.ls(pv_ctrl)[0], mc.ls(pv_grp)[0])






