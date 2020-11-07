"""
.Project Name - FRIDAY (digital voice asstistant)
.Programmed By - Himanshu Raj Verma
.Language Used - Python 3.7.1
.Modules (Package used) - datetime, json, os, webbrowser, requests, speech recognition, wikipedia, random, pyttsx3
.version - 0.0.1
.Description - This is a digital voice assistant which take the command from the user and perform the task based on that command.
"""

import datetime  # this is for date and time related queries.
import json  # this is for news related queries.
import os  # operating system work related queries.
import webbrowser  # browser related queries.
import requests  # http related queries.
import speech_recognition as sr  # speech recognition work.
import wikipedia  # for wikipedia related queries.
import random  # for generating random file names.
import pyttsx3  # for coverting the text into speech

# chrome path registration
webbrowser.register('chrome', None, webbrowser.BackgroundBrowser("C:\\Program Files (x86)\\Google\\Chrome\\Application\\chrome.exe") )

engine = pyttsx3.init('sapi5')
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[0].id)


def speak(audio):
    print(audio.upper())
    engine.say(audio)
    engine.runAndWait()


def wishMe():
    hour = int(datetime.datetime.now().hour)
    if 0 <= hour < 12:
        speak("Good Morning.")
    elif 12 <= hour < 18:
        speak("Good Afternoon.")
    else:
        speak("Good Evening.")


def takeCommand():
    # It takes microphone input from the user and returns string output

    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        r.pause_threshold = 0.7
        r.energy_threshold = 8000
        r.phrase_threshold = 0.6
        r.adjust_for_ambient_noise(source, duration=0.3)
        audio = r.listen(source)

    try:
        print("Recognizing...")
        query = r.recognize_google(audio, language='en-IN')
        print(f"User said: {query}\n")

    except Exception:
        # print(e)
        print("Say that again please...")
        return "None"
    return query


def trigger():
    """
    This is a trigger word function for waking up our FRIDAY AI
    """
    r1=sr.Recognizer()
    with sr.Microphone() as mic:
        r1.pause_threshold = 0.5
        r1.energy_threshold = 10000
        r1.phrase_threshold = 0.4
        r1.adjust_for_ambient_noise(mic, duration=0.2)
        trigger_Word = r1.listen(mic)
        try:
            user_said = r1.recognize_google(trigger_Word, language='en-IN')
            print(user_said)
        except Exception:
            return "None"
    return user_said


def note():
    """
    This function make a note to store some information in my note txt file.
    """
    with open("my note.txt", "w") as f:
        speak("my note open.")
        speak('what do you want to write?')
        writefile = takeCommand().lower()
        f.close()
        while True:
            speak('do you want to save it?')
            save_note = takeCommand().lower()
            if 'yes' in save_note:
                with open("my note.txt", "w") as f:
                    f.write(writefile)
                    speak("note saved as my note.")
                    f.close()
                    break
            elif 'no' in save_note:
                f.close()
                speak('note is not saved!')
                break
            else:
                continue


def appreciation(query):
    """
       This function takes the query and return the words if it get appreciated
       :param query: takes from user
       """
    praise_words = ["you are on fire", "very good", "awesome", "hilarious", "fantastic", "mind blowing", "amazing", "thank you"]
    words = ["Thank You.", "My Pleasure.", "i am glad.", "i am glad that i helped you.", "Thank You,That's Very Kind Of You"]
    for item in praise_words:
        if item in query:
            say = random.choice(words)
            speak(say)
            break


def shutoff(query):
    """
    this function takes query and close the friday
    :param query:
    """
    commands = ['bye', 'shut down', 'take rest', 'switch off', 'ok stop', 'quit', 'exit', 'go to sleep']
    for command in commands:
        if command in query:
            speak("Bye Sir.")
            hour = int(datetime.datetime.now().hour)
            if 0 <= hour < 12:
                speak("May God Bless you With A Beautiful Day.")
            elif 12 <= hour < 17:
                speak("Have A Nice Day.")
            elif 17 <= hour <= 19:
                speak("Wishing you A Wonderful Evening.")
            else:
                speak("Wishing you The Sweetest Dreams as You Drift Off To Sleep.\nGood Night")
            global shutdown
            shutdown = True
            break


