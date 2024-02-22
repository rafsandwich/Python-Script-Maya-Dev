'''TB Animation Tools is a toolset for animators

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

*******************************************************************************
'''

__author__ = 'user'
import pymel.core as pm


class optionVar_utils():
    def __init__(self):
        pass

    @staticmethod
    def set_option_var(variable, value):
        pm.optionVar(stringValue=(variable, value))


    @staticmethod
    def get_option_var(variable):
        if not pm.optionVar[variable]:
            pm.optionVar(stringValue=(variable, "None"))
        return pm.optionVar.get(variable, False)

    @staticmethod
    # list from option var
    def cycleOption(option_name="", full_list=[], current=int(), default=""):
        # get list from optionvar array
        optionVar_list = pm.optionVar.get(option_name, [default])
        print("Initial List : ", end=' ')
        print(optionVar_list)
        if not optionVar_list:
            optionVar_list = [default]
            print("Gets set to default")
        # find the current index in the full list
        current_name = full_list[current]

        # check if the current name is in our option var list
        if current_name in optionVar_list:
            index = optionVar_list.index(current_name) + 1
            print("This is what it should go to : ", end=' ')
            print(index)
            # loop around the list
            print("This is the list : ", end=' ')
            print(optionVar_list)
            name = optionVar_list[index % len(optionVar_list)]
        else:
            print("current value not in option var list, set to first")
            name = optionVar_list[0]
        index = full_list.index(name)
        print(name, index)
        return index, name


def set_default_values():
    # from zshotmask_ui import ZShotMask
    from .TB_Manipulators import manips
    if pm.optionVar.get('tb_firstRun', True):

        print("# INFO: Setting up option vars / FirstRun ")

        pm.optionVar(intValue=(manips().translate_optionVar+"_msg", 1))
        pm.optionVar(stringValue=(manips().translate_messageVar+"_msg", 'topLeft'))

        pm.optionVar(intValue=(manips().rotate_optionVar+"_msg", 1))
        pm.optionVar(stringValue=(manips().rotate_messageVar+"_msg", 'topLeft'))

        pm.optionVar(intValue=(manips().key_optionVar+"_msg", 1))
        pm.optionVar(stringValue=(manips().key_messageVar+"_msg", 'topLeft'))

        # pm.optionVar(intValue=(ZShotMask.OPT_VAR_STAGE + "_msg", 1))
        # pm.optionVar(stringValue=(ZShotMask.OPT_VAR_MESSAGE + "_msg", 'topLeft'))

        default_moves = ['Object', 'Local', 'World']
        pm.optionVar.pop(manips().translate_optionVar)
        for modes in default_moves:
            pm.optionVar(stringValueAppend=(manips().translate_optionVar, modes))

        default_rotations = ['Local', 'World', 'Gimbal']
        pm.optionVar.pop(manips().rotate_optionVar)
        for modes in default_rotations:
            pm.optionVar(stringValueAppend=(manips().rotate_optionVar, modes))

        default_keys = ['spline', 'linear', 'step']
        pm.optionVar.pop(manips().key_optionVar)
        for modes in default_keys:
            pm.optionVar(stringValueAppend=(manips().key_optionVar, modes))

        # default_stages = ['Previs', 'Blocking', 'Animation', 'Polish', 'Final']
        # pm.optionVar.pop(ZShotMask.OPT_VAR_STAGE)
        # for modes in default_stages:
        #     pm.optionVar(stringValueAppend=(ZShotMask.OPT_VAR_STAGE, modes))

        return True

    else:
        return False