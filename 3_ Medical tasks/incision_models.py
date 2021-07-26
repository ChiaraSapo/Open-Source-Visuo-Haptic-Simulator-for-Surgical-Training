import Sofa
import numpy as np

# Data
skin_youngModulus=300
thread_youngModulus=2000
skin_poissonRatio=0.49
thread_poissonRatio=0.8


def Skin(parentNode=None, name=None, rotation=[0.0, 0.0, 0.0], translation=[0.0, 0.0, 0.0], 
scale3d=[0.0, 0.0, 0.0],  fixingBox=[0.0, 0.0, 0.0], indicesBox=[0.0, 0.0, 0.0], borderBox=[0.0, 0.0, 0.0], importFile=None, 
carving=False, side=0, task=None, borderBox1=[0.0, 0.0, 0.0],borderBox2=[0.0, 0.0, 0.0],borderBox3=[0.0, 0.0, 0.0],borderBox4=[0.0, 0.0, 0.0]):

    name=parentNode.addChild(name)
    
    #################### BEHAVIOUR ##########################
    # Solvers
    name.addObject('EulerImplicitSolver', name="odesolver", rayleighStiffness="0.01", rayleighMass="0.01") #added  2 params
    name.addObject('CGLinearSolver', iterations="25", name="EpiLinearsolver", tolerance="1.0e-9", threshold="1.0e-9")
    #name.addObject('SparseLDLSolver')

    # Volumetric mesh loader
    name.addObject('MeshGmshLoader', name='volumeLoader', filename=importFile, scale3d=scale3d)

    # Tetrahedra container
    name.addObject('TetrahedronSetTopologyContainer', src='@volumeLoader', name='TetraContainer')
    name.addObject('TetrahedronSetGeometryAlgorithms', template='Vec3d')
    name.addObject('TetrahedronSetTopologyModifier') # Leave it there for the carving plugin!

    # Mechanical object and mass
    name.addObject('MechanicalObject', name='SkinMechObj', src='@volumeLoader', template='Vec3d', translation=translation) #added src for trial
    name.addObject('DiagonalMass', name="SkinMass", massDensity="2.0")#, template="Vec3d,double"

    # Forces
    name.addObject('TetrahedronFEMForceField', template='Vec3d', name='FEM', method='large', youngModulus=skin_youngModulus, poissonRatio=skin_poissonRatio)
    name.addObject('UncoupledConstraintCorrection', compliance=0.001)
    #name.addObject('LinearSolverConstraintCorrection')

    # Fixed box for constraints
    boxROI=name.addObject('BoxROI', name='boxROI', box=fixingBox, drawBoxes='true', computeTriangles='true')
    name.addObject('RestShapeSpringsForceField', name='rest', points='@boxROI.indices', stiffness='1e12', angularStiffness='1e12')

    # Border box
    name.addObject('BoxROI', name='borderBox', box=borderBox, drawBoxes='true')

    name.addObject('BoxROI', name='borderBox1', box=borderBox1, drawBoxes='true')
    name.addObject('BoxROI', name='borderBox2', box=borderBox2, drawBoxes='true')
    name.addObject('BoxROI', name='borderBox3', box=borderBox3, drawBoxes='true')
    name.addObject('BoxROI', name='borderBox4', box=borderBox4, drawBoxes='true')


    #################### COLLISION ##########################

    SkinColl = name.addChild('SkinColl')

    # Mapped from the tetra of behaviour model
    SkinColl.addObject('TriangleSetTopologyContainer', name="T_Container")
    SkinColl.addObject('TriangleSetTopologyModifier', name="T_Modifier")
    SkinColl.addObject('TriangleSetGeometryAlgorithms', template="Vec3d", name="T_GeomAlgo")
    SkinColl.addObject('Tetra2TriangleTopologicalMapping', name="default8", input="@../TetraContainer", output="@T_Container")

    # Types of collision
    if carving==True:
        SkinColl.addObject('TriangleCollisionModel', name="TriangleCollisionSkin", tags="CarvingSurface")
    else: 
        SkinColl.addObject('TriangleCollisionModel', name="TriangleCollisionSkin")


    #################### VISUALIZATION ########################
    
    SkinVisu = SkinColl.addChild('SkinVisu')
    SkinVisu.addObject('MechanicalObject', name="VisuMO")
    SkinVisu.addObject('OglModel', template="Vec3d", name="Visual", color="1 0.75 0.796", 
    material="Default Diffuse 1 0 0 1 1 Ambient 1 0 0 0.2 1 Specular 0 0 0 1 1 Emissive 0 0 0 1 1 Shininess 0 45 ")
    #SkinVisu.addObject('BarycentricMapping', template="Vec3d,Vec3d", name="default12", input="@..", output="@Visual" ) # For grids
    SkinVisu.addObject('IdentityMapping', template="Vec3d,Vec3d", name="default12", input="@..", output="@Visual" )

    # Data
    if side==0: # left
        Skin.itself=name.getLinkPath()
        Skin.MO=name.SkinMechObj.getLinkPath()
        Skin.COLL=name.SkinColl.TriangleCollisionSkin.getLinkPath()
        Skin.borderBox= name.borderBox
        Skin.borderBox1=name.borderBox1
        Skin.borderBox2=name.borderBox2
        Skin.borderBox3=name.borderBox3
        Skin.borderBox4=name.borderBox4

    if side==1: # right
        Skin.itself_right=name.getLinkPath()
        Skin.MO_right=name.SkinMechObj.getLinkPath()
        Skin.COLL_right=name.SkinColl.TriangleCollisionSkin.getLinkPath()
        Skin.borderBox_right = name.borderBox
        Skin.borderBox1_right=name.borderBox1
        Skin.borderBox2_right=name.borderBox2
        Skin.borderBox3_right=name.borderBox3
        Skin.borderBox4_right=name.borderBox4
    Skin.CONTAINER=name.TetraContainer.getLinkPath()



