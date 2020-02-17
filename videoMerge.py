#批量合并特定文件夹下的视频文件，然后输出到指定文件夹下
# 主要是需要moviepy这个库
from moviepy.editor import *
import os
from natsort import natsorted
import json

# psutil是一个跨平台库能够轻松实现获取系统运行的进程和系统利用率（包括CPU、内存、磁盘、网络等）信息。它主要用来做系统监控，性能分析，进程管理。它实现了同等命令行工具提供的功能，如ps、top、lsof、netstat、ifconfig、who、df、kill、free、nice、ionice、iostat、iotop、uptime、pidof、tty、taskset、pmap等。目前支持32位和64位的Linux、Windows、OS X、FreeBSD和Sun Solaris等操作系统.
import psutil

# 杀死moviepy产生的特定进程
def killProcess():
    # 处理python程序在运行中出现的异常和错误
    try:
        # pids方法查看系统全部进程
        pids = psutil.pids()
        for pid in pids:
            # Process方法查看单个进程
            p = psutil.Process(pid)
            # print('pid-%s,pname-%s' % (pid, p.name()))
            # 进程名
            if p.name() == 'ffmpeg-win64-v4.1.exe':
                # 关闭任务 /f是强制执行，/im对应程序名
                cmd = 'taskkill /f /im ffmpeg-win64-v4.1.exe  2>nul 1>null'
                # python调用Shell脚本执行cmd命令
                os.system(cmd)
    except:
        pass
if __name__ == '__main__':
    #循环体
    for i in range(120):
        #提取对应视频标题的json文件路径
        myjsondirs = './video/{}/entry.json'.format(i + 1)
        #定义拼接完成后视频的标题
        vdtitle = ''
        with open(myjsondirs, 'r', encoding='UTF-8') as load_f:
            # loads方法将json格式数据转换为字典（读取文本用此法）
            load_dict = json.load(load_f)
            vdtitle = load_dict['page_data']['part']
        #视频文件夹路径
        mydirs = './video/{}/lua.flv.bili2api.80'.format(i+1)
        # 定义拼接视频的数组
        L = []
        # 访问 video 文件夹
        # root指的是当前正在遍历的这个文件夹的本身的地址，dirs是一个 list，内容是该文件夹中所有的目录的名字(不包括子目录)，files同样是 list，内容是该文件夹中所有的文件(不包括子目录)
        for root, dirs, files in os.walk(mydirs):
            # 按文件名排序
            # files.sort()
            # 自然排序法
            files = natsorted(files)
            # print(files)
            # 遍历所有文件
            for file in files:
                # os.path.splitext(“文件路径”)    分离文件名与扩展名：默认返回(fname, fextension)元组，可做分片操作
                # 如果后缀名为 .blv
                if os.path.splitext(file)[1] == '.blv':
                    # .blv格式视频的完整路径
                    filePath = os.path.join(root, file)
                    # 读取视频到内存
                    myvideo = VideoFileClip(filePath)
                    # 添加到数组
                    L.append(myvideo)
        # 对多个视频在时长上进行拼接
        final_clip = concatenate_videoclips(L)
        targetdir = './target/{}.mp4'.format(vdtitle)
        # 法一：生成目标视频文件方法
        # final_clip.to_videofile(targetdir, fps=24)
        #法二：最常规的生成目标视频文件方法
        final_clip.write_videofile(targetdir,fps=24, remove_temp=True)  #remove_temp=True表示生成的音频文件是临时存放的，视频生成后，音频文件会自动处理掉！若为False表示，音频文件会同时生成！
        print("{}---{}---拼接成功！".format(i + 1, vdtitle))
        killProcess()