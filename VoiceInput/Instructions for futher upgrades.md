# Intro.  
实现长文本实时上屏所需资料及思路

---
# Possible References 
### 思路（三选一）
- **(1)双进程同步**  
使用MultiProcessing库将Recorder和Recognizer两个模块分开，并用两个并行进程实现同步。
- **(2)使用文件缓冲区实现**  
使用一个本地临时音频文件(格式为wav或pcm)存储本次开始识别后接收到的音频,再创建一个线程不断读写临时文件内的内容变化。每次读取1024*1024字节调用websocket传回结果。参考[链接](https://blog.csdn.net/u013484772/article/details/83187340)里的思路和代码
- **(3)快速高并发**  
本思路来自[百度语音WebAPI文档](https://ai.baidu.com/ai-doc/SPEECH/2k5dllqxj)。实现上每隔duration=100ms向server发送一次音频，每隔2~4s服务器传回一次结果，尽可能上[讯飞官方WebAPI文档](https://www.xfyun.cn/doc/asr/voicedictation/API.html#%E6%8E%A5%E5%8F%A3%E8%B0%83%E7%94%A8%E6%B5%81%E7%A8%8B)找一找有没有现成的接口,有现成的尽量用现成的，没有的话可以考虑手写一个API，或者再上网找一找。

### 其他参考
- [功能体验](https://www.xfyun.cn/services/voicedictation)  
- [实时音频录制 (已实现，通过谷歌的Speech-Recognition库)](https://www.i5seo.com/python-simple-realize-speech-recognition.html)  
- [代码上可能会对方法(2)有帮助](https://github.com/ssky87/iflytek_sdk_python/blob/master/stt.py)  

### 一些图片
- 目前演示效果  
<div align=center><img src="http://47.92.96.62/pics/demo.png"></img></div>  

- 参考中提到的中有关(2)的代码片段
<div align=center><img src="http://47.92.96.62/pics/Sample%20Code%20for%20(2).png"></img></div>  

- 【精华】(3)中思路
<div align=center><img src="http://47.92.96.62/pics/Instructions%20For%20(3).png"></img></div>  

# Suggestions
- 推荐优先使用第3种方法，第3种方法理论上实现效果最好。
- 如果官方文档和网上实在找不到系统API，自己也写不出来，再试第2种。
- 第1种我已经试过了，没戏。
