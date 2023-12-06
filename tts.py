from gtts import gTTS 

#writes the myText into audio file audio.mp3
def tts(myText):
    language = 'en'
    myobj = gTTS(text=myText, lang=language, slow=False) 
    myobj.save("audio.mp3") 
    pass