# Required import for python
import Sofa
import numpy as np
import models 
import Sofa.SofaDeformable
import controllers


scale3d_skin=[0.5, 0.5, 1]
scale3d_scalpel="1 1 1 "

skinVolume_fileName="mesh\skinVolume_thin"
scalpel_Instrument="mesh\scalpel.obj"
# Collision particles positions
pointPosition_onscalpel1="8 -7.4 -17" 

# # x,y fixing box left
# x1=scale3d_skin[0]*100
# y1=scale3d_skin[1]*100

# # x,y borderbox left
# xb1=x1-1
# yb1=y1
# xb12=x1+1
# yb12=y1

# # x,y fixing box right
# x2=x1+1
# y2=-0.1
# x22=x2+scale3d_skin[0]*100
# y22=y2+scale3d_skin[1]*100

# # x,y borderbox right
# xb2=x2+1
# yb2=y2
# xb22=x2+1
# yb22=y2




    


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

    # Define root properties
    root.gravity=[0, 0, -20]
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




    # Define the variables
    geomagic=False
    carving=True

    #################### GEOMAGIC TOUCH DEVICE ##################################################################
    if geomagic==True:
        root.addObject('GeomagicDriver', name="GeomagicDevice", deviceName="Default Device", 
        scale="1", drawDeviceFrame="1", drawDevice="1", positionBase="-11 5 8",  orientationBase="0.707 0 0 0.707")
        
        # Add Geomagic Touch
        models.GeomagicDevice(parentNode=root, name='Omni')
    #############################################################################################################

    #################### CARVING #############################################
    if carving==True:
        root.addObject('CarvingManager', active="true", carvingDistance="0.1")
    ##########################################################################

    
    # Add skin
    models.Skin(parentNode=root, name='SkinLeft', rotation=[0.0, 0.0, 0.0], translation=[0.0, 0.0, 0.0], 
    scale3d=scale3d_skin, fixingBox=[-0.1, -0.1, -2, 50, 50, 0.5], 
    importFile=skinVolume_fileName, carving=carving, borderBox=[48, -0.1, -2, 50, 50, 1], task="Incision")

    models.Skin(parentNode=root, name='SkinRight', rotation=[0.0, 0.0, 0.0], translation=[51, 0, 0], 
    scale3d=scale3d_skin, fixingBox=[51, -0.1, -2, 101, 50, 0.1],
    importFile=skinVolume_fileName, carving=carving, side=1, borderBox=[51, -0.1, -2, 53, 50, 1], task="Incision") 

    
    # models.Skin(parentNode=root, name='SkinLeft', rotation=[0.0, 0.0, 0.0], translation=[0.0, 0.0, 0.0], 
    # scale3d=scale3d_skin, fixingBox=[-0.1, -0.1, -2, x1, y1, 0.5], 
    # importFile=skinVolume_fileName, carving=carving, borderBox=[xb1, yb1, -2, xb12, yb12, 1], task="Incision")

    # models.Skin(parentNode=root, name='SkinRight', rotation=[0.0, 0.0, 0.0], translation=[51, 0, 0], 
    # scale3d=scale3d_skin, fixingBox=[x2, -0.1, -2, 101, 50, 0.1],
    # importFile=skinVolume_fileName, carving=carving, side=1, borderBox=[xb2, yb2, -2, xb22, yb22, 1], task="Incision") 
    
    # Add scalpel
    models.Scalpel(parentNode=root, name='Scalpel', rotation=[0.0, 0.0, 0.0], translation=[10, 10, 30], scale3d=scale3d_scalpel,  
    fixingBox=None, importFile=scalpel_Instrument,  carving=carving, geomagic=geomagic)

    # Add contact listener: uncomment to do stuff at animation time
    root.addObject(controllers.IncisionContactController(name="MyController", rootNode=root))





    return root



if __name__ == '__main__':
    main()
