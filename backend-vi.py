# coding: utf-8
from VoiceInput.voiceinput import VoiceInput

vi = VoiceInput()
tot_last = 0
vi.clearCache()
while tot_last<=60:
    duration,sr_result = vi.recognize(log=True)
    tot_last += duration
    print('[Dur]: {}s\n[Result]:\n{}\n'.format(duration,sr_result))
