# Required import for python
import Sofa
import numpy as np
import Sofa.SofaDeformable


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
    root.gravity=[0, 0, -5]
    root.dt=0.01

    # Required plugins
    root.addObject('RequiredPlugin', pluginName="SofaBaseMechanics SofaBaseTopology  SofaBoundaryCondition  SofaConstraint SofaDeformable SofaEngine SofaGeneralLoader SofaGeneralObjectInteraction SofaGeneralSimpleFem SofaImplicitOdeSolver SofaLoader SofaMeshCollision SofaOpenglVisual SofaRigid SofaSimpleFem SofaSparseSolver SofaUserInteraction SofaTopologyMapping SofaValidation")
    root.addObject('CollisionPipeline', depth="6", verbose="0", draw="0")

    # Forces
    root.addObject('BruteForceDetection', name="detection")
    root.addObject('DefaultContactManager', name="CollisionResponse", response="FrictionContact")
    root.addObject('LocalMinDistance', name="proximity", alarmDistance="0.3", contactDistance="0.05", angleCone="0.0")

    # Animation loop
    root.addObject('FreeMotionAnimationLoop')
    LCPConstraintSolver=root.addObject('LCPConstraintSolver', tolerance="0.001", maxIt="1000")
    root.addObject('OglViewport', screenPosition="0 0", cameraPosition="-0.00322233 -20.3537 18.828", cameraOrientation="0.418151 -6.26277e-06 -0.000108372 0.908378")

    # Add skin
    Skin(parentNode=root, name='Skin', rotation=[0.0, 0.0, 0.0], translation=[0.0, 0.0, 0.0], 
    scale3d="0.25 0.65 0.1", fixingBox=[-0.1, -0.1, -2, 10, 20, 0.1], importFile="mesh\skin_volume_403020_05")

    # Add needle
    SutureNeedle(parentNode=root, name='SutureNeedle', rotation=[0.0, 0.0, 0.0], translation=[14, 2, 5],     
    scale3d="5 5 5", importFile="mesh\suture_needle.obj")

    # Add controller
    root.addObject(SutureTrainingContactController("MyController",root))

    return root



def Skin(parentNode=None, name=None, rotation=[0.0, 0.0, 0.0], translation=[0.0, 0.0, 0.0], 
scale3d=[0.0, 0.0, 0.0], fixingBox=[0.0, 0.0, 0.0], importFile=None):
    
    #################### BEHAVIOUR ##########################
    name=parentNode.addChild(name)
    
    name.addObject('EulerImplicitSolver', name="odesolver", rayleighStiffness="0.01", rayleighMass="0.01") #added  2 params
    name.addObject('CGLinearSolver', iterations="25", name="EpiLinearsolver", tolerance="1.0e-9", threshold="1.0e-9")
    name.addObject('MeshGmshLoader', name='volumeLoader', filename=importFile, scale3d=scale3d)
    name.addObject('TetrahedronSetTopologyContainer', src='@volumeLoader', name='TetraContainer')
    name.addObject('TetrahedronSetGeometryAlgorithms', template='Vec3d')
    name.addObject('TetrahedronSetTopologyModifier')
    name.addObject('MechanicalObject', name='SkinMechObj', src='@volumeLoader', template='Vec3d', translation=translation)
    name.addObject('DiagonalMass', name="SkinMass", massDensity="2.0")
    name.addObject('TetrahedronFEMForceField', template='Vec3d', name='FEM', method='large', youngModulus=1500, poissonRatio=0.49)
    name.addObject('UncoupledConstraintCorrection', compliance=0.001)

    # Fixed box for constraints
    boxROI=name.addObject('BoxROI', name='boxROI', box=fixingBox, drawBoxes='true', computeTriangles='true')
    name.addObject('RestShapeSpringsForceField', name='rest', points='@boxROI.indices', stiffness='1e12', angularStiffness='1e12')

    # Add box for springs
    name.addObject('BoxROI', name='sphere1Box', box=[8-2, 3-2, -0.1, 8+2, 3+2, 3], drawBoxes='true', computeTriangles='true')
       

    #################### COLLISION ##########################
    SkinColl = name.addChild('SkinColl')

    # Mapped from the tetra of behaviour model
    SkinColl.addObject('TriangleSetTopologyContainer', name="T_Container")
    SkinColl.addObject('TriangleSetTopologyModifier', name="T_Modifier")
    SkinColl.addObject('TriangleSetGeometryAlgorithms', template="Vec3d", name="T_GeomAlgo")
    SkinColl.addObject('Tetra2TriangleTopologicalMapping', name="default8", input="@../TetraContainer", output="@T_Container")
    SkinColl.addObject('TriangleCollisionModel', name="TriangleCollisionSkin")


    #################### VISUALIZATION ########################
    SkinVisu = SkinColl.addChild('SkinVisu')

    SkinVisu.addObject('MechanicalObject', name="VisuMO")
    SkinVisu.addObject('OglModel', template="Vec3d", name="Visual", color="1 0.75 0.796", 
    material="Default Diffuse 1 0 0 1 1 Ambient 1 0 0 0.2 1 Specular 0 0 0 1 1 Emissive 0 0 0 1 1 Shininess 0 45 ")
    SkinVisu.addObject('IdentityMapping', template="Vec3d,Vec3d", name="default12", input="@..", output="@Visual" )

    # Data
    Skin.MO=name.SkinMechObj.getLinkPath()
    Skin.COLL=name.SkinColl.TriangleCollisionSkin.getLinkPath()
    Skin.sphere1Box=name.sphere1Box
    

