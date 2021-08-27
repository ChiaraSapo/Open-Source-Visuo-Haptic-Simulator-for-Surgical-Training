# Data

scale3d_skin="0.25 0.65 0.05"
scale3d_needle="3 3 3"
scale3d_thread="0.5 0.5 0.5"

pointPosition_onNeedle="-6.98 0.02 0.05" #N: 5,5,5

GeomagicPosition="0 20 15"
skinVolume_fileName="C:\sofa\src\Chiara\mesh\skin_volume_403020_05" #03 troppo lento
needleVolume_fileName="C:\sofa\src\Chiara\mesh\suture_needle.obj"
threadVolume_fileName="C:\sofa\src\Chiara\mesh\threadCh2"

# Data
skin_youngModulus=3000#300
thread_youngModulus=2000
skin_poissonRatio=0.1
thread_poissonRatio=0.8


## This function defines a training sphere node with visual model
# @param parentNode: parent node of the sphere
# @param name: name of the node
# @param translation: translation
# @param scale3d: scale of the sphere along all directions
# @param color: color of the sphere
# @param SphereModelNumber: indicates the number of the sphere (its position on the skin)

def sphere(parentNode=None, name=None, translation=[0.0, 0.0, 0.0], scale3d=[0.0, 0.0, 0.0], color=[0.0, 0.0, 0.0], SphereModelNumber=None):

    name=parentNode.addChild(name)
    name.addObject('MeshObjLoader', name='sphere', filename="C:\sofa\src\Chiara\mesh\sphere.obj") 
    name.addObject('OglModel', name='sphereVis', src='@sphere', scale3d="1 1 1", translation=translation, color=color)
    if SphereModelNumber=="M1":
        sphere.M1=name.sphereVis
    if SphereModelNumber=="M2":
        sphere.M2=name.sphereVis
    if SphereModelNumber=="M3":
        sphere.M3=name.sphereVis
    if SphereModelNumber=="M4":
        sphere.M4=name.sphereVis


## This function defines a training ring node with behavior/collision/visual models
# @param parentNode: parent node of the ring
# @param name: name of the node
# @param translation: translation
# @param scale3d: scale of the ring along all directions
# @param RingModelNumber: indicates the number of the ring (its position on the skin)

def ring(parentNode=None, name=None, translation=[0, 0, 0], scale3d=[0.0, 0.0, 0.0],  RingModelNumber=None): 
    # Taken from C:\sofa\src\examples\Components\collision\RuleBasedContactManager

    name=parentNode.addChild(name)
    name.addObject('EulerImplicitSolver',  rayleighStiffness="0.1", rayleighMass="0.1" )
    name.addObject('CGLinearSolver', iterations="25", tolerance="1e-5" ,threshold="1e-5")
    name.addObject('MechanicalObject', template="Rigid3d", scale="1.1" ,dx=translation[0], dy=translation[1], dz=translation[2])
    name.addObject('UniformMass' ,filename="BehaviorModels/torus.rigid")
    name.addObject('UncoupledConstraintCorrection')
    name.addObject('BoxROI', name='boxROI', box=[translation[0]-1,translation[1]-1,translation[2]-3,translation[0]+1,translation[1]+1,translation[2]], drawBoxes='true', computeTriangles='true')
    name.addObject('RestShapeSpringsForceField', name='rest', points='@boxROI.indices', stiffness='1e12', angularStiffness='1e12')
    
    Visu=name.addChild('Visu')
    Visu.addObject('MeshObjLoader' ,name="meshLoader_3", filename="mesh/torus.obj", scale="1.1", handleSeams="1" )
    Visu.addObject('OglModel' ,name="VisualOGL" ,src="@meshLoader_3",material="Default Diffuse 1 0 0.5 0 1 Ambient 1 0 0.1 0 1 Specular 0 0 0.5 0 1 Emissive 0 0 0.5 0 1 Shininess 0 45")
    Visu.addObject('RigidMapping' ,input="@..", output="@VisualOGL")
    
    Surf=name.addChild('Surf')
    Surf.addObject('MeshObjLoader' ,filename="mesh/torus_for_collision.obj" ,name="loader" )
    Surf.addObject('MeshTopology' ,src="@loader")
    Surf.addObject('MechanicalObject' ,src="@loader", scale="1.1")
    Surf.addObject('TriangleCollisionModel', name="Torus2Triangle" ,group="2")
    Surf.addObject('LineCollisionModel', name="Torus2Line" ,group="2")
    Surf.addObject('PointCollisionModel' ,name="Torus2Point" ,group="2")
    Surf.addObject('RigidMapping')
    
    if RingModelNumber=="M1":
        ring.C1=name.Surf.Torus2Triangle.getLinkPath()
        ring.V1=name.Visu.VisualOGL
        ring.itself1=name
    if RingModelNumber=="M2":
        ring.C2=name.Surf.Torus2Triangle.getLinkPath()
        ring.V2=name.Visu.VisualOGL
    if RingModelNumber=="M3":
        ring.C3=name.Surf.Torus2Triangle.getLinkPath()
        ring.V3=name.Visu.VisualOGL
    if RingModelNumber=="M4":
        ring.C4=name.Surf.Torus2Triangle.getLinkPath()
        ring.V4=name.Visu.VisualOGL
    

