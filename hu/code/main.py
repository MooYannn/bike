import cv2
import sys
import cap_init
import logging

class ALL_INIT():
    def __init__(self):
        self.model = sys.argv[1]
        self.camera = cap_init.Camear_Init(0, frame_height=480, frame_width=640, model=self.model)

    def start(self):
        self.frame = self.camera.read()
        cv2.imshow("frame", self.frame)
        cv2.waitKey(1)


if __name__ == "__main__":
    all_init = ALL_INIT()
    while True:
        try:
            all_init.start()
        except KeyboardInterrupt:
            all_init.camera.release()
            cv2.destroyAllWindows()
            break
        finally:
            logging.info("program end")
        

