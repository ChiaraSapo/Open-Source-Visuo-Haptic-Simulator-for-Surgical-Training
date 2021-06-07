import Sofa
import numpy as np

# Data
skin_youngModulus=300
thread_youngModulus=2000
skin_poissonRatio=0.49
thread_poissonRatio=0.8

# CHECK IF FUNCTIONS CAN READ GEO POS OR IT MUST BE PASSED

def Skin(parentNode=None, name=None, rotation=[0.0, 0.0, 0.0], translation=[0.0, 0.0, 0.0], 
scale3d=[0.0, 0.0, 0.0],  fixingBox=[0.0, 0.0, 0.0], importFile=None, carving=False):

    #################### BEHAVIOUR ##########################
    
    name = parentNode.addChild(name)
    
    # Solvers
    name.addObject('EulerImplicitSolver', name="odesolver")
    name.addObject('CGLinearSolver', iterations="25", name="EpiLinearsolver", tolerance="1.0e-9", threshold="1.0e-9")
    
    # Volumetric mesh loader
    name.addObject('MeshGmshLoader', name='volumeLoader', filename=importFile, scale3d=scale3d)
    #name.addObject('MeshTopology', src='@volumeLoader')

    # Tetrahedra container
    name.addObject('TetrahedronSetTopologyContainer', src='@volumeLoader', name='TetraContainer')#,  template='Vec3d')
    name.addObject('TetrahedronSetGeometryAlgorithms', template='Vec3d')
    name.addObject('TetrahedronSetTopologyModifier')

    # Mechanical object and mass
    name.addObject('MechanicalObject', name='nameMechObj', template='Vec3d', translation=translation)#, src="@volumeLoader", position="1 1 20")
    name.addObject('DiagonalMass', name="nameMass", template="Vec3d,double", massDensity="1.0")

    # Constraints
    name.addObject('BoxROI', name='boxROI', box=fixingBox, drawBoxes='true')
    name.addObject('RestShapeSpringsForceField', points='@boxROI.indices', stiffness='1e12', angularStiffness='1e12')

    # Forces
    name.addObject('TetrahedronFEMForceField', template='Vec3d', name='FEM', method='large', youngModulus=skin_youngModulus, poissonRatio=skin_poissonRatio)
    name.addObject('UncoupledConstraintCorrection')


    #################### COLLISION ##########################

    nameCollis = name.addChild('nameCollis')

    # Mapped from the tetra of behaviour model
    nameCollis.addObject('TriangleSetTopologyContainer', name="T_Container")
    nameCollis.addObject('TriangleSetTopologyModifier', name="T_Modifier")
    nameCollis.addObject('TriangleSetGeometryAlgorithms', template="Vec3d", name="T_GeomAlgo")
    nameCollis.addObject('Tetra2TriangleTopologicalMapping', name="default8", input="@../TetraContainer", output="@T_Container")

    # Types of collision
    if carving==True:
        nameCollis.addObject('TriangleCollisionModel', name="nameTri", tags="CarvingSurface")
    else: 
        nameCollis.addObject('TriangleCollisionModel', name="nameTri")
    nameCollis.addObject('LineCollisionModel')
    nameCollis.addObject('PointCollisionModel') 


    #################### VISUALIZATION ########################

    nameVisu = nameCollis.addChild('nameVisu')
    nameVisu.addObject('OglModel', template="Vec3d", name="Visual", color="1 0.75 0.796", material="Default Diffuse 1 0 0 1 1 Ambient 1 0 0 0.2 1 Specular 0 0 0 1 1 Emissive 0 0 0 1 1 Shininess 0 45 ")
    nameVisu.addObject('IdentityMapping', template="Vec3d,Vec3d", name="default12", input="@..", output="@Visual" )
    




