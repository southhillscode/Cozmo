#!/usr/bin/env python3
import cozmo
from cozmo.util import degrees, distance_mm

def pickupMyObject(robot: cozmo.robot.Robot):
    
    robot.set_head_angle(degrees(0)).wait_for_completed()
    lookAround = robot.start_behavior(cozmo.behavior.BehaviorTypes.LookAroundInPlace)
    
    #this is how to initialize a variable that equals nothing in python... apparently!
    cube = None
    
    cubes = robot.world.wait_until_observe_num_objects(num=3, object_type=cozmo.objects.LightCube, timeout=60)
    
    cube1 = robot.world.light_cubes.get(cozmo.objects.LightCube1Id)  # paperclip
    cube2 = robot.world.light_cubes.get(cozmo.objects.LightCube2Id)  # lamp
    cube3 = robot.world.light_cubes.get(cozmo.objects.LightCube3Id)  # squiggle

    paperClip = robot.world._objects[cube1.object_id]
    lamp = robot.world._objects[cube2.object_id]
    squiggle = robot.world._objects[cube3.object_id]
    
    lookAround.stop()
    
    if len(cubes) > 1:
    
        putDistanceBetween = robot.go_to_object(paperClip, distance_mm(70.0))
        putDistanceBetween.wait_for_completed()
        
        print("completed, result = %s" % putDistanceBetween)
        pickupTheFirstCube = robot.pickup_object(paperClip)
        pickupTheFirstCube.wait_for_completed()




cozmo.run_program(pickupMyObject)
