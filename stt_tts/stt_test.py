import speech_recognition as sr
from playsound import playsound
import os

# 마이크객체얻기
r = sr.Recognizer()
with sr.Microphone() as source:
    print("Say something")
    audio = r.listen(source)
    
# mp3 파일을 저장
filename = "./stt-result.mp3"
with open(filename, 'wb') as f:
    f.write(audio.get_wav_data())  

playsound(filename)
