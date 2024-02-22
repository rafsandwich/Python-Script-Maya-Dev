import pymel.core as pm
from pymel.all import *
import maya.cmds as cmds
import maya.mel as Mm
import logging

def create_camera(name):
    """
    Creates a camera with the desired settings
    :param name:
    :param settings:
    :return:
    """
    try:
        print("Creating camera >> " + name)
        camera = pm.camera(n=name)[0]
        return camera
    except:
        cmds.warning("Error creating camera")


def create_panel(camera, image_size):
    MyLabel = 'Pose Panel'
    window = cmds.window(title=MyLabel, iconName=MyLabel, w=int(image_size[0] / 2), h=int(image_size[1] / 1.85))
    cmds.frameLayout(lv=0)
    model_panel = pm.modelPanel(l=MyLabel, me=True)
    cmds.showWindow()

    panels = cmds.getPanel(all=True)

    for panel in panels:
        if MyLabel == cmds.panel(panel, q=True, label=True):
            myPanel = panel
            print(('Found: ' + MyLabel))

    return model_panel


def create_image_plane(name, camera, image):
    imagePlane = pm.imagePlane(n=name, fileName=image)[0]
    imagePlane.setCamera(camera)
    return imagePlane

def fourPane():
    '''
    Creates a four pane view through MEL script and updates the images
    Only useful if the Camera_Base files are being used
    TEMP fix, TODO list cameras and select, change to python, find ImageShape for each

    returns none
    '''
    Mm.eval('source "showEditor.mel"')
    pm.select("Viewport_Camera1_v0_image")
    Mm.eval('FourViewArrangement;')
    Mm.eval('lookThroughModelPanel "persp" modelPanel4')
    Mm.eval('lookThroughModelPanel "Viewport_Camera1_v0_image" modelPanel3;')
    Mm.eval('lookThroughModelPanel "Viewport_Camera2_v1_image" modelPanel2;')
    Mm.eval('lookThroughModelPanel "Viewport_Camera3_v7_image" modelPanel1;')
    refreshImages()

    #Mm.eval('AEimagePlaneViewUpdateCallback("pictureShape2");')
    #Mm.eval('select -r Viewport_Camera3_v7_imageShape->picture3 ;')
    #Mm.eval('select -r Viewport_Camera2_v1_imageShape->picture2 ;')
    #Mm.eval('select -r Viewport_Camera1_v0_imageShape->picture1 ;') these update when called multiple times
    
    print("Four Pane view loaded, images refreshed")

def loadFile():
    img_file = cmds.fileDialog2(cap='Select the viewport image', fm=1)[0]
    return img_file

def refreshImages():
    Mm.eval('source "showEditor.mel"')
    Mm.eval('select -r Viewport_Camera1_v0_image->pictureShape2 ;')
    Mm.eval('setAttr Viewport_Camera1_v0_imageShape->pictureShape2.displayOnlyIfCurrent on;optionMenu -edit -enable true AELookThroughCameraMenu;')
    Mm.eval('select -r Viewport_Camera2_v1_image->pictureShape3 ;')
    Mm.eval('setAttr Viewport_Camera2_v1_imageShape->pictureShape3.displayOnlyIfCurrent on;optionMenu -edit -enable true AELookThroughCameraMenu;')
    Mm.eval('select -r Viewport_Camera3_v7_image->pictureShape4 ;')
    Mm.eval('setAttr Viewport_Camera3_v7_imageShape->pictureShape4.displayOnlyIfCurrent on;optionMenu -edit -enable true AELookThroughCameraMenu;')
    Mm.eval('refreshAE;')
    print("Images refreshed, repeat if some images are still incorrect ")

