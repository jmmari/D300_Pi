# D300_Pi

These codes allow to easily use the LDROBOT D300 LiDar with a Raspberry Pi.

It uses the linux sdk from LDROBOTS: https://github.com/ldrobotSensorTeam/ldlidar_stl_sdk/tree/master

Unzip the SDK in the same folder. The current build is for RP4. If you want to use it on another Pi, 
re-build using command "./auto_build.sh"

You have Bash scripts and Python scripts to start with.

Plug the D300 with its USB adpater, and run the scripts (the settings are not modifiable, they are set by the SDK program) !

You can: 
- run the D300 and get the values
- run the D300 and save values to a file
- run the D300 and plot the points (Python, slow).


