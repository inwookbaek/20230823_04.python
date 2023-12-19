from gtts import gTTS
from playsound import playsound
import os

audio = './speech.mp3'  # wav파일은 utf8 디코딩에러발생
language = 'ko'

sp = gTTS(
    lang=language,
    text="안녕하세요? 반갑습니다. 저는 홍길동입니다!",
    slow=False
)

sp.save(audio)
playsound(audio)
os.remove(audio)
