import maya.cmds as cmds
import os
import logging
from pathlib import Path

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

class module_maker():
    def __init__(self):
        self.colours = {'red': "color:#F05A5A;",
                        'green': "color:#82C99A;",
                        'yellow': "color:#F4FA58;"
                        }
        self.platform = cmds.about(operatingSystem=True)
        self.maya_version = cmds.about(version=True)
        self.script_dir = str(Path(__file__).resolve().parent)
        self.python_paths = ['apps', 'apps/thirdParty/new', 'lib']
        self.maya_script_paths = ['scripts']
        self.xbmlang_paths = ['Icons']
        maya_module_dir = cmds.internalVar(userAppDir=True) + 'modules'
        self.module_file = os.path.join(maya_module_dir, 'SK_Tools.mod')
        if not os.path.isdir(maya_module_dir):
            logging.info('Creating maya module folder: ' + maya_module_dir)
            os.mkdir(maya_module_dir)

    def make_module_path(self):
        module_path = '+ PLATFORM:' \
                      + self.platform \
                      + ' MAYAVERSION:' \
                      + self.maya_version \
                      + ' Skelmesh_Tools 0.2 ' \
                      + self.script_dir + os.path.sep
        return module_path

    def make_module_data(self):
        lines = [self.make_module_path()]
        for paths in self.python_paths:
            lines.append('PYTHONPATH+:='+paths)
        for paths in self.maya_script_paths:
            lines.append('MAYA_SCRIPT_PATH+:='+paths)
        for paths in self.xbmlang_paths:
            lines.append('XBMLANGPATH+:='+paths)
        return lines

    def write_module_file(self):
        lines = self.make_module_data()
        with open(self.module_file, 'w') as f:
            f.write('\n'.join(lines))

    def install(self):
        result_message = "<h3>SK_Tools Installation result</h3>\t\n"
        try:
            self.write_module_file()
            result_message += "module file created <span style=\""+self.colours['green']+ "\">Successfully</span> \n"
            result_message += "module file location <span style=\""+self.colours['yellow']+ "\">" \
                              + self.module_file + "</span>\n\nEnjoy!"
            logging.info('Module file created: '+self.module_file)
            self.result_window()
        except Exception as e:
            logging.error('Failed to write module file: '+str(e))
            result_message += "<span style=\""+self.colours['red']+"\">Failed to write module file: "+str(e)+"</span>"

        message_state = cmds.optionVar(q='inViewMessageEnable')
        cmds.optionVar(intValue=("inViewMessageEnable", 1))
        cmds.inViewMessage(amg=result_message,
                         pos='botRight',
                         dragKill=True,
                         fadeOutTime=4.0,
                         fade=True)
        cmds.optionVar(intValue=("inViewMessageEnable", message_state))


    def result_window(self):
        if cmds.window("installWin", exists=True):
            cmds.deleteUI("installWin")
        window = cmds.window( title="Skelmesh Tools")
        layout = cmds.columnLayout(adjustableColumn=True )
        cmds.text(font="boldLabelFont",label="Skelmesh Tools installed")
        cmds.text(label="")
        cmds.text(label="Please restart Maya for everything to load")

        cmds.button( label='Close', command=('cmds.deleteUI(\"' + window + '\", window=True)') , parent=layout)
        cmds.setParent( '..' )
        cmds.showWindow( window )

def onMayaDroppedPythonFile(obj):
    module_maker().install()
