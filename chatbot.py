import numpy as np 
import speech_recognition as sr 
from gtts import gTTS
import datetime
import transformers
import os
import time 


class ChatBot():
    def __init__(self, name):
        print('---iniciando', name, '---')
        self.name = name
    
    def speech_to_text(self):
        recognizer = sr.Recognizer()
        with sr.Microphone() as mic:
            print('escutando...')
            audio = recognizer.listen(mic)
            self.text = 'ERROR'
        try:
            self.text = recognizer.recognize_google(audio)
            print('me ---->', self.text)
        except:
            print('me -----> error')


    @staticmethod
    def text_to_speech(text):
        print('dev---->', text)
        speaker = gTTS(text=text, lang='pt', slow=False)

        speaker.save('res.mp3')
        statbuf = os.stat('res.mp3')
        mbytes = statbuf.st_size / 1024
        duration = mbytes / 200
        os.system('start_res.mp3')
        time.sleep(int(50*duration))
        os.remove('res.mp3')

    
    def wake_up(self, text):
        return True if self.name in text.lower() else False
    
    @staticmethod
    def action_time():
        return datetime.datetime.now().time().strftime('%H:%M')
    


if __name__ == "__main__":

    ai = ChatBot(name='dev')
    nlp = transformers.PYTORCH_PRETRAINED_BERT_CACHE
    os.environ['TOKENIZERS_PARALLELISM'] = 'true'


    ex = True
    while ex:
        ai.speech_to_text()

        if ai.wake_up(ai.text) is True:
            res = 'Ola, eu sou o LegalAIBOT, como posso te ajudar?'

        elif "time" in ai.text:
            res = ai.action_time()

        elif any(i in ai.text for i in ["Obrigado", "Obrigada", "Grato", "Grata"]):
            res = np.random.choice(['Nao ha de que', 'Sem problemas', 'De nada!', 'Estou feliz em ajudar', 'Estou aqui para o que voce precisar'])

        elif any(i in ai.text for i in ["fechar", "sair"]):
            res = np.random.choice(["Tenha um bom dia", 'Ate logo', 'Tchau tchau'])

            ex = False

        else:
            if ai.text == 'ERROR':
                res = 'Perdao, voce poderia repetir por favor?'

            else:
                chat = nlp(transformers.Conversation(ai.text), pad_token_id = 50256)
                res = str(chat)
                res = res[res.find("bot >> ")+6:].strip()

        

        ai.text_to_speech(res)
    print('----Fechando o Chat----')