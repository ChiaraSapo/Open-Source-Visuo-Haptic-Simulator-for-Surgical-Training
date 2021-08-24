import Sofa
import numpy as np

# Data
skin_youngModulus=4000
thread_youngModulus=3000
skin_poissonRatio=0.1
thread_poissonRatio=0.8


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
borderBox5=[0.0, 0.0, 0.0],borderBox6=[0.0, 0.0, 0.0],borderBox7=[0.0, 0.0, 0.0],borderBox8=[0.0, 0.0, 0.0],borderBox9=[0.0, 0.0, 0.0],
borderBox10=[0.0, 0.0, 0.0], borderBox11=[0.0, 0.0, 0.0], borderBox12=[0.0, 0.0, 0.0]):

    name=parentNode.addChild(name)
    
    #################### BEHAVIOUR ##########################
    # Solvers
    name.addObject('EulerImplicitSolver', name="odesolver", rayleighStiffness="0.01", rayleighMass="0.01") #added  2 params
    name.addObject('CGLinearSolver', iterations="25", name="EpiLinearsolver", tolerance="1.0e-9", threshold="1.0e-9")

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

    # Fixed box for constraints
    boxROI=name.addObject('BoxROI', name='boxROI', box=fixingBox, drawBoxes='true', computeTriangles='true')
    name.addObject('RestShapeSpringsForceField', name='rest', points='@boxROI.indices', stiffness='1e12', angularStiffness='1e12')


    name.addObject('BoxROI', name='borderBox1', box=borderBox1, drawBoxes='true', computeTriangles='true')
    name.addObject('BoxROI', name='borderBox2', box=borderBox2, drawBoxes='true', computeTriangles='true')
    name.addObject('BoxROI', name='borderBox3', box=borderBox3, drawBoxes='true', computeTriangles='true')
    name.addObject('BoxROI', name='borderBox4', box=borderBox4, drawBoxes='true', computeTriangles='true')
    name.addObject('BoxROI', name='borderBox5', box=borderBox5, drawBoxes='true', computeTriangles='true')
    name.addObject('BoxROI', name='borderBox6', box=borderBox6, drawBoxes='true', computeTriangles='true')
    name.addObject('BoxROI', name='borderBox7', box=borderBox7, drawBoxes='true', computeTriangles='true')
    name.addObject('BoxROI', name='borderBox8', box=borderBox8, drawBoxes='true', computeTriangles='true')
    name.addObject('BoxROI', name='borderBox9', box=borderBox9, drawBoxes='true', computeTriangles='true')
    name.addObject('BoxROI', name='borderBox10', box=borderBox10, drawBoxes='true', computeTriangles='true')
    name.addObject('BoxROI', name='borderBox11', box=borderBox11, drawBoxes='true', computeTriangles='true')
    name.addObject('BoxROI', name='borderBox12', box=borderBox12, drawBoxes='true', computeTriangles='true')

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
        Skin.borderBox1=name.borderBox1
        Skin.borderBox2=name.borderBox2
        Skin.borderBox3=name.borderBox3
        Skin.borderBox4=name.borderBox4
        Skin.borderBox5=name.borderBox5
        Skin.borderBox6=name.borderBox6
        Skin.borderBox7=name.borderBox7
        Skin.borderBox8=name.borderBox8
        Skin.borderBox9=name.borderBox9
        Skin.borderBox10=name.borderBox10
        Skin.borderBox11=name.borderBox11
        Skin.borderBox12=name.borderBox12

    if side==1: # right
        Skin.itself_right=name.getLinkPath()
        Skin.MO_right=name.SkinMechObj.getLinkPath()
        Skin.COLL_right=name.SkinColl.TriangleCollisionSkin.getLinkPath()
        Skin.borderBox1_right=name.borderBox1
        Skin.borderBox2_right=name.borderBox2
        Skin.borderBox3_right=name.borderBox3
        Skin.borderBox4_right=name.borderBox4
        Skin.borderBox5_right=name.borderBox5
        Skin.borderBox6_right=name.borderBox6
        Skin.borderBox7_right=name.borderBox7
        Skin.borderBox8_right=name.borderBox8
        Skin.borderBox9_right=name.borderBox9
        Skin.borderBox10_right=name.borderBox10
        Skin.borderBox11_right=name.borderBox11
        Skin.borderBox12_right=name.borderBox12
    Skin.CONTAINER=name.TetraContainer.getLinkPath()

    return name