## This function defines a skin patch node with behavior/collision/visual models
# @param parentNode: parent node of the skin patch
# @param name: name of the behavior node
# @param rotation: rotation 
# @param translation: translation
# @param scale3d: scale of the skin along all directions
# @param fixingBox: vertices of the box that fixes the skin base
# @param side: Can be set to 0: left patch, 1: right patch. 
# @param sphere1Box: vertices of box1 that computes indices underneath sphere1
# @param sphere2Box: vertices of box2 that computes indices underneath sphere2
# @param sphere3Box: vertices of box3 that computes indices underneath sphere3
# @param sphere4Box: vertices of box4 that computes indices underneath sphere4

def Skin(parentNode=None, name=None, rotation=[0.0, 0.0, 0.0], translation=[0.0, 0.0, 0.0], 
scale3d=[0.0, 0.0, 0.0],  fixingBox=[0.0, 0.0, 0.0],
side=0, sphere1Box=[0.0, 0.0, 0.0], sphere2Box=[0.0, 0.0, 0.0],sphere3Box=[0.0, 0.0, 0.0],sphere4Box=[0.0, 0.0, 0.0]):

    name=parentNode.addChild(name)
    
    #################### BEHAVIOUR ##########################
    # Solvers
    name.addObject('EulerImplicitSolver', name="odesolver", rayleighStiffness="0.01", rayleighMass="0.01") #added the 2 params
    name.addObject('CGLinearSolver', iterations="25", name="EpiLinearsolver", tolerance="1.0e-9", threshold="1.0e-9")

    # Volumetric mesh loader

    name.addObject('MeshGmshLoader', name='volumeLoader', filename="C:\sofa\src\Chiara\mesh\skin_volume_403020_05", scale3d=scale3d)

    # Tetrahedra container
    name.addObject('TetrahedronSetTopologyContainer', src='@volumeLoader', name='TetraContainer')
    name.addObject('TetrahedronSetGeometryAlgorithms', template='Vec3d')
    name.addObject('TetrahedronSetTopologyModifier') # Leave it there for the carving plugin!

    # Mechanical object and mass
    name.addObject('MechanicalObject', name='SkinMechObj',  template='Vec3d', translation=translation) #src=,'@volumeLoader') added src for trial
    name.addObject('DiagonalMass', name="SkinMass", massDensity="2.0")#, template="Vec3d,double"

    # Forces
    name.addObject('TetrahedronFEMForceField', template='Vec3d', name='FEM', method='large', youngModulus=skin_youngModulus, poissonRatio=skin_poissonRatio)
    name.addObject('UncoupledConstraintCorrection', compliance=0.001)
    #name.addObject('LinearSolverConstraintCorrection')

    # Fixed box for constraints
    boxROI=name.addObject('BoxROI', name='boxROI', box=fixingBox, drawBoxes='true', computeTriangles='true')
    name.addObject('RestShapeSpringsForceField', name='rest', points='@boxROI.indices', stiffness='1e12', angularStiffness='1e12')
    
    if sphere1Box!=[0.0, 0.0, 0.0] or sphere3Box!=[0.0, 0.0, 0.0]:
        if side==0: 
            name.addObject('BoxROI', name='sphere1Box', box=sphere1Box, drawBoxes='true', computeTriangles='true')
            name.addObject('BoxROI', name='sphere2Box', box=sphere2Box, drawBoxes='true', computeTriangles='true')
            #name.addObject('BoxROI', name='sphere3Box', box=[12-2, 7-2, -0.1, 12+2, 7+2, 3], drawBoxes='true', computeTriangles='true')
            #name.addObject('BoxROI', name='sphere4Box', box=[12-2, 17-2, -0.1, 12+2, 17+2, 3], drawBoxes='true', computeTriangles='true')  
        else:
            #name.addObject('BoxROI', name='sphere1Box', box=[8-2, 3-2, -0.1, 8+2, 3+2, 3], drawBoxes='true', computeTriangles='true')
            #name.addObject('BoxROI', name='sphere2Box', box=[8-2, 13-2, -0.1, 8+2, 13+2, 3], drawBoxes='true', computeTriangles='true')
            name.addObject('BoxROI', name='sphere3Box', box=sphere3Box, drawBoxes='true', computeTriangles='true')
            name.addObject('BoxROI', name='sphere4Box', box=sphere4Box, drawBoxes='true', computeTriangles='true')  
    
    #################### COLLISION ##########################

    SkinColl = name.addChild('SkinColl')

    # Mapped from the tetra of behaviour model
    SkinColl.addObject('TriangleSetTopologyContainer', name="T_Container")
    SkinColl.addObject('TriangleSetTopologyModifier', name="T_Modifier")
    SkinColl.addObject('TriangleSetGeometryAlgorithms', template="Vec3d", name="T_GeomAlgo")
    SkinColl.addObject('Tetra2TriangleTopologicalMapping', name="default8", input="@../TetraContainer", output="@T_Container")
    #SkinColl.addObject('MechanicalObject', template="Vec3d")

    # Types of collision
    SkinColl.addObject('TriangleCollisionModel', name="TriangleCollisionSkin", tags="CarvingSurface")

    # JUST UNCOMMENTED
    SkinColl.addObject('LineCollisionModel', name="LineCollisionSkin")
    SkinColl.addObject('PointCollisionModel', name="PointCollisionSkin") 
    #SkinColl.addObject('IdentityMapping')

    #################### VISUALIZATION ########################
    
    SkinVisu = SkinColl.addChild('SkinVisu')
    SkinVisu.addObject('MechanicalObject', name="VisuMO")
    SkinVisu.addObject('OglModel', template="Vec3d", name="Visual", color="1 0.75 0.796", 
    material="Default Diffuse 1 0 0 1 1 Ambient 0 0 0 0.2 0 Specular 0 0 0 0 0 Emissive 0 0 0 1 1 Shininess 0 100 ")
    #SkinVisu.addObject('BarycentricMapping', template="Vec3d,Vec3d", name="default12", input="@..", output="@Visual" ) # For grids
    SkinVisu.addObject('IdentityMapping', template="Vec3d,Vec3d", name="default12", input="@..", output="@Visual" )

    # Data
    if side==0: # left
        Skin.itself=name.getLinkPath()
        Skin.MO=name.SkinMechObj.getLinkPath()
        Skin.COLL=name.SkinColl.TriangleCollisionSkin.getLinkPath()
        Skin.COLL_TAG=name.SkinColl.TriangleCollisionSkin
        if sphere1Box!=[0.0, 0.0, 0.0]:
            Skin.sphere1Box=name.sphere1Box
            Skin.sphere2Box=name.sphere2Box

    if side==1: # right
        Skin.itself_right=name.getLinkPath()
        Skin.MO_right=name.SkinMechObj.getLinkPath()
        Skin.COLL_right=name.SkinColl.TriangleCollisionSkin.getLinkPath()
        Skin.COLL_TAG_right=name.SkinColl.TriangleCollisionSkin
        if sphere3Box!=[0.0, 0.0, 0.0]:
            Skin.sphere3Box=name.sphere3Box
            Skin.sphere4Box=name.sphere4Box

    Skin.CONTAINER=name.TetraContainer.getLinkPath()

    return name


