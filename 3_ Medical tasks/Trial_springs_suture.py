# Required import for python
import Sofa
import numpy as np
import Sofa.SofaDeformable
import models
import controllers


# Data
#scale3d_skin="0.2 0.3 1" #thin
scale3d_skin="1 0.6 1"
scale3d_needle="5 5 5"
scale3d_thread="0.5 0.5 0.5"

pointPosition_onNeedle="-6.98 0.02 0.05" #N: 5,5,5

GeomagicPosition="0 20 15"
skinVolume_fileName="C:\sofa\src\Chiara\mesh\skin_30201"
needleVolume_fileName="C:\sofa\src\Chiara\mesh\suture_needle.obj"
threadVolume_fileName="mesh/threadCh2"

# Data
skin_youngModulus=300
thread_youngModulus=2000
skin_poissonRatio=0.49
thread_poissonRatio=0.8


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
    root.gravity=[0, 0, -15]
    root.dt=0.01

    # Required plugins
    root.addObject('RequiredPlugin', pluginName="SofaBaseMechanics SofaBaseTopology  Geomagic SofaBoundaryCondition  SofaConstraint SofaDeformable SofaEngine SofaGeneralLoader SofaGeneralObjectInteraction SofaGeneralSimpleFem SofaHaptics SofaImplicitOdeSolver SofaLoader SofaMeshCollision SofaOpenglVisual SofaRigid SofaSimpleFem SofaSparseSolver SofaUserInteraction SofaTopologyMapping ")

    # Collision pipeline
    root.addObject('CollisionPipeline', depth="6", verbose="0", draw="0")

    # Forces
    root.addObject('BruteForceDetection', name="detection")
    root.addObject('DefaultContactManager', name="CollisionResponse", response="FrictionContact")
    root.addObject('LocalMinDistance', name="proximity", alarmDistance="0.3", contactDistance="0.05", angleCone="0.0")

    # Animation loop
    root.addObject('FreeMotionAnimationLoop')

    # Constraint solver
    LCPConstraintSolver=root.addObject('LCPConstraintSolver', tolerance="0.001", maxIt="1000")

    # View
    root.addObject('OglViewport', screenPosition="0 0", cameraPosition="-0.00322233 -20.3537 18.828", cameraOrientation="0.418151 -6.26277e-06 -0.000108372 0.908378")


    # Define the variables
    geomagic=True
    carving=False

    #################### CARVING ########s#####################################
    if carving==True:
        root.addObject('CarvingManager', active="true", carvingDistance="0.1")
    ##########################################################################

    # Add skin
    models.Skin(parentNode=root, name='SkinLeft', rotation=[0.0, 0.0, 0.0], translation=[0.0, 0.0, 0.0], 
    scale3d=scale3d_skin, fixingBox=[-0.1, -0.1, -2, 10, 20, 0.1], borderBox=[7, -0.1, -2, 10, 20, 1], 
    importFile=skinVolume_fileName, carving=carving, task="Suture")

    models.Skin(parentNode=root, name='SkinRight', rotation=[0.0, 0.0, 0.0], translation=[11, 0, 0], 
    scale3d=scale3d_skin, fixingBox=[11, -0.1, -2, 22, 20, 0.1], borderBox=[11, -0.1, -2, 14, 20, 1],
    importFile=skinVolume_fileName, carving=carving, side=1, task="Suture") 

    #################### GEOMAGIC TOUCH DEVICE ##################################################################
    if geomagic==True:

        root.addObject('GeomagicDriver', name="GeomagicDevice", deviceName="Default Device", 
        scale="1", drawDeviceFrame="1", drawDevice="1", positionBase="10 20 10",  orientationBase="0.707 0 0 0.707")
        
        models.GeomagicDevice(parentNode=root, name='Omni')

    #############################################################################################################

    # Add needle
    models.SutureNeedle(parentNode=root, name='SutureNeedle', rotation=[0.0, 0.0, 0.0], translation=[55, 30, 5],     
    scale3d=scale3d_needle, fixingBox=None, importFile=needleVolume_fileName, carving=carving, geomagic=geomagic)

    # # Add thread: not added to Geo yet
    # models.Thread(parentNode=root, name='SutureThread', rotation=[-90, 90, 0], translation=[10, 10, 5], 
    # scale3d=[0.5, 0.5, 0.6],  fixingBox=None, importFile=threadVolume_fileName, geomagic=geomagic)

    # Add contact listener
    root.addObject(controllers.SutureTrainingContactController(name="MyController", rootNode=root))

    # Add training spheres: add when necessary
    models.sphere(parentNode=root, name="Sphere1", translation=[8, 3.0, 1.0], scale3d="1.5 1.5 1.5", color="0.0 0.5 0.0")
    models.sphere(parentNode=root, name="Sphere2", translation=[8, 13.0, 1.0], scale3d="1.5 1.5 1.5", color="0.0 0.5 0.0")
    models.sphere(parentNode=root, name="Sphere3", translation=[12, 7.0, 1.0], scale3d="1.5 1.5 1.5", color="0.0 0.5 0.0")
    models.sphere(parentNode=root, name="Sphere4", translation=[12, 17.0, 1.0], scale3d="1.5 1.5 1.5", color="0.0 0.5 0.0")


    return root


if __name__ == '__main__':
    main()
