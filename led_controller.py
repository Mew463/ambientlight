import cv2
import rpi_ws281x as ws
import time
from myconfig import *
from pixelcolors import *
import asyncio

class led_controller:
    def __init__(self):
        
        self.captureCard = MyDisplay(resolution = (640, 480), pixelSideOffset = 20, colorOffset = [0,0,0])
        self.ledSettings = MyLeds(horizontal = 56, vertical = 34, gpio_pin = 18, startSide = Sides.RIGHT, isCounterClockwise = True)
        self.pixelHandler = pixelcolors(self.captureCard, self.ledSettings)
        self.strip = ws.PixelStrip(self.ledSettings.numLeds, self.ledSettings.gpio_pin)
        self.cap = None 
        self.running = True
    
        self.strip.begin()
        self.setRGBColor(0,0,0) # Initalize to all black leds
        
    def closeCamera(self):
        self.cap.release() # Release the camera
    
    def setRGBColor(self, aRed, aGreen, aBlue):
        for i in range(self.ledSettings.numLeds):
            self.strip.setPixelColor(i, ws.Color(aRed, aGreen, aBlue))
        self.strip.show()

    def openCamera(self):
        # Open the default camera (0)
        self.cap = cv2.VideoCapture(0)
        self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, self.captureCard.getX())
        self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, self.captureCard.getY())

        # Check if the camera opened successfully
        if not self.cap.isOpened():
            print("Error: Could not open camera.")
            exit()
    
    async def ambientLightHandler(self):
        while self.running:
            returnValue, frame = self.cap.read()

            if not returnValue:
                print("Error: Failed to capture image.")
                break
            
            frame = cv2.blur(frame, (30, 30))
            
            theRgbGenerator = self.pixelHandler.getPixelColorGenerator(frame)

            for thePixelIndex, (theR, theG, theB) in enumerate(theRgbGenerator):
                self.strip.setPixelColor(self.pixelHandler.getAdjustedLEDIndex(thePixelIndex), ws.Color(theR, theG, theB))

            self.strip.show()
            
            # await asyncio.sleep(0.005) # Uh oh, I hope I dont need this line
            
    async def startAmbientLight(self):
        self.openCamera()
        self.running = True
        asyncio.create_task(self.ambientLightHandler())
        
    def stopAmbientLight(self):
        self.running = False
        self.closeCamera()
        
async def main():
    aLedController = led_controller()
    await aLedController.startAmbientLight()
    await asyncio.sleep(20)
    aLedController.stopAmbientLight()

asyncio.run(main())

