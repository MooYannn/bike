import cv2
import numpy as np

def ract_imp_para():
    #以下参数需要根据摄像头安装位置和角度自行调整
    objdx = 210
    objdy = 420
    imgdx = 220
    imgdy = 250
    list_pst = [[170, 260], [465, 260], [75, 470], [545, 470]]
    pts1 = np.float32(list_pst)
    pts2 = np.float32([[imgdx, imgdy], [imgdx + objdx, imgdy],
    [imgdx, imgdy + objdy], [imgdx + objdx, imgdy + objdy]])
    M = cv2.getPerspectiveTransform(pts1, pts2)
    return M

def img_preprocess(img):
    img_size = (640, 480)
    #img 是摄像头获取的原图像
    img = cv2.medianBlur(img, 9)
    #进行逆透视操作
    M = ract_imp_para()
    warp_img = cv2.warpPerspective(img, M, img_size)
    # edges = cv2.Canny(warp_img, 50, 40, apertureSize=3)
    # # 遮罩
    # edges_mask = np.zeros((img_size[1], img_size[0]),
    # dtype=np.uint8)
    # cv2.rectangle(edges_mask, (160, 0), (480, 480), 255,
    # thickness=cv2.FILLED)
    # edges = cv2.bitwise_and(edges, edges, mask=edges_mask)
    return warp_img

#方法1用于分离图像的BGR通道
def channel_split(img):
    #分离BGR通道
    pass


#方法2用于将图像从BGR颜色空间转换为HSV颜色空间
def hsv_split(img):
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    h, s, v = cv2.split(hsv)
    return h, s, v


#使用灰度图像和阈值自适应
def gray_scale(img):
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    return gray