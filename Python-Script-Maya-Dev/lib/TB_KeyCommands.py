'''NT Animation Tools is a toolset for animators

*******************************************************************************
    License and Copyright
    Copyright 2015-Tom Bailey
    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU Lesser General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU Lesser General Public License for more details.

    You should have received a copy of the GNU Lesser General Public License
    along with this program.  If not, see <http://www.gnu.org/licenses/>.

    send issues/ requests to brimblashman@gmail.com
    visit tb-animator.blogspot.com for "stuff"

    usage - to automatically add a bunch of commands for hotkeys
    import TB_keyCommands as TB_hotKeys
    TB_hotKeys.hotkey_tool().update_commands()

*******************************************************************************
'''

import pymel.core as pm

from TB_Hkey import TB_Hkey

SK_TOOLS = 'SK_Tools_View'
EXTRA = 'SK_Extra_commands'

def make_command_list():
    command_list = []

    # viewport tools
    cat = SK_TOOLS

    command_list.append(TB_Hkey(name='ZeroChannels', annotation='Zeroes all keyable channels except scale',
                                category=cat, command=['import SK_ZeroChannels as zeroChannels',
                                                       'zeroChannels.zeroAll_NoScale()']))
    command_list.append(TB_Hkey(name='ZeroRotOnly', annotation='Zeroes all rotations',
                                category=cat, command=['import SK_ZeroChannels as zeroChannels',
                                                       'zeroChannels.zeroRotOnly()']))

    command_list.append(TB_Hkey(name='cycle_rotation', annotation='cycle the rotation mode',
                                category=cat, command=['import TB_Manipulators as TB_M',
                                                       'from importlib import reload',
                                                       'reload(TB_M)',
                                                       'TB_M.manips().cycleRotation()']))
    command_list.append(TB_Hkey(name='cycle_translation', annotation='cycle the translation mode',
                                category=cat, command=['import TB_Manipulators as TB_M',
                                                       'from importlib import reload',
                                                       'reload(TB_M)',
                                                       'TB_M.manips().cycleTranslation()']))
    command_list.append(TB_Hkey(name='Load_PoseViewer', annotation='Launches the pose viewer tool',
                                category=cat, command=['import SK_ViewportSetup as SK_ViewportSetup',
                                                       'from importlib import reload',
                                                       'reload(SK_ViewportSetup)',
                                                       'SK_ViewportSetup.ViewportUI().showUI()']))

    command_list.append(TB_Hkey(name='toggleIntersectHK', annotation='Toggles the intersection shader',
                                category=cat, command=['import SK_Skelmesh as skelmesh',
                                                       'skelmesh.load_intersections()']))

                                                       
    return command_list


class hotkey_tool():
    def __init__(self):
        self.categories = [SK_TOOLS]
        self.command_list = make_command_list()
        self.name_list = self.get_command_names()
        self.SK_commands = self.get_existing_commands()
        self.extra_commands = pm.optionVar.get(EXTRA, '')
        self.remove_unneeded_ignore_entries()
        pass

    def update_commands(self):
        for commands in self.command_list:
            self.add_command(commands)

    def add_command(self, hkey=TB_Hkey()):
        if not pm.runTimeCommand(hkey.name, exists=True):
            pm.runTimeCommand(hkey.name)

        pm.runTimeCommand(
            hkey.name,
            edit=True,
            annotation=hkey.annotation,
            category=hkey.category,
            commandLanguage=hkey.language,
            command=hkey.command)

    def remove_unneeded_ignore_entries(self):
        needed_ignore_names = []
        if self.extra_commands and self.SK_commands:
            for items in self.extra_commands:
                if items in self.SK_commands:
                    needed_ignore_names.append(items)

        pm.optionVar.pop(EXTRA)
        for items in needed_ignore_names:
            pm.optionVar(stringValueAppend=(EXTRA, items))


    def get_existing_commands(self):
        _commands = []
        existing_commands = pm.runTimeCommand(query=True, userCommandArray=True)

        if existing_commands:
            # loop through existing commands
            for com in existing_commands:
                # filter out non awtools commands
                if pm.runTimeCommand(com, query=True, category=True) in self.categories:
                    _commands.append(com)
            return _commands


    def remove_bad_commands(self):
        commands_for_deletion = []
        for com in self.SK_commands:
            if com not in self.name_list:
                if com not in self.extra_commands:
                    commands_for_deletion.append(com)

        if commands_for_deletion:
            hotkey_cleanup(commands_to_delete=commands_for_deletion)

    def get_command_names(self):
        names = []
        for cmd in self.command_list:
            names.append(cmd.name)
        return names


class hotkey_cleanup():
    def __init__(self, commands_to_delete=[]):
        self.command_list = commands_to_delete
        self.showUI()
        pass

    def remove_hotkey(self, command_name, layout_name):
        pm.runTimeCommand(command_name, edit=True, delete=True)
        pm.deleteUI(layout_name)

    def ignore_hotkey(self, command_name, layout_name):
        pm.optionVar(stringValueAppend=(EXTRA, command_name))
        pm.rowLayout(layout_name, edit=True, bgc=(0.2, 0.6, 0.2))

    def command_widget(self, command_name="", parent=""):
        rLayout = pm.rowLayout(numberOfColumns=4, adjustableColumn=2, parent=parent)
        pm.text(label="command:", parent=rLayout)
        pm.text(label=str(command_name), parent=rLayout)

        pm.button(label="keep", parent=rLayout, command=lambda *args: self.ignore_hotkey(command_name, rLayout))
        pm.button(label="delete", parent=rLayout, command=lambda *args: self.remove_hotkey(command_name, rLayout))

    def showUI(self):
        window = pm.window(title="Hotkey check!")
        layout = pm.columnLayout(adjustableColumn=True)
        pm.text(font="boldLabelFont", label="Uknown or outdated commands")
        pm.text(label="")

        pm.text(label="your own commands saved in SKTools categories")
        pm.text(label="will show up here. If you wish to keep them,")
        pm.text(label="press the 'keep' button and they won't appear")
        pm.text(label="in this window again.")
        pm.text(label="")
        pm.text(label="If you didn't make it and it's here it means it")
        pm.text(label="is an old or outdated hotkey and should be removed")
        pm.text(label="")

        for items in self.command_list:
            self.command_widget(command_name=items, parent=layout)

        # pm.button( label='Delete all', parent=layout)
        pm.button(label='Close', command=('cmds.deleteUI(\"' + window + '\", window=True)'), parent=layout)
        pm.setParent('..')
        pm.showWindow(window)
