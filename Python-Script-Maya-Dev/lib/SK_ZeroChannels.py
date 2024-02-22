import pymel.core as pm
import maya.mel as mel

def zeroAllKeyable():
    sel = pm.selected()

    for obj in sel:
        for each in pm.listAttr(obj,k=True):
            pm.setAttr(obj+ "."+each, 0 )


def zeroAll_NoScale():
    sel = pm.selected()
    for obj in sel:
        for each in pm.listAttr(obj, k=True):
            if each =="scaleY" or each =="scaleX" or each =="scaleZ" or each == "visibility":
                pass
            else:
                pm.setAttr(obj + "." + each, 0)

def zeroRotOnly():
    sel = pm.selected()
    for obj in sel:
        for each in pm.listAttr(obj, k=True):
            if each =="rotateY" or each =="rotateX" or each =="rotateZ":
                pm.setAttr(obj + "." + each, 0)
            else:
                pass