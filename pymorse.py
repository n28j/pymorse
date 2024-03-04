import sounddevice as sd
import numpy as np
import traceback
import random

dot_length_s = 0.05
dash_length_s = 3 * dot_length_s
inter_dot_length_s = 1 * dot_length_s
inter_letter_length_s = 2 * dot_length_s
inter_word_length_s = 4 * dot_length_s

morse = {
    'a': '.-',
    'b': '-...',
    'c': '-.-.',
    'd': '-..',
    'e': '.',
    'f': '..-.',
    'g': '--.',
    'h': '....',
    'i': '..',
    'j': '.---',
    'k': '-.-',
    'l': '.-..',
    'm': '--',
    'n': '-.',
    'o': '---',
    'p': '.--.',
    'q': '--.-',
    'r': '.-.',
    's': '...',
    't': '-',
    'u': '..-',
    'v': '...-',
    'w': '.--',
    'x': '-..-',
    'y': '-.--',
    'z': '--..',
    '0': '-----',
    '1': '.----',
    '2': '..---',
    '3': '...--',
    '4': '....-',
    '5': '.....',
    '6': '-....',
    '7': '--...',
    '8': '---..',
    '9': '----.'
}

def soften(data, exponent: float = 0.1):
    multiplier = np.zeros((len(data)))
    for i in range(multiplier.shape[0]):
        multiplier[i] = (1.0 - (2.0 * (i / multiplier.shape[0]) - 1)**2)**exponent
    data = np.multiply(data, multiplier)
    return data

_samples_per_second = 44100
_freq_hz = 440.0
_attenuation = 0.3
_dot_samples_number = np.arange(dot_length_s * _samples_per_second)
_dash_samples_number = np.arange(dash_length_s * _samples_per_second)

_dot_wav = np.sin(2 * np.pi * _dot_samples_number * _freq_hz / _samples_per_second)
_dash_wav = np.sin(2 * np.pi * _dash_samples_number * _freq_hz / _samples_per_second)
_inter_dot_wav = np.zeros((int(inter_dot_length_s * _samples_per_second)))
_inter_letter_wav = np.zeros((int(inter_letter_length_s * _samples_per_second)))
_inter_word_wav = np.zeros((int(inter_word_length_s * _samples_per_second)))

_dot_wav = soften(_dot_wav)
_dash_wav = soften(_dash_wav)
_inter_dot_wav = soften(_inter_dot_wav)
_inter_letter_wav = soften(_inter_letter_wav)
_inter_word_wav = soften(_inter_word_wav)

def generate_morse_code(text: str):
   
    text = text.strip()

    waveform = np.ndarray(1)
    for val in text:
        val = val.lower()
        if val in morse:
            morse_string = morse[val]
            for m_val in morse_string:
                if m_val == '.':
                    waveform = np.concatenate((waveform.copy(), _dot_wav))
                elif m_val == '-':
                    waveform = np.concatenate((waveform.copy(), _dash_wav))
                waveform = np.concatenate((waveform.copy(), _inter_dot_wav))
            waveform = np.concatenate((waveform.copy(), _inter_letter_wav))
        else:
            if val == ' ':
                waveform = np.concatenate((waveform.copy(), _inter_word_wav))
    
    waveform = _attenuation * waveform
    sd.play(waveform, _samples_per_second)

def input_number(prompt: str):
    val = input(prompt).strip()
    while not val.isnumeric():
        print('{} is not a number!'.format(val))
        val = input(prompt).strip()
    return int(val)
    
def input_yes_no(prompt: str):
    val = input(prompt).lower()
    while 'y' not in val and 'n' not in val:
        print("It's a yes or no question...")
        val = input(prompt).lower()
    if 'y' in val:
        return True
    return False


words = {}
ignore_characters = ['-', '.', '/']

def init_word_lists():
    global words
    with open('/usr/share/dict/words', 'r') as file_in:
        word_list = [a for a in file_in.read().split('\n') if a != '']
        for ic in ignore_characters:
            word_list = [a for a in word_list if ic not in a]
        for word in word_list:
            word_length = len(word)
            if word_length not in words:
                words[word_length] = set()
            words[word_length].add(word.lower())
    for wl in words:
        print('{}: {}'.format(wl, len(words[wl])))


def get_word(min_length: int, max_length: int, random_letters: bool = False) -> str:
    global words
    target_length = [a for a in range(min_length, max_length + 1) if a in words]
    return random.choice(list(words[random.choice(target_length)]))

def training():
    init_word_lists()
    word_count_min = input_number('Minimum word count: ')
    word_count_max = input_number('Maximum word count: ')
    word_length_min = input_number('Minimum word length: ')
    word_length_max = input_number('Maximum word length: ')
    #use_random_letters = input_yes_no('Use Random Letters? ')
    try:
        while True:
            word_count = random.randint(word_count_min, word_count_max)
            my_words = []
            for wc in range(word_count):
                my_words.append(get_word(word_length_min, word_length_max))
            generate_morse_code(' '.join(my_words))
            guess = input('What was the message? ').lower()
            if guess == ' '.join(my_words):
                print('Correct!')
            else:
                print('Incorrect: {}'.format(' '.join(my_words)))
    except KeyboardInterrupt:
        pass
    except:
        print(traceback.format_exc())
    print()


def text_to_morse():
    try:
        while True:
            target_string = input("Input String: ")
            generate_morse_code(target_string)
    except KeyboardInterrupt:
        pass
    except:
        print(traceback.format_exc())
    print()


if __name__ == '__main__':
    try:
        while True:
            print('1. Text to Morse Code')
            print('2. Morse Code Training')
            selection = input('What would you like to do? ')
            if selection.strip().isnumeric():
                i_sel = int(selection.strip())
                if i_sel == 1:
                    text_to_morse()
                elif i_sel == 2:
                    training()
    except KeyboardInterrupt:
        pass
    except:
        print(traceback.format_exc())
    print()
