'''
Snap to an object
'''
import maya.cmds as cmds
import pymel.core as pm


def _snap_to_object(mode):
    '''
    Snaps the last selected object to the first selected One
    '''
    nodes = cmds.ls(sl=True, fl=True)
    if len(nodes) > 1:
        location = nodes[-1]
        locators = []

        if mode == 1:
            for node in nodes:
                if ".vtx" in node:
                    currentLocator = cmds.spaceLocator()[0]
                    locators.append(currentLocator)
                    vtxPos = cmds.xform(node, q=True, ws=True, t=True)
                    pm.setAttr(currentLocator + ".translate", vtxPos)

            if len(locators) > 0:
                cmds.select(locators, r=True)
                cmds.select(location, add=True)

            constraints = cmds.pointConstraint()
            translateVector = pm.getAttr(location + ".translate")
            cmds.delete(constraints)
            pm.setAttr(location + ".translate", translateVector)

            if len(locators) > 0:
                cmds.delete(locators)

        if mode == 2:
            # Orient Constraint #
            constraints = cmds.orientConstraint()
            rotateVector = pm.getAttr(location + ".rotate")
            cmds.delete(constraints)
            pm.setAttr(location + ".rotate", rotateVector)

        if mode == 3:
            # Parent Constraint #
            constraints = cmds.parentConstraint()
            translateVector = pm.getAttr(location + ".translate")
            rotateVector = pm.getAttr(location + ".rotate")
            cmds.delete(constraints)
            pm.setAttr(location + ".translate", translateVector)
            pm.setAttr(location + ".rotate", rotateVector)