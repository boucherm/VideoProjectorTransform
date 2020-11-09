# VideoProjector transform estimator

## vph.py

  A simple python script to estimate the transform ( homography ) that would allow to undistort the image of a video projector not frontoparallel to the screen.
  It was written to be used with `xrandr --transform`.
  Unfortunately, I haven't yet figured out how to use `xrandr --transform` properly.
  Would you get more lucky than me please tell me.


  How it works / how to use:

  It displays four blue circles linked by green edges.
  These blue circles and green frame are to be used to point out how the image should be transformed.
  At start, circles are placed at the corners of the screen.
  The green frame would be a distorted rectangle if your video-projector is not fronto-parallel to the screen.
  Using the mouse grab the corners and move them so that the frame becomes rectangular ( i.e. to cancel the distortion ).
  Press `Enter`.
  The estimated homography will be displayed on the terminal.
  Use it to feed `xrandr --transform` ( again, I haven't figured out how to use it properly ).
  The frame of latest estimated "configuration" is displayed in magenta-ish.
  This is in case you want to improve upon it.
  Press `Esc` or `q` to quit.


  Dependencies: python3, pygame, numpy, a terminal


## check.py

  This script can be used to check the estimated transform by `vph.py`.
  It requires to have an image in the folder named `img.png`.
  The image should be a screenshot of the whole screen.
  You can use `gimp` to snap one.
  Just run the script.


  Dependencies: python3, OpenCV, numpy, a terminal

