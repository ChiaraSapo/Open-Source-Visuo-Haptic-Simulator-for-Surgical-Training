import Sofa
import numpy as np

# Data
skin_youngModulus=4000
thread_youngModulus=3000
skin_poissonRatio=0.1
thread_poissonRatio=0.8



def SkinHexa(parentNode=None, name=None, rotation=[0.0, 0.0, 0.0], translation=[0.0, 0.0, 0.0], 
scale3d=[0.0, 0.0, 0.0],  fixingBox=[0.0, 0.0, 0.0],
side=0,  borderBox1=[0.0, 0.0, 0.0],borderBox2=[0.0, 0.0, 0.0],borderBox3=[0.0, 0.0, 0.0],borderBox4=[0.0, 0.0, 0.0],
borderBox5=[0.0, 0.0, 0.0],borderBox6=[0.0, 0.0, 0.0],borderBox7=[0.0, 0.0, 0.0],borderBox8=[0.0, 0.0, 0.0]):

    name=parentNode.addChild(name)
    name.addObject('EulerImplicitSolver', name="ODE solver", rayleighStiffness="0.01", rayleighMass="0.01")
    name.addObject('CGLinearSolver', iterations="25", name="EpiLinearsolver", tolerance="1.0e-9", threshold="1.0e-9")
    #epi.addObject('SparseLDLSolver')

    name.addObject('MechanicalObject', template="Vec3d", name="EpiMechObj", scale3d="2 1 0.2", position="0 0 -8", showVectors="true", drawMode="2")
    #epi.addObject('MechanicalObject', template="Vec3d", name="EpiMechObj", scale3d="1 1 1", position="0 0 -2", showVectors="true", drawMode="2")
    if side==1:
        name.addObject('RegularGridTopology', name="grid",nx=7, ny=12, nz=3, xmin=3.6, xmax=7, ymin=10, ymax=22, zmin=0, zmax=4)
    else:
        name.addObject('RegularGridTopology', name="grid", nx=7, ny=12, nz=3, xmin=0, xmax=3.5, ymin=10, ymax=22, zmin=0, zmax=4)
    name.addObject('HexahedronSetGeometryAlgorithms')
    
    #epi.addObject('DiagonalMass', template="Vec3d,double", name="Mass", massDensity="1.0")
    name.addObject('UniformMass', template="Vec3d,double", name="EpiMass", totalMass="10")
    name.addObject('HexahedronFEMForceField', template="Vec3d", name="FEM", poissonRatio=skin_poissonRatio, youngModulus=skin_youngModulus )
    #epi.addObject('GenericConstraintCorrection')
    #epi.addObject('LinearSolverConstraintCorrection')
    name.addObject('UncoupledConstraintCorrection')

    name.addObject('BoxROI', name='borderBox1', box=borderBox1, drawBoxes='true', computeTriangles='true')
    name.addObject('BoxROI', name='borderBox2', box=borderBox2, drawBoxes='true', computeTriangles='true')
    name.addObject('BoxROI', name='borderBox3', box=borderBox3, drawBoxes='true', computeTriangles='true')
    name.addObject('BoxROI', name='borderBox4', box=borderBox4, drawBoxes='true', computeTriangles='true')
    name.addObject('BoxROI', name='borderBox5', box=borderBox5, drawBoxes='true', computeTriangles='true')
    name.addObject('BoxROI', name='borderBox6', box=borderBox6, drawBoxes='true', computeTriangles='true')
    name.addObject('BoxROI', name='borderBox7', box=borderBox7, drawBoxes='true', computeTriangles='true')
    name.addObject('BoxROI', name='borderBox8', box=borderBox8, drawBoxes='true', computeTriangles='true')


    posy=10
    if side==1:
        boxROI=name.addObject('BoxROI', name='boxROI', box=[7, 10, -2, 14, 22, 0.1], drawBoxes='true', computeTriangles='true')
    else:
        boxROI=name.addObject('BoxROI', name='boxROI', box=[-0.1, posy, -2, 7, posy+12, 0.1], drawBoxes='true', computeTriangles='true')
    name.addObject('RestShapeSpringsForceField', name='rest', points='@boxROI.indices', stiffness='1e12', angularStiffness='1e12')

    # Hexa -> Quad
    quad=name.addChild('quad')
    quad.addObject('QuadSetTopologyContainer', name="Q_Container")
    quad.addObject('QuadSetTopologyModifier', name="Q_Modifier")
    quad.addObject('QuadSetGeometryAlgorithms', template="Vec3d", name="Q_GeomAlgo")
    quad.addObject('Hexa2QuadTopologicalMapping', name="default6", input="@../grid", output="@Q_Container")

    # Quad -> Tri
    tri=quad.addChild('tri')
    tri.addObject('TriangleSetTopologyContainer', name="T_Container")
    tri.addObject('TriangleSetTopologyModifier', name="T_Modifier")
    tri.addObject('TriangleSetGeometryAlgorithms', template="Vec3d", name="T_GeomAlgo")
    tri.addObject('Quad2TriangleTopologicalMapping', name="default8", input="@../Q_Container", output="@T_Container")
    
    # Triangle collision model
    tri.addObject('TriangleCollisionModel', name="TriangleCollisionSkin", contactStiffness="0.01")
    #tri.addObject('TriangleCollisionModel', name="EpiCollision", contactStiffness="0.01", tags="CarvingSurface") #CARVING

    visu=tri.addChild('visu') 
    visu.addObject('OglModel', template="Vec3d", name="Visual", color="1 0.75 0.796", material="Default Diffuse 1 0 0 1 1 Ambient 1 0 0 0.2 1 Specular 0 0 0 1 1 Emissive 0 0 0 1 1 Shininess 0 45 ")
    visu.addObject('OglViewport', screenPosition="0 0", screenSize="250 250", cameraPosition="-0.285199 -15.2745 16.7859", cameraOrientation="0.394169 0.0120415 0.00490558 0.918946" )
    visu.addObject('IdentityMapping', template="Vec3d,Vec3d", name="default12", input="@..", output="@Visual" )

    if side==0: # left
        SkinHexa.itself=name.getLinkPath()
        SkinHexa.MO=name.EpiMechObj.getLinkPath()
        #Skin.borderBox= name.borderBox
        SkinHexa.COLL=name.quad.tri.TriangleCollisionSkin.getLinkPath()
        SkinHexa.borderBox1=name.borderBox1
        SkinHexa.borderBox2=name.borderBox2
        SkinHexa.borderBox3=name.borderBox3
        SkinHexa.borderBox4=name.borderBox4
        SkinHexa.borderBox5=name.borderBox5
        SkinHexa.borderBox6=name.borderBox6
        SkinHexa.borderBox7=name.borderBox7
        SkinHexa.borderBox8=name.borderBox8

    if side==1: # right
        SkinHexa.itself_right=name.getLinkPath()
        SkinHexa.MO_right=name.EpiMechObj.getLinkPath()
        #Skin.borderBox_right = name.borderBox
        SkinHexa.COLL_right=name.quad.tri.TriangleCollisionSkin.getLinkPath()
        SkinHexa.borderBox1_right=name.borderBox1
        SkinHexa.borderBox2_right=name.borderBox2
        SkinHexa.borderBox3_right=name.borderBox3
        SkinHexa.borderBox4_right=name.borderBox4
        SkinHexa.borderBox5_right=name.borderBox5
        SkinHexa.borderBox6_right=name.borderBox6
        SkinHexa.borderBox7_right=name.borderBox7
        SkinHexa.borderBox8_right=name.borderBox8
    return name





