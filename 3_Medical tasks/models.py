import Sofa
import numpy as np


# Data
poissonRatio_ALL=0.48
youngModulus_H=3400
youngModulus_D=300
youngModulus_E=1000
scale3d_needle="5 5 5"
pointPosition_onNeedle="-6.98 0.02 0.05" #N: 5,5,5
scale3d_name="0.5 0.5 1"
GeomagicPosition="0 20 15"
nameVolume_fileName="C:\sofa\src\Chiara\mesh\nameVolume_thin"
#nameSurface_fileName="C:\sofa\src\examples\nameSurface.stl"
needleVolume_fileName="C:\sofa\src\Chiara\mesh\suture_needle.obj"
nameVolume_fileName="mesh/nameCh2"
scale3d_name="0.5 0.5 0.6"
sphereVolume_fileName="mesh/sphere.obj"

# Choose in your script to activate or not the GUI
USE_GUI = True

def Skin(parentNode=None, name=None, rotation=[0.0, 0.0, 0.0], translation=[0.0, 0.0, 0.0], 
scale3d=[0.0, 0.0, 0.0],  fixingBox=[0.0, 0.0, 0.0], importFile=None):
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

    # Mechanical object
    name.addObject('MechanicalObject', name='nameMechObj', template='Vec3d', translation=translation)#, src="@volumeLoader", position="1 1 20")

    # Mass
    name.addObject('DiagonalMass', name="nameMass", template="Vec3d,double", massDensity="1.0")

    # Constraints: check to have not overconstrained the name!
    name.addObject('BoxROI', name='boxROI', box=fixingBox, drawBoxes='true')
    name.addObject('RestShapeSpringsForceField', points='@boxROI.indices', stiffness='1e12', angularStiffness='1e12')

    name.addObject('TetrahedronFEMForceField', template='Vec3d', name='FEM', method='large', youngModulus='300', poissonRatio='0.49')
    name.addObject('UncoupledConstraintCorrection')


    #################### COLLISION ##########################

    nameCollis = name.addChild('nameCollis')

    # Mapped from the tetra of behaviour model
    nameCollis.addObject('TriangleSetTopologyContainer', name="T_Container")
    nameCollis.addObject('TriangleSetTopologyModifier', name="T_Modifier")
    nameCollis.addObject('TriangleSetGeometryAlgorithms', template="Vec3d", name="T_GeomAlgo")
    nameCollis.addObject('Tetra2TriangleTopologicalMapping', name="default8", input="@../TetraContainer", output="@T_Container")

    # Types of collision
    nameCollis.addObject('TriangleCollisionModel', name="nameTri", tags="CarvingSurface")
    nameCollis.addObject('LineCollisionModel')
    nameCollis.addObject('PointCollisionModel')#, tags="CarvingSurface")   


    #################### VISUALIZATION ########################

    nameVisu = nameCollis.addChild('nameVisu')
    nameVisu.addObject('OglModel', template="Vec3d", name="Visual", color="1 0.75 0.796", material="Default Diffuse 1 0 0 1 1 Ambient 1 0 0 0.2 1 Specular 0 0 0 1 1 Emissive 0 0 0 1 1 Shininess 0 45 ")
    nameVisu.addObject('IdentityMapping', template="Vec3d,Vec3d", name="default12", input="@..", output="@Visual" )
    



def Needle(parentNode=None, name=None, rotation=[0.0, 0.0, 0.0], translation=[0.0, 0.0, 0.0], 
scale3d=[0.0, 0.0, 0.0],  fixingBox=[0.0, 0.0, 0.0], importFile=None, pointPosition=None):
   
    name = parentNode.addChild(name)

    name.addObject('EulerImplicitSolver', name='ODE solver', rayleighStiffness="0.01", rayleighMass="1.0")
    name.addObject('CGLinearSolver', name='linear solver', iterations="25", tolerance="1e-7", threshold="1e-7")
    name.addObject('MeshObjLoader', name='instrumentMeshLoader', filename=needleVolume_fileName)
    name.addObject('MechanicalObject', src="@instrumentMeshLoader", name='NeeldemechObject', template='Rigid3d', translation=translation, scale3d=scale3d)
    
    name.addObject('UniformMass', name='mass', totalMass="5")
    name.addObject('UncoupledConstraintCorrection') #without this the neeedle doesn't fall

    # Visual node
    needleVisNode = name.addChild('VisualModel')
    needleVisNode.addObject('OglModel', name='InstrumentVisualModel', src='@../instrumentMeshLoader', scale3d=scale3d, color="0 0.5 0.796")
    needleVisNode.addObject('RigidMapping', template="Rigid3d,Vec3d", name='MM-VM mapping', input='@../NeeldemechObject', output='@InstrumentVisualModel')

    # Collision node
    needleColNode = name.addChild('CollisionModel')
    
    needleColNode.addObject('MechanicalObject', template="Vec3d", name="Particle", position=pointPosition)
    needleColNode.addObject('SphereCollisionModel', radius="0.09", name="ParticleModel", contactStiffness="2", tags="CarvingTool")
    needleColNode.addObject('RigidMapping', template="Rigid3d,Vec3d", name="MM->CM mapping",  input="@../NeeldemechObject",  output="@Particle")
    


