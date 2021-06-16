import Sofa
import numpy as np

# Data
skin_youngModulus=300
thread_youngModulus=2000
skin_poissonRatio=0.49
thread_poissonRatio=0.8

def Skin(parentNode=None, name=None, rotation=[0.0, 0.0, 0.0], translation=[0.0, 0.0, 0.0], 
scale3d=[0.0, 0.0, 0.0],  fixingBox=[0.0, 0.0, 0.0], indicesBox=[0.0, 0.0, 0.0], importFile=None, carving=False):

    name=parentNode.addChild(name)
    
    #################### BEHAVIOUR ##########################
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
    name.addObject('MechanicalObject', name='SkinMechObj', template='Vec3d', translation=translation)#, src="@volumeLoader", position="1 1 20")
    Mass=name.addObject('DiagonalMass', name="SkinMass", template="Vec3d,double", massDensity="1.0")

    # Constraints
    name.addObject('BoxROI', name='boxROI', box=fixingBox, drawBoxes='true')
    name.addObject('RestShapeSpringsForceField', points='@boxROI.indices', stiffness='1e12', angularStiffness='1e12')

    # Forces
    name.addObject('TetrahedronFEMForceField', template='Vec3d', name='FEM', method='large', youngModulus=skin_youngModulus, poissonRatio=skin_poissonRatio)
    name.addObject('UncoupledConstraintCorrection')

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
    SkinColl.addObject('LineCollisionModel', name="LineCollisionSkin")
    SkinColl.addObject('PointCollisionModel', name="PointCollisionSkin") 

    # SkinColl.addObject('BoxROI', name="indicesBoxROI", box=indicesBox, drawBoxes='true')
    # print(name.SkinColl.indicesBoxROI.triangleIndices.value)
    # print(name.SkinColl.indicesBoxROI.findData('indices').value)


    #################### VISUALIZATION ########################
    
    SkinVisu = SkinColl.addChild('SkinVisu')
    SkinVisu.addObject('OglModel', template="Vec3d", name="Visual", color="1 0.75 0.796", material="Default Diffuse 1 0 0 1 1 Ambient 1 0 0 0.2 1 Specular 0 0 0 1 1 Emissive 0 0 0 1 1 Shininess 0 45 ")
    SkinVisu.addObject('IdentityMapping', template="Vec3d,Vec3d", name="default12", input="@..", output="@Visual" )
    SkinVisu.addObject('BoxROI', name='indicesBoxROI', box=indicesBox, drawBoxes='true')

    #print(name.SkinColl.SkinVisu.indicesBoxROI.triangleIndices.value)
    #print(name.SkinColl.SkinVisu.indicesBoxROI.findData('indices').value)

    
    # Data
    Skin.MO=name.SkinMechObj.getLinkPath()
    Skin.COLL=name.SkinColl.TriangleCollisionSkin.getLinkPath()
    # Skin.BoxIndexes_P=name.SkinColl.SkinVisu.indicesBoxROI.triangleIndices.value
    # Skin.BoxIndexes_T=name.SkinColl.SkinVisu.indicesBoxROI.indices.value



def Thread(parentNode=None, name=None, rotation=[0.0, 0.0, 0.0], translation=[0.0, 0.0, 0.0], 
scale3d=[0.0, 0.0, 0.0], fixingBox=[0.0, 0.0, 0.0], importFile=None, geomagic=False):

    name=parentNode.addChild(name)

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

    ThreadColl = name.addChild('ThreadColl')

    ThreadColl.addObject('PointCollisionModel', name="nameTri", selfCollision="True")
    ThreadColl.addObject('TriangleCollisionModel', name="nameTri", selfCollision="True") 

    #################### VISUALIZATION ########################

    ThreadVisu = ThreadColl.addChild('ThreadVisu')
    ThreadVisu.addObject('OglModel', template="Vec3d", name="Visual", color="1 0.75 0.796", material="Default Diffuse 1 0 0 1 1 Ambient 1 0 0 0.2 1 Specular 0 0 0 1 1 Emissive 0 0 0 1 1 Shininess 0 45 ")
    ThreadVisu.addObject('IdentityMapping', template="Vec3d,Vec3d", name="default12", input="@..", output="@Visual" )
    

