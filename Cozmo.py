import sys
import time
from enum import *
import cozmo
from cozmo.util import degrees, distance_mm, speed_mmps
from Triggers import *

# Log Error
def error(message):
    print("*********************ERROR:", message)

# Enumerations
class Direction(IntEnum):
    '''Driving direction.'''
    forward = 1
    backward = -1

class Speed(IntEnum):
    '''Driving speed.'''
    normal = 1
    fast = 2

# Cubes
cube1ID = cozmo.objects.LightCube1Id # paperclip
cube2ID = cozmo.objects.LightCube2Id # lamp
cube3ID = cozmo.objects.LightCube3Id # dot
cubeIDs = [cube1ID, cube2ID, cube3ID] # [1, 2, 3]

# Colors
def lightLevel(level):
    return int(level * 255.0)

def lightColor(r: float, g: float, b: float):
    return cozmo.lights.Color(rgb=(lightLevel(r),
        lightLevel(g), lightLevel(b)))

def light(color):
    return cozmo.lights.Light(color)

class Cube:
    def __init__(self, cube):
        self.cube = cube

    def setColor(self, color):
        self.cube.set_lights(light(color))

    def switchOff(self):
        self.cube.set_lights(cozmo.lights.off_light)

    def waitForTap(self, seconds = 3):
        try:
            self.cube.wait_for_tap(timeout = seconds)
            return True
        except:
            print("cube tap timed out")
        return False
            
    def getCubePosition(self):
        return self.cube.pose

    def getCubeId(self):
        cube_object_id = self.world.light_cubes.get(cozmo.objects.LightCube1Id).object_id

        return cube_object_id

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

    def cube(self, idx):
        return Cube(self.robot.world.light_cubes.get(cubeIDs[idx]))
    
    def moveHeadUpAndDown(self, myDegrees = 0):
        self.robot.move_head(myDegrees)
        self.robot.move_head(15)
    
    def turnInPlace(self, myDegrees = 0):
        return self.robot.turn_in_place(degrees(myDegrees)).wait_for_completed()
    
    def wait(self, sleepTime):
        time.sleep(sleepTime)
    
    def changeBackPackColor(self, myColor):
        if myColor == "red":
            self.robot.set_all_backpack_lights(cozmo.lights.red_light)
        elif myColor == "blue":
            self.robot.set_all_backpack_lights(cozmo.lights.blue_light)
        else:
            self.robot.set_all_backpack_lights(cozmo.lights.green_light)

    def driveCozmo(self, myDistance):
         self.robot.drive_straight(distance_mm(myDistance),speed_mmps(30000)).wait_for_completed()
    
    def say(self, text):
        '''Instruct cozmo to speak text.'''
        speak = self.robot.say_text(text)
        speak.wait_for_completed()

    def drive(self,
              time = 3,
              direction: Direction = Direction.forward,
              speed: Speed = Speed.normal):
        '''Drive cozmo for `time` seconds  in `direction` at `speed`'''
        goSpeed = float(direction) * float(speed) * 50
        print(str(goSpeed))
        self.robot.drive_wheels(goSpeed, goSpeed, duration = time)

    def turn(self, degrees = 180):
        '''Turn cozmo for n degrees'''
        rotation = self.robot.turn_in_place(cozmo.util.degrees(degrees))
        rotation.wait_for_completed()
    
    def moveForward(goNow = 100):
        self.robot.Forward(goNow).now()
    
    # Behaviors
    
    def stopBehavior(self):
        if self.currentBehavior == "idle":
            return
        self.currentBehavior.stop()
        self.currentBehavior = "idle"
    
    def findFaces(self):
        self.currentBehavior = self.robot.start_behavior(self.behaviors.FindFaces)

    def knockOverCubes(self):
        self.currentBehavior = self.robot.start_behavior(self.behaviors.KnockOverCubes)

    def lookAroundInPlace(self):
        self.currentBehavior = self.robot.start_behavior(self.behaviors.LookAroundInPlace)
    
    def pounceOnMotion(self):
        self.currentBehavior = self.robot.start_behavior(self.behaviors.PounceOnMotion)
    
    def rollBlock(self):
        self.currentBehavior = self.robot.start_behavior(self.behaviors.RollBlock)

    def stackBlocks(self):
        self.currentBehavior = self.robot.start_behavior(self.behaviors.StackBlocks)
    
    def findACube(self):
        self.lookAroundInPlace()
        try:
            cube = self.robot.world.wait_for_observed_light_cube(timeout=30)
            self.stopBehavior()
            self.activeCube = cube
            self.cubes = [cube]
            return True
        except:
            self.activeCube = "no cube"
            self.cubes = []
            self.stopBehavior()
            return False

    def findCubes(self, count):
        self.lookAroundInPlace()
        self.cubes = self.robot.world.wait_until_observe_num_objects(num=count, object_type=cozmo.objects.LightCube, timeout=60)
        self.stopBehavior()
        return self.cubes
    
    def countCubes(self):
        count = len(self.cubes)
        responses = { 0 : "No cubes", 1 : "One cube", 2 : "Two cubes", 3 : "Three Cubes" }
        response = responses[count]
        self.say(response)

    def pickupCube(idx):
        if idx < len(self.cubes):
            self.robot.pickup_object(self.cubes[idx]).wait_for_completed()
        else:
            error("Bad cube idx " + str(idx))

    def takeCube(self):
        if self.activeCube == "no cube":
            error("No cube")
            self.say("No cube")
        self.robot.pickup_object(self.activeCube).wait_for_completed()

    def dropCube(self):
        if self.activeCube == "no cube":
            error("No cube")
            self.say("No cube")
        self.robot.place_object_on_ground_here(self.activeCube).wait_for_completed()

    # Triggered Animations
    
   
    #Not Needed
    def trigger(self, triggerName):
        if triggerName in triggerActions:
            theTrigger = getTrigger(triggerName)
            try:
                anim = self.robot.play_anim_trigger(theTrigger)
                anim.wait_for_completed()
            except:
                error("problem during anim")

    def celebrate(self):
        self.trigger("MajorWin")

