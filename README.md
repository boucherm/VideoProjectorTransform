# VideoProjector transform estimator

## vph.py

  A simple python script to estimate the transform ( homography ) that would allow to undistort the image of a video projector not frontoparallel to the screen.
  It was written to be used with `xrandr --transform`.
  I've still not completely figured out how to use `xrandr --transform` properly.
  Two issues are:
  1. The appropriate frame buffer (`--fb WidthxHeight`) size eludes me, if you are lucky `xrandr` will tell you which value it expects
  2. Some "borders" of the screen are missing. This may be linked to the previous issue ( current guess: the translation values may be slightly off ).


  How it works / how to use:

  It displays four blue circles linked by green edges.
  These blue circles and green frame are to be used to point out how the image should be transformed.
  At start, circles are placed at the corners of the screen.
  The green frame would be a distorted rectangle if your video-projector is not fronto-parallel to the screen.
  Using the mouse grab the corners and move them so that the frame becomes rectangular ( i.e. to cancel the distortion ).
  Press `Enter`.
  The estimated frame buffer size and homography values will be displayed on the terminal.
  Use it to feed `xrandr`.
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


## Resetting xrandr

  To properly reset call `xrandr --output THE_OUTPUT --fb Screen_widthxScreen_height --transform none`.

  You should probably try this command, and make sure it doesn't fail, before any other call to `xrandr`.
