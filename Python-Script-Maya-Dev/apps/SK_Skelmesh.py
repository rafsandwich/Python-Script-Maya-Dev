from genericpath import exists
from tokenize import Double3
import maya.cmds as cmds
import maya.mel as Mm
import json
import sys
import os
import pymel.core as pm


def importFbx(filename):
    """
    Function to Import an FBX FILE
    :param strDir:
    :return:
    """
    pm.mel.FBXImport(f=filename)

def loadFile(title):
    """
    Launches dialogue to open file
    :return:
    """
    fbx_file = cmds.fileDialog2(cap=title, fm=1)[0]
    return fbx_file

def file_save(old_translations):
    saved_data= convert_json_data(old_translations)

    extension = "*.json"
    name = cmds.fileDialog2(fileFilter=extension, dialogStyle=2, fm=0)[0]

    with open(name, "w") as jsonFile:
        json.dump(saved_data, jsonFile, indent=2, sort_keys=True)

def create_controlling_chain(startJnt=None, ignoreEnds=True):
    """
    Creates a copy of the skelmesh to be used as CONTROLS
    :param startJnt:
    :param ignoreEnds:
    :return:
    """
    joint_list = _get_joints()
    if startJnt is None:
        try:
            jnt = _get_hierarchy_root_joint(joint_list[0])
            print("Root is >>> ", end=' ')
            print(jnt)
        except:
            jnt = _get_joints()[0]
            cmds.warning("Could not find root joint, using the first from the list")
    else:
        jnt = pm.PyNode(startJnt)

    chain = jnt.listRelatives(ad=True)
    chain.reverse()
    chain.insert(0, jnt)

    # Removes any joints without children from the list
    if ignoreEnds:
        for jnt in chain[:]:
            if not jnt.getChildren():
                chain.remove(jnt)
    controls = []
    for i, jnt in enumerate(chain):
        # Duplicate one joint at a time
        dup = jnt.duplicate(parentOnly=True)[0]
        dup.rename(jnt.name() + 'CTRL')
        controls.append(dup)

        # Constrain the original to the new duplicate
        pm.pointConstraint(dup, jnt)
        pm.orientConstraint(dup, jnt)

        # If the parent is in the chain, it has already been duplicated
        if jnt.getParent() in chain:
            # We find the joint's parent's index in the chain
            jntIndex = chain.index(jnt.getParent())
            # And set the parent of the duplicate joint to the corresponding duplicate
            dup.setParent(controls[jntIndex])
        else:
            # Otherwise, it is the start of the joint chain,
            # so we parent the first control to the world
            dup.setParent(world=True)
    return controls[0]

def color_joints(startJnt=None, ignoreEnds=True):
    """
    Overrides the colors of a skeleton hierarchy
    :param startJnt:
    :param ignoreEnds:
    :return:
    """
    joint_list = _get_joints()
    if startJnt is None:
        try:
            jnt = _get_hierarchy_root_joint(joint_list[0])
            print("Root is >>> ", end=' ')
            print(jnt)
        except:
            jnt = _get_joints()[0]
            cmds.warning("Could not find root joint, using the first from the list")
    else:
        jnt = pm.PyNode(startJnt)

    chain = jnt.listRelatives(ad=True)
    chain.reverse()
    chain.insert(0, jnt)

    # Removes any joints without children from the list
    if ignoreEnds:
        for jnt in chain[:]:
            if not jnt.getChildren():
                chain.remove(jnt)

    for i, jnt in enumerate(chain):
        if str(jnt).startswith("r"):
            set_node_color(jnt, "red")
        elif str(jnt).startswith("l"):
            set_node_color(jnt, "blue")
        else :
            set_node_color(jnt, "yellow")
    return

def copyPose():
    """
    Copies pose data on a keyframe

    """
    joints = _get_joints()
    pm.select(joints)
    Mm.eval("timeSliderCopyKey;")
    print("Keyframe copied ")