# WHEN I'LL UNDERSTAND WHY THE SAME THING WORKS FOR THE NEEDLE AND NOT FOR THE SCALPEL I'LL CANCEL ONE OF THE TWO INSTRUMENT FUNCTIONS! 
# OR I'LL DO THE SAME WHEN I'LL BE WORKING WITH THE GEOMAGIC ONLY

# Good for the needle... (BEST VERSION I THINK), but without carving the object falls under skin a part from collision point...
def Instrument(parentNode=None, name=None, rotation=[0.0, 0.0, 0.0], translation=[0.0, 0.0, 0.0],
scale3d=[0.0, 0.0, 0.0],  fixingBox=[0.0, 0.0, 0.0], importFile=None, pointPosition=None, carving=False, geomagic=False):

    #################### BEHAVIOUR ##########################
    name=parentNode.addChild(name)
    name.addObject('EulerImplicitSolver', name='ODE solver', rayleighStiffness="0.01", rayleighMass="1.0")
    name.addObject('CGLinearSolver', name='linear solver', iterations="25", tolerance="1e-7", threshold="1e-7")
    name.addObject('MeshObjLoader', name='instrumentMeshLoader', filename=importFile)
    if geomagic==True:
        name.addObject('MechanicalObject', src="@instrumentMeshLoader", name='InstrumentMechObject', template='Rigid3d', position=translation, scale3d=scale3d)
        name.addObject('RestShapeSpringsForceField', stiffness='1000', angularStiffness='1000', external_rest_shape='@../Omni/DOFs', points='0', external_points='0') 
        name.addObject('LCPForceFeedback', name="LCPFF1", activate="true", forceCoef="0.5")
    else:
        name.addObject('MechanicalObject', src="@instrumentMeshLoader", name='InstrumentMechObject', template='Rigid3d', translation=translation, scale3d=scale3d)
    
    name.addObject('UniformMass', name='mass', totalMass="5")
    name.addObject('UncoupledConstraintCorrection')

    #################### COLLISION ##########################
    
    InstrumentColl = name.addChild('InstrumentColl')
    
    InstrumentColl.addObject('MechanicalObject', template="Vec3d", name="Particle", position=pointPosition)
    if carving==True:
        InstrumentColl.addObject('SphereCollisionModel', radius="1", name="SphereCollisionInstrument", contactStiffness="2", tags="CarvingTool")
    else:
        InstrumentColl.addObject('SphereCollisionModel', radius="1", name="SphereCollisionInstrument", contactStiffness="2")
    InstrumentColl.addObject('RigidMapping', template="Rigid3d,Vec3d", name="MM->CM mapping",  input="@../InstrumentMechObject",  output="@Particle")

    InstrumentColl2 = name.addChild('InstrumentColl2')
    
    InstrumentColl2.addObject('MechanicalObject', template="Vec3d", name="Particle2", position="0 0.02 0.05")
    if carving==True:
        InstrumentColl2.addObject('SphereCollisionModel', radius="1", name="SphereCollisionInstrument2", contactStiffness="2", tags="CarvingTool")
    else:
        InstrumentColl2.addObject('SphereCollisionModel', radius="1", name="SphereCollisionInstrument2", contactStiffness="2")
    InstrumentColl2.addObject('RigidMapping', template="Rigid3d,Vec3d", name="MM->CM mapping",  input="@../InstrumentMechObject",  output="@Particle2")

    #################### VISUALIZATION ########################
    
    InstrumentVisu = name.addChild('InstrumentVisu')
    InstrumentVisu.addObject('OglModel', name='InstrumentVisualModel', src='@../instrumentMeshLoader', scale3d=scale3d, color="0 0.5 0.796")
    InstrumentVisu.addObject('RigidMapping', template="Rigid3d,Vec3d", name='MM-VM mapping', input='@../InstrumentMechObject', output='@InstrumentVisualModel')

    # Data
    Instrument.MO=name.InstrumentMechObject.getLinkPath()
    Instrument.COLL_BACK_MO=name.InstrumentColl2.Particle2.getLinkPath()
    Instrument.POS=name.InstrumentMechObject.findData('position').value
    Instrument.COLL_FRONT=name.InstrumentColl.SphereCollisionInstrument.getLinkPath()
    Instrument.COLL_BACK=name.InstrumentColl2.SphereCollisionInstrument2.getLinkPath()
    


