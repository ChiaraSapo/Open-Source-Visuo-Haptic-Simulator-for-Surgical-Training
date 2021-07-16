# Required import for python
import Sofa
import numpy as np
import Sofa.SofaDeformable

# Choose in your script to activate or not the GUI
USE_GUI = True



def main():
    import SofaRuntime
    import Sofa.Gui
    import Sofa.Core
    #import Sofa.SofaDeformable
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



def createScene(root):
    root.addObject('RequiredPlugin', pluginName="SofaBaseMechanics SofaBaseTopology SofaDeformable")
    root.addChild('plane_1')
    root.plane_1.addObject('RegularGridTopology', name='grid', min=[-0.5, -1.5, -1.5], max=[-0.5, 1.5, 1.5], n=[1, 3, 3])
    root.plane_1.addObject('MechanicalObject', name='mo', template="Vec3d", position='@grid.position')

    # Create a simple plane having 3x3 nodes and a size of 3x3 on the yz plane centered on (0.5,0,0).
    root.addChild('plane_2')
    root.plane_2.addObject('RegularGridTopology', name='grid', min=[0.5, -1.5, -1.5], max=[0.5, 1.5, 1.5], n=[1, 3, 3])
    root.plane_2.addObject('MechanicalObject', name='mo', template="Vec3d", position='@grid.position')
    
    # Create a StiffSpringForceField between the two planes: works but no modifications can be made (no error, no succeeding)
    # spring_force_field2=root.addObject(
    #     'StiffSpringForceField',
    #     template='Vec3d',
    #     name='spring_ff',
    #     object1=root.plane_1.mo.getLinkPath(),
    #     object2=root.plane_2.mo.getLinkPath(),
    #     indices1=list(range(8)),
    #     indices2=list(range(8)),
    #     stiffness=1,
    #     damping=0,
    #     length=1.
    # )

    # Create a StiffSpringForceField between the two planes: works and supports modifications
    #Sofa.SofaDeformable
    spring_force_field2 = root.addObject("StiffSpringForceField",object1=root.plane_1.mo.getLinkPath(),  object2=root.plane_2.mo.getLinkPath())
    springs2 = [Sofa.SofaDeformable.LinearSpring(index1=i, index2=i, springStiffness=100, dampingFactor=5, restLength=1) for i in range(8)]
    spring_force_field2.addSprings(springs2)
    
    add=0
    
    if add==0:
        print("Remove spring")
        spring_force_field2.removeSpring(0)
    if add==1:
        print("Add spring")
        spring = [Sofa.SofaDeformable.LinearSpring(index1=8, index2=8, springStiffness=1, dampingFactor=0, restLength=1)] #works with [] only
        spring_force_field2.addSprings(spring)
    
    return root



if __name__ == '__main__':
    main()
