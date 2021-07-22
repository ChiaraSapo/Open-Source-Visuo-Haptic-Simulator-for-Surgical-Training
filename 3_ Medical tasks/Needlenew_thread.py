# Required import for python
import Sofa
import numpy as np
import Sofa.SofaDeformable

thread_youngModulus=2000
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
    root.gravity=[0, 0, -6]
    root.dt=0.01

    # Required plugins
    #root.addObject('RequiredPlugin', pluginName="SofaBaseMechanics SofaBaseTopology  SofaBoundaryCondition  SofaConstraint SofaDeformable SofaEngine SofaGeneralLoader SofaGeneralObjectInteraction SofaGeneralSimpleFem SofaImplicitOdeSolver SofaLoader SofaMeshCollision SofaOpenglVisual SofaRigid SofaSimpleFem SofaSparseSolver SofaUserInteraction SofaTopologyMapping SofaValidation")
    root.addObject('CollisionPipeline', depth="6", verbose="0", draw="0")
    root.addObject('VisualStyle', displayFlags="showInteractionForceFields")

    # Forces
    root.addObject('BruteForceDetection', name="detection")
    root.addObject('DefaultContactManager', name="CollisionResponse", response="FrictionContact")
    root.addObject('LocalMinDistance', name="proximity", alarmDistance="0.3", contactDistance="0.05", angleCone="0.0")

    # Animation loop
    root.addObject('FreeMotionAnimationLoop')
    LCPConstraintSolver=root.addObject('LCPConstraintSolver', tolerance="0.001", maxIt="1000")
    root.addObject('OglViewport', screenPosition="0 0", cameraPosition="-0.00322233 -20.3537 18.828", cameraOrientation="0.418151 -6.26277e-06 -0.000108372 0.908378")


    # Add needle
    SutureNeedle(parentNode=root, name='SutureNeedle', dx=0, dy=0, dz=0) # To fall on sphere: dx=12, dy=3, dz=6

    Thread(parentNode=root, name="Thread", rotation=[90, 0, 0], translation=[0,10,-0.1], importFile="mesh/threadCh2", scale3d=[0.3, 0.3, 0.1])

    root.addObject('BilateralInteractionConstraint', template="Vec3d", object1=SutureNeedle.COLL_BACK_MO, object2=Thread.MO,  first_point="0", second_point="0")


    return root



def SutureNeedle(parentNode=None, name=None, dx=0, dy=0, dz=0, scale3d=[0.0, 0.0, 0.0], color=[0.0, 0.0, 0.0],
geomagic=False, monitor=False): 
    # Taken from C:\sofa\src\examples\Components\collision\RuleBasedContactManager

    name=parentNode.addChild(name)
    name.addObject('EulerImplicitSolver',  rayleighStiffness="0.1", rayleighMass="0.1" )
    name.addObject('CGLinearSolver', iterations="25", tolerance="1e-5" ,threshold="1e-5")
    if geomagic==True:
        name.addObject('MechanicalObject',  name='InstrumentMechObject', template='Rigid3d', position="@GeomagicDevice.positionDevice", scale3d="3", rotation="0 0 10" ) #, src="@instrumentMeshLoader")
        name.addObject('RestShapeSpringsForceField', name="InstrumentRestShape", stiffness='1000', angularStiffness='1000', external_rest_shape='@../Omni/DOFs', points='0', external_points='0') 
        name.addObject('LCPForceFeedback', name="LCPFFNeedle",  forceCoef="0.1", activate="true")# Decide forceCoef value better
        SutureNeedle.RS=name.InstrumentRestShape
    else: 
        name.addObject('MechanicalObject', name="InstrumentMechObject", template="Rigid3d", scale="3.0" ,dx=dx, dy=dy, dz=dz)
    name.addObject('UniformMass' , totalMass="3")
    name.addObject('UncoupledConstraintCorrection')
    if monitor==True:
        name.addObject('Monitor', template="Vec3d", name="SutureNeedle_pos", listening="1", indices="0", shoWPositions="True", ExportPositions="True")

    Visu=name.addChild('Visu')
    Visu.addObject('MeshObjLoader' ,name="meshLoader_3", filename="mesh/Suture_needle.obj", scale="3.0", handleSeams="1" )
    if geomagic==True:
        Visu.addObject('OglModel',name="Visual", src='@meshLoader_3', rx="-10", ry="160", rz="180",  dz="-4", dx="0", dy="0",  color="0 0.5 0.796")
    else:
        Visu.addObject('OglModel' ,name="Visual" ,src="@meshLoader_3",  color="0 0.5 0.796")
    Visu.addObject('RigidMapping' ,input="@..", output="@Visual")
    
    Surf=name.addChild('Surf')
    Surf.addObject('MeshObjLoader' ,filename="mesh/Suture_needle.obj" ,name="loader" )
    Surf.addObject('MeshTopology' ,src="@loader")
    if geomagic==True:
        Surf.addObject('MechanicalObject' ,src="@loader", scale="3.0", rx="-10", ry="160", rz="180",  dz="-4", dx="0", dy="0")
    else: 
        Surf.addObject('MechanicalObject' ,src="@loader", scale="3.0")#, dx="8", dy="3", dz="6")
    #Surf.addObject('TriangleCollisionModel', name="Torus2Triangle") # DO NOT UNCOMMENT
    #Surf.addObject('LineCollisionModel', name="Torus2Line" ) # DO NOT UNCOMMENT
    Surf.addObject('PointCollisionModel' ,name="Torus2Point")
    Surf.addObject('RigidMapping')


    collFront = name.addChild('collFront')
    if geomagic==True:
        collFront.addObject('MechanicalObject', template="Vec3d", name="Particle", position="-4.2 0.02 -0.25", rx="-10", ry="160", rz="180",  dz="-4", dx="0", dy="0")
    else:
        collFront.addObject('MechanicalObject', template="Vec3d", name="Particle", position="-4.2 0.02 -0.25")

    collFront.addObject('SphereCollisionModel', radius="0.2", name="SphereCollisionInstrument", contactStiffness="1", tags="CarvingTool")


    collFront.addObject('RigidMapping', name="MM->CM mapping",  input="@../InstrumentMechObject",  output="@Particle")

    collBack = name.addChild('collBack')
    if geomagic==True:
        collBack.addObject('MechanicalObject', template="Vec3d", name="Particle2", position="0 0.007 -0.25", rx="-10", ry="160", rz="180",  dz="-4", dx="0", dy="0")
    else:
        collBack.addObject('MechanicalObject', template="Vec3d", name="Particle2", position="0 0.007 -0.25")
    collBack.addObject('SphereCollisionModel', radius="0.2", name="SphereCollisionInstrument2", contactStiffness="1")
    collBack.addObject('RigidMapping', name="MM->CM mapping",  input="@../InstrumentMechObject",  output="@Particle2")

    SutureNeedle.ITSELF=name
    SutureNeedle.COLL=name.Surf.Torus2Point.getLinkPath()
    SutureNeedle.MO=name.InstrumentMechObject.getLinkPath()
    SutureNeedle.COLL_BACK_MO=name.collBack.Particle2.getLinkPath()
    SutureNeedle.POS=name.InstrumentMechObject.findData('position').value
    SutureNeedle.COLL_FRONT=name.collFront.SphereCollisionInstrument.getLinkPath()
    SutureNeedle.COLL_FRONT_TAG=name.collFront.SphereCollisionInstrument
    SutureNeedle.COLL_BACK=name.collBack.SphereCollisionInstrument2.getLinkPath()
    SutureNeedle.MO_TAG=name.InstrumentMechObject

  

