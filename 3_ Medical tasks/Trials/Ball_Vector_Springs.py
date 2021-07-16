# Required import for python
import Sofa
import numpy as np
import Sofa.SofaDeformable
import models
import controllers



# Choose in your script to activate or not the GUI
USE_GUI = True


def main():
    import SofaRuntime
    import Sofa.Gui
    import Sofa.Core
    SofaRuntime.importPlugin("SofaComponentAll")
    SofaRuntime.importPlugin("SofaOpenglVisual")
    SofaRuntime.importPlugin("SofaImplicitOdeSolver")

    root = Sofa.Core.Node("root")
    createScene(root)

    Sofa.Simulation.init(root)

    if not USE_GUI:
        for iteration in range(10):
            Sofa.Simulation.animate(root, root.dt.value)
    else:
        Sofa.Gui.GUIManager.Init("myscene", "qglviewer")
        Sofa.Gui.GUIManager.addGUI(root, __file__)
        Sofa.Gui.GUIManager.SetDimension(1080, 1080)
        Sofa.Gui.GUIManager.MainLoop(root)
        Sofa.Gui.GUIManager.closeGUI()

def computeIndices():
    result=' '
    indices=range(15)

    for i in range(15):
        result += str(indices[i]) + " "

    return result

def createScene(root):

    # Define root properties
    root.gravity=[0, 0, -5]
    root.dt=0.01

    # Required plugins
    root.addObject('RequiredPlugin', pluginName="SofaBaseMechanics SofaBaseTopology  Geomagic SofaBoundaryCondition  SofaConstraint SofaDeformable SofaEngine SofaGeneralLoader SofaGeneralObjectInteraction SofaGeneralSimpleFem SofaHaptics SofaImplicitOdeSolver SofaLoader SofaMeshCollision SofaOpenglVisual SofaRigid SofaSimpleFem SofaSparseSolver SofaUserInteraction SofaTopologyMapping ")

    # Collision pipeline
    root.addObject('CollisionPipeline', depth="6", verbose="0", draw="0")

    # Forces
    root.addObject('BruteForceDetection', name="detection")
    root.addObject('DefaultContactManager', name="CollisionResponse", response="FrictionContact")
    root.addObject('LocalMinDistance', name="proximity", alarmDistance="0.3", contactDistance="0.05", angleCone="0.0")

    # Animation loop
    root.addObject('FreeMotionAnimationLoop')

    # Constraint solver
    LCPConstraintSolver=root.addObject('LCPConstraintSolver', tolerance="0.001", maxIt="1000")

    # View
    root.addObject('OglViewport', screenPosition="0 0", cameraPosition="-0.00322233 -20.3537 18.828", cameraOrientation="0.418151 -6.26277e-06 -0.000108372 0.908378")

    physicalSphere1(parentNode=root, name="sphere", translation=[0,0,-3])
    physicalSphere2(parentNode=root, name="sphere2", translation=[0,0,4])

    #root.addObject('AttachConstraint', name="lowerConstraint", object1=physicalSphere1.MO1,       object2=physicalSphere2.MO2,     indices1=computeIndices(),  indices2=computeIndices())
    
    spring_force_field_skins = root.addObject("VectorSpringForceField", name="SkinsFF", object1 = physicalSphere1.MO1,  object2=physicalSphere2.MO2)
    #springs = [Sofa.SofaDeformable.LinearSpring(index1=i, index2=j, springStiffness=1000, dampingFactor=5, restLength=0.1) for i, j in zip(range(150),range(150))] 
    #spring_force_field_skins.addSprings(springs)


