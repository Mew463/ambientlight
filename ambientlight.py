import cv2
import rpi_ws281x as ws
import time
from myconfig import *
from pixelcolors import *

captureCard = MyDisplay(resolution = (640, 480), pixelSideOffset = 20, colorOffset = [0,0,0])
ledSettings = MyLeds(horizontal = 56, vertical = 34, gpio_pin = 18, startSide = Sides.RIGHT, isCounterClockwise = True)
pixelHandler = pixelcolors(captureCard, ledSettings)

strip = ws.PixelStrip(ledSettings.numLeds, ledSettings.gpio_pin)
strip.begin()

for i in range(ledSettings.numLeds):
    strip.setPixelColor(i, ws.Color(0, 0, 0))
strip.show()

# Open the default camera (0)
cap = cv2.VideoCapture(0)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, captureCard.getX())
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, captureCard.getY())

# Check if the camera opened successfully
if not cap.isOpened():
    print("Error: Could not open camera.")
    exit()

while True:
    returnValue, frame = cap.read()

    if not returnValue:
      print("Error: Failed to capture image.")
      break
      
    frame = cv2.blur(frame, (30, 30))
    # cv2.imshow('Camera Feed', frame)
    # if cv2.waitKey(1) & 0xFF == ord('q'):
    #     break
    
    theRgbGenerator = pixelHandler.getPixelColorGenerator(frame)

    for thePixelIndex, (theR, theG, theB) in enumerate(theRgbGenerator):
        strip.setPixelColor(pixelHandler.getAdjustedLEDIndex(thePixelIndex), ws.Color(theR, theG, theB))

    strip.show()

# Release the camera and close windows
cap.release()
cv2.destroyAllWindows()

