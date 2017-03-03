#!/usr/bin/env python3
import cozmo
from cozmo.util import degrees, distance_mm

class cubeObjects:
    
    def pickupMyObject(self):
                
        self.set_head_angle(degrees(0)).wait_for_completed()
        lookAround = self.start_behavior(cozmo.behavior.BehaviorTypes.LookAroundInPlace)
                        
        #this is how to initialize a variable that equals nothing in python... apparently!
        cube = None
                            
        cubes = self.world.wait_until_observe_num_objects(num=3, object_type=cozmo.objects.LightCube, timeout=60)
                                
                      
                                
        lookAround.stop()
        
        
        cube1 = robot.world.light_cubes.get(cozmo.objects.LightCube1Id)  # paperclip
        cube2 = robot.world.light_cubes.get(cozmo.objects.LightCube2Id)  # lamp
        cube3 = robot.world.light_cubes.get(cozmo.objects.LightCube3Id)  # squiggle
        
        paperClip = robot.world._objects[cube1.object_id]
        lamp = robot.world._objects[cube2.object_id]
        squiggle = robot.world._objects[cube3.object_id]
        
        self.paperClip = paperClip
        self.lamp = lamp
        self.squiggle = squiggle

        
        
        putDistanceBetween = self.go_to_object(paperClip, distance_mm(70.0))
        putDistanceBetween.wait_for_completed()
                                            
        print("completed, result = %s" % putDistanceBetween)
        pickupTheFirstCube = self.pickup_object(paperClip)
        pickupTheFirstCube.wait_for_completed()
                                                        
        placeTheFirstCubeOnTop = self.place_object_on_ground_here(theObject)
        placeTheFirstCubeOnTop.wait_for_completed()



class Cozmo:
    def __init__(self, robot):
        self.robot = robot
        self.world = robot.world
        self.behaviors = cozmo.behavior.BehaviorTypes
        self.currentBehavior = "idle"
        self.activeCube = "no cube"
        print(self.robot.pose)
        self.cubes = []
    
    @classmethod
    def startUp(self, mainFunction):
        '''Initialize basic logging and make connection'''
        cozmo.setup_basic_logging()
        try:
            cozmo.connect(mainFunction)
        except cozmo.ConnectionError as err:
            sys.exit("Connection error: %s" % err)

    @classmethod
    def robot(self, sdk_conn):
        '''Fetch robot instance'''
        return Cozmo(sdk_conn.wait_for_robot())




cozmo.run_program(cubeObjects.pickupMyObject)
