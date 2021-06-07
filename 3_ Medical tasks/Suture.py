# Required import for python
import Sofa
import numpy as np
import models 


# Data
scale3d_skin="0.5 0.5 1"
scale3d_needle="5 5 5"
scale3d_thread="0.5 0.5 0.6"

pointPosition_onNeedle="-6.98 0.02 0.05" #N: 5,5,5

GeomagicPosition="0 20 15"
skinVolume_fileName="C:\sofa\src\Chiara\mesh\skinVolume_thin"
needleVolume_fileName="C:\sofa\src\Chiara\mesh\suture_needle.obj"
threadVolume_fileName="mesh/threadCh2"

# sphereVolume_fileName="mesh/sphere.obj"

# Choose in your script to activate or not the GUI
USE_GUI = True

def main():
    import SofaRuntime
    import Sofa.Gui
    SofaRuntime.importPlugin("SofaOpenglVisual")
    SofaRuntime.importPlugin("SofaImplicitOdeSolver")
    root = Sofa.Core.Node("root")
    addScene(root)
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
    root.gravity=[0, 0, -15]
    root.dt=0.01

    root.addObject('RequiredPlugin', pluginName="Geomagic SofaBoundaryCondition SofaCarving SofaConstraint SofaDeformable SofaEngine SofaGeneralLoader SofaGeneralObjectInteraction SofaGeneralSimpleFem SofaHaptics SofaImplicitOdeSolver SofaLoader SofaMeshCollision SofaOpenglVisual SofaRigid SofaSimpleFem SofaSparseSolver SofaUserInteraction SofaTopologyMapping ")

    # Collision pipeline
    root.addObject('CollisionPipeline', depth="6", verbose="0", draw="0")

    # Forces
    root.addObject('BruteForceDetection', name="detection")
    root.addObject('DefaultContactManager', name="CollisionResponse", response="FrictionContact")
    root.addObject('LocalMinDistance', name="proximity", alarmDistance="0.5", contactDistance="0.05", angleCone="0.1")

    # Animation loop
    root.addObject('FreeMotionAnimationLoop')

    # Constraint solver
    #root.addObject('GenericConstraintSolver')
    root.addObject('LCPConstraintSolver', tolerance="0.001", maxIt="1000")

    #################### GEOMAGIC TOUCH DEVICE ################################################################
    # root.addObject('GeomagicDriver', name="GeomagicDevice", deviceName="Default Device", 
    # scale="1", drawDeviceFrame="1", drawDevice="1", positionBase="0 0 8",  orientationBase="0.707 0 0 0.707")
    # geomagic=True
    #---------------------------------------------------------------------------------------------------------#
    geomagic=False
    ###########################################################################################################

    #################### CARVING #########################################
    root.addObject('CarvingManager', active="true", carvingDistance="0.1")
    carving=True
    #--------------------------------------------------------------------#
    #carving=False
    ######################################################################



    # Add skin
    models.Skin(parentNode=root, name="SkinLeft", rotation=[0.0, 0.0, 0.0], translation=[0.0, 0.0, 0.0], 
    scale3d=scale3d_skin, fixingBox=[-0.1, -0.1, -2, 50, 50, 0.1], importFile=skinVolume_fileName, carving=carving)
    models.Skin(parentNode=root, name="SkinRight", rotation=[0.0, 0.0, 0.0], translation=[55, 0, 0], 
    scale3d=scale3d_skin, fixingBox=[54, -0.1, -2, 106, 50, 0.1], importFile=skinVolume_fileName, carving=carving)    

    # Add Geomagic Touch
    models.GeomagicDevice(parentNode=root, name="Omni")
    
    # Add needle
    if geomagic==True:
        models.Instrument(parentNode=root, name="SutureNeedle", rotation=[0.0, 0.0, 0.0], translation="@GeomagicDevice.positionDevice", 
    scale3d=scale3d_needle,  fixingBox=None, importFile=needleVolume_fileName, pointPosition=pointPosition_onNeedle, carving=carving, geomagic=geomagic)
    else:
        models.Instrument(parentNode=root, name="SutureNeedle", rotation=[0.0, 0.0, 0.0], translation=[25, 25, 5], 
    scale3d=scale3d_needle,  fixingBox=None, importFile=needleVolume_fileName, pointPosition=pointPosition_onNeedle, carving=carving, geomagic=geomagic)

    # Add thread
    models.Thread(parentNode=root, name="SutureThread", rotation=[90, 0, 0], translation=[-5, 60, 5], 
    scale3d=[0.5, 0.5, 0.6],  fixingBox=None, importFile=threadVolume_fileName, geomagic=geomagic)




    return root



if __name__ == '__main__':
    main()