def set_node_color(node, color):
    """
    Sets color override for a maya node
    :param node:
    :param color:
    :return:
    """

    if color == 'yellow':
        cmds.setAttr((node+(".overrideEnabled")), 1)
        cmds.setAttr((node+(".overrideColor")), 17)

    elif color == 'blue':
        cmds.setAttr((node+(".overrideEnabled")), 1)
        cmds.setAttr((node+(".overrideColor")), 6)

    elif color == 'red':
        cmds.setAttr((node+(".overrideEnabled")), 1)
        cmds.setAttr((node+(".overrideColor")), 13)

def create_control_curve(crvColor='yellow', infl='orient', joint=""):

    ctrlCurve = pm.circle(ch=0, n=(joint+('_CTRL')))

    cmds.delete(cmds.pointConstraint(joint, ctrlCurve))
    cmds.delete(cmds.orientConstraint(joint,ctrlCurve))

    ## create grpFreeze

    grpFrz = cmds.duplicate(ctrlCurve, n=(ctrlCurve[0]+('_grpFrz')))
    cmds.delete(cmds.listRelatives(grpFrz[0],c=1, shapes=1))
    cmds.parent(ctrlCurve, grpFrz)

    ## if orient is on

    if infl == 'orient':
        cmds.orientConstraint(ctrlCurve,joint)

    if infl == 'parent':
        cmds.parentConstraint(ctrlCurve,joint)

    ## color override

    if crvColor == 'yellow':
        cmds.setAttr((ctrlCurve[0]+(".overrideEnabled")), 1)
        cmds.setAttr((ctrlCurve[0]+(".overrideColor")), 17)

    elif crvColor == 'blue':
        cmds.setAttr((ctrlCurve[0]+(".overrideEnabled")), 1)
        cmds.setAttr((ctrlCurve[0]+(".overrideColor")), 6)

    elif crvColor == 'red':
        cmds.setAttr((ctrlCurve[0]+(".overrideEnabled")), 1)
        cmds.setAttr((ctrlCurve[0]+(".overrideColor")), 13)

    cmds.setAttr((ctrlCurve[0]+(".scaleX")),10)
    cmds.setAttr((ctrlCurve[0] + (".scaleY")),10)
    cmds.setAttr((ctrlCurve[0] + (".scaleZ")),10)

    return ctrlCurve[0]

def _get_hierarchy_root_joint(joint):
    """
    Function to find the top parent joint node from the given
    'joint' maya node

    """
    # Search through the root_joint's top most joint parent node
    root_joint = joint

    print("getting Root joint", end=' ')
    print(joint)
    while (True):
        parent = cmds.listRelatives(root_joint,
                                    parent=True,
                                    type='joint')
        if not parent:
            print("Root is >>> ", end=' ')
            print(root_joint)
            break

        root_joint = parent[0]

    print("Root is >>> ", end=' ')
    print(root_joint)
    return root_joint

def _get_joints():
    """
    Retruns a lits of Joints from the scene
    :return:
    """
    print ("Listing joints ...")
    joints_list = []
    try:
        joints_list = pm.ls(type="joint")
    except:
        cmds.warning("No joints available.")
    return joints_list


def load_json_rotOrder():
    """
    Loads a Json File with rotation Orders
    :return: The rotation order
    """
    data = json.load(open(loadFile("Select RotationOrder file")))
    return data

def store_translations():
    """
    Stores a bind pose translation data
    :return:
    """
    currentKeyframe = cmds.currentTime(query=True)
    Mm.eval("currentTime 0 ;")
    data = {}
    joints = _get_joints()
    pm.select(joints)
    for joint in joints:
        data[joint] = [get_joint_attr(joint, ".translateX"), get_joint_attr(joint, ".translateY"), get_joint_attr(joint, ".translateZ")]
    print(("Original Joint translations: ", data))
    cmds.currentTime(currentKeyframe)
    return  data