## This function defines a suture needle node with behavior/collision/visual models
# @param parentNode: parent node of the suture needle
# @param name: name of the behavior node
# @param scale3d: scale of the needle along all directions
# @param geomagic: if True, the needle is positioned on the Geomagic end effector
# @param position: position of the geomagic end effector
# @param external_rest_shape: rest shape of the geomagic end effector
# @param monitor: if True, saves position, velocity and force of the needle 
# @param file1: name of the file that saves positions
# @param file2: name of the file that saves velocities
# @param file3: name of the file that saves forces

def SutureNeedle(parentNode=None, name=None, scale3d=[0.0, 0.0, 0.0], 
position="@GeomagicDevice.positionDevice", external_rest_shape='@../Omni/DOFs', # position and external_rest_shape are set by default for the single station case 
monitor=False, file1=None, file2=None, file3=None, rx=0, ry=0, rz=0): # If plots are desired: save results in three different files
    
    # Taken from C:\sofa\src\examples\Components\collision\RuleBasedContactManager

    name=parentNode.addChild(name)
    name.addObject('EulerImplicitSolver',  rayleighStiffness="0.1", rayleighMass="0.1" )
    name.addObject('CGLinearSolver', iterations="25", tolerance="1e-5" ,threshold="1e-5")
    name.addObject('MechanicalObject',  name='InstrumentMechObject', template='Rigid3d', position=position, scale3d="2", rotation="0 0 10" ) #, src="@instrumentMeshLoader")
    name.addObject('RestShapeSpringsForceField', name="InstrumentRestShape", stiffness='100', angularStiffness='100', external_rest_shape=external_rest_shape, points='0', external_points='0') 
    name.addObject('LCPForceFeedback', name="LCPFFNeedle",  forceCoef="0.005", activate="true")# Decide forceCoef value better
    #SutureNeedle.RS=name.InstrumentRestShape
    name.addObject('UniformMass' , totalMass="3")
    name.addObject('UncoupledConstraintCorrection')

    Visu=name.addChild('Visu')
    Visu.addObject('MeshObjLoader' ,name="meshLoader_3", filename="mesh/Suture_needle.obj", scale="2.0", handleSeams="1" )
    Visu.addObject('OglModel', name="Visual", src='@meshLoader_3', rx=rx, ry=ry, rz=rz,  dz="0", dx="0", dy="0",  color="0 0.5 0.796", scale=1)
    Visu.addObject('RigidMapping' ,input="@..", output="@Visual")
    
    Surf=name.addChild('Surf')
    Surf.addObject('MeshObjLoader' ,filename="mesh/Suture_needle.obj" ,name="loader" )
    Surf.addObject('MeshTopology' ,src="@loader")
    Surf.addObject('MechanicalObject' ,src="@loader", scale="2.0", rx=rx, ry=ry, rz=rz,  dz="0", dx="0", dy="0") #rz=180
    #Surf.addObject('TriangleCollisionModel', name="Torus2Triangle") # DO NOT UNCOMMENT
    #Surf.addObject('LineCollisionModel', name="Torus2Line" ) # DO NOT UNCOMMENT
    Surf.addObject('PointCollisionModel' ,name="Torus2Point")
    Surf.addObject('RigidMapping')

    collFront = name.addChild('collFront') #"-4.2 0.02 -0.25" for scale5
    collFront.addObject('MechanicalObject', template="Vec3d", name="Particle", position="-2.9 0.02 -0.4", rx=rx, ry=ry, rz=rz,  dz="0", dx="0", dy="0")
    collFront.addObject('SphereCollisionModel', radius="0.3", name="SphereCollisionInstrument", contactStiffness="2", tags="CarvingTool")
    collFront.addObject('RigidMapping', name="MM->CM mapping",  input="@../InstrumentMechObject",  output="@Particle")

    collBack = name.addChild('collBack') #"0 0.007 -0.25" for scale5
    collBack.addObject('MechanicalObject', template="Vec3d", name="Particle2", position="0 0.007 -0.25", rx=rx, ry=ry, rz=rz,  dz="0", dx="0", dy="0")
    collBack.addObject('SphereCollisionModel', radius="0.2", name="SphereCollisionInstrument2", contactStiffness="2")
    collBack.addObject('RigidMapping', name="MM->CM mapping",  input="@../InstrumentMechObject",  output="@Particle2")
    
    if monitor==True:
        collBack.addObject("Monitor", name=file1, indices="0", listening="1", TrajectoriesPrecision="0.1", ExportPositions="true", showTrajectories=0)
        collBack.addObject("Monitor", name=file2, indices="0", listening="1", TrajectoriesPrecision="0.1", ExportVelocities="true")
        collBack.addObject("Monitor", name=file3, indices="0", listening="1", showForces="1", ExportForces="true")

    SutureNeedle.ITSELF=name
    SutureNeedle.COLL=name.Surf.Torus2Point.getLinkPath()
    SutureNeedle.MO=name.InstrumentMechObject.getLinkPath()
    SutureNeedle.COLL_BACK_MO=name.collBack.Particle2.getLinkPath()
    SutureNeedle.POS=name.InstrumentMechObject.findData('position').value
    SutureNeedle.COLL_FRONT=name.collFront.SphereCollisionInstrument.getLinkPath()
    SutureNeedle.COLL_FRONT_TAG=name.collFront.SphereCollisionInstrument
    SutureNeedle.COLL_BACK=name.collBack.SphereCollisionInstrument2.getLinkPath()
    SutureNeedle.MO_TAG=name.InstrumentMechObject
    SutureNeedle.VIS=name.Visu.Visual