## This function defines a scalpel node with behavior/collision/visual models
# @param parentNode: parent node of the scalpel
# @param name: name of the behavior node
# @param scale3d: scale of the scalpel along all directions
# @param monitor: if True, saves position, velocity and force of the scalpel 
# @param file1: name of the file that saves positions
# @param file2: name of the file that saves velocities
# @param file3: name of the file that saves forces

def Scalpel(parentNode=None, name=None, scale3d=[0.0, 0.0, 0.0], monitor=False, file1=None, file2=None, file3=None): 

    name=parentNode.addChild(name)
    name.addObject('EulerImplicitSolver',  rayleighStiffness="0.1", rayleighMass="0.1" )
    name.addObject('CGLinearSolver', iterations="25", tolerance="1e-5" ,threshold="1e-5")
    name.addObject('MechanicalObject',  name='InstrumentMechObject', template='Rigid3d', position="@GeomagicDevice.positionDevice", scale="1.0", rotation="0 0 10",  dz="2", dx="-4", dy="-3",  rx="0", ry="0", rz="90") #, src="@instrumentMeshLoader")
    name.addObject('RestShapeSpringsForceField', stiffness='1000', angularStiffness='1000', external_rest_shape='@../Omni/DOFs', points='0', external_points='0') 
    name.addObject('LCPForceFeedback', name="LCPFFNeedle",  forceCoef="0.007", activate="true")
    name.addObject('UniformMass' , totalMass="5")
    name.addObject('UncoupledConstraintCorrection')

    Visu=name.addChild('Visu')
    Visu.addObject('MeshObjLoader' ,name="meshLoader_3", filename="mesh/scalpel.obj", scale="1.0", handleSeams="1" )
    Visu.addObject('OglModel' ,name="Visual" ,src="@meshLoader_3",  color="0 0.5 0.796", dz="2", dx="-4", dy="-3",  rx="0", ry="0", rz="90")
    Visu.addObject('RigidMapping' ,input="@..", output="@Visual")
    
    Surf=name.addChild('Surf')
    Surf.addObject('MeshObjLoader' ,filename="mesh/scalpel.obj" ,name="loader" )
    Surf.addObject('MeshTopology' ,src="@loader")
    Surf.addObject('MechanicalObject' ,src="@loader", scale="1.0",  dz="2", dx="-4", dy="-3",  rx="0", ry="0", rz="90")
    Surf.addObject('TriangleCollisionModel', name="Torus2Triangle" , contactStiffness="1000")#, tags="CarvingTool")
    Surf.addObject('LineCollisionModel', name="Torus2Line" , contactStiffness="1000")#, tags="CarvingTool")
    Surf.addObject('PointCollisionModel' ,name="Torus2Point" , contactStiffness="10000")#, tags="CarvingTool")
    Surf.addObject('RigidMapping')

    collFront = name.addChild('collFront')
    collFront.addObject('MechanicalObject', template="Vec3d", name="Particle", position="4 -3.7 -8.5",  dz="2", dx="-4", dy="-3",  rx="0", ry="0", rz="90")
    collFront.addObject('SphereCollisionModel', radius="0.2", name="SphereCollisionInstrument", contactStiffness="1")#, tags="CarvingTool")
    collFront.addObject('RigidMapping')#, template="Rigid3d,Vec3d", name="MM->CM mapping",  input="@../InstrumentMechObject",  output="@Particle")

    collFront2 = name.addChild('collFront2')
    collFront2.addObject('MechanicalObject', template="Vec3d", name="Particle", position="4 -3.7 -8.5",  dz="4", dx="-4", dy="-4",  rx="0", ry="0", rz="90")
    collFront2.addObject('SphereCollisionModel', radius="0.2", name="SphereCollisionInstrument2", contactStiffness="1", tags="CarvingTool")
    collFront2.addObject('RigidMapping')#, template="Rigid3d,Vec3d", name="MM->CM mapping",  input="@../InstrumentMechObject",  output="@Particle")
    
    if monitor==True:
        collFront.addObject("Monitor", name=file1, indices="0", listening="1", TrajectoriesPrecision="0.1", ExportPositions="true")
        collFront.addObject("Monitor", name=file2, indices="0", listening="1", TrajectoriesPrecision="0.1", ExportVelocities="true")
        collFront.addObject("Monitor", name=file3, indices="0", listening="1", showForces="1", ExportForces="true")
    
    Scalpel.MO=name.InstrumentMechObject.getLinkPath()
    Scalpel.POS=name.InstrumentMechObject.findData('position').value
    Scalpel.COLL_FRONT=name.collFront.SphereCollisionInstrument.getLinkPath()
    Scalpel.COLL_FRONT2=name.collFront2.SphereCollisionInstrument2.getLinkPath()


