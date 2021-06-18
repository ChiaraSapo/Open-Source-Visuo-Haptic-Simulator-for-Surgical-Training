# Required import for python
import Sofa
import numpy as np
import Sofa.SofaDeformable
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

    root.addObject('RequiredPlugin', pluginName="SofaBaseMechanics SofaBaseTopology  Geomagic SofaBoundaryCondition SofaCarving SofaConstraint SofaDeformable SofaEngine SofaGeneralLoader SofaGeneralObjectInteraction SofaGeneralSimpleFem SofaHaptics SofaImplicitOdeSolver SofaLoader SofaMeshCollision SofaOpenglVisual SofaRigid SofaSimpleFem SofaSparseSolver SofaUserInteraction SofaTopologyMapping ")

    # Collision pipeline
    root.addObject('CollisionPipeline', depth="6", verbose="0", draw="0")

    # Forces
    root.addObject('BruteForceDetection', name="detection")
    root.addObject('DefaultContactManager', name="CollisionResponse", response="FrictionContact")
    root.addObject('LocalMinDistance', name="proximity", alarmDistance="0.5", contactDistance="0.05", angleCone="0.1")

    # Animation loop
    root.addObject('FreeMotionAnimationLoop')

    # Constraint solver
    LCPConstraintSolver=root.addObject('LCPConstraintSolver', tolerance="0.001", maxIt="1000")

    # Define the variables
    geomagic=False
    carving=True

    # Add skin
    models.Skin(parentNode=root, name='SkinLeft', rotation=[0.0, 0.0, 0.0], translation=[0.0, 0.0, 0.0], 
    scale3d=scale3d_skin, fixingBox=[-0.1, -0.1, -2, 50, 50, 0.1], indicesBox=[-0.1, -0.1, -2, 50, 50, 2], 
    importFile=skinVolume_fileName, carving=carving)
    
    # Add needle
    models.Instrument(parentNode=root, name='SutureNeedle', rotation=[0.0, 0.0, 0.0], translation=[25, 45, 5], 
    scale3d=scale3d_needle, fixingBox=None, importFile=needleVolume_fileName, pointPosition=pointPosition_onNeedle, 
    carving=carving, geomagic=geomagic)
    
    # Add contact listener: uncomment to do stuff at animation time
    root.addObject(models.SutureContactController(name="MyController", rootNode=root))

    # sphereVolume_fileName="mesh/sphere.obj"
    #print(str(models.Instrument.POS[70,:3]).strip('[]')) # Why is the needle position around 0 for all indices?!
    #models.sphere(parentNode=root, name='Sphere1', translation=str(models.Instrument.POS[0,:3]).strip('[]'))


    return root



if __name__ == '__main__':
    main()
