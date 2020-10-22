# VideoProjector transform estimator

A simple python script to estimate the transform ( homography ) that would allow to undistort the image of a video projector not frontoparallel to the screen.
It was written to be used with `xrandr --transform`.
Unfortunately, I can't get it ( `xrandr --transform`) to work properly.
Maybe you'll be more lucky than me ( please tell if so ).


How it works:

It displays four corners ( blue circles ) linked by green edges.
In the beginning they are placed at the corners of the (distorted) screen.
With the mouse grab the corners and move them so that the parallelogram gets rectangular ( i.e. to cancel the distortion ).
Press `Enter`.
The estimated homography, and its inverse, will be display on the terminal.
Use one or the other ( I'm not sure which, as I can't get `xrandr --transform` to work properly ) to feed to `xrandr`.
The frame of latest estimated "configuration" is displayed in magenta-ish.
This is in case you want to improve upon it.
Press `Esc` or `q` to quit.


Dependencies: python3, pygame, numpy, a terminal
