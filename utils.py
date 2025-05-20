from deep_translator import GoogleTranslator
import soundfile as sf
import scipy.signal as signal
import re
import asyncio
import edge_tts

def translate_text(text):
    return GoogleTranslator(source='auto', target='vi').translate(text)

def change_speed(input_file, output_file, speed_factor):
    # audio, sample_rate = sf.read(input_file)
    #
    # adjusted_audio = signal.resample(audio, int(len(audio) / speed_factor))
    #
    # sf.write(output_file, adjusted_audio, sample_rate)
    pass

def convert_username_youtube(username):
    username = re.sub(r'\W+', '', username)
    return username
def cut_string(string, start, end):
    try:
        return string.split(start)[1].split(end)[0]
    except:
        return ''

def cut_string_head(string, key):
    try:
        return string.split(key)[0]
    except:
        return ''
def cut_string_last(string, key):
    try:
        return string.split(key)[1]
    except:
        return ''

def save_speech(text: str, filename: str = "output.mp3", voice: str = "vi-VN-HoaiMyNeural"):
    async def _save():
        communicate = edge_tts.Communicate(text=text, voice=voice)
        await communicate.save(filename)
    asyncio.run(_save())