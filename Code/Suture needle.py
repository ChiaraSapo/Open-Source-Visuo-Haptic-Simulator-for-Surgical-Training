
    # Needle model found at https://drive.google.com/drive/folders/1vSpPHsdLy5iyegFA8Qa1roHtjZ-NivXJ
    
    #####################################################
    #--------------------- NEEDLE ----------------------#
    #####################################################   
    needleNode = root.addChild('Needle')

    needleNode.addObject('EulerImplicitSolver', name='ODE solver', rayleighStiffness="0.01", rayleighMass="1.0")
    needleNode.addObject('CGLinearSolver', name='linear solver', iterations="25", tolerance="1e-7", threshold="1e-7")
    needleNode.addObject('MechanicalObject', name='mechObject', template='Rigid3d', 
                            position="0 0 10", scale3d=[1.2*scale, scale, scale])
    needleNode.addObject('UniformMass', name='mass', totalMass="1")
    needleNode.addObject('UncoupledConstraintCorrection')

    # Visual node
    needleVisNode = needleNode.addChild('VisualModel')

    needleVisNode.addObject('MeshObjLoader', name='instrumentMeshLoader', filename="mesh/suture_needle.obj")
    needleVisNode.addObject('OglModel', name='InstrumentVisualModel', src='@instrumentMeshLoader', 
                                dy="0", scale3d=[1.2*scale, scale, scale])
    needleVisNode.addObject('RigidMapping', name='MM-VM mapping', input='@../mechObject', output='@InstrumentVisualModel')

    # Collision node
    needleColNode = needleNode.addChild('CollisionModel')

    needleColNode.addObject('MeshObjLoader', filename="mesh/suture_needle.obj", name='loader')
    needleColNode.addObject('MeshTopology', src='@loader', name='InstrumentCollisionModel')
    needleColNode.addObject('MechanicalObject', src='@InstrumentCollisionModel', name='instrumentCollisionState', 
                                dy="0", scale3d=[1.2*scale, scale, scale])
    needleColNode.addObject('RigidMapping', name='MM-CM mapping', input='@../mechObject', output='@instrumentCollisionState')

    #needleColNode.addObject('TriangleCollisionModel', name='instrumentTriangle', contactStiffness=10, contactFriction=10)
    needleColNode.addObject('LineCollisionModel', name='instrumentLine', contactStiffness=10, contactFriction=10)
    needleColNode.addObject('PointCollisionModel', name='instrumentPoint', contactStiffness="10", contactFriction="10")
    