def Thread(parentNode=None, name=None, rotation=[0.0, 0.0, 0.0], translation=[0.0, 0.0, 0.0], 
scale3d=[0.0, 0.0, 0.0], fixingBox=[0.0, 0.0, 0.0], importFile=None, geomagic=False):

    name = parentNode.addChild(name)

    #################### BEHAVIOUR ##########################
    
    # Solvers
    name.addObject('EulerImplicitSolver', name="odesolver")
    name.addObject('CGLinearSolver', iterations="25", name="EpiLinearsolver", tolerance="1.0e-9", threshold="1.0e-9")
    name.addObject('MeshGmshLoader', name='name_volumeLoader', filename=importFile, scale3d=scale3d, rotation=rotation, translation=translation)#translation=" 39 39 9")
    #name.addObject('MeshTopology', src='@volumeLoader')

    # Tetrahedra container
    name.addObject('TriangleSetTopologyContainer', src='@name_volumeLoader')
    name.addObject('TriangleSetGeometryAlgorithms', template='Vec3d')
    name.addObject('TriangleSetTopologyModifier')

    # Mechanical object and mass
    name.addObject('MechanicalObject', name='nameMechObj', template='Vec3d')
    name.addObject('UniformMass', name="nameMass", template="Vec3d,double", totalMass="1.0")

    name.addObject('TriangleFEMForceField', template='Vec3d', name='FEM', method='large', youngModulus=thread_youngModulus, poissonRatio=thread_poissonRatio)
    #name.addObject('MeshSpringForceField', name="FEM-Bend", template="Vec3d", stiffness="1000", damping="0.1")
    name.addObject('UncoupledConstraintCorrection')

    #################### COLLISION ##########################

    nameCollis = name.addChild('nameCollis')

    nameCollis.addObject('PointCollisionModel', name="nameTri", selfCollision="True")
    nameCollis.addObject('TriangleCollisionModel', name="nameTri", selfCollision="True") 


    #################### VISUALIZATION ########################

    nameVisu = nameCollis.addChild('nameVisu')
    nameVisu.addObject('OglModel', template="Vec3d", name="Visual", color="1 0.75 0.796", material="Default Diffuse 1 0 0 1 1 Ambient 1 0 0 0.2 1 Specular 0 0 0 1 1 Emissive 0 0 0 1 1 Shininess 0 45 ")
    nameVisu.addObject('IdentityMapping', template="Vec3d,Vec3d", name="default12", input="@..", output="@Visual" )
    

# WHEN I'LL UNDERSTAND WHY THE SAME THING WORKS FOR THE NEEDLE AND NOT FOR THE SCALPEL I'LL CANCEL ONE OF THE TWO INSTRUMENT FUNCTIONS! 
# OR I'LL DO THE SAME WHEN I'LL BE WORKING WITH THE GEOMAGIC ONLY

# Good for the needle... (BEST VERSION I THINK)
def Instrument(parentNode=None, name=None, rotation=[0.0, 0.0, 0.0], translation=[0.0, 0.0, 0.0],
scale3d=[0.0, 0.0, 0.0],  fixingBox=[0.0, 0.0, 0.0], importFile=None, pointPosition=None, carving=False, geomagic=False):
    
    name = parentNode.addChild(name)

    #################### BEHAVIOUR ##########################

    name.addObject('EulerImplicitSolver', name='ODE solver', rayleighStiffness="0.01", rayleighMass="1.0")
    name.addObject('CGLinearSolver', name='linear solver', iterations="25", tolerance="1e-7", threshold="1e-7")
    name.addObject('MeshObjLoader', name='instrumentMeshLoader', filename=importFile)
    if geomagic==True:
        name.addObject('MechanicalObject', src="@instrumentMeshLoader", name='InstrumentmechObject', template='Rigid3d', position=translation, scale3d=scale3d)
        name.addObject('RestShapeSpringsForceField', stiffness='1000', angularStiffness='1000', external_rest_shape='@../Omni/DOFs', points='0', external_points='0') 
        name.addObject('LCPForceFeedback', name="LCPFF1", activate="true", forceCoef="0.5")
    else:
        name.addObject('MechanicalObject', src="@instrumentMeshLoader", name='InstrumentmechObject', template='Rigid3d', translation=translation, scale3d=scale3d)
    name.addObject('UniformMass', name='mass', totalMass="5")
    name.addObject('UncoupledConstraintCorrection')

    #################### COLLISION ##########################
    InstrumentColNode = name.addChild('CollisionModel')
    
    InstrumentColNode.addObject('MechanicalObject', template="Vec3d", name="Particle", position=pointPosition)
    if carving==True:
        InstrumentColNode.addObject('SphereCollisionModel', radius="0.09", name="ParticleModel", contactStiffness="2", tags="CarvingTool")
    else:
        InstrumentColNode.addObject('SphereCollisionModel', radius="0.09", name="ParticleModel", contactStiffness="2")
    InstrumentColNode.addObject('RigidMapping', template="Rigid3d,Vec3d", name="MM->CM mapping",  input="@../InstrumentmechObject",  output="@Particle")

    #################### VISUALIZATION ########################
    InstrumentVisNode = name.addChild('VisualModel')
    InstrumentVisNode.addObject('OglModel', name='InstrumentVisualModel', src='@../instrumentMeshLoader', scale3d=scale3d, color="0 0.5 0.796")
    InstrumentVisNode.addObject('RigidMapping', template="Rigid3d,Vec3d", name='MM-VM mapping', input='@../InstrumentmechObject', output='@InstrumentVisualModel')