def Thread(parentNode=None, name=None, rotation=[0.0, 0.0, 0.0], translation=[0.0, 0.0, 0.0], 
scale3d=[0.0, 0.0, 0.0],  fixingBox=[0.0, 0.0, 0.0], importFile=None):

    name = parentNode.addChild('name')
    
    # Solvers
    name.addObject('EulerImplicitSolver', name="odesolver")
    name.addObject('CGLinearSolver', iterations="25", name="EpiLinearsolver", tolerance="1.0e-9", threshold="1.0e-9")
    name.addObject('MeshGmshLoader', name='name_volumeLoader', filename=importFile, scale3d=scale3d, rotation=rotation, translation=translation)#translation=" 39 39 9")
    #name.addObject('MeshTopology', src='@volumeLoader')

    # Tetrahedra container
    name.addObject('TriangleSetTopologyContainer', src='@name_volumeLoader')
    name.addObject('TriangleSetGeometryAlgorithms', template='Vec3d')
    name.addObject('TriangleSetTopologyModifier')

    # Mechanical object
    name.addObject('MechanicalObject', name='nameMechObj', template='Vec3d')
    name.addObject('UniformMass', name="nameMass", template="Vec3d,double", totalMass="1.0")

    name.addObject('TriangleFEMForceField', template='Vec3d', name='FEM', method='large', youngModulus='2000', poissonRatio='0.8')
    #name.addObject('MeshSpringForceField', name="FEM-Bend", template="Vec3d", stiffness="1000", damping="0.1")
    name.addObject('UncoupledConstraintCorrection')

    #name.addObject('BoxROI', name='boxROI', box='-1 -1 0 2 2 2 ', drawBoxes='true')
    #name.addObject('FixedConstraint', template="Vec3d", name="fixedConstraint", indices="@boxROI.indices")


    #################### COLLISION ##########################

    nameCollis = name.addChild('nameCollis')

    # Types of collision
    nameCollis.addObject('PointCollisionModel', name="nameTri", selfCollision="True")
    nameCollis.addObject('TriangleCollisionModel', name="nameTri", selfCollision="True") 


    #################### VISUALIZATION ########################

    nameVisu = nameCollis.addChild('nameVisu')
    nameVisu.addObject('OglModel', template="Vec3d", name="Visual", color="1 0.75 0.796", material="Default Diffuse 1 0 0 1 1 Ambient 1 0 0 0.2 1 Specular 0 0 0 1 1 Emissive 0 0 0 1 1 Shininess 0 45 ")
    nameVisu.addObject('IdentityMapping', template="Vec3d,Vec3d", name="default12", input="@..", output="@Visual" )
    