## This function defines a suture needle node with behavior/collision/visual models. It is mostly the same as SutureNeedle class............
# @param parentNode: parent node of the suture needle
# @param name: name of the behavior node
# @param scale3d: scale of the needle along all directions
# @param geomagic: if True, the needle is positioned on the Geomagic end effector
# @param position: position of the geomagic end effector
# @param external_rest_shape: rest shape of the geomagic end effector
# @param monitor: if True, saves position, velocity and force of the needle 
# @param file1: name of the file that saves positions
# @param file2: name of the file that saves velocities
# @param file3: name of the file that saves forces

def SutureNeedleLeft(parentNode=None, name=None, scale3d=[0.0, 0.0, 0.0], 
position="@GeomagicDevice.positionDevice", external_rest_shape='@../Omni/DOFs', # position and external_rest_shape are set by default for the single station case 
monitor=False, file1=None, file2=None, file3=None): # If plots are desired: save results in three different files
    rz=120
    # Taken from C:\sofa\src\examples\Components\collision\RuleBasedContactManager

    name=parentNode.addChild(name)
    name.addObject('EulerImplicitSolver',  rayleighStiffness="0.1", rayleighMass="0.1" )
    name.addObject('CGLinearSolver', iterations="25", tolerance="1e-5" ,threshold="1e-5")
    name.addObject('MechanicalObject',  name='InstrumentMechObject', template='Rigid3d', position=position, scale3d="2", rotation="0 0 10" ) #, src="@instrumentMeshLoader")
    name.addObject('RestShapeSpringsForceField', name="InstrumentRestShape", stiffness='100', angularStiffness='100', external_rest_shape=external_rest_shape, points='0', external_points='0') 
    name.addObject('LCPForceFeedback', name="LCPFFNeedle",  forceCoef="0.002", activate="true")# Decide forceCoef value better
    name.addObject('UniformMass' , totalMass="3")
    name.addObject('UncoupledConstraintCorrection')

    Visu=name.addChild('Visu')
    Visu.addObject('MeshObjLoader' ,name="meshLoader_3", filename="mesh/Suture_needle.obj", scale="2.0", handleSeams="1" )
    Visu.addObject('OglModel', name="Visual", src='@meshLoader_3', rx="-10", ry="160", rz=rz,  dz="0", dx="0", dy="0",  color="0 0.5 0.796", scale=1, isEnabled=0)
    Visu.addObject('RigidMapping' ,input="@..", output="@Visual")
    
    Surf=name.addChild('Surf')
    Surf.addObject('MeshObjLoader' ,filename="mesh/Suture_needle.obj" ,name="loader" )
    Surf.addObject('MeshTopology' ,src="@loader")
    Surf.addObject('MechanicalObject' ,src="@loader", scale="2.0", rx="-10", ry="160", rz=rz,  dz="0", dx="0", dy="0") #rz=180
    #Surf.addObject('TriangleCollisionModel', name="Torus2Triangle") # DO NOT UNCOMMENT
    #Surf.addObject('LineCollisionModel', name="Torus2Line" ) # DO NOT UNCOMMENT
    Surf.addObject('PointCollisionModel' ,name="Torus2Point")
    Surf.addObject('RigidMapping')

    collFront = name.addChild('collFront') #"-4.2 0.02 -0.25" for scale5
    collFront.addObject('MechanicalObject', template="Vec3d", name="Particle", position="-2.9 0.02 -0.25", rx="-10", ry="160", rz=rz,  dz="0", dx="0", dy="0")
    collFront.addObject('SphereCollisionModel', radius="0.2", name="SphereCollisionInstrument", contactStiffness="2", tags="CarvingTool")
    collFront.addObject('RigidMapping', name="MM->CM mapping",  input="@../InstrumentMechObject",  output="@Particle")

    collBack = name.addChild('collBack') #"0 0.007 -0.25" for scale5
    collBack.addObject('MechanicalObject', template="Vec3d", name="Particle2", position="0 0.007 -0.25", rx="-10", ry="160", rz=rz,  dz="0", dx="0", dy="0")
    collBack.addObject('SphereCollisionModel', radius="0.2", name="SphereCollisionInstrument2", contactStiffness="2")
    collBack.addObject('RigidMapping', name="MM->CM mapping",  input="@../InstrumentMechObject",  output="@Particle2")
    
    if monitor==True:
        collBack.addObject("Monitor", name=file1, indices="0", listening="1", TrajectoriesPrecision="0.1", ExportPositions="true")
        collBack.addObject("Monitor", name=file2, indices="0", listening="1", TrajectoriesPrecision="0.1", ExportVelocities="true")
        collBack.addObject("Monitor", name=file3, indices="0", listening="1", showForces="1", ExportForces="true")

    SutureNeedleLeft.ITSELF=name
    SutureNeedleLeft.COLL=name.Surf.Torus2Point.getLinkPath()
    SutureNeedleLeft.MO=name.InstrumentMechObject.getLinkPath()
    SutureNeedleLeft.COLL_BACK_MO=name.collBack.Particle2.getLinkPath()
    SutureNeedleLeft.POS=name.InstrumentMechObject.findData('position').value
    SutureNeedleLeft.COLL_FRONT=name.collFront.SphereCollisionInstrument.getLinkPath()
    SutureNeedleLeft.COLL_FRONT_TAG=name.collFront.SphereCollisionInstrument
    SutureNeedleLeft.COLL_BACK=name.collBack.SphereCollisionInstrument2.getLinkPath()
    SutureNeedleLeft.MO_TAG=name.InstrumentMechObject
    SutureNeedleLeft.VIS=name.Visu.Visual


