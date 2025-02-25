from myconfig import *

class pixelcolors:
  ledSettings: MyLeds
  captureCard: MyDisplay
  
  pixelStepsY: int
  pixelStepsX: int
  
  startLed: int
  
  def __init__(self, aCaptureCard, aLedSettings):
    self.captureCard = aCaptureCard
    self.ledSettings = aLedSettings  
    
    self.pixelStepsY = int((aCaptureCard.getY() - aCaptureCard.pixelSideOffset*2) / aLedSettings.vertical)
    self.pixelStepsX = int((aCaptureCard.getX() - aCaptureCard.pixelSideOffset*2) / aLedSettings.horizontal)

    self.startLed = 0
    for i in range(aLedSettings.startSide.value):
      self.startLed = self.startLed + self.getLedsPerSide(i)
    if (not aLedSettings.isCounterClockwise):
      self.startLed = self.startLed + self.getLedsPerSide(aLedSettings.startSide)
    
  def getLedsPerSide(self, aSide):
    return self.ledSettings.vertical if (aSide.value % 2 == 0) else self.ledSettings.horizontal

  # This function needs to return the color at a point
  def getPixelColorGenerator(self, aFrame):
    basePixelSideOffset = self.captureCard.pixelSideOffset
    
    for i in range(self.ledSettings.vertical):
      ycoord = self.captureCard.getY() -  basePixelSideOffset - (i * self.pixelStepsY)
      yield self.getCorrectionRGB(aFrame, self.captureCard.getX() - basePixelSideOffset, ycoord)

    for i in range(self.ledSettings.horizontal):
      xcoord = self.captureCard.getX() - basePixelSideOffset - (i * self.pixelStepsX)
      yield self.getCorrectionRGB(aFrame, xcoord, basePixelSideOffset)

    for i in range(self.ledSettings.vertical):
      ycoord =  basePixelSideOffset + (i * self.pixelStepsY)
      yield self.getCorrectionRGB(aFrame, basePixelSideOffset, ycoord)

    for i in range(self.ledSettings.horizontal):
      xcoord = basePixelSideOffset + (i * self.pixelStepsX)
      yield self.getCorrectionRGB(aFrame, xcoord, self.captureCard.getY() - basePixelSideOffset)
  
  # Get pixel color and apply correction filters
  def getCorrectionRGB(self, aFrame, aX, aY):
    b, g, r = aFrame[aY, aX] # [Y,X]
    colorList = [r, g, b]
    for i in range(len(colorList)):
      if colorList[i] < 50:
        colorList[i] = colorList[i] * 0.25   
  
    return int(colorList[0]), int(colorList[1]), int(colorList[2])
  
  def getAdjustedLEDIndex(self, aPixelIndex):
    # if self.ledSettings.isCounterClockwise:
    #   computed = self.startLed + aPixelIndex
    # else:
    #   computed = self.startLed - aPixelIndex
      
    computed = self.startLed + aPixelIndex if self.ledSettings.isCounterClockwise else self.startLed - aPixelIndex
    
    return computed % self.ledSettings.numLeds
