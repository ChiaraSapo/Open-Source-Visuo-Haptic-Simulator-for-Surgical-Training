import Sofa
import numpy as np

# Data
skin_youngModulus=300
thread_youngModulus=2000
skin_poissonRatio=0.49
thread_poissonRatio=0.8

# indicesBox: to retrieve indices of all points (usually a bit bigger than fixing box)
# importFile: msh or obj file
# borderBox: used  to retrieve indices of the borders 
# side: usually left

def Skin(parentNode=None, name=None, rotation=[0.0, 0.0, 0.0], translation=[0.0, 0.0, 0.0], 
scale3d=[0.0, 0.0, 0.0],  fixingBox=[0.0, 0.0, 0.0], indicesBox=[0.0, 0.0, 0.0], borderBox=[0.0, 0.0, 0.0], importFile=None, 
carving=False, side=0, task=None):

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
    
    if task=="Suture":
        name.addObject('BoxROI', name='sphere1Box', box=[8-1, 3-1, -0.1, 8+1, 3+1, 1.5], drawBoxes='true', computeTriangles='true')
        name.addObject('BoxROI', name='sphere2Box', box=[8-1, 13-1, -0.1, 8+1, 13+1, 1.5], drawBoxes='true', computeTriangles='true')
        name.addObject('BoxROI', name='sphere3Box', box=[12-1, 7-1, -0.1, 12+1, 7+1, 1.5], drawBoxes='true', computeTriangles='true')
        name.addObject('BoxROI', name='sphere4Box', box=[12-1, 17-1, -0.1, 12+1, 17+1, 1.5], drawBoxes='true', computeTriangles='true')  



    #################### COLLISION ##########################

    SkinColl = name.addChild('SkinColl')

    # Mapped from the tetra of behaviour model
    SkinColl.addObject('TriangleSetTopologyContainer', name="T_Container")
    SkinColl.addObject('TriangleSetTopologyModifier', name="T_Modifier")
    SkinColl.addObject('TriangleSetGeometryAlgorithms', template="Vec3d", name="T_GeomAlgo")
    SkinColl.addObject('Tetra2TriangleTopologicalMapping', name="default8", input="@../TetraContainer", output="@T_Container")
    #SkinColl.addObject('MechanicalObject', template="Vec3d")

    # Types of collision
    if carving==True:
        SkinColl.addObject('TriangleCollisionModel', name="TriangleCollisionSkin", tags="CarvingSurface")
    else: 
        SkinColl.addObject('TriangleCollisionModel', name="TriangleCollisionSkin")

    #SkinColl.addObject('LineCollisionModel', name="LineCollisionSkin")
    #SkinColl.addObject('PointCollisionModel', name="PointCollisionSkin") 
    #SkinColl.addObject('IdentityMapping')

    #################### VISUALIZATION ########################
    
    SkinVisu = SkinColl.addChild('SkinVisu')
    SkinVisu.addObject('MechanicalObject', name="VisuMO")
    SkinVisu.addObject('OglModel', template="Vec3d", name="Visual", color="1 0.75 0.796", 
    material="Default Diffuse 1 0 0 1 1 Ambient 1 0 0 0.2 1 Specular 0 0 0 1 1 Emissive 0 0 0 1 1 Shininess 0 45 ")
    #SkinVisu.addObject('BarycentricMapping', template="Vec3d,Vec3d", name="default12", input="@..", output="@Visual" ) # Tried now
    SkinVisu.addObject('IdentityMapping', template="Vec3d,Vec3d", name="default12", input="@..", output="@Visual" )

    # Data
    if side==0: # left
        Skin.MO=name.SkinMechObj.getLinkPath()
        Skin.COLL=name.SkinColl.TriangleCollisionSkin.getLinkPath()
        Skin.borderBox= name.borderBox
        if task=="Suture":
            Skin.sphere1Box=name.sphere1Box
            Skin.sphere2Box=name.sphere2Box
    if side==1: # right
        Skin.MO_right=name.SkinMechObj.getLinkPath()
        Skin.COLL_right=name.SkinColl.TriangleCollisionSkin.getLinkPath()
        Skin.borderBox_right = name.borderBox
        if task=="Suture":
            Skin.sphere3Box=name.sphere3Box
            Skin.sphere4Box=name.sphere4Box





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


def GeomagicDevice(parentNode=None, name=None):
    name=parentNode.addChild(name)
    name.addObject('MechanicalObject', template="Rigid3", name="DOFs", position="@GeomagicDevice.positionDevice")
    name.addObject('MechanicalStateController', template="Rigid3", listening="true", mainDirection="-1.0 0.0 0.0")

    

