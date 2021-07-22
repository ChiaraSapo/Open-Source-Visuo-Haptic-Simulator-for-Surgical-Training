# Data

scale3d_skin="0.25 0.65 0.1"
scale3d_needle="5 5 5"
scale3d_thread="0.5 0.5 0.5"

pointPosition_onNeedle="-6.98 0.02 0.05" #N: 5,5,5

GeomagicPosition="0 20 15"
skinVolume_fileName="mesh\skin_volume_403020_05" #03 troppo lento
needleVolume_fileName="mesh\suture_needle.obj"
threadVolume_fileName="mesh\threadCh2"

# Data
skin_youngModulus=1500#300
thread_youngModulus=2000
skin_poissonRatio=0.49
thread_poissonRatio=0.8

# Training sphere
def sphere(parentNode=None, name=None, translation=[0.0, 0.0, 0.0], scale3d=[0.0, 0.0, 0.0], color=[0.0, 0.0, 0.0], M=None):

    name=parentNode.addChild(name)
    name.addObject('MeshObjLoader', name='sphere', filename="C:\sofa\src\Chiara\mesh\sphere.obj") 
    name.addObject('OglModel', name='sphereVis', src='@sphere', scale3d="0.8 0.8 0.8", translation=translation, color=color)
    if M=="M1":
        sphere.M1=name.sphereVis
    if M=="M2":
        sphere.M2=name.sphereVis
    if M=="M3":
        sphere.M3=name.sphereVis
    if M=="M4":
        sphere.M4=name.sphereVis


def ring(parentNode=None, name=None, x=0, y=0, z=0, scale3d=[0.0, 0.0, 0.0],  M=None): 
    # Taken from C:\sofa\src\examples\Components\collision\RuleBasedContactManager

    name=parentNode.addChild(name)
    name.addObject('EulerImplicitSolver',  rayleighStiffness="0.1", rayleighMass="0.1" )
    name.addObject('CGLinearSolver', iterations="25", tolerance="1e-5" ,threshold="1e-5")
    name.addObject('MechanicalObject', template="Rigid3d", scale="1.0" ,dx=x, dy=y, dz=z)
    name.addObject('UniformMass' ,filename="BehaviorModels/torus.rigid")
    name.addObject('UncoupledConstraintCorrection')
    name.addObject('BoxROI', name='boxROI', box=[x-1,y-1,z-3,x+1,y+1,z], drawBoxes='true', computeTriangles='true')
    name.addObject('RestShapeSpringsForceField', name='rest', points='@boxROI.indices', stiffness='1e12', angularStiffness='1e12')
    Visu=name.addChild('Visu')
    Visu.addObject('MeshObjLoader' ,name="meshLoader_3", filename="mesh/torus.obj", scale="1.0", handleSeams="1" )
    Visu.addObject('OglModel' ,name="VisualOGL" ,src="@meshLoader_3",material="Default Diffuse 1 0 0.5 0 1 Ambient 1 0 0.1 0 1 Specular 0 0 0.5 0 1 Emissive 0 0 0.5 0 1 Shininess 0 45")
    Visu.addObject('RigidMapping' ,input="@..", output="@VisualOGL")
    Surf=name.addChild('Surf')
    Surf.addObject('MeshObjLoader' ,filename="mesh/torus_for_collision.obj" ,name="loader" )
    Surf.addObject('MeshTopology' ,src="@loader")
    Surf.addObject('MechanicalObject' ,src="@loader", scale="1.0")
    Surf.addObject('TriangleCollisionModel', name="Torus2Triangle" ,group="2")
    Surf.addObject('LineCollisionModel', name="Torus2Line" ,group="2")
    Surf.addObject('PointCollisionModel' ,name="Torus2Point" ,group="2")
    Surf.addObject('RigidMapping')
    if M=="M1":
        ring.C1=name.Surf.Torus2Triangle.getLinkPath()
        ring.V1=name.Visu.VisualOGL
        ring.itself1=name
    if M=="M2":
        ring.C2=name.Surf.Torus2Triangle.getLinkPath()
        ring.V2=name.Visu.VisualOGL
    if M=="M3":
        ring.C3=name.Surf.Torus2Triangle.getLinkPath()
        ring.V3=name.Visu.VisualOGL
    if M=="M4":
        ring.C4=name.Surf.Torus2Triangle.getLinkPath()
        ring.V4=name.Visu.VisualOGL
    