def load_json_data(rotOrder):
    """
    Loads a Json file with pose information for the avatar
    :return: nothing
    """
    rotationMap = {"x": 0, "y": 1, "z": 2}
    translationMap = {"x": 6, "y": 7, "z": 8}
    rotationOrder = rotOrder
    data = json.load(open(loadFile("Select JSON Pose file")))
    print (data)

    #fixes loads distorting avatar
    resetPose() #if someone cancels their load OK, but if someone cancels loadRot then pose information is lost on the frame, minor problem TODO take load rotation order out of for loop?

    for entry in data["pose"]:
        # Check if we have a rotation order stored,
        # Load rotation order if not found.
        try:
            print((rotationOrder["jointRotationOrder"][entry]))
        except Exception as e:
            pm.warning("Please load a rotation order file", e)
            rotationOrder = load_json_rotOrder()

        # Apply transforms in reverse order
        for each in reversed(rotationOrder["jointRotationOrder"][entry]):
            # Starting with Rotations
            try:
                print(("Applying rotation to  >>> R" +each+ " : ", str(entry)))
                print((data["pose"][str(entry)][rotationMap[str(each)]]))
                pm.setAttr(str(entry) + ".rotate"+ str(each).upper(), data["pose"][str(entry)][rotationMap[str(each)]])
            except Exception as e:
                pm.warning("Couldn't handle rotations", e)
            # Applying Translations
            try:
                print(("Applying translation to  >>> T" +each+ " : ", str(entry)))
                print((data["pose"][str(entry)][rotationMap[str(each)]]))
                pm.setAttr(str(entry) + ".translate"+str(each).upper(), pm.getAttr(str(entry) + ".translate"+str(each).upper()) + data["pose"][str(entry)][translationMap[each]])
            except Exception as e:
                pm.warning("No translation found", e)


def get_joint_attr(joint, string):
    """
    Local function to simplify access
    :param joint:
    :param string:
    :return:
    """
    return pm.getAttr(str(joint) + string)


def convert_json_data(old_translations):
    """
    Reads all transfroms from our bind skeleton and creates a dictionary from it
    :return: The converted Json data
    """

    pose_data = {}
    original_data = old_translations

    for joint in _get_joints():
        try:
            print((original_data[joint]))
        except Exception as e:
            pm.warning("Please store an initial pose", e)
            original_data =  store_translations()

    for joint in _get_joints():
        print(("This would convert this >> "), end=' ')
        print (joint)
        RX = get_joint_attr(joint, ".rotateX")
        RY = get_joint_attr(joint, ".rotateY")
        RZ = get_joint_attr(joint, ".rotateZ")
        print(("Total rotations = ", RX, RY, RZ))
        # print ("Total translations = "),
        # print (pm.getAttr(str(joint)+".translateX") + pm.getAttr(str(joint)+".translateY") + pm.getAttr(str(joint)+".translateZ"))
        TX = get_joint_attr(joint, ".translateX")
        TY = get_joint_attr(joint, ".translateY")
        TZ = get_joint_attr(joint, ".translateZ")
        print(("New Translations: ", TX, TY, + TZ,))
        TX = get_joint_attr(joint, ".translateX") - original_data[joint][0]
        TY = get_joint_attr(joint, ".translateY") - original_data[joint][1]
        TZ = get_joint_attr(joint, ".translateZ") - original_data[joint][2]
        print(("Total translations = ", TX, TY, + TZ,))
        SX = get_joint_attr(joint, ".scaleX")
        SY = get_joint_attr(joint, ".scaleY")
        SZ = get_joint_attr(joint, ".scaleZ")

        # Skip pose animation Controls
        if "CTRL" in str(joint):
            pass

        try:
            pose_data.__setitem__(str(joint),
                                  [RX, RY, RZ, SX, SY, SZ, TX, TY, TZ])
        except Exception as e:
            pm.warning("Error saving skeleton data : ", e)


        # if "genesis" in str(joint).lower():
        #     pose_data.__setitem__(str(joint),
        #                           [pm.getAttr(str(joint) + ".rotateX"), pm.getAttr(str(joint) + ".rotateY"),
        #                            pm.getAttr(str(joint) + ".rotateZ"), pm.getAttr(str(joint) + ".scaleX"),
        #                            pm.getAttr(str(joint) + ".scaleY"), pm.getAttr(str(joint) + ".scaleZ"),
        #                            pm.getAttr(str(joint) + ".translateX"), pm.getAttr(str(joint) + ".translateY"),
        #                            pm.getAttr(str(joint) + ".translateZ"),])
        # else:
        #     pose_data.__setitem__(str(joint),
        #                           [pm.getAttr(str(joint) + ".rotateX"),
        #                            pm.getAttr(str(joint) + ".rotateY"),
        #                            pm.getAttr(str(joint) + ".rotateZ")])

    json_data = {"pose": pose_data}
    return json_data

