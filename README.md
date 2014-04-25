Some demo materials
===================

/arduino contains 3 programs for the Arduino platform.

access.ino
+ Uses an Arduino Uno, GPRS shield and 16*2 character LCD screen
+ The user can call the number of the SIM in the GPRS shield, and if the number that they are calling from matches the hard coded number, the LCD will display "Authorized". Otherwise it will display "Unauthorized".

sms.ino
+ Uses the same hardware as access.ino
+ A user can send an SMS to the number of the SIM in the GPRS shield, and the SMS message will be displayed on the LCD screen.
+ The message will be displayed scrolling across the top line of the LCD screen.

memory.ino
+ Uses an Arduino Uno, 5 red LEDs, each with a corresponding push button, and a green LED.
+ The Arduino will light up the red LEDs in a random sequence, and the player has to push the corresponding buttons in the same sequence after the sequece playback is complete.
+ If the player presses the correct button, the green LED will light to indicate that. If the player presses the incorrect button, all red LEDs light up indicating GAME OVER, MAN! GAME OVER!
+ If the player completes 10 sequences (each longer than the previous), the red LEDS do a Knight Rider-esque pulsing animation, to let the player know that they are the best.

/C contains a command line C program for managing the day to day operation of a computer repair shop.

/JESS contains my solution to an exam question for a course titled Expert Systems / Rule Based Programming

+ Uses the Jess rule engine for Java.
+ A program for determining what a car dealership should do with their used cars.
+ Assert statements evaluate the given car against the defined rules and print what should be done with each car.

/python contains 2 games made with Python using the pygame library

+ pong.py is Pong. W, S, O, and K to move, R to reset.
+ asteroids/asteroids.py is Asteroids. Arrows to move, Z to shoot.
+ asteroids/asteroids_ai.py is also Asteroids, except the player ship is controlled by AI.
+ Require pygame, should run with the built in OSX Mavericks python.

/haskell contains Haskell solutions to Project Euler problems 2, 4 and 6.
+ I have a few more problems solved as well, but the solutions aren't as aesthetically pleasing.