## This function defines a straight needle node with behavior/collision/visual models. 
# @param parentNode: parent node of the suture needle
# @param name: name of the behavior node
# @param scale3d: scale of the needle along all directions
# @param geomagic: if True, the needle is positioned on the Geomagic end effector
# @param position: position of the geomagic end effector
# @param monitor: if True, saves position, velocity and force of the needle 
# @param file1: name of the file that saves positions
# @param file2: name of the file that saves velocities
# @param file3: name of the file that saves forces

def StraightNeedle(parentNode=None, name=None, scale3d=[0.1, 0.4, 0.4], color=[0.0, 0.0, 0.0],
position="@GeomagicDevice.positionDevice", external_rest_shape='@../Omni/DOFs', # position and external_rest_shape are set by default for the single station case 
monitor=False, file1=None, file2=None, file3=None): 

    name=parentNode.addChild(name)
    name.addObject('EulerImplicitSolver',  rayleighStiffness="0.1", rayleighMass="0.1" )
    name.addObject('CGLinearSolver', iterations="25", tolerance="1e-5" ,threshold="1e-5")
    name.addObject('MechanicalObject',  name='InstrumentMechObject', template='Rigid3d', position=position, scale3d=scale3d) #, src="@instrumentMeshLoader")
    name.addObject('RestShapeSpringsForceField', name="InstrumentRestShape", stiffness='1000', angularStiffness='1000', external_rest_shape=external_rest_shape, points='0', external_points='0') 
    name.addObject('LCPForceFeedback', name="LCPFFNeedle", forceCoef="0.02", activate="true")# Decide forceCoef value better
    name.addObject('UniformMass' , totalMass="3")
    name.addObject('UncoupledConstraintCorrection')

    Visu=name.addChild('Visu')
    Visu.addObject('MeshObjLoader' ,name="meshLoader_3", filename="C:\sofa\src\Chiara\mesh\straight_needle.obj", scale3d=scale3d, handleSeams="1" , translation=[0, 0, 10] , rotation=[0, 90, 0])
    Visu.addObject('OglModel',name="Visual", src='@meshLoader_3',  color="0 0.5 0.796", translation=[0,0,-11])#, rotation=[90, 0, 0])#, dz=3)
    Visu.addObject('RigidMapping' ,input="@..", output="@Visual")
    
    Surf=name.addChild('Surf')
    Surf.addObject('MeshObjLoader' ,filename="C:\sofa\src\Chiara\mesh\straight_needle.obj" ,scale3d=scale3d, name="loader", translation=[0, 0, 10] , rotation=[0, 90, 0])
    Surf.addObject('MeshTopology' ,src="@loader")
    Surf.addObject('MechanicalObject' ,src="@loader", translation=[0,0,-11])#, rotation=[90, 0, 0])
    #Surf.addObject('TriangleCollisionModel', name="Torus2Triangle") # DO NOT UNCOMMENT
    #Surf.addObject('LineCollisionModel', name="Torus2Line" ) # DO NOT UNCOMMENT
    Surf.addObject('PointCollisionModel' ,name="Torus2Point")
    Surf.addObject('RigidMapping')
    
    if monitor==True:
        Surf.addObject("Monitor", name=file1, indices="0", listening="1", TrajectoriesPrecision="0.1", showTrajectories="1", ExportPositions="true" ,sizeFactor="2")
        Surf.addObject("Monitor", name=file2, indices="0", listening="1", TrajectoriesPrecision="0.1",  ExportVelocities="true")
        Surf.addObject("Monitor", name=file3, indices="0", listening="1", TrajectoriesPrecision="0.1", ExportForces="true")
        #StraightNeedle.Monitor=name.Surf.RingsTask_pos


    StraightNeedle.ITSELF=name
    StraightNeedle.COLL=name.Surf.Torus2Point.getLinkPath()
    StraightNeedle.MO=name.InstrumentMechObject.getLinkPath()
    StraightNeedle.POS=name.InstrumentMechObject.findData('position').value
    StraightNeedle.MO_TAG=name.InstrumentMechObject


