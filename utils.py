from deep_translator import GoogleTranslator
import soundfile as sf
import scipy.signal as signal
import re
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