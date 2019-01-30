import os

# When using Google as TTS, you can specify a language. This makes the voice
# speak that languange more accuately, but also gives an interesting accent
# Refer to https://ctrlq.org/code/19899-google-translate-languages#languages
# for language choices.
google_language = 'it'

# Set a maximum queue length of stacked messages before blocking
# set this to False to disable
max_queue = False

playing = False

_message_queue = []


def googleSay(message):
    global playing
    if not max_queue and len(_message_queue) <= max_queue:  # Queue length control
        _message_queue.append(message)
    if playing:  # If playing, add to queue and exit
        return
    playing = True
    while len(_message_queue) > 0:  # Keep playing until queue is exhausted
        message = _message_queue.pop(0).lstrip().replace(" ", "%20")
        cmdLine = ('wget --header "Referer: http://translate.google.com/" --header "User-Agent: stagefright/1.2 (Linux;Android 5.0)" -qO- "https://translate.google.com/translate_tts?ie=UTF-8&q={msg}&tl={lang}&client=tw-ob" | ffplay -loglevel quiet -nodisp -autoexit -').format(msg=message, lang=google_language)
        forgetme = os.system(cmdLine)
    playing = False


def setup(robot_config):
    return


def say(*args):
    message = args[0]
    googleSay(message)
