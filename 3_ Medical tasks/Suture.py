# Required import for python
import Sofa
import numpy as np
import models 


# Data
poissonRatio_ALL=0.48
youngModulus_H=3400
youngModulus_D=300
youngModulus_E=1000
scale3d_needle="5 5 5"
pointPosition_onNeedle="-6.98 0.02 0.05" #N: 5,5,5
scale3d_skin="0.5 0.5 1"
GeomagicPosition="0 20 15"
skinVolume_fileName="C:\sofa\src\Chiara\mesh\skinVolume_thin"
#skinLeftSurface_fileName="C:\sofa\src\examples\skinLeftSurface.stl"
needleVolume_fileName="C:\sofa\src\Chiara\mesh\suture_needle.obj"
threadVolume_fileName="mesh/threadCh2"
scale3d_thread="0.5 0.5 0.6"
sphereVolume_fileName="mesh/sphere.obj"

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

    # Geomagic device
    #root.addObject('GeomagicDriver', name="GeomagicDevice", deviceName="Default Device", scale="1", drawDeviceFrame="1", drawDevice="1", positionBase=GeomagicPosition,  orientationBase="0.707 0 0 0.707")
    
    # Carving
    #root.addObject('CarvingManager', active="true", carvingDistance="0.1") #CARVING



    # Add skin
    models.Skin(parentNode=root, name="SkinLeft", rotation=[0.0, 0.0, 0.0], translation=[0.0, 0.0, 0.0], 
    scale3d=scale3d_skin, fixingBox=[-0.1, -0.1, -2, 50, 50, 0.1], importFile=skinVolume_fileName)
    models.Skin(parentNode=root, name="SkinRight", rotation=[0.0, 0.0, 0.0], translation=[55, 0, 0], 
    scale3d=scale3d_skin, fixingBox=[54, -0.1, -2, 106, 50, 0.1], importFile=skinVolume_fileName)    

    # Add needle
    models.Needle(parentNode=root, name="SutureNeedle", rotation=[0.0, 0.0, 0.0], translation=[25, 25, 5], 
    scale3d=scale3d_needle,  fixingBox=None, importFile=needleVolume_fileName, pointPosition=pointPosition_onNeedle)

    # Add thread
    models.Thread(parentNode=root, name="SutureThread", rotation=[90, 0, 0], translation=[-5, 60, 5], 
    scale3d=[0.5, 0.5, 0.6],  fixingBox=None, importFile=threadVolume_fileName)




    return root



if __name__ == '__main__':
    main()
