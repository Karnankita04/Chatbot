from tkinter import *
from chatterbot import ChatBot
from chatterbot.trainers import ListTrainer
import os 
import pyttsx3
import speech_recognition
import threading

bot = ChatBot('Chattu')
trainer=ListTrainer(bot)

# Here we are training our chatbot 
for files in os.listdir('data/'):
    data = open('data/'+files,'r',encoding='utf-8').readlines()
    trainer.train(data)

def botReply():
    question=questionfield.get()
    question=question.capitalize()
    answer= bot.get_response(question)
    textarea.insert(END,'You: '+question+'\n\n') 
    textarea.insert(END,'Bot: '+str(answer)+'\n\n') 
    pyttsx3.speak(answer)
    questionfield.delete(0,END)

# Here we'll use the concept of thread because The main thread will be executing all the program so In this case we have to provide a separate thread to execute this particular function otherwise Main thread will be busy to execute this function and rest of the task will be waiting to be executed #

def audioToText():
    while True:
        sr=speech_recognition.Recognizer()
        try:
            with speech_recognition.Microphone()as m:
                sr.adjust_for_ambient_noise(m,duration=0.2)
                audio=sr.listen(m)
                query=sr.recognize_google(audio)
                # query=query.capitalize()
                questionfield.delete(0,END)
                questionfield.insert(0,query)
                botReply()

        except Exception as e:
            print(e)

root = Tk()  # creating main window with the help of TK method

root.geometry('500x570+100+30')
root.title('Ankita\'s Chatbot')
root.config(bg='purple')

logoPic = PhotoImage(file='pic.png')
logopiclabel = Label(root,image=logoPic,bg='purple')
logopiclabel.pack()

centreframe = Frame(root)
centreframe.pack()

scrollbar = Scrollbar(centreframe)
scrollbar.pack(side=RIGHT)

textarea = Text(centreframe,font=('times new roman',20,'bold'),height=10,yscrollcommand=scrollbar.set,wrap='word')
textarea.pack(side=LEFT)
scrollbar.config(command=textarea.yview)

questionfield = Entry(root,font=('verdana',20,'bold'))
questionfield.pack(pady=15,fill=X)

AskPic = PhotoImage(file='ask.png')
askButton = Button(root,image=AskPic,command=botReply)
askButton.pack()

# pressing enter key for asking questions
def click(event):
    askButton.invoke()

root.bind('<Return>',click)

thread=threading.Thread(target=audioToText)
thread.setDaemon(True)
thread.start()
root.mainloop()  