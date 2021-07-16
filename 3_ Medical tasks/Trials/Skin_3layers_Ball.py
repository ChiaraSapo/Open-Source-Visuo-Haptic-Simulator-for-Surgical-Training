# Required import for python
import Sofa
import numpy as np

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


# Choose in your script to activate or not the GUI
USE_GUI = True

def main():
    import SofaRuntime
    import Sofa.Gui
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
        Sofa.Gui.GUIManager.createGUI(root, __file__)
        Sofa.Gui.GUIManager.SetDimension(1080, 1080)
        Sofa.Gui.GUIManager.MainLoop(root)
        Sofa.Gui.GUIManager.closeGUI()

def computeIndices(layer, z):
    result=' '
    indices = np.array(range(z*n_vertices_per_layer)).reshape(z,n_vertices_per_layer)

    for i in range(n_vertices_per_layer):
        if layer=="bottom":
            result += str(indices[0,i]) + " "
        elif layer=="top":
            result += str(indices[-1,i]) + " "

    return result

def createScene(root):
    root.gravity=[0, 0, -10]
    root.dt=0.01

    root.addObject('RequiredPlugin', pluginName="Geomagic SofaBoundaryCondition SofaCarving SofaConstraint SofaDeformable SofaGeneralLoader SofaGeneralObjectInteraction SofaGeneralSimpleFem SofaHaptics SofaImplicitOdeSolver SofaLoader SofaMeshCollision SofaOpenglVisual SofaRigid SofaSimpleFem SofaSparseSolver SofaUserInteraction SofaTopologyMapping ")

    # Collision
    root.addObject('CollisionPipeline', depth="6", verbose="0", draw="0")
    root.addObject('BruteForceDetection', name="detection")
    root.addObject('LocalMinDistance', name="proximity", alarmDistance="1", contactDistance="0.05", angleCone="0.1")
    root.addObject('DefaultContactManager', name="CollisionResponse", response="FrictionContact")
    #root.addObject('DiscreteIntersection')
    
    # Animation loop
    root.addObject('FreeMotionAnimationLoop')
    root.addObject('LCPConstraintSolver', tolerance="0.001", maxIt="1000")

    ###################################################################
    #--------------------- SKIN EPIDERMIS LAYER ----------------------#
    ###################################################################
    epi=root.addChild('epi')
    epi.addObject('EulerImplicitSolver', name="ODE solver", rayleighStiffness="0.01", rayleighMass="0.01")
    epi.addObject('CGLinearSolver', iterations="25", name="linear solver", tolerance="1.0e-9", threshold="1.0e-9")
    #epi.addObject('SparseLDLSolver')

    epi.addObject('MechanicalObject', template="Vec3d", name="Hexa_E", scale3d="2 1 0.2", position="0 0 -8", showVectors="true", drawMode="2")

    #epi.addObject('RegularGridTopology', name="grid", n="5 2 2", min="-5 -5 -10", max="3 4 10", p0="-4 -4 -10")
    epi.addObject('RegularGridTopology', name="grid", nx=x_vertices, ny=y_vertices, nz=z_epi, xmin=x_offset, xmax=x_length, ymin=y_offset, ymax=y_length, zmin=z_derma+z_hypo+z_offset, zmax=(z_hypo+z_derma+z_epi+z_offset+1))
    epi.addObject('HexahedronSetGeometryAlgorithms')
    
    epi.addObject('DiagonalMass', template="Vec3d,double", name="Mass", massDensity="1.0")
    epi.addObject('HexahedronFEMForceField', template="Vec3d", name="FEM", poissonRatio=poissonRatio_ALL, youngModulus=youngModulus_E )
    epi.addObject('UncoupledConstraintCorrection')

    quad=epi.addChild('quad')
    quad.addObject('QuadSetTopologyContainer', name="Q_Container")
    quad.addObject('QuadSetTopologyModifier', name="Q_Modifier")
    quad.addObject('QuadSetGeometryAlgorithms', template="Vec3d", name="Q_GeomAlgo")
    quad.addObject('Hexa2QuadTopologicalMapping', name="default6", input="@../grid", output="@Q_Container")

    tri=quad.addChild('tri')
    tri.addObject('TriangleSetTopologyContainer', name="T_Container")
    tri.addObject('TriangleSetTopologyModifier', name="T_Modifier")
    tri.addObject('TriangleSetGeometryAlgorithms', template="Vec3d", name="T_GeomAlgo")
    tri.addObject('Quad2TriangleTopologicalMapping', name="default8", input="@../Q_Container", output="@T_Container")
    tri.addObject('TriangleCollisionModel', name="EpiCollision", contactStiffness="0.01")

    visu=tri.addChild('visu') 
    visu.addObject('OglModel', template="Vec3d", name="Visual", color="1 0.75 0.796", material="Default Diffuse 1 0 0 1 1 Ambient 1 0 0 0.2 1 Specular 0 0 0 1 1 Emissive 0 0 0 1 1 Shininess 0 45 ")
    visu.addObject('OglViewport', screenPosition="0 0", screenSize="250 250", cameraPosition="-0.285199 -15.2745 16.7859", cameraOrientation="0.394169 0.0120415 0.00490558 0.918946" )
    visu.addObject('IdentityMapping', template="Vec3d,Vec3d", name="default12", input="@..", output="@Visual" )
    

   
    
    ###############################################################
    #--------------------- SKIN DERMA LAYER ----------------------#
    ###############################################################
    derma=root.addChild('derma')
    derma.addObject('EulerImplicitSolver', name="ODE solver", rayleighStiffness="0.01", rayleighMass="0.01")
    derma.addObject('SparseLDLSolver')
    
    derma.addObject('MechanicalObject', template="Vec3d", name="Hexa_D", scale3d="2 1 0.2", position="0 0 -8", showVectors="true", drawMode="2")

    derma.addObject('RegularGridTopology', name="grid", nx=x_vertices, ny=y_vertices, nz=z_derma, xmin=x_offset, xmax=x_length, ymin=y_offset, ymax=y_length, zmin=z_hypo+z_offset, zmax=(z_hypo+z_derma+z_offset+1))
    derma.addObject('HexahedronSetGeometryAlgorithms')
    
    derma.addObject('DiagonalMass', template="Vec3d,double", name="Mass", massDensity="1.0")
    derma.addObject('HexahedronFEMForceField', template="Vec3d", name="FEM", poissonRatio=poissonRatio_ALL, youngModulus=youngModulus_D )
    #derma.addObject('SparseLDLSolver', name="preconditioner")
    derma.addObject('UncoupledConstraintCorrection')

    quad=derma.addChild('quad')
    quad.addObject('QuadSetTopologyContainer', name="Q_Container")
    quad.addObject('QuadSetTopologyModifier', name="Q_Modifier")
    quad.addObject('QuadSetGeometryAlgorithms', template="Vec3d", name="Q_GeomAlgo")
    quad.addObject('Hexa2QuadTopologicalMapping', name="default6", input="@../grid", output="@Q_Container")

    tri=quad.addChild('tri')
    tri.addObject('TriangleSetTopologyContainer', name="T_Container")
    tri.addObject('TriangleSetTopologyModifier', name="T_Modifier")
    tri.addObject('TriangleSetGeometryAlgorithms', template="Vec3d", name="T_GeomAlgo")
    tri.addObject('Quad2TriangleTopologicalMapping', name="default8", input="@../Q_Container", output="@T_Container")
    #tri.addObject('TriangleCollisionModel', name="SkinCollision", contactStiffness="0.01")

    visu=tri.addChild('visu')
    visu.addObject('OglModel', template="Vec3d", name="Visual", color="1 1 0.7", material="Default Diffuse 1 0 0 1 1 Ambient 1 0 0 0.2 1 Specular 0 0 0 1 1 Emissive 0 0 0 1 1 Shininess 0 45 ")
    visu.addObject('OglViewport', screenPosition="0 0", screenSize="250 250", cameraPosition="-0.285199 -15.2745 16.7859", cameraOrientation="0.394169 0.0120415 0.00490558 0.918946" )
    visu.addObject('IdentityMapping', template="Vec3d,Vec3d", name="default12", input="@..", output="@Visual" )





    ####################################################################
    #--------------------- SKIN HYPODERMIS LAYER ----------------------#
    ####################################################################
    hypo=root.addChild('hypo')
    hypo.addObject('EulerImplicitSolver', name="ODE solver", rayleighStiffness="0.01", rayleighMass="0.01")
    hypo.addObject('SparseLDLSolver')
    
    hypo.addObject('MechanicalObject', template="Vec3d", name="Hexa_H", scale3d="2 1 0.2", position="0 0 -8", showVectors="true", drawMode="2")
    hypo.addObject('RegularGridTopology', name="grid", nx=x_vertices, ny=y_vertices, nz=z_hypo, xmin=x_offset, xmax=x_length, ymin=y_offset, ymax=y_length, zmin=z_offset, zmax=(z_hypo+z_offset))
    #, name="grid", n="8 8 2", min="-5 -4 -10", max="3 4 10", p0="-4 -4 -10" )
    #, name="grid", nx=x_vertices, ny=y_vertices, nz=z_hypo, xmin=x_offset, xmax=x_length-6, ymin=y_offset, ymax=y_length-1, zmin="0", zmax=(z_hypo))
    hypo.addObject('HexahedronSetGeometryAlgorithms')
    
    hypo.addObject('DiagonalMass', template="Vec3d,double", name="Mass", massDensity="1.0")
    hypo.addObject('HexahedronFEMForceField', template="Vec3d", name="FEM", poissonRatio=poissonRatio_ALL, youngModulus=youngModulus_H )
    #hypo.addObject('SparseLDLSolver', name="preconditioner")
    hypo.addObject('UncoupledConstraintCorrection')
    hypo.addObject('FixedConstraint', template="Vec3d", name="Fixed Dofs", indices=computeIndices("bottom", z_hypo))
    hypo.addObject('FixedPlaneConstraint', template="Vec3d", name="defaultPlane", direction="0 0 1", dmin="0") #??????????????????????
    
    quad=hypo.addChild('quad')
    quad.addObject('QuadSetTopologyContainer', name="Q_Container")
    quad.addObject('QuadSetTopologyModifier', name="Q_Modifier")
    quad.addObject('QuadSetGeometryAlgorithms', template="Vec3d", name="Q_GeomAlgo")
    quad.addObject('Hexa2QuadTopologicalMapping', name="default6", input="@../grid", output="@Q_Container")

    tri=quad.addChild('tri')
    tri.addObject('TriangleSetTopologyContainer', name="T_Container")
    tri.addObject('TriangleSetTopologyModifier', name="T_Modifier")
    tri.addObject('TriangleSetGeometryAlgorithms', template="Vec3d", name="T_GeomAlgo")
    tri.addObject('Quad2TriangleTopologicalMapping', name="default8", input="@../Q_Container", output="@T_Container")
    #tri.addObject('TriangleCollisionModel', name="SkinCollision", contactStiffness="0.01")

    visu=tri.addChild('visu')
    visu.addObject('OglModel', template="Vec3d", name="Visual", color="1 1 0.4", material="Default Diffuse 1 0 0 1 1 Ambient 1 0 0 0.2 1 Specular 0 0 0 1 1 Emissive 0 0 0 1 1 Shininess 0 45 ")
    visu.addObject('OglViewport', screenPosition="0 0", screenSize="250 250", cameraPosition="-0.285199 -15.2745 16.7859", cameraOrientation="0.394169 0.0120415 0.00490558 0.918946" )
    visu.addObject('IdentityMapping', template="Vec3d,Vec3d", name="default12", input="@..", output="@Visual" )




    ############################################################
    #--------------------- ATTACH LAYERS ----------------------#
    ############################################################    
    root.addObject('AttachConstraint', name="lowerConstraint", object1="@hypo",       object2="@derma",     indices1=computeIndices("top", z_hypo),  indices2=computeIndices("bottom", z_derma))
    root.addObject('AttachConstraint', name="upperConstraint", object1="@derma",      object2="@epi",       indices1=computeIndices("top", z_derma), indices2=computeIndices("bottom", z_epi))
    
    physicalSphere(parentNode=root, name="sph")


    return root


