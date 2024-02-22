import maya.cmds as cmds
import startup as startup
cmds.evalDeferred("startup.initialise().load_module()")