def SutureNeedle(parentNode=None, name=None, rotation=[0.0, 0.0, 0.0], translation=[0.0, 0.0, 0.0],
scale3d=[0.0, 0.0, 0.0],  fixingBox=[0.0, 0.0, 0.0], importFile=None,  carving=False, geomagic=False):

    #################### BEHAVIOUR ##########################
    name=parentNode.addChild(name)
    name.addObject('EulerImplicitSolver', name='ODE solver', rayleighMass="1.0", rayleighStiffness="0.01")
    name.addObject('CGLinearSolver', name='linear solver', iterations="25", tolerance="1e-7", threshold="1e-7") #SparseLDLSolver
    name.addObject('MeshObjLoader', name='instrumentMeshLoader', filename=importFile)

    if geomagic==True:
        name.addObject('MechanicalObject',  name='InstrumentMechObject', template='Rigid3d', position="@GeomagicDevice.positionDevice", scale3d=scale3d, rotation="0 0 10" ) #, src="@instrumentMeshLoader")
        name.addObject('RestShapeSpringsForceField', stiffness='1000', angularStiffness='1000', external_rest_shape='@../Omni/DOFs', points='0', external_points='0') 
        name.addObject('LCPForceFeedback', name="LCPFFNeedle",  forceCoef="0.1", activate="true")# Decide forceCoef value better
    else: 
        name.addObject('MechanicalObject', src="@instrumentMeshLoader", name='InstrumentMechObject', template='Rigid3d', translation=translation, scale3d=scale3d)

    name.addObject('UniformMass', name='mass', totalMass="3") # With mass=1: [WARNING] 
    # [CGLinearSolver(linear solver)] denominator threshold reached at first iteration of CG. 
    # Check the 'threshold' data field, you might decrease it
    name.addObject('UncoupledConstraintCorrection') # LinearSolverConstraintCorrection

    #################### COLLISION ##########################
    
    InstrumentColl_Front = name.addChild('InstrumentColl_Front')
    if geomagic==True:
        InstrumentColl_Front.addObject('MechanicalObject', template="Vec3d", name="Particle", position="-6.98 0.02 0.05", rx="-10", ry="160", rz="180",  dz="-4", dx="0", dy="0")
    else:
        InstrumentColl_Front.addObject('MechanicalObject', template="Vec3d", name="Particle", position="-6.98 0.02 0.05")

    if carving==True:
        InstrumentColl_Front.addObject('SphereCollisionModel', radius="0.2", name="SphereCollisionInstrument", contactStiffness="1", tags="CarvingTool") # Reduced contact stiffness
    else:
        InstrumentColl_Front.addObject('SphereCollisionModel', radius="0.2", name="SphereCollisionInstrument", contactStiffness="1")
    InstrumentColl_Front.addObject('RigidMapping', template="Rigid3d,Vec3d", name="MM->CM mapping",  input="@../InstrumentMechObject",  output="@Particle")

    InstrumentColl_Back = name.addChild('InstrumentColl_Back')

    if geomagic==True:
        InstrumentColl_Back.addObject('MechanicalObject', template="Vec3d", name="Particle2", position="0 0.02 0.05", rx="-10", ry="160", rz="180",  dz="-4", dx="0", dy="0")
    else:
        InstrumentColl_Back.addObject('MechanicalObject', template="Vec3d", name="Particle2", position="0 0.02 0.05")

    InstrumentColl_Back.addObject('SphereCollisionModel', radius="0.2", name="SphereCollisionInstrument2", contactStiffness="1")
    InstrumentColl_Back.addObject('RigidMapping', template="Rigid3d,Vec3d", name="MM->CM mapping",  input="@../InstrumentMechObject",  output="@Particle2")

    #################### VISUALIZATION ########################
    
    InstrumentVisu = name.addChild('InstrumentVisu')
    if geomagic==True:
        InstrumentVisu.addObject('OglModel', name='InstrumentVisualModel', src='@../instrumentMeshLoader', scale3d=scale3d, rx="-10", ry="160", rz="180",  dz="-4", dx="0", dy="0",  color="0 0.5 0.796")
    else:
        InstrumentVisu.addObject('OglModel', name='InstrumentVisualModel', src='@../instrumentMeshLoader', scale3d=scale3d,  color="0 0.5 0.796")
    InstrumentVisu.addObject('RigidMapping', template="Rigid3d,Vec3d", name='MM-VM mapping', input='@../InstrumentMechObject', output='@InstrumentVisualModel')

    # Data
    SutureNeedle.MO=name.InstrumentMechObject.getLinkPath()
    SutureNeedle.COLL_BACK_MO=name.InstrumentColl_Back.Particle2.getLinkPath()
    SutureNeedle.POS=name.InstrumentMechObject.findData('position').value
    SutureNeedle.COLL_FRONT=name.InstrumentColl_Front.SphereCollisionInstrument.getLinkPath()
    SutureNeedle.COLL_BACK=name.InstrumentColl_Back.SphereCollisionInstrument2.getLinkPath()
    

 

