import cv2
import threading
import logging



class Camear_Init(threading.Thread):
    def __init__(self,cam_index:int,frame_height:int,frame_width:int,model:str):
        super().__init__()
        self.cam_index = cam_index
        self.frame_height = frame_height
        self.frame_width = frame_width
        self.model      = model
        self.cap = cv2.VideoCapture(self.cam_index)
        self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, self.frame_width)
        self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, self.frame_height)
        self.video_path = r"C:\Users\12081\Desktop\bike\hu\video\vio_1.mp4"
        if self.model == "video":
            self.cap = cv2.VideoCapture(self.video_path)
            logging.info("video source init")
        elif self.model == "cap":
            logging.info("cap source init")
    
    def read(self):
        if self.model == "video":
           _ret, frame = self.cap.read()
           if not _ret:
               logging.warn("video read error")
               return None
           else:
               logging.info("video frame read")
               frame = cv2.resize(frame,(self.frame_width,self.frame_height))
               return frame
        elif self.model == "cap":
            pass
        else:
            logging.warn("please again")
        

    def release(self):
        self.cap.release()
        logging.info("cap source released")

