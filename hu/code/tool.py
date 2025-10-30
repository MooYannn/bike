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
    edges = cv2.Canny(warp_img, 50, 40,apertureSize=3)
    edges_mask = np.zeros((img_size[1],img_size[0]), dtype=np.uint8)
    cv2.rectangle(edges_mask, (160,0),(480,480), 255, -1)
    edges = cv2.bitwise_and(edges, edges,mask=edges_mask)
    return edges

def lane_multiple(edges):
    # 1. 形态学操作：先膨胀填充缝隙，再腐蚀去除小噪点（调整迭代次数平衡）
    # 膨胀迭代次数减少，避免过度扩张引入噪声；腐蚀迭代次数增加，强化去噪
    kernel = np.ones((3, 3), np.uint8)
    _strength = cv2.dilate(edges, kernel, iterations=2)  # 原iterations=3→2（减少过度膨胀）
    _strength = cv2.erode(_strength, kernel, iterations=2)  # 原iterations=1→2（增强去噪）
    
    # 2. 高斯模糊：增大核尺寸增强平滑（保留边缘同时去噪）
    _strength = cv2.GaussianBlur(_strength, (7, 7), 0)  # 原(5,5)→(7,7)（更强模糊）
    
    # 3. 中值滤波：进一步去除椒盐噪声（核尺寸保持奇数，增强平滑）
    _lanes = cv2.medianBlur(_strength, 7)  # 原5→7（更适合去噪）
    
    # 4. 自适应阈值：调整块大小和常数，减少噪声干扰
    # 块大小增大（更稳定），常数减小（更容易保留弱边缘）
    _lanes = cv2.adaptiveThreshold(
        _lanes,
        255,
        cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
        cv2.THRESH_BINARY_INV,
        11,  # 原7→11（块大小增大，抗噪更稳定）
        3    # 原5→3（减小常数，保留更多有效边缘）
    )
    return _lanes



def least_squares_fit(lines):
    if not lines:
        return None
    all_x = []
    all_y = []
    for line in lines:
        x1, y1, x2, y2 = line[0]
        all_x.extend([x1, x2])
        all_y.extend([y1, y2])
    
    all_x = np.array(all_x)
    all_y = np.array(all_y)
    if len(all_x) < 2:
        return None
    try:
        # 拟合一次多项式 y = mx + b
        m, b = np.polyfit(all_x, all_y, 1)
        return m, b
    except np.linalg.LinAlgError:
        return None
    


def find_lane(edges_img,show_img):
    lines = cv2.HoughLinesP(edges_img, 
                            1,
                            np.pi / 180,
                            15, 
                            minLineLength=80,
                            maxLineGap=20
    )
    for _lane in lines:
        x1, y1, x2, y2 = _lane[0]
        cv2.line(show_img, (x1, y1), (x2, y2), (0, 0, 255), 2)
    if lines is None:
        return None, None
    
    # 1. 扁平化 lines 结构
    flat_lines = lines.reshape(-1, 4) 
    lines_list = [[[x1, y1, x2, y2]] for x1, y1, x2, y2 in flat_lines]

    return lines_list



def lane_process(edges_img):
    line_list = find_lane(edges_img=edges_img)
    lane_params = least_squares_fit(line_list)
    return lane_params  


def draw_lines(img, lane_params):
    if lane_params is None:
        return img
    print("-----",lane_params)
    m, b = lane_params
    y1 = img.shape[0]
    y2 = int(y1 * 0.6)
    x1 = int((y1 - b) / m)
    x2 = int((y2 - b) / m)
    cv2.line(img, (x1, y1), (x2, y2), (0, 255, 0), 5)
    return img