## This function defines a skin patch node with behavior/collision/visual models
# @param parentNode: parent node of the skin patch
# @param name: name of the behavior node
# @param rotation: rotation 
# @param translation: translation
# @param scale3d: scale of the skin along all directions
# @param fixingBox: vertices of the box that fixes the skin base
# @param side: Can be set to 0: left patch, 1: right patch. 
# @param borderBox1: vertices of box1 that computes indices along the border
# @param borderBox2: vertices of box2 that computes indices along the border
# @param borderBox3: vertices of box3 that computes indices along the border
# @param borderBox4: vertices of box4 that computes indices along the border
# @param borderBox5: vertices of box5 that computes indices along the border
# @param borderBox6: vertices of box6 that computes indices along the border
# @param borderBox7: vertices of box7 that computes indices along the border
# @param borderBox8: vertices of box8 that computes indices along the border

def Skin(parentNode=None, name=None, rotation=[0.0, 0.0, 0.0], translation=[0.0, 0.0, 0.0], 
scale3d=[0.0, 0.0, 0.0],  fixingBox=[0.0, 0.0, 0.0], importFile=None, 
side=0,  borderBox1=[0.0, 0.0, 0.0],borderBox2=[0.0, 0.0, 0.0],borderBox3=[0.0, 0.0, 0.0],borderBox4=[0.0, 0.0, 0.0],
borderBox5=[0.0, 0.0, 0.0],borderBox6=[0.0, 0.0, 0.0],borderBox7=[0.0, 0.0, 0.0],borderBox8=[0.0, 0.0, 0.0],
borderBox9=[0.0, 0.0, 0.0],borderBox10=[0.0, 0.0, 0.0], borderBox11=[0.0, 0.0, 0.0], borderBox12=[0.0, 0.0, 0.0]):

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
    #name.addObject('BoxROI', name='borderBox', box=borderBox, drawBoxes='true')

    name.addObject('BoxROI', name='borderBox1', box=borderBox1, drawBoxes='true', computeTriangles='true')
    name.addObject('BoxROI', name='borderBox2', box=borderBox2, drawBoxes='true', computeTriangles='true')
    name.addObject('BoxROI', name='borderBox3', box=borderBox3, drawBoxes='true', computeTriangles='true')
    name.addObject('BoxROI', name='borderBox4', box=borderBox4, drawBoxes='true', computeTriangles='true')
    name.addObject('BoxROI', name='borderBox5', box=borderBox5, drawBoxes='true', computeTriangles='true')
    name.addObject('BoxROI', name='borderBox6', box=borderBox6, drawBoxes='true', computeTriangles='true')
    name.addObject('BoxROI', name='borderBox7', box=borderBox7, drawBoxes='true', computeTriangles='true')
    name.addObject('BoxROI', name='borderBox8', box=borderBox8, drawBoxes='true', computeTriangles='true')


    #################### COLLISION ##########################

    SkinColl = name.addChild('SkinColl')

    # Mapped from the tetra of behaviour model
    SkinColl.addObject('TriangleSetTopologyContainer', name="T_Container")
    SkinColl.addObject('TriangleSetTopologyModifier', name="T_Modifier")
    SkinColl.addObject('TriangleSetGeometryAlgorithms', template="Vec3d", name="T_GeomAlgo")
    SkinColl.addObject('Tetra2TriangleTopologicalMapping', name="default8", input="@../TetraContainer", output="@T_Container")

    # Types of collision
    SkinColl.addObject('TriangleCollisionModel', name="TriangleCollisionSkin")

    #SkinColl.addObject('LineCollisionModel', name="LineCollisionSkin")
    #SkinColl.addObject('PointCollisionModel', name="PointCollisionSkin") 

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
        #Skin.borderBox= name.borderBox
        Skin.borderBox1=name.borderBox1
        Skin.borderBox2=name.borderBox2
        Skin.borderBox3=name.borderBox3
        Skin.borderBox4=name.borderBox4
        Skin.borderBox5=name.borderBox5
        Skin.borderBox6=name.borderBox6
        Skin.borderBox7=name.borderBox7
        Skin.borderBox8=name.borderBox8

    if side==1: # right
        Skin.itself_right=name.getLinkPath()
        Skin.MO_right=name.SkinMechObj.getLinkPath()
        Skin.COLL_right=name.SkinColl.TriangleCollisionSkin.getLinkPath()
        #Skin.borderBox_right = name.borderBox
        Skin.borderBox1_right=name.borderBox1
        Skin.borderBox2_right=name.borderBox2
        Skin.borderBox3_right=name.borderBox3
        Skin.borderBox4_right=name.borderBox4
        Skin.borderBox5_right=name.borderBox5
        Skin.borderBox6_right=name.borderBox6
        Skin.borderBox7_right=name.borderBox7
        Skin.borderBox8_right=name.borderBox8
    Skin.CONTAINER=name.TetraContainer.getLinkPath()

    return name





