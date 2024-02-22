import SK_BasicUI as SK_UI
import SK_ImagePlane as SK_ImagePlane
import SK_Skelmesh as SK_Skelmesh
import Qt.QtWidgets as QtWidgets
#from Qt import QtWidgets
from presets import CameraPresets
from importlib import reload

reload(SK_ImagePlane)
reload(SK_Skelmesh)
reload(SK_UI)


# Defaults
CTRL_BTN = "ctrl_btn"
CTRL_INPUT_NAME ="line_name"
NAMESPACE_SPLITTER = ":"
LOAD_IMAGE_BTN = "Load Image"
LOAD_FBX_BTN = "Load FBX"


class ViewportUI(SK_UI.SK_QWindow):
    def __init__(self, title="Maya Posing Plugin"):
        super(ViewportUI, self).__init__()
        self.setWindowTitle(title)
        self.viewport_Layout = QtWidgets.QVBoxLayout()
        self.setLayout(self.viewport_Layout)
        self.rotationOrder = {}
        self.original_translations = {}

        self.sections = {
            "viewport": {
                "title": "Workspace Panel",
                "buttons": {
                    "loadA": {
                        "name": "Load Image (A)",
                        "action": lambda: SK_ImagePlane.pose_viewport(CameraPresets.get('A_v0'))
                    },
                    "loadB": {
                        "name": "Load Image (B)",
                        "action": lambda: SK_ImagePlane.pose_viewport(CameraPresets.get('B_v0'))
                    },
                    "loadKids": {
                        "name": "Load Image (Kids)",
                        "action": lambda: SK_ImagePlane.pose_viewport(CameraPresets.get('Kids_v0'))
                    },
                    "four pane": {
                        "name": "Four Pane Workspace",
                        "action": lambda: SK_ImagePlane.fourPane()
                    },
                    "refresh images": {
                        "name": "Refresh Images",
                        "action": lambda: SK_ImagePlane.refreshImages()
                    }
                }
            },

            "skelmesh": {
                "title": "Posing Panel",
                "buttons": {
                    "load": {
                        "name": "Load FBX",
                        "action": lambda: SK_Skelmesh.skelmesh()
                    },
                    "sceneSetup": {
                        "name": "Setup scene",
                        "action": lambda: SK_Skelmesh.sceneSetup()
                    },
                    # "constraint":{
                    #     "name": "Create controls",
                    #     "action": lambda: SK_Skelmesh.create_controlling_chain()
                    # },
                    "storeTranslates": {
                        "name": "Store initial translates",
                        "action": getattr(self, "store_translates")
                    },
                    "save_pose": {
                        "name": "Save JSON data",
                        "action": lambda: SK_Skelmesh.file_save(self.original_translations)
                    },
                    "json": {
                        "name": "Load JSON data",
                        "action": lambda: SK_Skelmesh.load_json_data(self.rotationOrder)
                    },
                    "rotOrder": {
                        "name": "Load JSON Rotation Order",
                        "action": getattr(self, "load_rot_order")
                    },
                    "color joints": {
                        "name": "Color override existing joints",
                        "action": lambda: SK_Skelmesh.color_joints()
                    },
                    "load intersects": {
                        "name": "Toggle Intersection Shader",
                        "action": lambda: SK_Skelmesh.load_intersections()
                    },
                    "floorPlane": {
                        "name": "Toggle FloorPlane",
                        "action": lambda: SK_Skelmesh.toggleFloorPlane()
                    },
                    "copyPose": {
                        "name": "Copy pose on keyframe",
                        "action": lambda: SK_Skelmesh.copyPose()
                    },
                    "pastePose": {
                        "name": "Paste pose to keyframe",
                        "action": lambda: SK_Skelmesh.pastePose()
                    },
                    "resetPose": {
                        "name": "Reset to A pose",
                        "action": lambda: SK_Skelmesh.resetPose()
                    }
                }
            }
        }


    def UI(self):
        """
        Initializes the UI with default values
        :return:
        """
        self.build_main_layout()


    def build_main_layout(self):
        """
        Builds the main window with all its sections
        :return:
        """
        for section in self.sections:
            print (section)
            title = self.sections[section]["title"]
            buttons = self.sections[section]["buttons"]
            self.viewport_Layout.addWidget(self.select_files_widget(title, buttons))


    def select_files_widget(self, title, buttons):

            menuBar = QtWidgets.QMenuBar()
            section_main_widget = QtWidgets.QGroupBox(title)
            section_main_layout = QtWidgets.QVBoxLayout()
            section_main_widget.setLayout(section_main_layout)

            # Main widget and layout to load items
            section_widget = QtWidgets.QWidget()
            section_layout = QtWidgets.QGridLayout()


            # Buttons and execution #
            for button in buttons:
                print ("Loading button >> "),
                print (button)
                section_button = QtWidgets.QPushButton(buttons[button]["name"])
                print (self)
                section_button.clicked.connect(buttons[button]["action"])
                section_main_layout.addWidget(section_button)

            section_widget.setLayout(section_layout)
            section_main_layout.addWidget(section_widget)



            return section_main_widget

    def load_rot_order(self):
        """
        Loads and stores the current rotationOrder
        """
        self.rotationOrder = SK_Skelmesh.load_json_rotOrder()
        return self.rotationOrder

    def store_translates(self):
        """
        Loads and stores the original translations on bones
        :return:
        """
        self.original_translations = SK_Skelmesh.store_translations()
        return self.original_translations