# Good for the scalpel, but has a lot of collision points...
def Instrument2(parentNode=None, name=None, rotation=[0.0, 0.0, 0.0], translation=[0.0, 0.0, 0.0], 
scale3d=[0.0, 0.0, 0.0],  fixingBox=[0.0, 0.0, 0.0], importFile=None, pointPosition=None, carving=False, geomagic=False):

    name = parentNode.addChild(name)

    name.addObject('EulerImplicitSolver', name='ODE solver', rayleighStiffness="0.01", rayleighMass="1.0")
    name.addObject('CGLinearSolver', name='linear solver', iterations="25", tolerance="1e-7", threshold="1e-7")
    if geomagic==True: #not sure
        name.addObject('MeshObjLoader', name='instrumentMeshLoader', filename=importFile, scale3d=scale3d) 
        name.addObject('MechanicalObject', src="@instrumentMeshLoader", name='mechObject', position=translation, template='Rigid3d')
        name.addObject('RestShapeSpringsForceField', stiffness='1000', angularStiffness='1000', external_rest_shape='@../Omni/DOFs', points='0', external_points='0') 
        name.addObject('LCPForceFeedback', name="LCPFF1", activate="true", forceCoef="0.5")
    else:
        name.addObject('MeshObjLoader', name='instrumentMeshLoader', filename=importFile, translation=translation, scale3d=scale3d)
        name.addObject('MechanicalObject', src="@instrumentMeshLoader", name='mechObject', template='Rigid3d')
    name.addObject('UniformMass', name='mass', totalMass="2")
    name.addObject('UncoupledConstraintCorrection')

    #################### VISUALIZATION ########################
    InstrumentVisNode = name.addChild('VisualModel')
    InstrumentVisNode.addObject('OglModel', name='InstrumentVisualModel', src='@../instrumentMeshLoader', color="0 0.5 0.796")
    InstrumentVisNode.addObject('IdentityMapping', name='MM-VM mapping', input='@../mechObject', output='@InstrumentVisualModel')

    #################### COLLISION ##########################
    InstrumentColNode1 = name.addChild('CollisionModel1')
    InstrumentColNode1.addObject('MechanicalObject', template="Vec3d", name="Particle", position=pointPosition)
    if carving==True:
        InstrumentColNode1.addObject('SphereCollisionModel', radius=0.4, name="ParticleModel", contactStiffness="2", tags="CarvingTool")
    else:
        InstrumentColNode1.addObject('SphereCollisionModel', radius=0.4, name="ParticleModel", contactStiffness="2")

    InstrumentColNode1.addObject('IdentityMapping', name="MM->CM mapping",  input="@../mechObject",  output="@Particle")


def GeomagicDevice(parentNode=None, name=None):
    name=parentNode.addChild(name)
    name.addObject('MechanicalObject', template="Rigid3", name="DOFs", position="@GeomagicDevice.positionDevice")
    name.addObject('MechanicalStateController', template="Rigid3", listening="true", mainDirection="-1.0 0.0 0.0")
    