''' Does not cut...
def Scalpel2(parentNode=None, name=None, scale3d=[0.0, 0.0, 0.0], monitor=False, file1=None, file2=None, file3=None): 
    # Taken from C:\sofa\src\examples\Components\collision\RuleBasedContactManager

    name=parentNode.addChild(name)
    name.addObject('EulerImplicitSolver',  rayleighStiffness="0.1", rayleighMass="0.1" )
    name.addObject('CGLinearSolver', iterations="25", tolerance="1e-5" ,threshold="1e-5")

    name.addObject('MechanicalObject',  name='InstrumentMechObject', template='Rigid3d', position="@GeomagicDevice.positionDevice", scale="1.0", rotation="0 0 10",  dz="2", dx="-4", dy="-3",  rx="0", ry="0", rz="90") #, src="@instrumentMeshLoader")
    #name.addObject("Monitor", input="@InstrumentMechObject", name="ooooooooooooo", indices="0", listening="1", showForces="1", ExportForces="true")
    name.addObject('RestShapeSpringsForceField', stiffness='100', angularStiffness='100', external_rest_shape='@../Omni/DOFs', points='0', external_points='0') 
    name.addObject('LCPForceFeedback', name="LCPFFScalpel",  forceCoef="0.007", activate="true")# Decide forceCoef value better

    name.addObject('UniformMass' , totalMass="6")
    name.addObject('UncoupledConstraintCorrection')
    

    Visu=name.addChild('Visu')
    Visu.addObject('MeshObjLoader' ,name="meshLoader_3", filename="mesh/scalpel.obj", scale="1.0", handleSeams="1" )
    Visu.addObject('OglModel' ,name="Visual" ,src="@meshLoader_3",  color="0 0.5 0.796", dz="7", dx="-4", dy="-3",  rx="0", ry="0", rz="90")
    Visu.addObject('RigidMapping' ,input="@..", output="@Visual")
    
    Surf=name.addChild('Surf')
    Surf.addObject('MeshObjLoader' ,filename="mesh/scalpel.obj" ,name="loader" )
    Surf.addObject('MeshTopology' ,src="@loader")
    Surf.addObject('MechanicalObject' ,src="@loader", scale="1.0",  dz="2", dx="-4", dy="-3",  rx="0", ry="0", rz="90")
    Surf.addObject('TriangleCollisionModel', name="Torus2Triangle")# , contactStiffness="2")#, tags="CarvingTool")
    Surf.addObject('LineCollisionModel', name="Torus2Line" , contactStiffness="1000")#, tags="CarvingTool")
    Surf.addObject('PointCollisionModel' ,name="Torus2Point" , contactStiffness="1000")#, tags="CarvingTool")
    Surf.addObject('RigidMapping')
    

    collFront = name.addChild('collFront')
    collFront.addObject('MechanicalObject', template="Vec3d", name="Particle", position="4 -3.7 -8.5",  dz="2", dx="-4", dy="-3",  rx="0", ry="0", rz="90")
    #collFront.addObject('UniformMass', totalMass="0.01")
    collFront.addObject('SphereCollisionModel', radius="0.2", name="SphereCollisionInstrument", tags="CarvingTool")
    collFront.addObject('RigidMapping')#, template="Rigid3d,Vec3d", name="MM->CM mapping",  input="@../InstrumentMechObject",  output="@Particle")

    collFront2 = name.addChild('collFront2')
    collFront2.addObject('MechanicalObject', template="Vec3d", name="Particle", position="4 -3.7 -8.5",  dz="4", dx="-4", dy="-2.2",  rx="0", ry="0", rz="90")
    collFront2.addObject('SphereCollisionModel', radius="0.2", name="SphereCollisionInstrument2", contactStiffness="1", tags="CarvingTool")
    collFront2.addObject('RigidMapping')#, template="Rigid3d,Vec3d", name="MM->CM mapping",  input="@../InstrumentMechObject",  output="@Particle")

    Scalpel.MO=name.InstrumentMechObject
    # Scalpel.POS=name.InstrumentMechObject.findData('position').value
    #Scalpel.COLL_FRONT=name.Surf.Torus2Triangle.getLinkPath()
    Scalpel.COLL_FRONT=name.collFront.SphereCollisionInstrument.getLinkPath()
    Scalpel.COLL_FRONT2=name.collFront2.SphereCollisionInstrument2.getLinkPath()
'''