def Skin(parentNode=None, name=None, rotation=[0.0, 0.0, 0.0], translation=[0.0, 0.0, 0.0], 
scale3d=[0.0, 0.0, 0.0],  fixingBox=[0.0, 0.0, 0.0], indicesBox=[0.0, 0.0, 0.0], borderBox=[0.0, 0.0, 0.0], importFile=None, 
side=0, task=None, borderBox1=[0.0, 0.0, 0.0],borderBox2=[0.0, 0.0, 0.0],borderBox3=[0.0, 0.0, 0.0],borderBox4=[0.0, 0.0, 0.0]):

    name=parentNode.addChild(name)
    
    #################### BEHAVIOUR ##########################
    # Solvers
    name.addObject('EulerImplicitSolver', name="odesolver", rayleighStiffness="0.01", rayleighMass="0.01") #added the 2 params
    name.addObject('CGLinearSolver', iterations="25", name="EpiLinearsolver", tolerance="1.0e-9", threshold="1.0e-9")
    #name.addObject('SparseLDLSolver')

    # Volumetric mesh loader
    name.addObject('MeshGmshLoader', name='volumeLoader', filename=importFile, scale3d=scale3d)

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

    # Border box
    name.addObject('BoxROI', name='borderBox', box=borderBox, drawBoxes='true')
    
    name.addObject('BoxROI', name='sphere1Box', box=[8-2, 3-2, -0.1, 8+2, 3+2, 3], drawBoxes='true', computeTriangles='true')
    name.addObject('BoxROI', name='sphere2Box', box=[8-2, 13-2, -0.1, 8+2, 13+2, 3], drawBoxes='true', computeTriangles='true')
    name.addObject('BoxROI', name='sphere3Box', box=[12-2, 7-2, -0.1, 12+2, 7+2, 3], drawBoxes='true', computeTriangles='true')
    name.addObject('BoxROI', name='sphere4Box', box=[12-2, 17-2, -0.1, 12+2, 17+2, 3], drawBoxes='true', computeTriangles='true')  

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

    #SkinColl.addObject('LineCollisionModel', name="LineCollisionSkin")
    #SkinColl.addObject('PointCollisionModel', name="PointCollisionSkin") 
    #SkinColl.addObject('IdentityMapping')

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
        Skin.COLL_TAG=name.SkinColl.TriangleCollisionSkin
        Skin.borderBox= name.borderBox
        Skin.sphere1Box=name.sphere1Box
        Skin.sphere2Box=name.sphere2Box

    if side==1: # right
        Skin.itself_right=name.getLinkPath()
        Skin.MO_right=name.SkinMechObj.getLinkPath()
        Skin.COLL_right=name.SkinColl.TriangleCollisionSkin.getLinkPath()
        Skin.COLL_TAG_right=name.SkinColl.TriangleCollisionSkin
        Skin.borderBox_right = name.borderBox
        Skin.sphere3Box=name.sphere3Box
        Skin.sphere4Box=name.sphere4Box

    Skin.CONTAINER=name.TetraContainer.getLinkPath()

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
    
    #name.addObject('UniformMass', name="threadMass", template="Vec3d,double", totalMass="1.0")
    name.addObject('DiagonalMass', name="threadMass", massDensity="2.0")

    name.addObject('TetrahedronFEMForceField', template='Vec3d', name='FEM', method='large', youngModulus=thread_youngModulus, poissonRatio=thread_poissonRatio)
    #name.addObject('MeshSpringForceField', name="FEM-Bend", template="Vec3d", stiffness="1000", damping="0.1")
    name.addObject('UncoupledConstraintCorrection')
    #name.addObject('BoxROI', name='boxROI', box=[-1, -1, -1, 1, 1, 1], drawBoxes='true')
    #name.addObject('RestShapeSpringsForceField', name='rest', points='@boxROI.indices', stiffness='1e12', angularStiffness='1e12')


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


