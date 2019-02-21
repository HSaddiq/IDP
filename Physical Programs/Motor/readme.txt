A class for movement of the robot.

Initialised by typing:
  Movement <name of object>;
 
To move forwards or backwards:
  <name of object>.drive(direction, level, distance);
direction:
  0 - backwards
  1 - forwards
level:
  An interger from 0-255 that sets the speed of the movement.
distance:
  The distance wanted in cm.

To turn on the spot:
  <name of object>.turn(direction, level, angle);
direction:
  0 - right/clockwise
  1 - left/anti-clockwise
level:
  An interger from 0-255 that sets the speed of the movement.
angle:
  The angle desired in degrees.  If more than 360 degrees is wanted, just add that to the angle wanted.
  
Hope you have a pleasant time using this class!  Thanks!