def Thread(parentNode=None, name=None, rotation=[0.0, 0.0, 0.0], translation=[0.0, 0.0, 0.0], 
scale3d=[0.0, 0.0, 0.0], fixingBox=[0.0, 0.0, 0.0], importFile=None, geomagic=False):

    name=parentNode.addChild(name)

    #################### BEHAVIOUR ##########################
    
    # Solvers
    name.addObject('EulerImplicitSolver', name="odesolver")
    name.addObject('CGLinearSolver', iterations="25", name="EpiLinearsolver", tolerance="1.0e-9", threshold="1.0e-9")
    name.addObject('MeshGmshLoader', name='name_volumeLoader', filename=importFile, scale3d=scale3d, rotation=rotation, translation=translation)
    #name.addObject('MeshTopology', src='@volumeLoader')

    # Tetrahedra container
    name.addObject('TriangleSetTopologyContainer', src='@name_volumeLoader')
    name.addObject('TriangleSetGeometryAlgorithms', template='Vec3d')
    name.addObject('TriangleSetTopologyModifier')

    # Mechanical object and mass
    if geomagic==True:
        name.addObject('MechanicalObject', name='ThreadMechObject', template='Vec3d', position="@GeomagicDevice.positionDevice", scale3d=scale3d, rotation="0 0 0" )
        #name.addObject('RestShapeSpringsForceField', name="ThreadRest", stiffness='1000', angularStiffness='1000', external_rest_shape='@../Omni/DOFs', points='0', external_points='0') 
        #name.addObject('LCPForceFeedback', name="LCPFFThread", activate="true", forceCoef="0.5")
    else:
        name.addObject('MechanicalObject', name='ThreadMechObject', template='Vec3d')
    
    name.addObject('UniformMass', name="nameMass", template="Vec3d,double", totalMass="1.0")

    name.addObject('TriangleFEMForceField', template='Vec3d', name='FEM', method='large', youngModulus=thread_youngModulus, poissonRatio=thread_poissonRatio)
    #name.addObject('MeshSpringForceField', name="FEM-Bend", template="Vec3d", stiffness="1000", damping="0.1")
    name.addObject('UncoupledConstraintCorrection')

    #################### COLLISION ##########################

    ThreadColl = name.addChild('ThreadColl')

    ThreadColl.addObject('PointCollisionModel', name="ThreadPointCollisionModel", selfCollision="True")
    ThreadColl.addObject('TriangleCollisionModel', name="ThreadTriangleCollisionModel", selfCollision="True") 

    #################### VISUALIZATION ########################

    ThreadVisu = ThreadColl.addChild('ThreadVisu')
    ThreadVisu.addObject('OglModel', template="Vec3d", name="Visual", color="1 0.75 0.796", material="Default Diffuse 1 0 0 1 1 Ambient 1 0 0 0.2 1 Specular 0 0 0 1 1 Emissive 0 0 0 1 1 Shininess 0 45 ")
    ThreadVisu.addObject('IdentityMapping', template="Vec3d,Vec3d", name="default12", input="@..", output="@Visual" )

    Thread.MO=name.ThreadMechObject.getLinkPath()


if __name__ == '__main__':
    main()
