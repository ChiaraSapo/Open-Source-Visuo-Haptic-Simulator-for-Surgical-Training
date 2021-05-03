# Required import for python
import Sofa
import numpy as np

x_vertices=9
y_vertices=9
x_length=11
y_length=11
n_vertices_per_layer=x_vertices*y_vertices
z_epidermis=2
z_derma=4
z_hypodermis=2

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
    root.gravity=[0, -9.81, 0]
    root.dt=0.01
    root.addObject('RequiredPlugin', pluginName="SofaTopologyMapping SofaLoader SofaMeshCollision SofaRigid SofaGeneralObjectInteraction SofaConstraint SofaOpenglVisual SofaBoundaryCondition SofaGeneralLoader SofaGeneralSimpleFem SofaImplicitOdeSolver SofaSimpleFem SofaSparseSolver")
    #root.addObject('RequiredPlugin', pluginName="Geomagic")

    # Collision
    root.addObject('CollisionPipeline', depth="6", verbose="0", draw="0")
    root.addObject('BruteForceDetection', name="detection")
    root.addObject('DefaultContactManager', name="CollisionResponse", response="FrictionContact")
    root.addObject('DiscreteIntersection')
    root.addObject('LocalMinDistance', name="LMD-proximity", alarmDistance="0.5", contactDistance="0.25", angleCone="0.1")
    
    # Animation loop
    root.addObject('FreeMotionAnimationLoop')

    # Constraint solver
    root.addObject('LCPConstraintSolver', tolerance="0.001", maxIt="1000")

    # Geomagic device
    #root.addObject('GeomagicDriver', name="GeomagicDevice", deviceName="Default Device", scale="1", drawDeviceFrame="1", drawDevice="0", positionBase="0 0 0",  orientationBase="0 0 0 1")


    #--------------------- SKIN HYPODERMIS LAYER ----------------------#
    hypodermis=root.addChild('hypodermis')
    hypodermis.addObject('EulerImplicitSolver', name="ODE solver", rayleighStiffness="0.01", rayleighMass="0.01")
    hypodermis.addObject('SparseLDLSolver')
    
    hypodermis.addObject('MechanicalObject', template="Vec3d", name="Hexa_H", scale3d="2 1 0.2", position="0 0 -8", showVectors="true", drawMode="2")
    hypodermis.addObject('RegularGridTopology', name="grid", nx=x_vertices, ny=y_vertices, nz=z_hypodermis, xmin="0", xmax=x_length, ymin="0", ymax=y_length, zmin="0", zmax=(z_hypodermis))
    #, name="grid", n="8 8 2", min="-5 -4 -10", max="3 4 10", p0="-4 -4 -10" )
    #, name="grid", nx=x_vertices, ny=y_vertices, nz=z_hypodermis, xmin="0", xmax=x_length-6, ymin="0", ymax=y_length-1, zmin="0", zmax=(z_hypodermis))
    hypodermis.addObject('HexahedronSetGeometryAlgorithms')
    
    hypodermis.addObject('DiagonalMass', template="Vec3d,double", name="Mass", massDensity="1.0")
    hypodermis.addObject('HexahedronFEMForceField', template="Vec3d", name="FEM", poissonRatio="0.47", youngModulus="2000" )
    hypodermis.addObject('LinearSolverConstraintCorrection')
    hypodermis.addObject('FixedConstraint', template="Vec3d", name="Fixed Dofs", indices=computeIndices("bottom", z_hypodermis))
    #hypodermis.addObject('FixedPlaneConstraint', template="Vec3d", name="defaultPlane", direction="0 0 1", indices=computeIndices("bottom", z_hypodermis))
    
    quad=hypodermis.addChild('quad')
    quad.addObject('QuadSetTopologyContainer', name="Q_Container")
    quad.addObject('QuadSetTopologyModifier', name="Q_Modifier")
    quad.addObject('QuadSetGeometryAlgorithms', template="Vec3d", name="Q_GeomAlgo")
    quad.addObject('Hexa2QuadTopologicalMapping', name="default6", input="@../grid", output="@Q_Container")

    tri=quad.addChild('tri')
    tri.addObject('TriangleSetTopologyContainer', name="T_Container")
    tri.addObject('TriangleSetTopologyModifier', name="T_Modifier")
    tri.addObject('TriangleSetGeometryAlgorithms', template="Vec3d", name="T_GeomAlgo")
    tri.addObject('Quad2TriangleTopologicalMapping', name="default8", input="@../Q_Container", output="@T_Container")
    tri.addObject('TriangleCollisionModel', name="SkinCollision", contactStiffness="0.01")

    visu=tri.addChild('visu')
    visu.addObject('OglModel', template="Vec3d", name="Visual", color="1 1 0.4", material="Default Diffuse 1 0 0 1 1 Ambient 1 0 0 0.2 1 Specular 0 0 0 1 1 Emissive 0 0 0 1 1 Shininess 0 45 ")
    visu.addObject('OglViewport', screenPosition="0 0", screenSize="250 250", cameraPosition="-0.285199 -15.2745 16.7859", cameraOrientation="0.394169 0.0120415 0.00490558 0.918946" )
    visu.addObject('IdentityMapping', template="Vec3d,Vec3d", name="default12", input="@..", output="@Visual" )

    
    
    #--------------------- SKIN DERMA LAYER ----------------------#
    derma=root.addChild('derma')
    derma.addObject('EulerImplicitSolver', name="ODE solver", rayleighStiffness="0.01", rayleighMass="0.01")
    derma.addObject('SparseLDLSolver')
    
    derma.addObject('MechanicalObject', template="Vec3d", name="Hexa_D", scale3d="2 1 0.2", position="0 0 -8", showVectors="true", drawMode="2")

    derma.addObject('RegularGridTopology', name="grid", nx=x_vertices, ny=y_vertices, nz=z_derma, xmin="0", xmax=x_length, ymin="0", ymax=y_length, zmin=z_hypodermis, zmax=(z_hypodermis+z_derma+1))
    derma.addObject('HexahedronSetGeometryAlgorithms')
    
    derma.addObject('DiagonalMass', template="Vec3d,double", name="Mass", massDensity="1.0")
    derma.addObject('HexahedronFEMForceField', template="Vec3d", name="FEM", poissonRatio="0.47", youngModulus="2000" )
    derma.addObject('LinearSolverConstraintCorrection')

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
    tri.addObject('TriangleCollisionModel', name="SkinCollision", contactStiffness="0.01")

    visu=tri.addChild('visu')
    visu.addObject('OglModel', template="Vec3d", name="Visual", color="1 1 0.7", material="Default Diffuse 1 0 0 1 1 Ambient 1 0 0 0.2 1 Specular 0 0 0 1 1 Emissive 0 0 0 1 1 Shininess 0 45 ")
    visu.addObject('OglViewport', screenPosition="0 0", screenSize="250 250", cameraPosition="-0.285199 -15.2745 16.7859", cameraOrientation="0.394169 0.0120415 0.00490558 0.918946" )
    visu.addObject('IdentityMapping', template="Vec3d,Vec3d", name="default12", input="@..", output="@Visual" )

    

    #derma.addObject('FixedConstraint', template="Vec3d", name="Fixed Dofs", indices=computeIndices("bottom", z_derma))

    
    #--------------------- SKIN EPIDERMIS LAYER ----------------------#
    epidermis=root.addChild('epidermis')
    epidermis.addObject('EulerImplicitSolver', name="ODE solver", rayleighStiffness="0.01", rayleighMass="0.01")
    epidermis.addObject('CGLinearSolver', iterations="25", name="linear solver", tolerance="1.0e-9", threshold="1.0e-9")
    
    epidermis.addObject('MechanicalObject', template="Vec3d", name="Hexa_E", scale3d="2 1 0.2", position="0 0 -8", showVectors="true", drawMode="2")

    #epidermis.addObject('RegularGridTopology', name="grid", n="5 2 2", min="-5 -5 -10", max="3 4 10", p0="-4 -4 -10")
    epidermis.addObject('RegularGridTopology', name="grid", nx=x_vertices, ny=y_vertices, nz=z_epidermis, xmin="0", xmax=x_length, ymin="0", ymax=y_length, zmin=z_derma+z_hypodermis, zmax=(z_hypodermis+z_derma+z_epidermis+1))
    epidermis.addObject('HexahedronSetGeometryAlgorithms')
    
    epidermis.addObject('DiagonalMass', template="Vec3d,double", name="Mass", massDensity="1.0")
    epidermis.addObject('HexahedronFEMForceField', template="Vec3d", name="FEM", poissonRatio="0.47", youngModulus="2000" )
    epidermis.addObject('LinearSolverConstraintCorrection')

    quad=epidermis.addChild('quad')
    quad.addObject('QuadSetTopologyContainer', name="Q_Container")
    quad.addObject('QuadSetTopologyModifier', name="Q_Modifier")
    quad.addObject('QuadSetGeometryAlgorithms', template="Vec3d", name="Q_GeomAlgo")
    quad.addObject('Hexa2QuadTopologicalMapping', name="default6", input="@../grid", output="@Q_Container")

    tri=quad.addChild('tri')
    tri.addObject('TriangleSetTopologyContainer', name="T_Container")
    tri.addObject('TriangleSetTopologyModifier', name="T_Modifier")
    tri.addObject('TriangleSetGeometryAlgorithms', template="Vec3d", name="T_GeomAlgo")
    tri.addObject('Quad2TriangleTopologicalMapping', name="default8", input="@../Q_Container", output="@T_Container")
    tri.addObject('TriangleCollisionModel', name="SkinCollision", contactStiffness="0.01")

    visu=tri.addChild('visu') #blue->pink, fucsia->
    visu.addObject('OglModel', template="Vec3d", name="Visual", color="1 0.75 0.796", material="Default Diffuse 1 0 0 1 1 Ambient 1 0 0 0.2 1 Specular 0 0 0 1 1 Emissive 0 0 0 1 1 Shininess 0 45 ")
    visu.addObject('OglViewport', screenPosition="0 0", screenSize="250 250", cameraPosition="-0.285199 -15.2745 16.7859", cameraOrientation="0.394169 0.0120415 0.00490558 0.918946" )
    visu.addObject('IdentityMapping', template="Vec3d,Vec3d", name="default12", input="@..", output="@Visual" )

    

    #epidermis.addObject('FixedConstraint', template="Vec3d", name="Fixed Dofs", indices=computeIndices("top", z_epidermis))
    

    #--------------------- ATTACH LAYERS ----------------------#    
    root.addObject('AttachConstraint', object1="@hypodermis", object2="@derma",     indices1=computeIndices("top", z_hypodermis), indices2=computeIndices("bottom", z_derma))
    root.addObject('AttachConstraint', object1="@derma",      object2="@epidermis", indices1=computeIndices("top", z_derma),      indices2=computeIndices("bottom", z_epidermis))
    
    

    return root



if __name__ == '__main__':
    main()
