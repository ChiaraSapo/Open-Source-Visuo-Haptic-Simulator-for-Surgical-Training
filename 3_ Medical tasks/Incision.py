# Required import for python
import Sofa
import numpy as np
import models 


scale3d_skin="1 1 0.1"
scale3d_scalpel="2 2 2"

skinVolume_fileName="mesh\skinVolume_thin"
scalpel_Instrument="mesh\scalpel.obj"
# Collision particles positions
pointPosition_onscalpel1="8 -7.4 -17" 


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
    root.gravity=[0, 0, -9.8]
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
    models.Skin(parentNode=root, name="Skin", rotation=[0.0, 0.0, 0.0], translation=[0.0, 0.0, 0.0], 
    scale3d=scale3d_skin, fixingBox=[-0.1, -0.1, -2, 100, 100, 0.1], importFile=skinVolume_fileName, carving=carving)

    # Add Geomagic Touch
    models.GeomagicDevice(parentNode=root, name="Omni")
    
    # Add scalpel
    models.Instrument(parentNode=root, name="SutureNeedle", rotation=[0.0, 0.0, 0.0], translation=[20, 20, 30], 
    scale3d=scale3d_scalpel,  fixingBox=None, importFile=scalpel_Instrument, pointPosition=pointPosition_onscalpel1, carving=carving, geomagic=geomagic)




    return root



if __name__ == '__main__':
    main()