def GeomagicDevice(parentNode=None, name=None):
    name=parentNode.addChild(name)
    name.addObject('MechanicalObject', template="Rigid3", name="DOFs", position="@GeomagicDevice.positionDevice")
    name.addObject('MechanicalStateController', template="Rigid3", listening="true", mainDirection="-1.0 0.0 0.0")

def Scalpel(parentNode=None, name=None, translation=[0.0, 0.0, 0.0], scale3d=[0.0, 0.0, 0.0], color=[0.0, 0.0, 0.0],
geomagic=False): 
    # Taken from C:\sofa\src\examples\Components\collision\RuleBasedContactManager

    name=parentNode.addChild(name)
    name.addObject('EulerImplicitSolver',  rayleighStiffness="0.1", rayleighMass="0.1" )
    name.addObject('CGLinearSolver', iterations="25", tolerance="1e-5" ,threshold="1e-5")
    if geomagic==True:
        name.addObject('MechanicalObject',  name='InstrumentMechObject', template='Rigid3d', position="@GeomagicDevice.positionDevice", scale="1.0", rotation="0 0 10",  dz="2", dx="-4", dy="-3",  rx="0", ry="0", rz="90") #, src="@instrumentMeshLoader")
        name.addObject('RestShapeSpringsForceField', stiffness='1000', angularStiffness='1000', external_rest_shape='@../Omni/DOFs', points='0', external_points='0') 
        name.addObject('LCPForceFeedback', name="LCPFFNeedle",  forceCoef="0.1", activate="true")# Decide forceCoef value better
    else: 
        name.addObject('MechanicalObject', name="InstrumentMechObject", template="Rigid3d", scale="1.0" ,dx="8", dy="3", dz="6")
    name.addObject('UniformMass' , totalMass="3")
    name.addObject('UncoupledConstraintCorrection')

    Visu=name.addChild('Visu')
    Visu.addObject('MeshObjLoader' ,name="meshLoader_3", filename="mesh/scalpel.obj", scale="1.0", handleSeams="1" )
    Visu.addObject('OglModel' ,name="Visual" ,src="@meshLoader_3",  color="0 0.5 0.796", dz="2", dx="-4", dy="-3",  rx="0", ry="0", rz="90")
    Visu.addObject('RigidMapping' ,input="@..", output="@Visual")
    
    Surf=name.addChild('Surf')
    Surf.addObject('MeshObjLoader' ,filename="mesh/scalpel.obj" ,name="loader" )
    Surf.addObject('MeshTopology' ,src="@loader")
    Surf.addObject('MechanicalObject' ,src="@loader", scale="1.0",  dz="2", dx="-4", dy="-3",  rx="0", ry="0", rz="90")
    Surf.addObject('TriangleCollisionModel', name="Torus2Triangle" ,group="2")
    Surf.addObject('LineCollisionModel', name="Torus2Line" ,group="2")
    Surf.addObject('PointCollisionModel' ,name="Torus2Point" ,group="2")
    Surf.addObject('RigidMapping')

    collFront = name.addChild('collFront')
    collFront.addObject('MechanicalObject', template="Vec3d", name="Particle", position="4 -3.7 -8.5",  dz="2", dx="-4", dy="-3",  rx="0", ry="0", rz="90")
    collFront.addObject('SphereCollisionModel', radius="0.2", name="SphereCollisionInstrument", contactStiffness="1", tags="CarvingTool")
    collFront.addObject('RigidMapping')#, template="Rigid3d,Vec3d", name="MM->CM mapping",  input="@../InstrumentMechObject",  output="@Particle")

    Scalpel.MO=name.InstrumentMechObject.getLinkPath()
    Scalpel.POS=name.InstrumentMechObject.findData('position').value
    Scalpel.COLL_FRONT=name.collFront.SphereCollisionInstrument.getLinkPath()