def Scalpel(parentNode=None, name=None, rotation=[0.0, 0.0, 0.0], translation=[0.0, 0.0, 0.0],
scale3d=[0.0, 0.0, 0.0],  fixingBox=[0.0, 0.0, 0.0], importFile=None, carving=False, geomagic=False):

    name=parentNode.addChild(name)
    #################### BEHAVIOUR ##########################
    
    name.addObject('EulerImplicitSolver', name='ODE solver', rayleighStiffness="0.01", rayleighMass="1.0")
    name.addObject('CGLinearSolver', name='linear solver', iterations="25", tolerance="1e-7", threshold="1e-7")
    name.addObject('MeshObjLoader', name='instrumentMeshLoader', filename=importFile)
    if geomagic==True:
        name.addObject('MechanicalObject', src="@instrumentMeshLoader", name='InstrumentMechObject', template='Rigid3d', position="@GeomagicDevice.positionDevice", scale3d=scale3d, dz="2", dx="-4", dy="-3",  rx="0", ry="0", rz="90")
        name.addObject('RestShapeSpringsForceField', stiffness='1000', angularStiffness='1000', external_rest_shape='@../Omni/DOFs', points='0', external_points='0') 
        name.addObject('LCPForceFeedback', name="LCPFFScalpel", activate="true", forceCoef="0.5")
    else:
        name.addObject('MechanicalObject', src="@instrumentMeshLoader", name='InstrumentMechObject', template='Rigid3d', translation=translation, scale3d=scale3d)
    
    name.addObject('UniformMass', name='mass', totalMass="1")
    name.addObject('UncoupledConstraintCorrection')

    #################### COLLISION ##########################
    
    InstrumentColl_Front = name.addChild('InstrumentColl_Front')
    InstrumentColl_Front.addObject('MechanicalObject', template="Vec3d", name="Particle", position="4 -3.7 -8.5" , dz="2", dx="-4", dy="-3",  rx="0", ry="0", rz="90")

    if carving==True:
        InstrumentColl_Front.addObject('SphereCollisionModel', radius="0.5", name="SphereCollisionInstrument", contactStiffness="1", tags="CarvingTool")
    else:
        InstrumentColl_Front.addObject('SphereCollisionModel', radius="0.5", name="SphereCollisionInstrument", contactStiffness="1")
    InstrumentColl_Front.addObject('RigidMapping', template="Rigid3d,Vec3d", name="MM->CM mapping",  input="@../InstrumentMechObject",  output="@Particle")

    # InstrumentColl_Back = name.addChild('InstrumentColl_Back')
    
    # InstrumentColl_Back.addObject('MechanicalObject', template="Vec3d", name="Particle2", position="0 0.02 0.05")
    # if carving==True:
    #     InstrumentColl_Back.addObject('SphereCollisionModel', radius="1", name="SphereCollisionInstrument2", contactStiffness="2", tags="CarvingTool")
    # else:
    #     InstrumentColl_Back.addObject('SphereCollisionModel', radius="1", name="SphereCollisionInstrument2", contactStiffness="2")
    # InstrumentColl_Back.addObject('RigidMapping', template="Rigid3d,Vec3d", name="MM->CM mapping",  input="@../InstrumentMechObject",  output="@Particle2")

    #################### VISUALIZATION ########################
    
    InstrumentVisu = name.addChild('InstrumentVisu')
    InstrumentVisu.addObject('OglModel', name='InstrumentVisualModel', src='@../instrumentMeshLoader', scale3d=scale3d, dz="2", dx="-4", dy="-3",  rx="0", ry="0", rz="90", color="0 0.5 0.796")
    InstrumentVisu.addObject('RigidMapping', template="Rigid3d,Vec3d", name='MM-VM mapping', input='@../InstrumentMechObject', output='@InstrumentVisualModel')

    # Data
    Scalpel.MO=name.InstrumentMechObject.getLinkPath()
    Scalpel.POS=name.InstrumentMechObject.findData('position').value
    Scalpel.COLL_FRONT=name.InstrumentColl_Front.SphereCollisionInstrument.getLinkPath()
    


# Training sphere
def sphere(parentNode=None, name=None, translation=[0.0, 0.0, 0.0], scale3d=[0.0, 0.0, 0.0], color=[0.0, 0.0, 0.0]):

    name=parentNode.addChild(name)
    name.addObject('MeshObjLoader', name='sphere', filename="C:\sofa\src\Chiara\mesh\sphere.obj") 
    name.addObject('OglModel', name='InstrumentVisualModel', src='@sphere', scale3d="0.8 0.8 0.8", translation=translation, color=color)
   
