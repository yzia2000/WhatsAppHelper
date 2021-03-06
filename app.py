import gi.repository.GLib
import dbus
from dbus.mainloop.glib import DBusGMainLoop
from gtts import gTTS
import re
import playsound
import speech_recognition as sr
from automation import sendMessage

mic = sr.Microphone()
r = sr.Recognizer()

exclusionList= ["Malaysia", "Family chat", "Joker Tuesday", "CEG Class of 2022"]

def keepAsking():
    while True:
        playsound.playsound('askForReply.mp3')

        with mic as source:
            r.adjust_for_ambient_noise(source)
            audio = r.listen(source)

        reply = r.recognize_google(audio)

        print(reply)

        tts = gTTS("You said: {}".format(reply), lang="en")
        tts.save('reply.mp3')
        playsound.playsound('reply.mp3')

        print("Playing confim")

        playsound.playsound('confirm.mp3')

        with mic as source:
            r.adjust_for_ambient_noise(source)
            audio = r.listen(source)

        confirm = r.recognize_google(audio)
        print(confirm)

        if "cancel" in confirm:
            print("cancelled")
            return None

        if "send" in confirm:
            print("sending")
            return reply




def notifications(bus, message):
    name = message.get_args_list()[3]
    text = message.get_args_list()[4]

    print(name)

    for excluded in exclusionList:
        if excluded in name:
            playsound.playsound('./excluded.mp3')
            return


    cleanr = re.compile('<.*?>|&([a-z0-9]+|#[0-9]{1,6}|#x[0-9a-f]{1,6});')
    cleantext = re.sub(cleanr, '', text)

    if "whatsapp" not in  cleantext:
        tts = gTTS("{} {}".format(name, cleantext), lang="en")
        tts.save("latest.mp3")
        playsound.playsound("latest.mp3")
        return

    cleantext = cleantext.replace("web.whatsapp.com", "")
    cleantext.rstrip()
    cleantext.strip()
    length = len(cleantext)
    cleantext = cleantext[:(length - 12)]

    readMessage(name, cleantext)

    notificationHandler(name, cleantext)

def notificationHandler(name, cleantext):
    with mic as source:
        r.adjust_for_ambient_noise(source)
        audio = r.listen(source)

    perm = r.recognize_google(audio)

    print(perm)

    if "yes" not in perm:
        playsound.playsound('discarded.mp3')
        return

    reply = keepAsking()

    if reply:
        playsound.playsound('sending.mp3')
        sendMessage(name, reply)
    else:
        playsound.playsound('discarded.mp3')

def readMessage(name, cleantext):
    print("{} says: {}".format(name, cleantext))
    tts = gTTS("{} says: {}. Do you want to reply?".format(name, cleantext), lang="en")
    tts.save('latest.mp3')
    playsound.playsound('latest.mp3')

DBusGMainLoop(set_as_default=True)

bus = dbus.SessionBus()
bus.add_match_string_non_blocking("eavesdrop=true, interface='org.freedesktop.Notifications', member='Notify'")
bus.add_message_filter(notifications)

mainloop = gi.repository.GLib.MainLoop()
mainloop.run()
