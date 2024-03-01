import sounddevice as sd
import numpy as np
import traceback

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

def generate_morse_code(text: str):
    samples_per_second = 44100
    freq_hz = 440.0
    attenuation = 0.3
    dot_samples_number = np.arange(dot_length_s * samples_per_second)
    dash_samples_number = np.arange(dash_length_s * samples_per_second)

    dot_wav = np.sin(2 * np.pi * dot_samples_number * freq_hz / samples_per_second)
    dash_wav = np.sin(2 * np.pi * dash_samples_number * freq_hz / samples_per_second)
    inter_dot_wav = np.zeros((int(inter_dot_length_s * samples_per_second)))
    inter_letter_wav = np.zeros((int(inter_letter_length_s * samples_per_second)))
    inter_word_wav = np.zeros((int(inter_word_length_s * samples_per_second)))
    
    text = text.strip()

    waveform = np.ndarray(1)
    for val in text:
        val = val.lower()
        if val in morse:
            morse_string = morse[val]
            for m_val in morse_string:
                if m_val == '.':
                    waveform = np.concatenate((waveform.copy(), dot_wav))
                elif m_val == '-':
                    waveform = np.concatenate((waveform.copy(), dash_wav))
                waveform = np.concatenate((waveform.copy(), inter_dot_wav))
            waveform = np.concatenate((waveform.copy(), inter_letter_wav))
        else:
            if val == ' ':
                waveform = np.concatenate((waveform.copy(), inter_word_wav))
    
    waveform = attenuation * waveform
    sd.play(waveform, samples_per_second)


if __name__ == '__main__':
    try:
        while True:
            target_string = input("Input String: ")
            generate_morse_code(target_string)
    except KeyboardInterrupt:
        pass
    except:
        print(traceback.format_exc())