def SutureNeedle(parentNode=None, name=None, rotation=[0.0, 0.0, 0.0], translation=[0.0, 0.0, 0.0],
scale3d=[0.0, 0.0, 0.0], importFile=None):

    #################### BEHAVIOUR ##########################
    name=parentNode.addChild(name)

    name.addObject('EulerImplicitSolver', name='ODE solver', rayleighMass="1.0", rayleighStiffness="0.01")
    name.addObject('CGLinearSolver', name='linear solver', iterations="25", tolerance="1e-7", threshold="1e-7") 
    name.addObject('MeshObjLoader', name='instrumentMeshLoader', filename=importFile)
    name.addObject('MechanicalObject', src="@instrumentMeshLoader", name='InstrumentMechObject', template='Rigid3d', translation=translation, scale3d=scale3d)
    name.addObject('UniformMass', name='mass', totalMass="3") 
    name.addObject('UncoupledConstraintCorrection') 

    #################### COLLISION ##########################
    InstrumentColl_Back = name.addChild('InstrumentColl_Back')

    InstrumentColl_Back.addObject("Monitor", name="SutureNeedle_pos", indices="0", listening="1", showPositions="1", PositionsColor="1 1 0 1", TrajectoriesPrecision="0.1", TrajectoriesColor="1 1 0 1", ExportPositions="true")
    InstrumentColl_Back.addObject('MechanicalObject', template="Vec3d", name="Particle2", position="0 0.02 0.05")
    InstrumentColl_Back.addObject('SphereCollisionModel', radius="0.2", name="SphereCollisionInstrument2", contactStiffness="1")
    InstrumentColl_Back.addObject('RigidMapping', template="Rigid3d,Vec3d", name="MM->CM mapping",  input="@../InstrumentMechObject",  output="@Particle2")

    #################### VISUALIZATION ########################
    InstrumentVisu = name.addChild('InstrumentVisu')

    InstrumentVisu.addObject('OglModel', name='InstrumentVisualModel', src='@../instrumentMeshLoader', scale3d=scale3d,  color="0 0.5 0.796")
    InstrumentVisu.addObject('RigidMapping', template="Rigid3d,Vec3d", name='MM-VM mapping', input='@../InstrumentMechObject', output='@InstrumentVisualModel')

    # Data
    SutureNeedle.MO=name.InstrumentMechObject.getLinkPath()
    SutureNeedle.COLL_BACK_MO=name.InstrumentColl_Back.Particle2.getLinkPath()
 

# Controller 
class SutureTrainingContactController(Sofa.Core.Controller):

    def __init__(self, name, rootNode):
        Sofa.Core.Controller.__init__(self, name, rootNode)
        
        # Define spring force field (Skin-Needle)
        self.spring_force_field = rootNode.addObject("StiffSpringForceField", name="LeftFF", object1 = Skin.MO,  object2=SutureNeedle.COLL_BACK_MO)

        
    # Function called at each begin of animation step
    def onAnimateBeginEvent(self, event):
        
        # Retrieve indexes of the box
        indicesBox = Skin.sphere1Box.findData('indices').value

        # Create springs
        springs = [Sofa.SofaDeformable.LinearSpring(index1=i, index2=0, springStiffness=50, dampingFactor=0.5, restLength=0.1) for i in indicesBox] 
        self.spring_force_field.addSprings(springs)

if __name__ == '__main__':
    main()
