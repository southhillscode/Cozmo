#!/usr/bin/env python3

from Cozmo import *
from Colors import *

# Run, Cozmo, run
def actions(cozmoLink):
    '''Specify actions for cozmo to run.'''
    
    # Fetch robot
    coz = Cozmo.robot(cozmoLink)
    
    # Say something
    coz.say("Hello")
    
    # Drive a little
    coz.drive(time = 3, direction = Direction.forward)
    
    # Turn
    coz.turn(degrees = 180)
    
    # Drive a little more
    coz.drive(time = 3, direction = Direction.forward)
    
    # Light up a cube
    cube = coz.cube(0)
    cube.setColor(colorLime)
    cube1 = coz.cube(1)
    cube1.setColor(colorTurquoise)
    cube2 = coz.cube(2)
    cube2.setColor(colorPurple)
    
    # Tap it!
    coz.say("Tap it")
    if cube.waitForTap():
        coz.say("It's about time")
    else:
        coz.say("Why no tap?")
            #cube.switchOff()

    # Count Cubes
    coz.driveCozmo(150)
    coz.turnInPlace(90)
    coz.moveHeadUpAndDown(-5)
    myPosition = cube1.getCubePosition()
    print(str(myPosition))
    coz.changeBackPackColor("blue")
    coz.trigger("DriveStartAngry")
    coz.celebrate()

Cozmo.startUp(actions)
