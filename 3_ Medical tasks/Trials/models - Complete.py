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
    


def SutureNeedle2(parentNode=None, name=None, rotation=[0.0, 0.0, 0.0], translation=[0.0, 0.0, 0.0],
scale3d=[0.0, 0.0, 0.0],  fixingBox=[0.0, 0.0, 0.0], importFile=None,  carving=False, geomagic=False):
    name=parentNode.addChild(name)
    name.addObject('EulerImplicitSolver', name="ODE solver", rayleighStiffness="0.01", rayleighMass="0.02")
    name.addObject('SparseLDLSolver')

    name.addObject('MechanicalObject', name="instrumentState", template="Rigid3")
    name.addObject('UniformMass', name="mass", totalMass="0.2" )
    name.addObject('RestShapeSpringsForceField', stiffness='1000', angularStiffness='1000', external_rest_shape='@../Omni/DOFs', points='0', external_points='0')
    name.addObject('LCPForceFeedback', name="LCPFF1", activate="true", forceCoef="0.05")
    name.addObject('UncoupledConstraintCorrection')

    VisuTool=name.addChild('VisuTool')
    VisuTool.addObject('MeshObjLoader', name="meshLoader_1", filename="Demos/Dentistry/data/mesh/dental_instrument.obj", handleSeams="1")
    VisuTool.addObject('OglModel', name="InstrumentVisualModel" ,src="@meshLoader_1", color="1.0 0.2 0.2 1.0" ,ry="-180", rz="-90" ,dz="3.5", dx="-0.3")
    VisuTool.addObject('RigidMapping' ,name="MM->VM mapping", input="@instrumentState", output="@InstrumentVisualModel")

    CollisionModel=VisuTool.addChild('CollisionModel')
    CollisionModel.addObject('MeshObjLoader' ,filename="Demos/Dentistry/data/mesh/dental_instrument_centerline.obj",  name="loader")
    CollisionModel.addObject('MeshTopology', src="@loader", name="InstrumentCollisionModel" )
    CollisionModel.addObject('MechanicalObject' ,src="@loader", name="instrumentCollisionState" , ry="-180", rz="-90" ,dz="3.5", dx="-0.3")
    CollisionModel.addObject('LineCollisionModel', contactStiffness="0.001")
    CollisionModel.addObject('PointCollisionModel' ,contactStiffness="0.001" ,name="Instrument")
    CollisionModel.addObject('RigidMapping', name="MM->CM mapping" ,input="@instrumentState" ,output="@instrumentCollisionState" )


 

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
   





   





    
################# Three layered skin ############################

x_vertices=10
y_vertices=10

x_offset=-10
y_offset=-10
z_offset=-20

x_length=20+x_offset
y_length=20+y_offset
n_vertices_per_layer=x_vertices*y_vertices

z_epi=3 #thickness=0.1mm youngModulus=1MPa
z_derma=z_epi*2 #thickness=1mm youngModulus=88-300kPa
z_hypo=z_epi*3 #thickness=1.2mm youngModulus=34kPa

# Actual values to try
poissonRatio_ALL=0.48
youngModulus_H=340#34000
youngModulus_D=300#300000
youngModulus_E=100#1000000

def computeIndices(layer, z):
    result=' '
    indices = np.array(range(z*n_vertices_per_layer)).reshape(z,n_vertices_per_layer)

    for i in range(n_vertices_per_layer):
        if layer=="bottom":
            result += str(indices[0,i]) + " "
        elif layer=="top":
            result += str(indices[-1,i]) + " "

    return result