def load_intersections():
    """
    Assigns new toon outline, changes attributes to show intersections. Toggling will disable intersections / reenable.

    :return: 
    """
    #TODO check if outline created, otherwise create toon outline, save a click, 

    cmds.select("mesh")

    try:
        cmds.select("pfxToon1")
    except:
        toon_exists = False
    else:
        toon_exists = True

    if toon_exists == False:
        Mm.eval("assignNewPfxToon;")
        print("New toon outline created")
    
    cmds.select("pfxToon1")
    thisSelection = cmds.ls(selection = True)
    selectedMesh = thisSelection[0]

    if cmds.getAttr(selectedMesh + ".intersectionLines") == 1:
        cmds.setAttr(selectedMesh + ".intersectionLines", 0)
        print("Intersections disabled")

    else:
        cmds.setAttr(selectedMesh + ".borderLines", 0),
        cmds.setAttr(selectedMesh + ".lineWidth", 0.05), #0.2
        cmds.setAttr(selectedMesh + ".intersectionLines", 1),
        cmds.setAttr(selectedMesh + ".intersectionColor", 1, 0, 0.0353),
        cmds.setAttr(selectedMesh + ".intersectionLineWidth", 10), #10 for thicker intersects
        cmds.setAttr(selectedMesh + ".selfIntersect", 1)
        print("Intersections enabled")
    
    #cmds.select("Viewport_Camera1")
    cmds.select("persp")

def pastePose():
    try:
        Mm.eval("timeSliderPasteKey false;")
    except: 
        print("No pose information copied")

def resetPose():
    currentKeyframe = cmds.currentTime(query=True)
    Mm.eval("currentTime 0 ;")
    joints = _get_joints()
    pm.select(joints)
    Mm.eval("timeSliderCopyKey;")
    cmds.currentTime(currentKeyframe)
    Mm.eval("timeSliderPasteKey false;")

def toggleFloorPlane():

    plane_exists = False

    try:
        cmds.select("floorPlane")
    except:
        plane_exists = False
    else:
        plane_exists = True
        Mm.eval('select -r floorPlane ;')
        Mm.eval('doDelete;')

    if plane_exists == False:
        cmds.polyPlane( n= "floorPlane", sx=1, sy=1, w=150, h=150)

def skelmesh():
    """
    Load an FBX Skelmesh in the scene
    :return:
    """
    importFbx(loadFile("Select the skelmesh file"))

def sceneSetup():

    #ensure correct working unit
    cmds.currentUnit( linear='cm' )

    ready = True
    joints_test = []

    try:
        joints_test = pm.ls(type="joint")
        if joints_test[1]:
            ready = True
    except Exception as e:
        ready = False
        pm.warning("Please load an FBX before using Setup scene", e)
    
    if ready == True:

        #ensure autokeyframe is on
        joints = _get_joints()
        pm.select(joints)
        Mm.eval("autoKeyframe -state true;")

         #set all keyframes
        attrs = ["tx","ty","tz","rx", "ry", "rz"]

        startFrame = cmds.playbackOptions(minTime=True, query=True)
        endFrame = cmds.playbackOptions(maxTime=True, query=True)
        #frames = [1,5,10]
        frames = list(range(int(startFrame), int(endFrame)+1, 1))
        print(frames)
        joints = _get_joints()
        pm.select(joints)

        ct = cmds.currentTime(q = True)
        for frame in frames:
            cmds.currentTime(frame)
            cmds.setKeyframe(at = attrs, t = [frame,frame])
        cmds.currentTime(ct)
        print("Scene setup successful!")