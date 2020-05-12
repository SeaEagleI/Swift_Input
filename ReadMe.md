# 项目说明及演示

---
## 运行
#### 先安装依赖:
```python
$ pip install requirements.txt
$ pip install PyQt5 PyQt5-tools pyaudio speechrecognition
```
#### 然后运行后端:
运行./backend-pi.py对PinyinInput的后端效果进行测试/使用；
```python
$ python3 backend-pi.py
```
运行./backend-vi.py对VoiceInput的后端效果进行测试/使用。
```python
$ python3 backend-vi.py
```
#### 再运行前端:
直接运行SwiftInput.py即可运行项目(含界面)。
```python
$ python3 SwiftInput.py
```

## 文件目录说明
（本ReadMe.txt中提及的所有"."均指项目目录Swift_Input）
- **.**  
.下是主目录文件，包括界面定义文件(*.ui,Homepage.py,ChoicePanel.py)、项目说明文件ReadMe.txt、依赖说明文件requirements.txt、主程序SwiftInput.py、和两个后端测试程序(backend-pi.py,backend-vi.py)。
- **./data**  
./data下是词库文件: core_wordlib.db是SQLite数据库文件，为PinyinInput提供支持，共含词条74万+，具体数据库格式见文档。词组来源包括百度搜索结果数量、新浪新闻语料库及词频统计、搜狗核心词库sgim_core.bin（使用Java解码）;单字来源为网上找的一个新华字典的TXT文件。
- ./**PinyinInput**  
./PinyinInput下是拼音输入模块代码: pinyininput.py中定义了该PinyinInput类，根据用户输入在先前准备的词库数据库文件（./data/core_wordlib.db）中查询，并迅速响应，取得了较为不错的效果，具体实例实例参见./backend-pi.py。
- ./**log**  
./log是相关输入的log记录。
- ./**VoiceInput**  
./VoiceInput下是语音输入模块代码: voiceinput.py中定义了该VoiceInput类，使用讯飞的WebAPI接口和Python3中的websocket、speech_recognition两个模块实现了异步语音识别，具体过程参考源码和讯飞API的官方文档。
- ./**icons**  
./icons下是界面开发时所用的图标。
- ./**pics**  
./pics下是部分有关程序界面截图。
- **./__pycache__**  
./__pycache__下是py程序编译产生的字节码文件。

## 运行效果演示
#### 拼音输入后端展示
<div align=center><img src="http://47.92.96.62/pics/PinyinInput%20Backend%20Demo.png"></img>
backend-pi.py运行效果</div>  

#### 语音输入后端展示
<div align=center><img src="http://47.92.96.62/pics/VoiceInput%20Backend%20Demo.png"></img>
backend-vi.py运行效果</div>  

#### 前端界面展示
<div align=center><img src="http://47.92.96.62/pics/GUI%20Demo.png"></img>
SwiftInput.py运行效果</div>