## This function defines a scalpel node with behavior/collision/visual models
# @param parentNode: parent node of the scalpel
# @param name: name of the behavior node
# @param scale3d: scale of the scalpel along all directions
# @param monitor: if True, saves position, velocity and force of the scalpel 
# @param file1: name of the file that saves positions
# @param file2: name of the file that saves velocities
# @param file3: name of the file that saves forces

def Scalpel(parentNode=None, name=None, scale3d=[0.0, 0.0, 0.0], monitor=False, file1=None, file2=None, file3=None, position="@GeomagicDevice.positionDevice", external_rest_shape='@../Omni/DOFs'): 

    name=parentNode.addChild(name)
    name.addObject('EulerImplicitSolver',  rayleighStiffness="0.1", rayleighMass="0.1" )
    name.addObject('CGLinearSolver', iterations="25", tolerance="1e-5" ,threshold="1e-5")
    #if geomagic==True:
    name.addObject('MechanicalObject',  name='InstrumentMechObject', template='Rigid3d', position=position, scale="1.0", rotation="0 0 10",  dz="2", dx="-4", dy="-3",  rx="0", ry="0", rz="90") #, src="@instrumentMeshLoader")
    name.addObject('RestShapeSpringsForceField', stiffness='1000', angularStiffness='1000', external_rest_shape=external_rest_shape, points='0', external_points='0') 
    name.addObject('LCPForceFeedback', name="LCPFFScalpel",  forceCoef="0.01", activate="true")# Decide forceCoef value better
    #else: 
    #    name.addObject('MechanicalObject', name="InstrumentMechObject", template="Rigid3d", scale="1.0" ,dx="8", dy="3", dz="25")
    name.addObject('UniformMass' , totalMass="5")
    name.addObject('UncoupledConstraintCorrection')

    #name.addObject("VectorSpringForceField",   object1="@Omni/ReferenceModel/instrumentRefState1", object2="@Scalpel/Surf/InstrumentMechObject", stiffness="50", viscosity="0" )


    Visu=name.addChild('Visu')
    Visu.addObject('MeshObjLoader' ,name="meshLoader_3", filename="mesh/scalpel.obj", scale="1.0", handleSeams="1" )
    Visu.addObject('OglModel' ,name="Visual" ,src="@meshLoader_3",  color="0 0.5 0.796", dz="2", dx="-4", dy="-3",  rx="0", ry="0", rz="90")
    Visu.addObject('RigidMapping' ,input="@..", output="@Visual")
    
    Surf=name.addChild('Surf')
    Surf.addObject('MeshObjLoader' ,filename="mesh/scalpel.obj" ,name="loader" )
    Surf.addObject('MeshTopology' ,src="@loader")
    Surf.addObject('MechanicalObject' ,src="@loader", name="InstrumentMechObject", scale="1.0",  dz="2", dx="-4", dy="-3",  rx="0", ry="0", rz="90")
    Surf.addObject('TriangleCollisionModel', name="Torus2Triangle" )#??????', contactStiffness="1000")#, tags="CarvingTool")
    Surf.addObject('LineCollisionModel', name="Torus2Line" , contactStiffness="1000")#, tags="CarvingTool")
    Surf.addObject('PointCollisionModel' ,name="Torus2Point" , contactStiffness="10000")#, tags="CarvingTool")
    #Surf.addObject("Monitor", name=file3, indices="0", listening="1", TrajectoriesPrecision="0.1", ExportForces="true")
    Surf.addObject('RigidMapping')

    collFront = name.addChild('collFront')
    collFront.addObject('MechanicalObject', template="Vec3d", name="Particle", position="4 -3.7 -8.5",  dz="2", dx="-4", dy="-3",  rx="0", ry="0", rz="90")
    collFront.addObject('SphereCollisionModel', radius="0.1", name="SphereCollisionInstrument", contactStiffness="1", tags="CarvingTool")
    collFront.addObject('RigidMapping')#, template="Rigid3d,Vec3d", name="MM->CM mapping",  input="@../InstrumentMechObject",  output="@Particle")

    if monitor==True:
        collFront.addObject("Monitor", name=file1, indices="0", listening="1", TrajectoriesPrecision="0.1", ExportPositions="true")
        collFront.addObject("Monitor", name=file2, indices="0", listening="1", TrajectoriesPrecision="0.1", ExportVelocities="true")

    collFront2 = name.addChild('collFront2')
    collFront2.addObject('MechanicalObject', template="Vec3d", name="Particle", position="4 -3.7 -8.5",  dz="4.5", dx="-4", dy="-4.3",  rx="0", ry="0", rz="90")
    collFront2.addObject('SphereCollisionModel', radius="0.1", name="SphereCollisionInstrument2", contactStiffness="1", tags="CarvingTool")
    collFront2.addObject('RigidMapping')#, template="Rigid3d,Vec3d", name="MM->CM mapping",  input="@../InstrumentMechObject",  output="@Particle")

    collFront3 = name.addChild('collFront3')
    collFront3.addObject('MechanicalObject', template="Vec3d", name="Particle", position="4 -3.7 -8.5",  dz="3", dx="-4", dy="-3.9",  rx="0", ry="0", rz="90")
    collFront3.addObject('SphereCollisionModel', radius="0.1", name="SphereCollisionInstrument3", contactStiffness="1", tags="CarvingTool")
    collFront3.addObject('RigidMapping')#, template="Rigid3d,Vec3d", name="MM->CM mapping",  input="@../InstrumentMechObject",  output="@Particle")

    Scalpel.MO=name.InstrumentMechObject.getLinkPath()
    Scalpel.POS=name.InstrumentMechObject.findData('position').value
    #Scalpel.COLL_FRONT=name.Surf.Torus2Triangle.getLinkPath()
    Scalpel.COLL_FRONT=name.collFront.SphereCollisionInstrument.getLinkPath()
    Scalpel.COLL_FRONT2=name.collFront2.SphereCollisionInstrument2.getLinkPath()
    Scalpel.COLL_FRONT3=name.collFront3.SphereCollisionInstrument3.getLinkPath()