def SutureNeedleOld(parentNode=None, name=None, rotation=[0.0, 0.0, 0.0], translation=[0.0, 0.0, 0.0],
scale3d=[0.0, 0.0, 0.0],  fixingBox=[0.0, 0.0, 0.0], importFile=None,  carving=False, geomagic=False):

    #################### BEHAVIOUR ##########################
    name=parentNode.addChild(name)
    name.addObject('EulerImplicitSolver', name='ODE solver', rayleighMass="1.0", rayleighStiffness="0.01")
    name.addObject('CGLinearSolver', name='linear solver', iterations="25", tolerance="1e-7", threshold="1e-7") #SparseLDLSolver
    name.addObject('CGLinearSolver', name='linear solver', iterations="25", tolerance="1e-7", threshold="1e-7")
    name.addObject('MeshObjLoader', name='instrumentMeshLoader', filename=importFile)

    if geomagic==True:
        name.addObject('MechanicalObject',  name='InstrumentMechObject', template='Rigid3d', position="@GeomagicDevice.positionDevice", scale3d=scale3d, rotation="0 0 10" ) #, src="@instrumentMeshLoader")
        name.addObject('RestShapeSpringsForceField', stiffness='1000', angularStiffness='1000', external_rest_shape='@../Omni/DOFs', points='0', external_points='0') 
        name.addObject('LCPForceFeedback', name="LCPFFNeedle",  forceCoef="0.1", activate="true")# Decide forceCoef value better
    else: 
        name.addObject('MechanicalObject',  name='InstrumentMechObject', template='Rigid3d', translation=translation, scale3d=scale3d) 
        #src="@instrumentMeshLoader": removing this you also remove that horrible effect you had, you're covering the secret........

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
    InstrumentColl_Back.addObject("Monitor", name="SutureNeedle_pos", indices="0", listening="1", TrajectoriesPrecision="0.1", ExportPositions="true")
    InstrumentColl_Back.addObject("Monitor", name="SutureNeedle_vel", indices="0", listening="1", TrajectoriesPrecision="0.1", ExportVelocities="true")
    InstrumentColl_Back.addObject("Monitor", name="SutureNeedle_force", indices="0", listening="1", TrajectoriesPrecision="0.1", ExportForces="true")

    if geomagic==True:
        InstrumentColl_Back.addObject('MechanicalObject', template="Vec3d", name="Particle2", position="0 0.007 0.05", rx="-10", ry="160", rz="180",  dz="-4", dx="0", dy="0")
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
    #InstrumentVisu.addObject('IdentityMapping',  input='@../InstrumentMechObject', output='@InstrumentVisualModel')

    # Data
    SutureNeedle.MO=name.InstrumentMechObject.getLinkPath()
    SutureNeedle.COLL_BACK_MO=name.InstrumentColl_Back.Particle2.getLinkPath()
    SutureNeedle.POS=name.InstrumentMechObject.findData('position').value
    SutureNeedle.COLL_FRONT=name.InstrumentColl_Front.SphereCollisionInstrument.getLinkPath()
    SutureNeedle.COLL_BACK=name.InstrumentColl_Back.SphereCollisionInstrument2.getLinkPath()


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
    
    if monitor==True:
        collBack.addObject("Monitor", name="SutureNeedle_pos", indices="0", listening="1", TrajectoriesPrecision="0.1", showPositions="1", ExportPositions="true")
        collBack.addObject("Monitor", name="SutureNeedle_vel", indices="0", listening="1", TrajectoriesPrecision="0.1", showVelocities="1", ExportVelocities="true")
        collBack.addObject("Monitor", name="SutureNeedle_force", indices="0", listening="1", TrajectoriesPrecision="0.1", showForces="1", ExportForces="true")

    SutureNeedle.ITSELF=name
    SutureNeedle.COLL=name.Surf.Torus2Point.getLinkPath()
    SutureNeedle.MO=name.InstrumentMechObject.getLinkPath()
    SutureNeedle.COLL_BACK_MO=name.collBack.Particle2.getLinkPath()
    SutureNeedle.POS=name.InstrumentMechObject.findData('position').value
    SutureNeedle.COLL_FRONT=name.collFront.SphereCollisionInstrument.getLinkPath()
    SutureNeedle.COLL_FRONT_TAG=name.collFront.SphereCollisionInstrument
    SutureNeedle.COLL_BACK=name.collBack.SphereCollisionInstrument2.getLinkPath()
    SutureNeedle.MO_TAG=name.InstrumentMechObject

        





def ThreadNEW(parentNode=None, name=None, translation=[0.0, 0.0, 0.0], scale3d=[0.0, 0.0, 0.0], color=[0.0, 0.0, 0.0],
carving=False, geomagic=False): 
    # Taken from C:\sofa\src\examples\Components\collision\RuleBasedContactManager

    name=parentNode.addChild(name)
    name.addObject('EulerImplicitSolver',  rayleighStiffness="0.1", rayleighMass="0.1" )
    name.addObject('CGLinearSolver', iterations="25", tolerance="1e-5" ,threshold="1e-5")
    name.addObject('MeshGmshLoader', name='name_volumeLoader', filename="mesh/threadCh2")
    name.addObject('TetrahedronSetTopologyContainer', src="@name_volumeLoader")
    name.addObject('TetrahedronSetGeometryAlgorithms', template='Vec3d')
    name.addObject('TetrahedronSetTopologyModifier')
    name.addObject('MechanicalObject', src="@name_volumeLoader", name="InstrumentMechObject", template="Vec3d", scale="1.0" ,dx="8", dy="3", dz="6")
    name.addObject('DiagonalMass', name="threadMass", massDensity="2.0")
    name.addObject('TetrahedronFEMForceField', template='Vec3d', name='FEM', method='large', youngModulus=2000, poissonRatio=0.8)
    name.addObject('UncoupledConstraintCorrection')

    Visu=name.addChild('Visu')
    Visu.addObject('MeshGmshLoader' ,name="meshLoader_3", filename="mesh/threadCh2", scale="1.0")
    Visu.addObject('OglModel' ,name="Visual" ,src="@meshLoader_3",  color="0 0.5 0.796")
    Visu.addObject('IdentityMapping' ,input="@..", output="@Visual")
    
    Surf=name.addChild('Surf')
    Surf.addObject('MeshGmshLoader' ,filename="mesh/threadCh2" ,name="loader" )
    Surf.addObject('MeshTopology' ,src="@loader")
    Surf.addObject('MechanicalObject' ,src="@loader", scale="1.0")
    Surf.addObject('TriangleCollisionModel', name="Torus2Triangle" ,group="2")
    Surf.addObject('LineCollisionModel', name="Torus2Line" ,group="2")
    Surf.addObject('PointCollisionModel' ,name="Torus2Point" ,group="2")
    Surf.addObject('IdentityMapping')

