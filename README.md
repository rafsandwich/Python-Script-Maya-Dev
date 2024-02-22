Maya Pose Plugin
================

About
-----

A plugin for Maya to assist with pose alignment.
The plugin is built on top of the [tbtools](http://tb-animator.blogspot.com/p/hello.html)

Read about the Pose Creation flow in these slides: [C3D Pose Creation Manual](https://drive.google.com/open?id=1YhkFOV4YaKcDxvO12cgVc9gpZot1DLkkGMZivTOWaBE) [SLIGHTLY OUTDATED]

Installation
------------

Once inside the repository,

1. Drag `install.py` into Maya.
2. Restart Maya
3. In Maya, go to `Windows -> Settings/Preferences -> Hotkey Editor`. Choose category `Custom Scripts`. Open `SK_Tools_View` and select a shortcut for `Load Pose Viewer` (for instance, <kbd>⌘</kbd>+<kbd>L</kbd> or <kbd>Ctrl</kbd>+<kbd>L</kbd>)

Usage
-----

Check this video: [Workflow (Lucas)](https://drive.google.com/open?id=1QNCZ6AorhQA5cSujZQwyqMD019FgY9hw) [OLD VERSION]

There are some sample assets inside the `assets` folder.
The pose files that end with `_detected.json` are the output of our automatic pose detection pipeline.


Function Documentation - 0.3dev
---------------------------------------

------ 'Load Image (A, B, Kids)' ------

These allow the user to select a saved model image and display it in a Pose Panel. It creates a Viewport Camera and depending on the option chosen (A, B, Kids) aligns the camera appropriately. 


------ 'Four Pane Workspace' ------

This creates a four pane layout for users to use when posing, and displays the model images if they have already been loaded into the file previously. Useful for when your previous layout did not save or did not appear when reopening a maya file, or initialising it in a new one. 

If you want to reorganise the panes hands off, space bar (or maximise) into any of the four panes and then press the button again. This will put the current pane in the top left of the four, and reshuffle the other 3 automatically.


------ 'Refresh Images' (WIP) ------

This attempts to refresh the images in the ImagePlane's which is useful when loading in a scene and finding the same image duplicating itself in multiple panes or viewports, or not updating. Currently it may need to be called multiple times to get the desired results. (if this doesn't seem to work please try to wait between button presses, half a second or so)


------ 'Load FBX' ------

Loads in a .fbx object for the scene. 


------ 'Setup Scene' ------

Ensures the correct working units are being used, then checks if an FBX has been loaded and if yes turns on autokey & sets the keyframes for each joints translates & rotates, across all frames in the scene. Necessary for when you export your JSON data later.


------ 'Color override existing joints' ------

Makes it clear which side of the avatar is left & right. Blue - left, Red - right.


------ 'Load JSON data' ------

Loads in data from a .json and a rotation order file, then poses the avatar. This allows the avatar to be aligned in terms of whatever previous joint information exists in the .json. 


------ 'Load JSON rotation order' ------

A bit redundant but left in at the moment, as Load JSON data asks for both the json including pose data & the rotation order file. But allows the rotation order to be changed. 


------ 'Store initial translates' ------

Stores translation data of a bind pose, so we can later export joint translations. Click this before saving your JSON data.


------ 'Save JSON data' ------

Exports the currently selected keyframe's pose information in the .json format. 


------ 'Toggle Intersection Shader' ------

Allows the user to check for intersections when aligning the avatar. Toggling it for the first time will create a toon outline for the avatar and show intersections and subsequent toggles will turn it off / on. 
If you find you want to see the intersects more clearly, select the pfxToon1 created in the outliner and in 'Intersection Lines' you can change the 'Intersection line width' to 10, for example. 

Note: This shader significantly slows down Maya and is built to be toggled when the user wants to see intersects, and then toggled off. Rotations / translations could then be made and after it can be toggled again to check progress. Whilst it can be left on when adjusting the pose, understand you'll need a decent GPU!

Note 2: This toon shader highlights only the outline where intersections happen. It does not display the whole intersected volume. To see the volume you may want to use a different tool. Read [how to visualize volume intersections](https://tech.metail.com/the-stencil-buffer-and-how-to-use-it-to-visualize-volume-intersections/). View ./docs/ToonShader04.jpg for a comparison of a shader that shows the intersected volume (left) versus what the toon shader renders.

Note this is able & encouraged to be hotkeyed. In Maya, go to Windows > Settings/Preferences > Hotkey Editor,
in the following window Edit Hotkeys For: Custom Scripts,
drop down SK_Tools_View, and assign your hotkeys. 


------ 'Toggle FloorPlane' ------

Creates (or removes) a FloorPlane object in Maya to help with avatar orientation & levelling. Also has use when translating leg joints, to maintain proportions. 


------ 'Copy pose on keyframe' ------

Copies all pose information on the current keyframe.


------ 'Paste pose to keyframe' ------

If pose data has been copied, this will paste that data on the currently selected keyframe, overwriting what was there before. 


------ 'Reset to A pose' ------

Resets the pose on the current keyframe to the A pose shown in keyframe 0.


Function documentation written by Raphael Hall, last updated 11/01/2023.



Alternative pose saving and sharing
-----------------------

If we want to save a pose to reuse it later we can use a third party script. A very lightweight and flexible is PAIE, here is a link on how it works.

http://animationapprentice.blogspot.com/2015/01/the-free-paie-plugin-for-maya-how-it.html


-----------------------
changelog raf-plugin-improvements:
-----------------------

added load kids image button
added preset kids camera parameters

added load intersections functionality
removed extra clicks of assigning toon line
fixed bug where load intersections only worked directly after toon creation
fixed bug where load intersections wouldn't toggle off
fixed bug where load intersections being pressed before fbx was loaded broke it
added ability to use load intersections whether the mesh is selected / deselected or if a toon has been created / not created
added redirect focus after use of load intersections to allow user to see the intersections without an additional click (to deselect)
slightly changed intersection loader attributes to mimic the MV more closely
added customisable hotkey for toggling intersection shader

fixed bug where load json would load translations incorrectly, and would get progressively worse as it's used
allowed for future joint changes to not break load json
fixed issue where cancelling a loadjson would reset pose data, could be further improved

added four pane view creation
added WIP reload image functionality, needs to be called multiple times 
added floorPlane toggle to create and remove the object
store initial translations improved, now selects all bones and automates the jump to frame 0 and returns to current frame

added reset pose to A pose
added copy pose
added paste pose

automated all scene setup via button press, keys all frames joint rotates & translates and checks units are correct, autokeyframe is on

TODO bugs
fix reload image upon loading camera bug
    - investigate 'looking through camera' option on cameras, which seems to have an impact on this
    - temp fix created through mel scripts -> dependant on base camera setup
    - could we list all cameras, and then alter the command based on the cameras listed? first three?
        for each in cameras, but then what about ->pictureshape? we'd have to find the name of the picture shape, list imagePlane?