# Training sphere
def physicalSphere(parentNode=None, name=None, translation=[0.0, 0.0, 0.0], scale3d=[0.0, 0.0, 0.0], color=[0.0, 0.0, 0.0]):

    name=parentNode.addChild(name)
    #################### BEHAVIOUR ##########################
    
    name.addObject('EulerImplicitSolver', name='ODE solver', rayleighStiffness="0.01", rayleighMass="1.0")
    name.addObject('CGLinearSolver', name='linear solver', iterations="25", tolerance="1e-7", threshold="1e-7")
    name.addObject('MeshObjLoader', name='instrumentMeshLoader', filename="mesh\sphere.obj")
   
    name.addObject('MechanicalObject', src="@instrumentMeshLoader", name='InstrumentMechObject', template='Rigid3d', translation=[4, 10, 5], scale3d=[2, 2, 2])
    
    name.addObject('UniformMass', name='mass', totalMass="5")
    name.addObject('UncoupledConstraintCorrection')
    Force = name.addObject('ConstantForceField', name="CFF", totalForce=[0, 0, 1, 0, 0, 0] )

    #################### COLLISION ##########################
    
    InstrumentColl_Front = name.addChild('InstrumentColl_Front')
    InstrumentColl_Front.addObject('MechanicalObject', template="Vec3d", name="Particle")#, position="5 5 5")


    InstrumentColl_Front.addObject('SphereCollisionModel', radius="1", name="SphereCollisionInstrument", contactStiffness="1")
    InstrumentColl_Front.addObject('RigidMapping', template="Rigid3d,Vec3d", name="MM->CM mapping",  input="@../InstrumentMechObject",  output="@Particle")


    #################### VISUALIZATION ########################
    
    InstrumentVisu = name.addChild('InstrumentVisu')
    InstrumentVisu.addObject('OglModel', name='InstrumentVisualModel', src='@../instrumentMeshLoader', scale3d=[2,2,2])
    InstrumentVisu.addObject('RigidMapping', template="Rigid3d,Vec3d", name='MM-VM mapping', input='@../InstrumentMechObject', output='@InstrumentVisualModel')







if __name__ == '__main__':
    main()
