import pyttsx3
import datetime
import speech_recognition as sr
import wikipedia
import smtplib
import webbrowser as wb
import psutil 
import pyjokes
import os
import pyautogui
import json
import requests
from urllib.request import urlopen
import time

engine=pyttsx3.init()

def speak(audio):
    engine.say(audio)
    engine.runAndWait()

def time_():
    Time=datetime.datetime.now().strftime("%H:%M:%S")
    speak("the current time according to 24 hour clock is")
    speak(Time)
    #Time=datetime.datetime.now().strftime("%I:%M:%S") # for 12-hour clock
    #speak("the current time according to 12 hour clock is")
    #speak(Time)

def date_():
    year= datetime.datetime.now().year
    month= datetime.datetime.now().month
    date= datetime.datetime.now().day
    speak("The current date is")
    speak(date)
    speak(month)
    speak(year)

def wishme():
    speak("Welcome back Pranaya Parjata Malla!")
    time_()
    date_()

    hour=datetime.datetime.now().hour

    if hour>=6 and hour<12:
        speak("Good morning Ma'am!")
    elif hour>=12 and hour<18:
        speak("Good Afternoon Ma'am!")
    elif hour>=18 and hour<24:
        speak("Good Evening Ma'am!")
    else:
        speak("Good Night Ma'am!")

    speak("Jarvis at your service. Please tell me how can I help you today?")

def TakeCommand():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        r.pause_threshold = 1
        audio = r.listen(source)
    try:
        print("Recognizing...")    
        query = r.recognize_google(audio, language='en-in') #Using google for voice recognition.
        print(f"User said: {query}\n")  #User query will be printed.

    except Exception as e:
        # print(e)    
        print("Say that again please...")   #Say that again will be printed in case of improper voice 
        return "None" #None string will be returned
    return query

def sendEmail(to,content):
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.ehlo() #identifying us to smtp server
    server.starttls() 
    # Enable low security in gmail 
    server.login('name@gmail.com', 'pwd')
    server.sendmail('name@gmail.com', to, content)
    server.close()

def cpu():
    usage=str(psutil.cpu_percent())
    speak('CPU is at'+usage)

    battery=psutil.sensors_battery()
    speak('Battery is at')
    speak(battery.percent)

def joke():
    speak(pyjokes.get_joke())

def screenshot():
    img=pyautogui.screenshot()

if __name__ == "__main__":
    wishme()
    while True:
        query=TakeCommand().lower()

        if 'time' in query:
            time_()
        elif 'date' in query:
            date_()
        elif 'wikipedia' in query:
            speak("Searching Wikipedia....")
            query = query.replace("wikipedia", "")
            result = wikipedia.summary(query, sentences=2) 
            speak("According to Wikipedia")
            print(result)
            speak(result)
        elif 'send email' in query:
            try:
                speak("What should I say?")
                content = TakeCommand()
                to = "name2@gmail.com"
                sendEmail(to,content)
                speak(content)
                speak("Email has been sent!")
            except Exception as e:
                print(e)
                speak("Sorry Ma'am Unable to send the email at this moment")
        elif 'search in chrome' in query:
            speak("What should I search Ma'am?")
            chromepath= 'C:/Program Files (x86)/Google/Chrome/Application/chrome.exe %s'

            search=TakeCommand().lower()
            wb.get(chromepath).open_new_tab(search+'.com')
        elif 'open youtube' in query:
            wb.open("youtube.com")
        elif 'open google' in query:
            wb.open("google.com")
        elif 'cpu' in query:
            cpu()
        
        elif 'joke' in query:
            joke()

        elif 'go offline' in query:
            speak("Going Offline Ma'am. Have a great day!")
            quit()

        elif 'write a note' in query:
            speak("What should I write,Ma'am?")
            note=TakeCommand()
            file = open('note.txt', 'w')
            speak("Sir, Should i include date and time")
            dt = TakeCommand()
            if 'yes' in dt or 'sure' in dt:
                strTime = datetime.datetime.now().strftime("%H:%M:%S")
                file.write(strTime)
                file.write(" :- ")
                file.write(note)
                speak('done taking notes')
            else:
                file.write(note)
        
        elif 'show note' in query:
            speak("showing notes..")
            file.open('notes.txt','r')
            print(file.read())
            speak(file.read())

        elif 'screenshot' in query:
            speak("Capturing screenshot")
            screenshot()
                
        elif 'remember that' in query:
            speak("what should i remember?")
            mem=TakeCommand()
            speak('you asked me to remember that'+mem)
            rem=open('mem.txt','w')
            rem.write(mem)
            rem.close()

        elif 'do you remember anything' in query:
            rem=open('mem.txt','r')
            speak('You asked me to remember that'+rem.read())

        elif 'news' in query:
            try:
                jsonObj = urlopen("https://newsapi.org/")
                data = json.load(jsonObj)
                i = 1
                
                speak('here are some top news from the times of india')
                print('''=============== TOP HEADLINES ============'''+ '\n')
                
                for item in data['articles']:
                        
                    print(str(i) + '. ' + item['title'] + '\n')
                    print(item['description'] + '\n')
                    speak(str(i) + '. ' + item['title'] + '\n')
                    i += 1
                    
            except Exception as e:
                print(str(e)) 
            
        elif "where is" in query:
            query = query.replace("where is", "")
            location = query
            speak("User asked to Locate")
            speak(location)
            wb.open("https://www.google.com/maps/place/" + location + "")

        elif 'stop listening' in query:
            speak('For how many seconds you want me to stop listening to your commands?')
            ans=int(TakeCommand())
            time.sleep(ans)
            print(ans)
            speak("Okay Ma'am")

        elif 'log out' in query:
            os.system("shutdown -l")
        elif 'restart' in query:
            os.system("shutdown /r /t 1")
        elif 'shutdown' in query:
            os.system("shutdown /s /t 1")

        
