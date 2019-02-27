# color-face_follower
A little project used to track and follow a color or a face using python and arduino.

A webcamera is attached to a servo motor which is connected to an arduino board. Using python we obtain the footage from the webcamera and process it using opencv in order to extract color information or face. After we detect the desired object, we calculate the center of it in the image and instruct arduino via serial port to move the servo right or left based on the distance of the center of the image from the center of the object.
