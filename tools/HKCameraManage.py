#!/usr/bin/env python
# coding:utf8
"""
@Time       :   2019/12/9
@Author     :   fls
@Contact    :   fls@darkripples.com
@Desc       :   海康威视网络摄像头

@Modify Time      @Author    @Version    @Desciption
------------      -------    --------    -----------
2019/12/9 10:53   fls        1.0         create
"""
from os import path, makedirs
from cv2 import (VideoCapture, imencode, namedWindow, imshow, waitKey, destroyAllWindows, VideoWriter_fourcc,
                 VideoWriter, WINDOW_NORMAL, WINDOW_KEEPRATIO, CAP_PROP_FRAME_WIDTH, CAP_PROP_FRAME_HEIGHT,
                 CAP_PROP_FPS)
from time import time
from ez_utils import fmt_date, FMT_DATE, FMT_DATETIME

BASE_DIR = path.dirname(path.dirname(path.abspath(__file__)))


def consoleLog(*args):
    print(*args)


class HKCManage:
    def __init__(self, place, ip, port, user, pwd, logPre=">"):
        """
        主码流：
            rtsp://admin:12345@192.0.0.64:554/h264/ch1/main/av_stream
            rtsp://admin:12345@192.0.0.64:554/MPEG-4/ch1/main/av_stream
        子码流：
            rtsp://admin:12345@192.0.0.64/mpeg4/ch1/sub/av_stream
            rtsp://admin:12345@192.0.0.64/h264/ch1/sub/av_stream
        :param place:
        :param ip:
        :param port:
        :param user:
        :param pwd:
        :param logPre:
        """
        self.logPre = logPre
        self.URL = f"rtsp://{user}:{pwd}@{ip}/h264/ch1/sub/av_stream"
        if port:
            self.URL = f"rtsp://{user}:{pwd}@{ip}:{port}/h264/ch1/sub/av_stream"
        # 截图或视频保存位置
        img_dir = path.join(BASE_DIR, "logs", "camera_img", place, fmt_date(fmt=FMT_DATE))
        if not path.exists(img_dir):
            makedirs(img_dir)
        # 截图保存文件名
        self.img_path = path.join(img_dir, "{carNo}" + "_" + "{now}" + ".jpg")
        # 视频保存文件名
        self.video_path = path.join(img_dir, "{carNo}" + "_" + "{now}" + ".avi")

    def get_screenshot(self, carNo, show_view=True):
        """
        截图一帧
        :param carNo:
        :param show_view:
        :return:
        """
        try:
            # 打开rtsp
            cap = VideoCapture(self.URL)
            ret, frame = cap.read()
            if not ret:
                consoleLog(self.logPre, "未捕获到帧")

            imencode('.jpg', frame)[1].tofile(self.img_path.format(carNo=carNo, now=fmt_date(fmt=FMT_DATETIME)))
            if show_view:
                # 预览窗口
                namedWindow('view', WINDOW_NORMAL | WINDOW_KEEPRATIO)
                imshow("view", frame)
                waitKey(5 * 1000)
        except Exception as e:
            consoleLog(self.logPre, "保存截图异常:", repr(e))
        finally:
            if cap:
                cap.release()
            destroyAllWindows()

    def videotape_seconds(self, carNo, t_seconds, show_view=True):
        """
        录像
        :param carNo:
        :param show_view:
        :return:
        """
        try:
            # 打开rtsp
            cap = VideoCapture(self.URL)
            # 视频分辨率
            size = (int(cap.get(CAP_PROP_FRAME_WIDTH)), int(cap.get(CAP_PROP_FRAME_HEIGHT)))
            # 帧率
            fps = cap.get(CAP_PROP_FPS)
            # 视频保存格式avi
            fourcc = VideoWriter_fourcc(*'XVID')
            # 视频保存obj
            outfile = VideoWriter(self.video_path.format(carNo=carNo, now=fmt_date(fmt=FMT_DATETIME)),
                                  fourcc, fps, size)
            if show_view:
                # 预览窗口
                namedWindow('view', WINDOW_NORMAL | WINDOW_KEEPRATIO)

            ret, frame = cap.read()
            t1 = time()
            while ret:
                if time() - t1 >= t_seconds:
                    break
                ret, frame = cap.read()
                outfile.write(frame)
                if show_view:
                    imshow("view", frame)
                    waitKey(1)
            else:
                consoleLog(self.logPre, "未捕获到帧")

        except Exception as e:
            consoleLog(self.logPre, "视频录制异常:", repr(e))
        finally:
            if cap:
                cap.release()
            if outfile:
                outfile.release()
            destroyAllWindows()


def t1(carNo, ip="10.0.0.243", port=None, user="admin", pwd="Whl649219"):
    """
    主码流：
        rtsp://admin:12345@192.0.0.64:554/h264/ch1/main/av_stream
        rtsp://admin:12345@192.0.0.64:554/MPEG-4/ch1/main/av_stream

    子码流：
        rtsp://admin:12345@192.0.0.64/mpeg4/ch1/sub/av_stream
        rtsp://admin:12345@192.0.0.64/h264/ch1/sub/av_stream
    :return:
    """
    url = f"rtsp://{user}:{pwd}@{ip}/h264/ch1/main/av_stream"
    if port:
        url = f"rtsp://{user}:{pwd}@{ip}:{port}/h264/ch1/main/av_stream"

    # 截图或视频保存位置-01.可以为摄像头位置类型
    img_dir = path.join(BASE_DIR, "logs", "camera_img", "01", fmt_date(fmt=FMT_DATE))
    if not path.exists(img_dir):
        makedirs(img_dir)
    date_now = fmt_date(fmt=FMT_DATETIME)
    # 截图保存文件名
    img_path = path.join(img_dir, carNo + "_" + date_now + ".jpg")
    # 视频保存文件名
    video_path = path.join(img_dir, carNo + "_" + date_now + ".avi")

    try:
        # 打开rtsp
        cap = VideoCapture(url)
        # 视频分辨率
        size = (int(cap.get(CAP_PROP_FRAME_WIDTH)), int(cap.get(CAP_PROP_FRAME_HEIGHT)))
        # 帧率
        fps = cap.get(CAP_PROP_FPS)
        # 视频保存格式avi
        fourcc = VideoWriter_fourcc(*'XVID')
        # 视频保存obj
        outfile = VideoWriter(video_path, fourcc, fps, size)

        # 预览窗口
        namedWindow('view', WINDOW_NORMAL | WINDOW_KEEPRATIO)

        ret, frame = cap.read()
        cnt = 0
        while ret:
            cnt += 1
            ret, frame = cap.read()
            outfile.write(frame)
            if cnt == 1:
                imencode('.jpg', frame)[1].tofile(img_path)

            imshow("view", frame)
            if waitKey(1) & 0xFF == ord('q'):
                break
        else:
            consoleLog("未读取到视频")

        cap.release()
        outfile.release()
        destroyAllWindows()
    except:
        consoleLog("异常")


if __name__ == '__main__':
    t1("鲁A12345")