# Training sphere
def physicalSphere1(parentNode=None, name=None, translation=[0.0, 0.0, 0.0]):

    name=parentNode.addChild(name)
    #################### BEHAVIOUR ##########################
    
    name.addObject('EulerImplicitSolver', name='ODE solver', rayleighStiffness="0.01", rayleighMass="1.0")
    name.addObject('CGLinearSolver', name='linear solver', iterations="25", tolerance="1e-7", threshold="1e-7")
    name.addObject('MeshObjLoader', name='instrumentMeshLoader', filename="mesh\sphere.obj")
    #name.addObject('MeshGmshLoader', name='instrumentMeshLoader', filename="mesh\cylinder.msh")
   
    name.addObject('MechanicalObject', src="@instrumentMeshLoader", name='InstrumentMechObject', template='Vec3d', translation=translation, scale3d=[2, 2, 2])
    
    name.addObject('UniformMass', name='mass', totalMass="5")
    name.addObject('UncoupledConstraintCorrection')
    #Force = name.addObject('ConstantForceField', name="CFF", totalForce=[0, 0, 1, 0, 0, 0] )

    physicalSphere1.MO1=name.InstrumentMechObject.getLinkPath()

    #################### COLLISION ##########################
    
    InstrumentColl_Front = name.addChild('InstrumentColl_Front')
    InstrumentColl_Front.addObject('MechanicalObject', template="Vec3d", name="Particle")#, position="5 5 5")


    InstrumentColl_Front.addObject('SphereCollisionModel', radius="0.7", name="SphereCollisionInstrument", contactStiffness="1")
    InstrumentColl_Front.addObject('IdentityMapping', template="Vec3d,Vec3d", name="MM->CM mapping",  input="@../InstrumentMechObject",  output="@Particle")


    #################### VISUALIZATION ########################
    
    InstrumentVisu = name.addChild('InstrumentVisu')
    InstrumentVisu.addObject('OglModel', name='InstrumentVisualModel', src='@../instrumentMeshLoader', scale3d=[2,2,2])
    InstrumentVisu.addObject('IdentityMapping', template="Vec3d,Vec3d", name='MM-VM mapping', input='@../InstrumentMechObject', output='@InstrumentVisualModel')


def physicalSphere2(parentNode=None, name=None, translation=[0.0, 0.0, 0.0]):

    name=parentNode.addChild(name)
    #################### BEHAVIOUR ##########################
    
    name.addObject('EulerImplicitSolver', name='ODE solver', rayleighStiffness="0.01", rayleighMass="1.0")
    name.addObject('CGLinearSolver', name='linear solver', iterations="25", tolerance="1e-7", threshold="1e-7")
    name.addObject('MeshObjLoader', name='instrumentMeshLoader', filename="mesh\sphere.obj")
    #name.addObject('MeshGmshLoader', name='instrumentMeshLoader', filename="mesh\cylinder.msh")
    name.addObject('MechanicalObject', src="@instrumentMeshLoader", name='InstrumentMechObject', template='Vec3d', translation=translation, scale3d=[2, 2, 2])
    
    name.addObject('UniformMass', name='mass', totalMass="5")
    name.addObject('UncoupledConstraintCorrection')
    #Force = name.addObject('ConstantForceField', name="CFF", totalForce=[0, 0, 1, 0, 0, 0] )

    physicalSphere2.MO2=name.InstrumentMechObject.getLinkPath()
    boxROI=name.addObject('BoxROI', name='boxROI', box=[-3,-3,2, 3,3,7], drawBoxes='true', computeTriangles='true')
    name.addObject('RestShapeSpringsForceField', name='rest', points='@boxROI.indices', stiffness='1e12', angularStiffness='1e12')
    #################### COLLISION ##########################
    
    InstrumentColl_Front = name.addChild('InstrumentColl_Front')
    InstrumentColl_Front.addObject('MechanicalObject', template="Vec3d", name="Particle")#, position="5 5 5")


    InstrumentColl_Front.addObject('SphereCollisionModel', radius="0.7", name="SphereCollisionInstrument", contactStiffness="1")
    InstrumentColl_Front.addObject('IdentityMapping', template="Vec3d,Vec3d", name="MM->CM mapping",  input="@../InstrumentMechObject",  output="@Particle")


    #################### VISUALIZATION ########################
    
    InstrumentVisu = name.addChild('InstrumentVisu')
    InstrumentVisu.addObject('OglModel', name='InstrumentVisualModel', src='@../instrumentMeshLoader', scale3d=[2,2,2])
    InstrumentVisu.addObject('IdentityMapping', template="Vec3d,Vec3d", name='MM-VM mapping', input='@../InstrumentMechObject', output='@InstrumentVisualModel')



if __name__ == '__main__':
    main()
