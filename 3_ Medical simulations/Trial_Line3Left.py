# Required import for python
import Sofa
import numpy as np
import Sofa.SofaDeformable
import suture_models
#from goto import goto, label
import subprocess
import ctypes
# Data


skinVolume_fileName="mesh/cube.obj" #03 troppo lento


# Choose in your script to activate or not the GUI
USE_GUI = True


def main():
    import SofaRuntime
    import Sofa.Gui
    import Sofa.Core
    SofaRuntime.importPlugin("SofaComponentAll")
    SofaRuntime.importPlugin("SofaOpenglVisual")
    SofaRuntime.importPlugin("SofaImplicitOdeSolver")

    root = Sofa.Core.Node("root")
    createScene(root)

    Sofa.Simulation.init(root)

    if not USE_GUI:
        for iteration in range(10):
            Sofa.Simulation.animate(root, root.dt.value)
    else:
        Sofa.Gui.GUIManager.Init("myscene", "qglviewer")
        Sofa.Gui.GUIManager.addGUI(root, __file__)
        Sofa.Gui.GUIManager.SetDimension(1080, 1080)
        Sofa.Gui.GUIManager.MainLoop(root)
        Sofa.Gui.GUIManager.closeGUI()


def createScene(root):


    # Define root properties
    root.gravity=[0, 0, 0]
    root.dt=0.01

    # Required plugins
    root.addObject('RequiredPlugin', pluginName="SofaBaseMechanics SofaBaseTopology  Geomagic SofaCarving SofaBoundaryCondition  SofaConstraint SofaDeformable SofaEngine SofaGeneralLoader SofaGeneralObjectInteraction SofaGeneralSimpleFem SofaHaptics SofaImplicitOdeSolver SofaLoader SofaMeshCollision SofaOpenglVisual SofaRigid SofaSimpleFem SofaSparseSolver SofaUserInteraction SofaTopologyMapping SofaValidation")
    #root.addObject('VisualStyle', displayFlags="showInteractionForceFields")
    root.addObject('OglLabel', label="FOLLOW THE LINE", x=20, y=20, fontsize=30, selectContrastingColor="1")
    #root.addObject('ViewerSetting', fullscreen="true")
    root.addObject('BackgroundSetting', color="0.3 0.5 0.8")

    # Collision pipeline
    root.addObject('CollisionPipeline', depth="6", verbose="0", draw="0")

    # Forces
    root.addObject('BruteForceDetection', name="detection")
    root.addObject('DefaultContactManager', name="CollisionResponse", response="FrictionContact")
    root.addObject('LocalMinDistance', name="proximity", alarmDistance="2", contactDistance="1.2", angleCone="0.0")

    # Animation loop
    root.addObject('FreeMotionAnimationLoop')

    # Constraint solver
    LCPConstraintSolver=root.addObject('LCPConstraintSolver', tolerance="0.001", maxIt="1000")

    # View
    root.addObject('OglViewport', screenPosition="0 0", cameraPosition="-0.00322233 -20.3537 18.828", cameraOrientation="0.418151 -6.26277e-06 -0.000108372 0.908378")

    # Add geomagic drivers

    root.addObject('GeomagicDriver', name="GeomagicDeviceLeft", deviceName="Left Device", scale="1", drawDeviceFrame="1", 
    drawDevice="0", positionBase="2 2 10",  orientationBase="0.707 0 0 0.707")#, forceFeedBack="@StraightNeedleLeft/LCPFFNeedle")

    # Add geomagic nodes
    GeomagicDevice(parentNode=root, name='OmniLeft', position="@GeomagicDeviceLeft.positionDevice")
    
    # Add needles
    suture_models.StraightNeedleLeft(parentNode=root, name='StraightNeedleLeft', monitor=False, position="@GeomagicDeviceLeft.positionDevice", external_rest_shape='@../OmniLeft/DOFs') # To fall on sphere: dx=12, dy=3, dz=6

    line(parentNode=root, name="line")

    
    
## This function defines a geomagic
# @param parentNode: parent node of the skin patch
# @param name: name of the behavior node
# @param rotation: rotation 
# @param translation: translation
def GeomagicDevice(parentNode=None, name=None, position=None):
    name=parentNode.addChild(name)
    name.addObject('MechanicalObject', template="Rigid3", name="DOFs", position=position)
    name.addObject('MechanicalStateController', template="Rigid3", listening="true", mainDirection="-1.0 0.0 0.0")


def line(parentNode=None, name=None, translation=[0.0, 5.0, 0.0], scale3d=[0.0, 0.0, 0.0], color=[0.0, 0.0, 0.0]):

    name=parentNode.addChild(name)
    name.addObject('MeshObjLoader' ,name="meshLoader_3", filename="mesh/cube.obj", translation=translation, scale3d="10 0.3 0.3", rotation="0 -30 0 3")#, handleSeams="1" )
    name.addObject('OglModel' ,name="VisualOGL" ,src="@meshLoader_3",material="Default Diffuse 1 0 0.5 0 1 Ambient 1 0 0.1 0 1 Specular 0 0 0.5 0 1 Emissive 0 0 0.5 0 1 Shininess 0 45")
    