# Required import for python
import Sofa
import numpy as np
import Sofa.SofaDeformable
import models
import controllers


# Data
scale3d_skin="0.5 0.5 1"
scale3d_needle="5 5 5"
scale3d_thread="0.5 0.5 0.6"

pointPosition_onNeedle="-6.98 0.02 0.05" #N: 5,5,5

GeomagicPosition="0 20 15"
skinVolume_fileName="C:\sofa\src\Chiara\mesh\skinVolume_thin"
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

    root.addObject('RequiredPlugin', pluginName="SofaBaseMechanics SofaBaseTopology  Geomagic SofaBoundaryCondition  SofaConstraint SofaDeformable SofaEngine SofaGeneralLoader SofaGeneralObjectInteraction SofaGeneralSimpleFem SofaHaptics SofaImplicitOdeSolver SofaLoader SofaMeshCollision SofaOpenglVisual SofaRigid SofaSimpleFem SofaSparseSolver SofaUserInteraction SofaTopologyMapping ")
    #root.addObject('RequiredPlugin', pluginName="SofaCarving")
    # Collision pipeline
    root.addObject('CollisionPipeline', depth="6", verbose="0", draw="0")

    # Forces
    root.addObject('BruteForceDetection', name="detection")
    root.addObject('DefaultContactManager', name="CollisionResponse", response="FrictionContact")
    root.addObject('LocalMinDistance', name="proximity", alarmDistance="0.5", contactDistance="0.05", angleCone="0.0")

    # Animation loop
    root.addObject('FreeMotionAnimationLoop')

    # Constraint solver
    LCPConstraintSolver=root.addObject('LCPConstraintSolver', tolerance="0.001", maxIt="1000")




    # Define the variables
    geomagic=False
    carving=False

    #################### CARVING ########s#####################################
    if carving==True:
        root.addObject('CarvingManager', active="true", carvingDistance="0.1")
    ##########################################################################

    # Add skin
    models.Skin(parentNode=root, name='SkinLeft', rotation=[0.0, 0.0, 0.0], translation=[0.0, 0.0, 0.0], 
    scale3d=scale3d_skin, fixingBox=[-0.1, -0.1, -2, 50, 50, 0.1], 
    importFile=skinVolume_fileName, carving=carving, borderBox=[45, -0.1, -2, 50, 50, 1])

    models.Skin(parentNode=root, name='SkinRight', rotation=[0.0, 0.0, 0.0], translation=[51, 0, 0], 
    scale3d=scale3d_skin, fixingBox=[51, -0.1, -2, 101, 50, 0.1],
    importFile=skinVolume_fileName, carving=carving, side=1, borderBox=[51, -0.1, -2, 56, 50, 1]) 

    #################### GEOMAGIC TOUCH DEVICE ##################################################################
    if geomagic==True:
        root.addObject('GeomagicDriver', name="GeomagicDevice", deviceName="Default Device", 
        scale="1", drawDeviceFrame="1", drawDevice="1", positionBase="-11 5 8",  orientationBase="0.707 0 0 0.707")
        # Add Geomagic Touch
        models.GeomagicDevice(parentNode=root, name='Omni')
    
        # Add needle
        # models.SutureNeedleGeo(parentNode=root, name='SutureNeedle', rotation=[0.0, 0.0, 0.0], translation=[25, 45, 5],     
        # scale3d=scale3d_needle, fixingBox=None, importFile=needleVolume_fileName, carving=carving, geomagic=geomagic)
    #############################################################################################################

    # Add needle
    models.SutureNeedle(parentNode=root, name='SutureNeedle', rotation=[0.0, 0.0, 0.0], translation=[55, 30, 5],     
    scale3d=scale3d_needle, fixingBox=None, importFile=needleVolume_fileName, carving=carving, geomagic=geomagic)

    # # Add thread: not added to Geo yet
    models.Thread(parentNode=root, name='SutureThread', rotation=[90, 0, 0], translation=[10, 60, 5], 
    scale3d=[0.5, 0.5, 0.6],  fixingBox=None, importFile=threadVolume_fileName, geomagic=geomagic)

    # Add contact listener
    root.addObject(controllers.Trial(name="MyController", rootNode=root))

    # Add training spheres: add when necessary
    models.sphere(parentNode=root, name="Sphere1", translation=[49, 10.0, 0.0], scale3d="1.5 1.5 1.5", color="0.0 0.5 0.0")
    models.sphere(parentNode=root, name="Sphere2", translation=[49, 30.0, 0.0], scale3d="1.5 1.5 1.5", color="0.0 0.5 0.0")
    models.sphere(parentNode=root, name="Sphere3", translation=[52, 20.0, 0.0], scale3d="1.5 1.5 1.5", color="0.0 0.5 0.0")
    models.sphere(parentNode=root, name="Sphere4", translation=[52, 40.0, 0.0], scale3d="1.5 1.5 1.5", color="0.0 0.5 0.0")


    return root


if __name__ == '__main__':
    main()