if __name__ == '__main__':
    wishMe()  # wishing function call
    speak("I Am Your Personal Digital Assistant Friday.\nPlease Tell Me What Can I Do For You?")
    shutdown = False  # for shutdown the assistant
    while not shutdown:
        if trigger().lower() == "friday":  # calling the trigger word function
            query = takeCommand().lower()  # start taking query
            # logic for executing the task based on query.

            try:
                shutoff(query)  # shutdown function.
                appreciation(query)  # appreciation function.
                if 'wikipedia' in query:  # block for wikipedia related queries.
                    speak("searching...")
                    search = query.replace("on wikipedia" or "in wikipedia", "")
                    result = wikipedia.summary(search, sentences=2)
                    speak("According to wikipedia...")
                    speak(result)

                elif 'what can you do' in query:  # task can perform block.
                    speak("i can perform wikipedia search,\nopen Application's,\nclose Applications,\nplay music,\nstop music,\nmake notes,\nopen saved notes,"
                          "\ntell time and date,\ngive you the latest tech news,\nmake a google search for you and many more.")

                elif 'who are you' in query:  # block for knowing the assstant.
                    speak("My name is VERONICA, and i am your personal digital assistant.")

                elif 'open google' in query:  # opening google.
                    speak('Opening google...')
                    webbrowser.get('chrome').open("google.com")

                elif 'close internet explorer' in query:  # closing google.
                    speak('Closing internet explorer...')
                    os.system("TASKKILL /F /IM iexplore.exe")

                elif 'open youtube' in query:  # open youtube.
                    speak('Opening youtube...')
                    webbrowser.get('chrome').open("youtube.com")

                elif 'close youtube' in query:  # query for closing Chrome browser
                    os.system("TASKKILL /F /IM chrome.exe")
                    speak("Chrome closed.")

                elif 'youtube' in query:  # youtube search.
                    speak("searching...")
                    search = query.replace("on youtube" or "in youtube", "")
                    url = "https://www.youtube.com/results?search_query=" + search
                    webbrowser.get('chrome').open(url)

                elif 'open stack overflow' in query:  # open stack overflow.
                    speak('Opening stackoverflow...')
                    webbrowser.get('chrome').open("stackoverflow.com")

                elif 'play music' in query:  # music play block.
                    music_dir = "D:\\mobile\\Download"
                    files_list = os.listdir(music_dir)
                    songs_files = [song for song in files_list if song.endswith(".mp3")]
                    music_play = random.choice(songs_files)
                    os.startfile(os.path.join(music_dir, music_play))
                    speak('Playing music...')

                elif 'stop music' in query:  # stop music block.
                    speak('Stopping music...')
                    os.system("TASKKILL /F /IM wmplayer.exe")

                elif 'open spotify' in query:  # open spotify block.
                    speak("Opening spotify...")
                    spotify = "C:\\Users\\Himanshu\\AppData\\Roaming\\Spotify\\Spotify.exe"
                    os.startfile(spotify)

                elif 'close spotify' in query:  # close spotify block.
                    speak("Closing spotify...")
                    os.system("TASKKILL /F /IM Spotify.exe")

                elif 'shutdown' in query:  # shutdown block.
                    speak('Shutting down...')
                    shutdown = True

                elif 'make a note' in query:  # taking a note block.
                    speak('making a note...')
                    note()

                elif 'open my note' in query:  # opening note block.
                    speak("opening note...")
                    with open('my note.txt', "r") as f:
                        data = f.read()
                        speak(data)

                elif 'time' in query:  # time block.
                    curr_time = datetime.datetime.now().strftime("%I:%M:%S:%p")  # format as 12/time -hour, minute, sec, am\pm.
                    speak(f'The time is {curr_time}')

                elif 'date' in query:  # date block
                    curr_date = datetime.date.today()
                    speak(f'The date is {curr_date}')

                elif 'tech news' in query:  # tech news block.
                    speak("News for Today..")
                    url = "http://newsapi.org/v2/top-headlines?country=in&category=technology&apiKey=4303a0cfb66641b2829d752db520fac8"
                    news = requests.get(url).text
                    news_dict = json.loads(news)
                    arts = news_dict['articles']
                    for article in arts:
                        speak(article['title'])
                        speak("do you want to continue?")
                        query = query.replace(query, "")
                        query = takeCommand().lower()
                        if 'no' in query:
                            speak('stopped!')
                            break
                        elif 'yes' in query:
                            speak("moving on to the next news")
                            continue
                        else:
                            continue
                    speak("Thanks for listening")

                elif 'google search' in query:  # google search query
                    speak('What do you want to search?')
                    search = takeCommand().lower()
                    speak("searching...")
                    url = "https://google.com/search?q=" + search
                    webbrowser.get('chrome').open(url)

                elif 'close firefox' in query:  # close google search query
                    os.system("TASKKILL /F /IM firefox.exe")
                    speak("firefox closed.")

                elif 'search location' in query:  # location related query
                    while True:
                        speak('Please tell me the location name to search?')
                        location = takeCommand().lower()
                        try:
                            speak("searching...")
                            url = "https://google.nl/maps/search/" + location + '/&amp;'
                            webbrowser.get('chrome').open(url)
                            break
                        except Exception as e:
                            print(e)
                            continue

                elif 'close browser' in query:  # query for closing edge browser
                    os.system("TASKKILL /F /IM msedge.exe")
                    speak("Microsoft Edge closed.")

                elif 'close chrome' in query:  # query for closing Chrome browser
                    os.system("TASKKILL /F /IM chrome.exe")
                    speak("Chrome closed.")
                
                elif 'close google' in query:  # query for closing Chrome browser
                    os.system("TASKKILL /F /IM chrome.exe")
                    speak("Chrome closed.")
                
            except Exception as e:  # for error handling.
                print(e)
                speak("sorry can't do that,try again!")
                continue
