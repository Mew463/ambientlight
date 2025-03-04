import cv2

def list_cameras():
    available_cameras = []
    for i in range(10):  # Check up to 10 possible camera indices
        cap = cv2.VideoCapture(i)
        if cap.read()[0]:
            available_cameras.append(i)
        cap.release()
    
    return available_cameras

print("Available cameras:", list_cameras())
