# Required import for python
import Sofa
import numpy as np
import Sofa.SofaDeformable
import models
import controllers


# Data
#scale3d_skin="0.2 0.3 1" #thin
#scale3d_skin="1 0.6 1"
scale3d_skin="0.2 0.5 0.1"
scale3d_needle="5 5 5"
scale3d_thread="0.5 0.5 0.5"

pointPosition_onNeedle="-6.98 0.02 0.05" #N: 5,5,5

GeomagicPosition="0 20 15"
skinVolume_fileName="mesh\skin_volume_403020_05" #03 troppo lento
needleVolume_fileName="mesh\suture_needle.obj"
threadVolume_fileName="mesh/threadCh2"

# Data
skin_youngModulus=1000#300
thread_youngModulus=2000
skin_poissonRatio=0.49
thread_poissonRatio=0.8
# Choose in your script to activate or not the GUI
USE_GUI = True


def main():
    import SofaRuntime
    import Sofa.Gui

    root = Sofa.Core.Node("root")
    createScene(root)
    Sofa.Simulation.init(root)

    if not USE_GUI:
        for iteration in range(10):
            Sofa.Simulation.animate(root, root.dt.value)
    else:
        Sofa.Gui.GUIManager.Init("myscene", "qglviewer")
        Sofa.Gui.GUIManager.createGUI(root, __file__)
        Sofa.Gui.GUIManager.SetDimension(1080, 1080)
        Sofa.Gui.GUIManager.MainLoop(root)
        Sofa.Gui.GUIManager.closeGUI()


def createScene(root):
    root.gravity=[0, 0, -10]
    root.dt=0.02

    root.addObject('DefaultVisualManagerLoop')
    root.addObject('DefaultAnimationLoop')

    root.addObject('VisualStyle', displayFlags="showCollisionModels hideVisualModels showForceFields")
    root.addObject('RequiredPlugin', pluginName="SofaImplicitOdeSolver SofaLoader SofaOpenglVisual SofaBoundaryCondition SofaGeneralLoader SofaGeneralSimpleFem") 
    root.addObject('DefaultPipeline', name="CollisionPipeline")
    root.addObject('BruteForceDetection', name="N2")
    root.addObject('DefaultContactManager', name="CollisionResponse", response="default")
    root.addObject('DiscreteIntersection')

    root.addObject('MeshObjLoader', name="LiverSurface", filename="mesh/liver-smooth.obj")

    models.Skin(parentNode=root, name='SkinLeft', rotation=[0.0, 0.0, 0.0], translation=[0.0, 0.0, 0.0], 
    scale3d=scale3d_skin, fixingBox=[-0.1, -0.1, -2, 10, 20, 0.1], borderBox=[7, -0.1, -2, 10, 20, 1], 
    importFile=skinVolume_fileName, task="Suture")

    #root.addObject(KeyPressedController(name = "SphereCreator"))
    createNewSphere(root)
    return root

def createNewSphere(root):
    newSphere = root.addChild('FallingSphere-')
    newSphere.addObject('EulerImplicitSolver')
    newSphere.addObject('CGLinearSolver', threshold='1e-09', tolerance='1e-09', iterations='200')
    MO = newSphere.addObject('MechanicalObject', showObject=True, position=[5, 10, 5, 0, 0, 0, 1], name=f'Particle-', template='Rigid3d')
    Mass = newSphere.addObject('UniformMass', totalMass=1)
    Force = newSphere.addObject('ConstantForceField', name="CFF", totalForce=[0, 0, -5, 0, 0, 0] )
    Sphere = newSphere.addObject('SphereCollisionModel', name="SCM", radius=1.0 )
    
    newSphere.init()

class KeyPressedController(Sofa.Core.Controller):
    """ This controller monitors new sphere objects.
    Press ctrl and the L key to make spheres falling!
    """
    def __init__(self, *args, **kwargs):
        Sofa.Core.Controller.__init__(self, *args, **kwargs)
        self.iteration = 0

    def onKeypressedEvent(self, event):
        # Press L key triggers the creation of new objects in the scene
        if event['key']=='L':
            self.createNewSphere()
            
    def createNewSphere(self):
        root = self.getContext()
        newSphere = root.addChild('FallingSphere-'+str(self.iteration))
        newSphere.addObject('EulerImplicitSolver')
        newSphere.addObject('CGLinearSolver', threshold='1e-09', tolerance='1e-09', iterations='200')
        MO = newSphere.addObject('MechanicalObject', showObject=True, position=[5, 10+self.iteration, 5, 0, 0, 0, 1], name=f'Particle-{self.iteration}', template='Rigid3d')
        Mass = newSphere.addObject('UniformMass', totalMass=1)
        Force = newSphere.addObject('ConstantForceField', name="CFF", totalForce=[0, 0, -5, 0, 0, 0] )
        Sphere = newSphere.addObject('SphereCollisionModel', name="SCM", radius=1.0 )
        
        newSphere.init()
        self.iteration = self.iteration+1


# Function used only if this script is called from a python environment
if __name__ == '__main__':
    main()