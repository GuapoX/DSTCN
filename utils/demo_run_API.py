import cv2
import detect_with_API
import torch

# cap = cv2.VideoCapture('D:/video/7_25_yun_1.2/7_25_1.mp4')  # 0
# a = detect_with_API.detectapi(weights='best.pt')
#
# fourcc = cv2.VideoWriter_fourcc('m','p','4','v')  # 视频编解码器
# fps = cap.get(cv2.CAP_PROP_FPS)  # 帧数
# width, height = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH)), int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))  # 宽高
# out = cv2.VideoWriter('D:/video/725cloud.mp4', fourcc, fps, (width, height))  # 写入视频


if __name__ == '__main__':
    #with torch.no_grad():
    while True:
        rec, img = cap.read()
        if rec == True:
            result, names = a.detect([img])
            img = result[0][0]  # 每一帧图片的处理结果图片
            # 每一帧图像的识别结果（可包含多个物体）
            for cls, (x1, y1, x2, y2), conf in result[0][1]:
                print(names[cls], x1, y1, x2, y2, conf)  # 识别物体种类、左上角x坐标、左上角y轴坐标、右下角x轴坐标、右下角y轴坐标，置信度
                '''
                cv2.rectangle(img,(x1,y1),(x2,y2),(0,255,0))
                cv2.putText(img,names[cls],(x1,y1-20),cv2.FONT_HERSHEY_DUPLEX,1.5,(255,0,0))'''
            print()  # 将每一帧的结果输出分开
            out.write(img)
            cv2.imshow("video", img)
        if not rec:
            break  # 当获取完最后一帧就结束



    # 释放资源
    cap.release()
    out.release()
    # 关闭窗口
    cv2.destroyAllWindows()