import cv2
import logging


logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")


class Camear_Init:
    """Simple capture wrapper. Use model='cap' for camera, 'video' for a video file.

    This class will open the proper VideoCapture depending on model and
    always return None from read() when no frame is available (caller should
    check and avoid calling cv2.imshow on None).
    """

    def __init__(self, cam_index: int = 0, frame_height: int = None, frame_width: int = None, model: str = "cap"):
        self.cam_index = cam_index
        self.frame_height = frame_height
        self.frame_width = frame_width
        self.model = model
        # 默认视频路径（可修改）
        self.video_path = r"C:\Users\12081\Desktop\bike\hu\video\vio_1.mp4"

        # 根据模式选择打开方式
        if self.model == "video":
            self.cap = cv2.VideoCapture(self.video_path)
        else:
            # cap 模式：打开摄像头索引
            self.cap = cv2.VideoCapture(self.cam_index)

        # 尝试设置分辨率（某些摄像头支持）
        try:
            if self.frame_width:
                self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, int(self.frame_width))
            if self.frame_height:
                self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, int(self.frame_height))
        except Exception:
            logging.exception("Failed to set capture properties")

    def read(self):
        """Read a frame. Returns resized frame or None if failed."""
        if not self.cap or not self.cap.isOpened():
            logging.warning("capture not opened for model=%s", self.model)
            return None

        ret, frame = self.cap.read()
        if not ret or frame is None:
            logging.warning("frame read error for model=%s", self.model)
            return None

        # 如果指定了目标大小，做 resize 以保证输出尺寸一致
        if self.frame_width and self.frame_height:
            try:
                h, w = frame.shape[:2]
                if (w != self.frame_width) or (h != self.frame_height):
                    frame = cv2.resize(frame, (self.frame_width, self.frame_height))
            except Exception:
                logging.exception("Failed to resize frame")

        return frame

    def release(self):
        try:
            if self.cap:
                self.cap.release()
                logging.info("cap source released")
        except Exception:
            logging.exception("error releasing cap")