def setResolution(width=1920, height=1080, pixelAspect=1.0):
    '''
    Sets render resolution properly.

    @param width- The width of the resolution.
    @param height- The width of the resolution.
    @param pixelAspect- The pixel aspect to set the defaultResolution to.

    Returns None
    '''
    # Calculates the device aspect since pixel aspect isn't an actual attribute.
    device_aspect = float(width * pixelAspect) / float(height)

    # Set the Lock Device Aspect Ratio. IMPORTANT!
    # If you don't do this it won't work.
    cmds.setAttr("defaultResolution.lockDeviceAspectRatio", 1)

    # Set width, height, and aspect ratio.
    cmds.setAttr("defaultResolution.width", width)
    cmds.setAttr("defaultResolution.height", height)
    cmds.setAttr("defaultResolution.deviceAspectRatio", device_aspect)


def set_Render_resolution(image_size):
    # get resolution values
    print("Old render values were >> ", end=' ')
    print(pm.getAttr("defaultResolution.width"), end=' ')
    print(pm.getAttr("defaultResolution.height"), end=' ')
    print("Setting them to >> ", end=' ')
    print(image_size)
    setResolution(int(image_size[0]), int(image_size[1]), 1)


def set_camera_image_sizes(cam, img, translation, rotation):
    """
    sets the  camera and image plane parameters
    :param cam:
    :param img:
    :return:
    """
    print("Setting camera parameters >>> ", end=' ')
    print(cam, end=' ')

    cam.setFocalLength(66.9019)
    camX = 1.260
    camY = 0.709

    cam.setDisplayGateMask(True)
    cam.setFilmFit('horizontalFilmFit')
    cam.setDisplayResolution(True)
    cam.setHorizontalFilmAperture(camX)
    cam.setVerticalFilmAperture(camY)
    pm.setAttr(cam.displayGateMaskColor, 0, 0, 0, type='double3')
    pm.setAttr(cam.displayGateMaskOpacity, 1)
    pm.setAttr(cam.translateX, translation[0])
    pm.setAttr(cam.translateY, translation[1])
    pm.setAttr(cam.translateZ, translation[2])
    pm.setAttr(cam.rotateX, rotation[0])
    pm.setAttr(cam.rotateY, rotation[1])
    pm.setAttr(cam.rotateZ, rotation[2])

    pm.setAttr(img.depth, 200)
    pm.setAttr(img.sizeX, camX)
    print("Camera X", end=' ')
    print(camX)
    print("Image Sizes", end=' ')
    print(img.getImageSize()[0])
    print(img.getImageSize()[1])
    pm.setAttr(img.sizeY, (camX / img.getImageSize()[0]) * img.getImageSize()[1])

    print(("dimensions >> " + str(camX) + " " + str(camY) + "Focal Length >> "), end=' ')
    print(cam.getFocalLength())


def pose_viewport(cameraParameters):

    #xIterator = 0
    #while xIterator <= 2:

    cmds.currentUnit(linear='m')

    try:
        viewport_pic = loadFile()
        cam = create_camera("Viewport_Camera")
        print(cam.getShape())
        img_Plane = create_image_plane("picture", cam, viewport_pic)
        print(img_Plane.getShape())
        set_Render_resolution((img_Plane.getImageSize()))
        translation = cameraParameters.get('translation', [0, 0, 3])
        rotation = cameraParameters.get('rotation', [0, 0, 0])
        set_camera_image_sizes(cam, img_Plane, translation, rotation)
        panel = create_panel(cam, img_Plane.getImageSize())
        print("locators set to false in ", end=' ')
        print(panel)
        cmds.modelEditor(panel, edit=True, lc=False, gr=False, jx=True, da="smoothShaded", xr=True)
    except Exception as e:
        logging.error('pose_viewport: ' + str(e))
        cmds.warning("Please select an image")

    print(img_Plane.getWidth())
    print ("tried")
    cmds.currentUnit(linear='cm')
        
        #xIterator +=1

    #TODO fix necessary click to (reload?) orientation image 
    #Viewport_CameraShape1->picture1
    #Viewport_Camera1

    # panel.setLocators(False)