def ScalpelHexa(parentNode=None, name=None, scale3d=[0.0, 0.0, 0.0], monitor=False, file1=None, file2=None, file3=None): 
    name=parentNode.addChild(name)
    name.addObject('EulerImplicitSolver',  rayleighStiffness="0.1", rayleighMass="0.1" )
    name.addObject('CGLinearSolver', iterations="25", tolerance="1e-5" ,threshold="1e-5")

    name.addObject('MechanicalObject',  name='InstrumentMechObject', template='Rigid3d', position="@GeomagicDevice.positionDevice", scale="1.0", rotation="0 0 10",  dz="2", dx="-4", dy="-3",  rx="0", ry="0", rz="90") #, src="@instrumentMeshLoader")
    #name.addObject("Monitor", input="@InstrumentMechObject", name="ooooooooooooo", indices="0", listening="1", showForces="1", ExportForces="true")
    name.addObject('RestShapeSpringsForceField', stiffness='100', angularStiffness='100', external_rest_shape='@../Omni/DOFs', points='0', external_points='0') 
    name.addObject('LCPForceFeedback', name="LCPFFScalpel",  forceCoef="0.007", activate="true")# Decide forceCoef value better

    name.addObject('UniformMass' , totalMass="6")
    name.addObject('UncoupledConstraintCorrection')
    

    Visu=name.addChild('Visu')
    Visu.addObject('MeshObjLoader' ,name="meshLoader_3", filename="mesh/scalpel.obj", scale="1.0", handleSeams="1" )
    Visu.addObject('OglModel' ,name="Visual" ,src="@meshLoader_3",  color="0 0.5 0.796", dz="7", dx="-4", dy="-3",  rx="0", ry="0", rz="90")
    Visu.addObject('RigidMapping' ,input="@..", output="@Visual")
    
    Surf=name.addChild('Surf')
    Surf.addObject('MeshObjLoader' ,filename="mesh/scalpel.obj" ,name="loader" )
    Surf.addObject('MeshTopology' ,src="@loader")
    Surf.addObject('MechanicalObject' ,src="@loader", scale="1.0",  dz="2", dx="-4", dy="-3",  rx="0", ry="0", rz="90")
    Surf.addObject('TriangleCollisionModel', name="Torus2Triangle")# , contactStiffness="2")#, tags="CarvingTool")
    Surf.addObject('LineCollisionModel', name="Torus2Line" , contactStiffness="1000")#, tags="CarvingTool")
    Surf.addObject('PointCollisionModel' ,name="Torus2Point" , contactStiffness="1000")#, tags="CarvingTool")
    Surf.addObject('RigidMapping')
    

    collFront = name.addChild('collFront')
    collFront.addObject('MechanicalObject', template="Vec3d", name="Particle", position="4 -3.7 -8.5",  dz="2", dx="-4", dy="-3",  rx="0", ry="0", rz="90")
    #collFront.addObject('UniformMass', totalMass="0.01")
    collFront.addObject('SphereCollisionModel', radius="0.2", name="SphereCollisionInstrument", tags="CarvingTool")
    collFront.addObject('RigidMapping')#, template="Rigid3d,Vec3d", name="MM->CM mapping",  input="@../InstrumentMechObject",  output="@Particle")

    collFront2 = name.addChild('collFront2')
    collFront2.addObject('MechanicalObject', template="Vec3d", name="Particle", position="4 -3.7 -8.5",  dz="4", dx="-4", dy="-4",  rx="0", ry="0", rz="90")
    collFront2.addObject('SphereCollisionModel', radius="0.2", name="SphereCollisionInstrument2", contactStiffness="1", tags="CarvingTool")
    collFront2.addObject('RigidMapping')#, template="Rigid3d,Vec3d", name="MM->CM mapping",  input="@../InstrumentMechObject",  output="@Particle")

    ScalpelHexa.MO=name.InstrumentMechObject
    # Scalpel.POS=name.InstrumentMechObject.findData('position').value
    #Scalpel.COLL_FRONT=name.Surf.Torus2Triangle.getLinkPath()
    ScalpelHexa.COLL_FRONT=name.collFront.SphereCollisionInstrument.getLinkPath()
    ScalpelHexa.COLL_FRONT2=name.collFront2.SphereCollisionInstrument2.getLinkPath()
    '''
    name=parentNode.addChild(name)
    name.addObject('EulerImplicitSolver',  rayleighStiffness="0.1", rayleighMass="0.1" )
    name.addObject('CGLinearSolver', iterations="25", tolerance="1e-5" ,threshold="1e-5")
    #if geomagic==True:
    name.addObject('MechanicalObject',  name='InstrumentMechObject', template='Rigid3d', position="@GeomagicDevice.positionDevice", scale="1.0", rotation="0 0 10",  dz="2", dx="-4", dy="-3",  rx="0", ry="0", rz="90") #, src="@instrumentMeshLoader")
    name.addObject('RestShapeSpringsForceField', stiffness='1000', angularStiffness='1000', external_rest_shape='@../Omni/DOFs', points='0', external_points='0') 
    name.addObject('LCPForceFeedback', name="LCPFFNeedle",  forceCoef="0.01", activate="true")# Decide forceCoef value better
    #else: 
    #    name.addObject('MechanicalObject', name="InstrumentMechObject", template="Rigid3d", scale="1.0" ,dx="8", dy="3", dz="25")
    name.addObject('UniformMass' , totalMass="5")
    name.addObject('UncoupledConstraintCorrection')

    #name.addObject("VectorSpringForceField",   object1="@Omni/ReferenceModel/instrumentRefState1", object2="@Scalpel/Surf/InstrumentMechObject", stiffness="50", viscosity="0" )


    Visu=name.addChild('Visu')
    Visu.addObject('MeshObjLoader' ,name="meshLoader_3", filename="mesh/scalpel.obj", scale="1.0", handleSeams="1" )
    Visu.addObject('OglModel' ,name="Visual" ,src="@meshLoader_3",  color="0 0.5 0.796", dz="2", dx="-4", dy="-3",  rx="0", ry="0", rz="90")
    Visu.addObject('RigidMapping' ,input="@..", output="@Visual")
    
    Surf=name.addChild('Surf')
    Surf.addObject('MeshObjLoader' ,filename="mesh/scalpel.obj" ,name="loader" )
    Surf.addObject('MeshTopology' ,src="@loader")
    Surf.addObject('MechanicalObject' ,src="@loader", name="InstrumentMechObject", scale="1.0",  dz="2", dx="-4", dy="-3",  rx="0", ry="0", rz="90")
    Surf.addObject('TriangleCollisionModel', name="Torus2Triangle" , contactStiffness="1000")#, tags="CarvingTool")
    Surf.addObject('LineCollisionModel', name="Torus2Line" , contactStiffness="1000")#, tags="CarvingTool")
    Surf.addObject('PointCollisionModel' ,name="Torus2Point" , contactStiffness="10000")#, tags="CarvingTool")
    #Surf.addObject("Monitor", name=file3, indices="0", listening="1", TrajectoriesPrecision="0.1", ExportForces="true")
    Surf.addObject('RigidMapping')

    collFront = name.addChild('collFront')
    collFront.addObject('MechanicalObject', template="Vec3d", name="Particle", position="4 -3.7 -8.5",  dz="2", dx="-4", dy="-3",  rx="0", ry="0", rz="90")
    collFront.addObject('SphereCollisionModel', radius="0.1", name="SphereCollisionInstrument", contactStiffness="1", tags="CarvingTool")
    collFront.addObject('RigidMapping')#, template="Rigid3d,Vec3d", name="MM->CM mapping",  input="@../InstrumentMechObject",  output="@Particle")

    if monitor==True:
        collFront.addObject("Monitor", name=file1, indices="0", listening="1", TrajectoriesPrecision="0.1", ExportPositions="true")
        collFront.addObject("Monitor", name=file2, indices="0", listening="1", TrajectoriesPrecision="0.1", ExportVelocities="true")

    collFront2 = name.addChild('collFront2')
    collFront2.addObject('MechanicalObject', template="Vec3d", name="Particle", position="4 -3.7 -8.5",  dz="4", dx="-4", dy="-4",  rx="0", ry="0", rz="90")
    collFront2.addObject('SphereCollisionModel', radius="0.1", name="SphereCollisionInstrument2", contactStiffness="1", tags="CarvingTool")
    collFront2.addObject('RigidMapping')#, template="Rigid3d,Vec3d", name="MM->CM mapping",  input="@../InstrumentMechObject",  output="@Particle")


    ScalpelHexa.MO=name.InstrumentMechObject.getLinkPath()
    ScalpelHexa.POS=name.InstrumentMechObject.findData('position').value
    #Scalpel.COLL_FRONT=name.Surf.Torus2Triangle.getLinkPath()
    ScalpelHexa.COLL_FRONT=name.collFront.SphereCollisionInstrument.getLinkPath()
    ScalpelHexa.COLL_FRONT2=name.collFront2.SphereCollisionInstrument2.getLinkPath()

    '''
