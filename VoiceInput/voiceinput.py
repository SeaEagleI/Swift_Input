# -*- coding: utf-8 -*-
import time,logging
import os,os.path as op
import speech_recognition as sr
from VoiceInput.config import *
from VoiceInput.iat_ws import AudioToWords
#import multiprocessing 
import pyaudio,time
import threading,wave

CACHE_DIR = './VoiceInput/cache'
INTERVAL  = 0.5
THRESH_W  = 5
THRESH_D  = 60
LOG_PATH  = './log/VoiceInput.log'

# 获取毫秒级时间戳
def GetCurTimestamp():
    return int(round((time.time())*1000))
def Log(s,log_file=LOG_PATH):
    open(log_file,'a').write(s)

class VoiceInput:
    def __init__(self, chunk=1024, channels=1, rate=64000):
        self.CHUNK = chunk
        self.FORMAT = pyaudio.paInt16
        self.CHANNELS = channels
        self.RATE = rate
        self.cacheFilePath = ''
        self._running = True
        self._frames = []
        self.start_t = 0
        self.end_t = 0
        self.duration = 0
        self.sr_result = ''

    def clearCache(self,dir=CACHE_DIR):
        last_vol = len(os.listdir(dir))
        for i in os.listdir(dir):
            os.remove(op.join(dir,i))
        cur_vol = len(os.listdir(dir))
        print('{} Wavs Removed.'.format(last_vol-cur_vol))

    def recognize(self,log=False):
        self.duration = 0
        self.sr_result = ''
        self.start_t = GetCurTimestamp()
        self.cacheFilePath = op.join(CACHE_DIR, "{}.wav".format(self.start_t))
        # 启用麦克风
        r = sr.Recognizer()
        mic = sr.Microphone()
        with mic as source:
            # 降噪
            r.adjust_for_ambient_noise(source)
            audio = r.listen(source)
        with open(self.cacheFilePath, "wb") as f:
            # 将麦克风录到的声音保存为wav文件
            f.write(audio.get_wav_data(convert_rate=16000))

        self.end_t = GetCurTimestamp()
        self.duration, self.sr_result = AudioToWords(self.cacheFilePath)
        os.rename(self.cacheFilePath,op.join(CACHE_DIR,'{}-{}.wav'.format(self.start_t,self.end_t)))
        if log:
            Log('[Start-End(ms)]: {}-{}\n[Duration]: {:.3f}ms\n[Result]:\n{}\n\n'.format(self.start_t,self.end_t,self.duration, self.sr_result))
        return self.duration,self.sr_result

    # def start(self):
    #     threading._start_new_thread(self.recording, ())
    #
    # def recording(self):
    #     self._running = True
    #     self._frames = []
    #     self.start_t = GetCurTimestamp()
    #     self.cacheFilePath = op.join(CACHE_DIR, "{}.wav".format(self.start_t))
    #     # Start
    #     p = pyaudio.PyAudio()
    #     stream = p.open(format=self.FORMAT,
    #                     channels=self.CHANNELS,
    #                     rate=self.RATE,
    #                     input=True,
    #                     frames_per_buffer=self.CHUNK)
    #     # Running
    #     while (self._running):
    #         data = stream.read(self.CHUNK)
    #         self._frames.append(data)
    #     # Stop
    #     stream.stop_stream()
    #     stream.close()
    #     p.terminate()
    #     self.end_t = GetCurTimestamp()
    #     # Save Wav
    #     wf = wave.open(self.cacheFilePath, 'wb')
    #     wf.setnchannels(self.CHANNELS)
    #     wf.setsampwidth(p.get_sample_size(self.FORMAT))
    #     wf.setframerate(self.RATE)
    #     wf.writeframes(b''.join(self._frames))
    #     wf.close()
    #
    # def stop(self):
    #     self._running = False
    #
    # def recognize(self,log=False):
    #     duration, sr_result = AudioToWords(self.cacheFilePath)
    #     os.rename(self.cacheFilePath, op.join(CACHE_DIR, '{}-{}.wav'.format(self.start_t, self.end_t)))
    #     if log:
    #         Log('[Start-End(ms)]: {}-{}\n[Duration]: {:.3f}ms\n[Result]:\n{}\n\n'.format(self.start_t, self.end_t, duration, sr_result))
    #     return sr_result
