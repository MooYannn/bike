import cv2
import argparse
import logging
import cap_init


logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")


class ALL_INIT:
    def __init__(self, model: str = "cap", source=None):
        # source is ignored for now in Camear_Init (it uses an internal default path for video)
        self.model = model
        # 如果是 video 模式且传入了 source（路径），把 source 传入 Camear_Init
        cam_arg = 0
        if self.model == "video" and source:
            cam_arg = source
        self.camera = cap_init.Camear_Init(cam_arg, frame_height=480, frame_width=640, model=self.model)

    def start(self):
        frame = self.camera.read()
        if frame is None:
            logging.warning("No frame available; stopping")
            return False
        cv2.imshow("frame", frame)
        # allow quitting by pressing 'q'
        if cv2.waitKey(1) & 0xFF == ord('q'):
            return False
        return True


def parse_args():
    p = argparse.ArgumentParser()
    p.add_argument("--model", choices=["cap", "video"], default="cap", help="选择数据源模式")
    p.add_argument("--source", help="可选的视频文件路径或摄像头索引")
    return p.parse_args()


if __name__ == "__main__":
    args = parse_args()
    all_init = ALL_INIT(model=args.model, source=args.source)
    try:
        while True:
            ok = all_init.start()
            if not ok:
                break
    except KeyboardInterrupt:
        logging.info("KeyboardInterrupt received, exiting")
    finally:
        try:
            all_init.camera.release()
        except Exception:
            logging.exception("Error releasing camera")
        cv2.destroyAllWindows()
        logging.info("program end")
        

