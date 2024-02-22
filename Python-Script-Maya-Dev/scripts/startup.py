import logging

logging.info("*******************************")
logging.info("  SK_Tools module loading")
logging.info("*******************************")

from importlib import reload
import pymel.core as pm
try:
    import TB_KeyCommands as SK_hotkeys
    import TB_OptionVars as TB_OptionVars
except Exception as e:
    logging.error("Failed to import TB libs (SK_Tools): {}".format(e))

class initialise():
    def __init__(self):
        pass

    def check_for_updates(self):
        """
        Not implemented for this version
        :return:
        """
        pass
    
    def scene_setup(self):
        """
        Sets the scene as soon as maya opens.
        :return:
        """
        pm.currentUnit(time='ntsc')
        pm.currentUnit(linear='cm')

    def load_shelf(self):
        """
        would load a shelf
        :return:
        """
        pass

    def load_hotkeys(self):
        """
        Loads hotkeys and removes corrupted ones
        :return:
        """
        reload(SK_hotkeys)
        SK_hotkeys.hotkey_tool().update_commands()
        SK_hotkeys.hotkey_tool().remove_bad_commands()

    def initOptionVars(self):
        """
        Initialises TB_OptionVars, for Manipulator cycle
        :return:
        """
        if TB_OptionVars.set_default_values():
            pm.optionVar(intValue=('tb_firstRun', 0))
        else:
            pass

    def load_module(self):
        try:
            self.scene_setup()
            print ("##############################")
            print ("# INFO:  SK_Tools Initialised")
            print ("# INFO:  SCENE Initialised")
        except Exception as e:
            print ("# WARNING:  Failed to Initialise scene_setup: "),
            print (e)

        try:
            self.initOptionVars()
            print ("# INFO:  Option Vars SET")
        except Exception as e:
            print ("# WARNING:  Option Vars failed to set: "),
            print (e)

        try:
            self.load_hotkeys()
            print ("# INFO:  Hotkeys Loaded")
        except Exception as e:
            print ("# WARNING:  Failed to load Hotkeys"),
            print (e)

        print ("##############################")