def Scalpel(parentNode=None, name=None, rotation=[0.0, 0.0, 0.0], translation=[0.0, 0.0, 0.0], 
scale3d=[0.0, 0.0, 0.0],  fixingBox=[0.0, 0.0, 0.0], importFile=None, pointPosition=None):
    name = parentNode.addChild(name)

    #name.addObject('EulerImplicitSolver', name='ODE solver', rayleighStiffness="0.01", rayleighMass="1.0")
    #name.addObject('CGLinearSolver', name='linear solver', iterations="25", tolerance="1e-7", threshold="1e-7")
    name.addObject('MeshObjLoader', name='instrumentMeshLoader', filename=importFile, translation="20 20 60 ", scale3d=scale3d)
    name.addObject('MechanicalObject', src="@instrumentMeshLoader", name='mechObject', template='Rigid3d', free_velocity="0 0 1")
    name.addObject('UniformMass', name='mass', totalMass="2")

    # Visual node
    scalpelVisNode = name.addChild('VisualModel')
    scalpelVisNode.addObject('OglModel', name='InstrumentVisualModel', src='@../instrumentMeshLoader', color="0 0.5 0.796")
    scalpelVisNode.addObject('IdentityMapping', name='MM-VM mapping', input='@../mechObject', output='@InstrumentVisualModel')

    # Collision node1
    scalpelColNode1 = name.addChild('CollisionModel1')
    scalpelColNode1.addObject('MechanicalObject', template="Vec3d", name="Particle", position=pointPosition)
    scalpelColNode1.addObject('SphereCollisionModel', radius=0.4, name="ParticleModel", contactStiffness="2", tags="CarvingTool")
    scalpelColNode1.addObject('IdentityMapping', name="MM->CM mapping",  input="@../mechObject",  output="@Particle")
















    '''
    # Collision node2
    scalpelColNode2 = name.addChild('CollisionModel2')
    
    scalpelColNode2.addObject('MechanicalObject', template="Vec3d", name="Particle", position=pointPosition_onscalpel2)
    scalpelColNode2.addObject('SphereCollisionModel', radius=r, name="ParticleModel", contactStiffness="2", tags="CarvingTool")
    scalpelColNode2.addObject('RigidMapping', template="Rigid3d,Vec3d", name="MM->CM mapping",  input="@../mechObject",  output="@Particle")

    # Collision node3
    scalpelColNode3 = name.addChild('CollisionModel3')
    
    scalpelColNode3.addObject('MechanicalObject', template="Vec3d", name="Particle", position=pointPosition_onscalpel3)
    scalpelColNode3.addObject('SphereCollisionModel', radius=r, name="ParticleModel", contactStiffness="2", tags="CarvingTool")
    scalpelColNode3.addObject('RigidMapping', template="Rigid3d,Vec3d", name="MM->CM mapping",  input="@../mechObject",  output="@Particle")

    # Collision node4
    scalpelColNode4 = name.addChild('CollisionModel4')
    
    scalpelColNode4.addObject('MechanicalObject', template="Vec3d", name="Particle", position=pointPosition_onscalpel4)
    scalpelColNode4.addObject('SphereCollisionModel', radius=r, name="ParticleModel", contactStiffness="2", tags="CarvingTool")
    scalpelColNode4.addObject('RigidMapping', template="Rigid3d,Vec3d", name="MM->CM mapping",  input="@../mechObject",  output="@Particle")
    '''







    #Constraints=name.addChild('Constraints')
    #Constraints.addObject('MechanicalObject', name="points", template="Vec3d", position="0 0 0")
    #Constraints.addObject('RigidMapping', input="@../nameMechObj", output="@points")


    
    # sphere=parentNode.addChild('sphere')
    # sphere.addObject('EulerImplicitSolver', name="odesolver")
    # sphere.addObject('CGLinearSolver', iterations="25", name="EpiLinearsolver", tolerance="1.0e-9", threshold="1.0e-9")
    # sphere.addObject('MechanicalObject', name='sphereMechObj', template="Vec3d")
    # sphere.addObject('RegularGridTopology', name="grid", nx=3, ny=3, nz=3, xmin=-4, xmax=-8, ymin=-4, ymax=-8, zmin=4, zmax=8)
    # sphere.addObject('HexahedronSetGeometryAlgorithms')
    # sphere.addObject('HexahedronFEMForceField', template="Vec3d", name="FEM", poissonRatio=200, youngModulus=0.5 )
    # sphere.addObject('UniformMass', name="sphereMass",  totalMass="1.0")
    
    # sphere.addObject('UncoupledConstraintCorrection')

    # sphereCol=sphere.addChild('sphereCol')
    # sphereCol.addObject('PointCollisionModel', name="collModel", contactStiffness="2")
    # sphereCol.addObject('MechanicalObject', name="coll", template="Vec3d")
    # sphereCol.addObject('IdentityMapping', template="Vec3d,Vec3d", name="default121", input="@../sphereMechObj", output="@coll")
    
    # sphereVisu=sphere.addChild('sphereVisu')
    # sphereVisu.addObject('MechanicalObject', name="visu", template="Vec3d")
    # sphereVisu.addObject('OglModel', template="Vec3d", name="Visual", color="0 0.75 0.796", material="Default Diffuse 1 0 0 1 1 Ambient 1 0 0 0.2 1 Specular 0 0 0 1 1 Emissive 0 0 0 1 1 Shininess 0 45 ")
    # sphereVisu.addObject('IdentityMapping', template="Vec3d,Vec3d", name="default12", input="@..", output="@visu")

    # #Constraints=sphere.addChild('Constraints')
    # #Constraints.addObject('MechanicalObject', name="points", template="Vec3d", position="0 0 0")
    # #Constraints.addObject('RigidMapping', input="@../sphereMechObj", output="@points")


    # #parentNode.addObject('BilateralInteractionConstraint', template='Vec3d', name="lowerConstraint", object1="@sphere/Constraints/points", object2="@name/Constraints/points", first_point="1", second_point="0")#, twoWay=True)
