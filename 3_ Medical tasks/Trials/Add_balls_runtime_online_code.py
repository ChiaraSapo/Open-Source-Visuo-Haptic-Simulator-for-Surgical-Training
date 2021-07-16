import Sofa
import Sofa.Simulation

def Marker(rootNode, name, pose):

    marker = rootNode.addChild(name)
    marker.addObject(
        "MechanicalObject", name="MechanicalModel", template="Rigid3", position=pose
    )

    visual = marker.addChild("VisualModel")

    visual.loader = visual.addObject(
        "MeshObjLoader",
        handleSeams="1",
        name="VisualMeshLoader",
        scale=1,
        filename="mesh/ball.obj",
    )

    visual.addObject(
        "OglModel", src="@VisualMeshLoader", name="VisualModel", color=[1, 1, 1]
    )

    visual.addObject(
        "RigidMapping",
        input="@../MechanicalModel",
        name="MM->VM mapping",
        output="@VisualModel",
    )
    print(f"Created {visual} with name {name}!")
    
    marker.init()
    Sofa.Simulation.initVisual(marker)
    print(visual.VisualModel.texcoords.value)
    triangles = visual.VisualModel.triangles.value
    blue_triangles = [0, 4, 9] # indices of triangles that must be blue
    blue_nodes = triangles[blue_triangles]
    blue_coordinates = [0.7, 0.9] # coordinates of a blue pixel in the texture image
    with visual.VisualModel.texcoords.writeableArray() as wa:
        wa[blue_nodes] = blue_coordinates    
    return marker
    
class Controller(Sofa.Core.Controller):

    def __init__(self):
        Sofa.Core.Controller.__init__(self)
        self.count = 0
        
    def onAnimateBeginEvent(self, e):
        Marker(self.getContext(), f'marker_{self.count}', [self.count*2, 0, 0, 0, 0, 0, 1])
        self.count+=1
    
def createScene(root):
    root.bbox = [[-1, -1, -1], [1, 1, 1]]
    root.addObject(Controller())