def ThreeLayeredSkin(parentNode=None, name=None, rotation=[0.0, 0.0, 0.0], translation=[0.0, 0.0, 0.0], scale3d=[0.0, 0.0, 0.0],  fixingBox=[0.0, 0.0, 0.0], carving=False):
    
    ###################################################################
    #--------------------- SKIN EPIDERMIS LAYER ----------------------#
    ###################################################################
    epi=parentNode.addChild('epi')
    epi.addObject('EulerImplicitSolver', name="ODE solver", rayleighStiffness="0.01", rayleighMass="0.01")
    epi.addObject('CGLinearSolver', iterations="25", name="linear solver", tolerance="1.0e-9", threshold="1.0e-9")
    #epi.addObject('SparseLDLSolver')

    #epi.addObject('RegularGridTopology', name="grid", n="5 2 2", min="-5 -5 -10", max="3 4 10", p0="-4 -4 -10")
    epi.addObject('RegularGridTopology', name="grid", nx=x_vertices, ny=y_vertices, nz=z_epi, xmin=x_offset, xmax=x_length, ymin=y_offset, ymax=y_length, zmin=z_derma+z_hypo+z_offset, zmax=(z_hypo+z_derma+z_epi+z_offset+1))
    epi.addObject('HexahedronSetGeometryAlgorithms')

    epi.addObject('MechanicalObject', template="Vec3d", name="Hexa_E", scale3d="2 1 0.2", position="0 0 -8", showVectors="true", drawMode="2")
    epi.addObject('UniformMass', name="SkinMass", totalMass="2.0", template='Vec3d,double')
    
    epi2=epi.addChild('epi2')

    epi2.addObject('TetrahedronSetTopologyContainer', name="Q_Container")
    epi2.addObject('TetrahedronSetTopologyModifier', name="Q_Modifier")
    epi2.addObject('TetrahedronSetGeometryAlgorithms', template="Vec3d", name="Q_GeomAlgo")
    epi2.addObject('Hexa2TetraTopologicalMapping', name="default6", input="@../grid", output="@Q_Container")
    epi2.addObject('TetrahedronSetTopologyModifier') # Leave it there for the carving plugin!

    epi2.addObject('MechanicalObject', template="Vec3d", name="Hexa_E", scale3d="2 1 0.2", position="0 0 -8", showVectors="true", drawMode="2")
    epi2.addObject('UniformMass', name="SkinMass", totalMass="2.0", template='Vec3d,double')

    epi2.addObject('UncoupledConstraintCorrection')

    tri=epi2.addChild('tri')
    tri.addObject('TriangleSetTopologyContainer', name="T_Container")
    tri.addObject('TriangleSetTopologyModifier', name="T_Modifier")
    tri.addObject('TriangleSetGeometryAlgorithms', template="Vec3d", name="T_GeomAlgo")
    tri.addObject('Tetra2TriangleTopologicalMapping', name="default8", input="@../Q_Container", output="@T_Container")
    tri.addObject('TriangleCollisionModel', name="EpiCollision", contactStiffness="0.01", tags="CarvingSurface")

    visu=tri.addChild('visu') 
    visu.addObject('MechanicalObject', name="VisuMO")
    visu.addObject('OglModel', template="Vec3d", name="Visual", color="1 0.75 0.796", material="Default Diffuse 1 0 0 1 1 Ambient 1 0 0 0.2 1 Specular 0 0 0 1 1 Emissive 0 0 0 1 1 Shininess 0 45 ")
    visu.addObject('OglViewport', screenPosition="0 0", screenSize="250 250", cameraPosition="-0.285199 -15.2745 16.7859", cameraOrientation="0.394169 0.0120415 0.00490558 0.918946" )
    visu.addObject('IdentityMapping', template="Vec3d,Vec3d", name="default12", input="@..", output="@Visual" )
    

    
    # ###############################################################
    # #--------------------- SKIN DERMA LAYER ----------------------#
    # ###############################################################
    # derma=parentNode.addChild('derma')
    # derma.addObject('EulerImplicitSolver', name="ODE solver", rayleighStiffness="0.01", rayleighMass="0.01")
    # derma.addObject('SparseLDLSolver')
    
    # derma.addObject('MechanicalObject', template="Vec3d", name="Hexa_D", scale3d="2 1 0.2", position="0 0 -8", showVectors="true", drawMode="2")

    # derma.addObject('RegularGridTopology', name="grid", nx=x_vertices, ny=y_vertices, nz=z_derma, xmin=x_offset, xmax=x_length, ymin=y_offset, ymax=y_length, zmin=z_hypo+z_offset, zmax=(z_hypo+z_derma+z_offset+1))
    # #derma.addObject('HexahedronSetGeometryAlgorithms')
    
    # derma.addObject('DiagonalMass', template="Vec3d,double", name="Mass", massDensity="1.0")
    # #derma.addObject('HexahedronFEMForceField', template="Vec3d", name="FEM", poissonRatio=poissonRatio_ALL, youngModulus=youngModulus_D )
    # #derma.addObject('SparseLDLSolver', name="preconditioner")
    # derma.addObject('UncoupledConstraintCorrection')

    # quad=derma.addChild('quad')
    # quad.addObject('QuadSetTopologyContainer', name="Q_Container")
    # quad.addObject('QuadSetTopologyModifier', name="Q_Modifier")
    # #quad.addObject('QuadSetGeometryAlgorithms', template="Vec3d", name="Q_GeomAlgo")
    # quad.addObject('Hexa2QuadTopologicalMapping', name="default6", input="@../grid", output="@Q_Container")

    # tri=quad.addChild('tri')
    # tri.addObject('TriangleSetTopologyContainer', name="T_Container")
    # tri.addObject('TriangleSetTopologyModifier', name="T_Modifier")
    # #tri.addObject('TriangleSetGeometryAlgorithms', template="Vec3d", name="T_GeomAlgo")
    # tri.addObject('Quad2TriangleTopologicalMapping', name="default8", input="@../Q_Container", output="@T_Container")
    # #tri.addObject('TriangleCollisionModel', name="SkinCollision", contactStiffness="0.01")

    # visu=tri.addChild('visu')
    # visu.addObject('OglModel', template="Vec3d", name="Visual", color="1 1 0.7", material="Default Diffuse 1 0 0 1 1 Ambient 1 0 0 0.2 1 Specular 0 0 0 1 1 Emissive 0 0 0 1 1 Shininess 0 45 ")
    # visu.addObject('OglViewport', screenPosition="0 0", screenSize="250 250", cameraPosition="-0.285199 -15.2745 16.7859", cameraOrientation="0.394169 0.0120415 0.00490558 0.918946" )
    # visu.addObject('IdentityMapping', template="Vec3d,Vec3d", name="default12", input="@..", output="@Visual" )


    # ####################################################################
    # #--------------------- SKIN HYPODERMIS LAYER ----------------------#
    # ####################################################################
    # hypo=parentNode.addChild('hypo')
    # hypo.addObject('EulerImplicitSolver', name="ODE solver", rayleighStiffness="0.01", rayleighMass="0.01")
    # hypo.addObject('SparseLDLSolver')
    
    # hypo.addObject('MechanicalObject', template="Vec3d", name="Hexa_H", scale3d="2 1 0.2", position="0 0 -8", showVectors="true", drawMode="2")
    # hypo.addObject('RegularGridTopology', name="grid", nx=x_vertices, ny=y_vertices, nz=z_hypo, xmin=x_offset, xmax=x_length, ymin=y_offset, ymax=y_length, zmin=z_offset, zmax=(z_hypo+z_offset))
    # #, name="grid", n="8 8 2", min="-5 -4 -10", max="3 4 10", p0="-4 -4 -10" )
    # #, name="grid", nx=x_vertices, ny=y_vertices, nz=z_hypo, xmin=x_offset, xmax=x_length-6, ymin=y_offset, ymax=y_length-1, zmin="0", zmax=(z_hypo))
    # #hypo.addObject('HexahedronSetGeometryAlgorithms')
    
    # hypo.addObject('DiagonalMass', template="Vec3d,double", name="Mass", massDensity="1.0")
    # #hypo.addObject('HexahedronFEMForceField', template="Vec3d", name="FEM", poissonRatio=poissonRatio_ALL, youngModulus=youngModulus_H )
    # #hypo.addObject('SparseLDLSolver', name="preconditioner")
    # hypo.addObject('UncoupledConstraintCorrection')
    # hypo.addObject('FixedConstraint', template="Vec3d", name="Fixed Dofs", indices=computeIndices("bottom", z_hypo))
    # hypo.addObject('FixedPlaneConstraint', template="Vec3d", name="defaultPlane", direction="0 0 1", dmin="0") #??????????????????????
    
    # quad=hypo.addChild('quad')
    # quad.addObject('QuadSetTopologyContainer', name="Q_Container")
    # quad.addObject('QuadSetTopologyModifier', name="Q_Modifier")
    # #quad.addObject('QuadSetGeometryAlgorithms', template="Vec3d", name="Q_GeomAlgo")
    # quad.addObject('Hexa2QuadTopologicalMapping', name="default6", input="@../grid", output="@Q_Container")

    # tri=quad.addChild('tri')
    # tri.addObject('TriangleSetTopologyContainer', name="T_Container")
    # tri.addObject('TriangleSetTopologyModifier', name="T_Modifier")
    # #tri.addObject('TriangleSetGeometryAlgorithms', template="Vec3d", name="T_GeomAlgo")
    # tri.addObject('Quad2TriangleTopologicalMapping', name="default8", input="@../Q_Container", output="@T_Container")
    # #tri.addObject('TriangleCollisionModel', name="SkinCollision", contactStiffness="0.01")

    # visu=tri.addChild('visu')
    # visu.addObject('OglModel', template="Vec3d", name="Visual", color="1 1 0.4", material="Default Diffuse 1 0 0 1 1 Ambient 1 0 0 0.2 1 Specular 0 0 0 1 1 Emissive 0 0 0 1 1 Shininess 0 45 ")
    # visu.addObject('OglViewport', screenPosition="0 0", screenSize="250 250", cameraPosition="-0.285199 -15.2745 16.7859", cameraOrientation="0.394169 0.0120415 0.00490558 0.918946" )
    # visu.addObject('IdentityMapping', template="Vec3d,Vec3d", name="default12", input="@..", output="@Visual" )




    # ############################################################
    # #--------------------- ATTACH LAYERS ----------------------#
    # ############################################################    
    # parentNode.addObject('AttachConstraint', name="lowerConstraint", object1="@hypo",       object2="@derma",     indices1=computeIndices("top", z_hypo),  indices2=computeIndices("bottom", z_derma))
    # parentNode.addObject('AttachConstraint', name="upperConstraint", object1="@derma",      object2="@epi",       indices1=computeIndices("top", z_derma), indices2=computeIndices("bottom", z_epi))
    
    
    