def ScalpelOld(parentNode=None, name=None, rotation=[0.0, 0.0, 0.0], translation=[0.0, 0.0, 0.0],
scale3d=[0.0, 0.0, 0.0],  fixingBox=[0.0, 0.0, 0.0], importFile=None, carving=False, geomagic=False):

    name=parentNode.addChild(name)
    #################### BEHAVIOUR ##########################
    
    name.addObject('EulerImplicitSolver', name='ODE solver', rayleighStiffness="0.01", rayleighMass="1.0")
    name.addObject('CGLinearSolver', name='linear solver', iterations="25", tolerance="1e-7", threshold="1e-7")
    name.addObject('MeshObjLoader', name='instrumentMeshLoader', filename=importFile)
    if geomagic==True:
        name.addObject('MechanicalObject',  name='InstrumentMechObject', template='Rigid3d', position="@GeomagicDevice.positionDevice", scale3d=scale3d, dz="2", dx="-4", dy="-3",  rx="0", ry="0", rz="90")
        name.addObject('RestShapeSpringsForceField', stiffness='1000', angularStiffness='1000', external_rest_shape='@../Omni/DOFs', points='0', external_points='0') 
        name.addObject('LCPForceFeedback', name="LCPFFScalpel", activate="true", forceCoef="0.5")
    else:
        name.addObject('MechanicalObject',  name='InstrumentMechObject', template='Rigid3d', translation=translation, scale3d=scale3d)
    
    name.addObject('UniformMass', name='mass', totalMass="1")
    name.addObject('UncoupledConstraintCorrection')

    #################### COLLISION ##########################
    
    InstrumentColl_Front = name.addChild('InstrumentColl_Front')
    if geomagic==True:
        InstrumentColl_Front.addObject('MechanicalObject', template="Vec3d", name="Particle", position="4 -3.7 -8.5" , dz="2", dx="-4", dy="-3",  rx="0", ry="0", rz="90")
    else:
        InstrumentColl_Front.addObject('MechanicalObject', template="Vec3d", name="Particle", position="4 -3.7 -8.5" )

    if carving==True:
        InstrumentColl_Front.addObject('SphereCollisionModel', radius="0.5", name="SphereCollisionInstrument", contactStiffness="1", tags="CarvingTool")
    else:
        InstrumentColl_Front.addObject('SphereCollisionModel', radius="0.5", name="SphereCollisionInstrument", contactStiffness="1")
    InstrumentColl_Front.addObject('RigidMapping', template="Rigid3d,Vec3d", name="MM->CM mapping",  input="@../InstrumentMechObject",  output="@Particle")

    #################### VISUALIZATION ########################
    
    InstrumentVisu = name.addChild('InstrumentVisu')

    if geomagic==True:
        InstrumentVisu.addObject('OglModel', name='InstrumentVisualModel', src='@../instrumentMeshLoader', scale3d=scale3d, dz="2", dx="-4", dy="-3",  rx="0", ry="0", rz="90", color="0 0.5 0.796")
    else:
        InstrumentVisu.addObject('OglModel', name='InstrumentVisualModel', src='@../instrumentMeshLoader', scale3d=scale3d, color="0 0.5 0.796")
    InstrumentVisu.addObject('RigidMapping', template="Rigid3d,Vec3d", name='MM-VM mapping', input='@../InstrumentMechObject', output='@InstrumentVisualModel')

    # Data
    Scalpel.MO=name.InstrumentMechObject.getLinkPath()
    Scalpel.POS=name.InstrumentMechObject.findData('position').value
    Scalpel.COLL_FRONT=name.InstrumentColl_Front.SphereCollisionInstrument.getLinkPath()
    


# Training sphere
def sphere(parentNode=None, name=None, translation=[0.0, 0.0, 0.0], scale3d=[0.0, 0.0, 0.0], color=[0.0, 0.0, 0.0]):

    name=parentNode.addChild(name)
    name.addObject('MeshObjLoader', name='sphere', filename="C:\sofa\src\Chiara\mesh\sphere.obj") 
    name.addObject('OglModel', name='sphereVis', src='@sphere', scale3d="0.8 0.8 0.8", translation=translation, color=color)
    sphere.M=name.sphereVis.getLinkPath()
    sphere.color=name.sphereVis.findData('scale3d').value
  