## This function defines a straight needle node with behavior/collision/visual models. It is mostly the same as SutureNeedle class............
# @param parentNode: parent node of the suture needle
# @param name: name of the behavior node
# @param scale3d: scale of the needle along all directions
# @param geomagic: if True, the needle is positioned on the Geomagic end effector
# @param position: position of the geomagic end effector
# @param monitor: if True, saves position, velocity and force of the needle 
# @param file1: name of the file that saves positions
# @param file2: name of the file that saves velocities
# @param file3: name of the file that saves forces

def StraightNeedleLeft(parentNode=None, name=None, scale3d=[0.1, 0.4, 0.4], color=[0.0, 0.0, 0.0],
position="@GeomagicDevice.positionDevice", external_rest_shape='@../Omni/DOFs', # position and external_rest_shape are set by default for the single station case 
monitor=False, file1=None, file2=None, file3=None): 

    name=parentNode.addChild(name)
    name.addObject('EulerImplicitSolver',  rayleighStiffness="0.1", rayleighMass="0.1" )
    name.addObject('CGLinearSolver', iterations="25", tolerance="1e-5" ,threshold="1e-5")
    name.addObject('MechanicalObject',  name='InstrumentMechObject', template='Rigid3d', position=position, scale3d=scale3d) #, src="@instrumentMeshLoader")
    name.addObject('RestShapeSpringsForceField', name="InstrumentRestShape", stiffness='1000', angularStiffness='1000', external_rest_shape=external_rest_shape, points='0', external_points='0') 
    name.addObject('LCPForceFeedback', name="LCPFFNeedle", forceCoef="0.02", activate="true")# Decide forceCoef value better
    name.addObject('UniformMass' , totalMass="3")
    name.addObject('UncoupledConstraintCorrection')

    Visu=name.addChild('Visu')
    Visu.addObject('MeshObjLoader' ,name="meshLoader_3", filename="C:\sofa\src\Chiara\mesh\straight_needle.obj", scale3d=scale3d, handleSeams="1" , translation=[0, 0, 10] , rotation=[0, 90, 0])
    Visu.addObject('OglModel',name="Visual", src='@meshLoader_3',  color="0 0.5 0.796", translation=[0,0,-11], isEnabled=0)#, rotation=[90, 0, 0])#, dz=3)
    Visu.addObject('RigidMapping' ,input="@..", output="@Visual")
    
    Surf=name.addChild('Surf')
    Surf.addObject('MeshObjLoader' ,filename="C:\sofa\src\Chiara\mesh\straight_needle.obj" ,scale3d=scale3d, name="loader", translation=[0, 0, 10] , rotation=[0, 90, 0])
    Surf.addObject('MeshTopology' ,src="@loader")
    Surf.addObject('MechanicalObject' ,src="@loader", translation=[0,0,-11])#, rotation=[90, 0, 0])
    #Surf.addObject('TriangleCollisionModel', name="Torus2Triangle") # DO NOT UNCOMMENT
    #Surf.addObject('LineCollisionModel', name="Torus2Line" ) # DO NOT UNCOMMENT
    Surf.addObject('PointCollisionModel' ,name="Torus2Point")
    Surf.addObject('RigidMapping')
    
    if monitor==True:
        Surf.addObject("Monitor", name=file1, indices="0", listening="1", TrajectoriesPrecision="0.1", showTrajectories="1", ExportPositions="true", 	sizeFactor="2")
        Surf.addObject("Monitor", name=file2, indices="0", listening="1", TrajectoriesPrecision="0.1",  ExportVelocities="true")
        Surf.addObject("Monitor", name=file3, indices="0", listening="1", TrajectoriesPrecision="0.1", ExportForces="true")
        StraightNeedle.Monitor=name.Surf.RingsTask_pos


    StraightNeedle.ITSELF=name
    StraightNeedle.COLL=name.Surf.Torus2Point.getLinkPath()
    StraightNeedle.MO=name.InstrumentMechObject.getLinkPath()
    StraightNeedle.POS=name.InstrumentMechObject.findData('position').value
    StraightNeedle.MO_TAG=name.InstrumentMechObject