# Good for the scalpel, but has a lot of collision points...
def Instrument2(parentNode=None, name=None, rotation=[0.0, 0.0, 0.0], translation=[0.0, 0.0, 0.0], 
scale3d=[0.0, 0.0, 0.0],  fixingBox=[0.0, 0.0, 0.0], importFile=None, pointPosition=None, carving=False, geomagic=False):
    name=parentNode.addChild(name)
    
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
    
    InstrumentVisu = name.addChild('InstrumentVisu')
    InstrumentVisu.addObject('OglModel', name='InstrumentVisualModel', src='@../instrumentMeshLoader', color="0 0.5 0.796")
    InstrumentVisu.addObject('IdentityMapping', name='MM-VM mapping', input='@../mechObject', output='@InstrumentVisualModel')

    #################### COLLISION ##########################
    
    InstrumentColl = name.addChild('InstrumentColl')
    InstrumentColl.addObject('MechanicalObject', template="Vec3d", name="Particle", position=pointPosition)
    if carving==True:
        InstrumentColl.addObject('SphereCollisionModel', radius=0.4, name="SphereCollisionInstrument", contactStiffness="2", tags="CarvingTool")
    else:
        InstrumentColl.addObject('SphereCollisionModel', radius=0.4, name="SphereCollisionInstrument", contactStiffness="2")

    InstrumentColl.addObject('IdentityMapping', name="MM->CM mapping",  input="@../mechObject",  output="@Particle")


def GeomagicDevice(parentNode=None, name=None):
    name=parentNode.addChild(name)
    name.addObject('MechanicalObject', template="Rigid3", name="DOFs", position="@GeomagicDevice.positionDevice")
    name.addObject('MechanicalStateController', template="Rigid3", listening="true", mainDirection="-1.0 0.0 0.0")
    

def MyContactListener(parentNode=None, name=None, collisionModel1=None, collisionModel2=None):
    name=parentNode.addChild(name)
    listener=name.addObject('ContactListener', collisionModel1 = collisionModel1, collisionModel2 = collisionModel2)
    print(listener.getNumberOfContacts())

def sphere(parentNode=None, name=None, translation=[0.0, 0.0, 0.0]):
    name=parentNode.addChild(name)
    name.addObject('MechanicalObject', name='sphereMechObj', template='Vec3d', position=translation)
    name.addObject('SphereCollisionModel', radius="2", name="SphereCollisionInstrument", contactStiffness="2")

    # Data
    sphere.MO=name.sphereMechObj.getLinkPath()


    #################### BEHAVIOUR ##########################
    # importFile="C:\sofa\src\Chiara\mesh\sphere"
    # name.addObject('EulerImplicitSolver', name='ODE solver', rayleighStiffness="0.01", rayleighMass="1.0")
    # name.addObject('CGLinearSolver', name='linear solver', iterations="25", tolerance="1e-7", threshold="1e-7")
    # name.addObject('MeshGmshLoader', name='instrumentMeshLoader', filename=importFile)
    # name.addObject('MechanicalObject', src="@instrumentMeshLoader", name='InstrumentmechObject', template='Vec3d', translation=translation, scale3d="0.1 0.1 0.1")
    # name.addObject('UniformMass', name='mass', totalMass="5")
    # name.addObject('UncoupledConstraintCorrection')

    # #################### COLLISION ##########################
    # SphereColl = name.addChild('SphereColl')
    # name.addObject('MeshGmshLoader', name='instrumentMeshLoader', filename=importFile)
    # name.addObject('MechanicalObject', src="@instrumentMeshLoader", name='InstrumentmechObject', template='Vec3d', translation=translation, scale3d="0.1 0.1 0.1")
    # SphereColl.addObject('MechanicalObject', template="Vec3d", name="Particle")
    # SphereColl.addObject('SphereCollisionModel', radius="2", name="SphereCollisionInstrument", contactStiffness="2")
    # SphereColl.addObject('IdentityMapping', name="MM->CM mapping",  input="@../InstrumentmechObject",  output="@Particle")

    
