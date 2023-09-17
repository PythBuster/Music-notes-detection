# install these libraries ----

import math
import struct
import wave

import matplotlib.pyplot as plt
import numpy as np

from config import FREQUENCIES, NOTES, WAV_FILES_PATH


def note_detect(audio_file):
    # -------------------------------------------
    # here we are just storing our sound file as a numpy array
    # you can also use any other method to store the file as an np array
    file_length = audio_file.getnframes()
    f_s = audio_file.getframerate()  # sampling frequency
    sound = np.zeros(file_length)  # blank array

    for i in range(file_length):
        wdata = audio_file.readframes(1)
        data = struct.unpack("<h", wdata)
        sound[i] = int(data[0])

    #plt.plot(sound)
    #plt.show()

    sound = np.divide(sound, float(2**15))  # scaling it to 0 - 1
    counter = audio_file.getnchannels()  # number of channels mono/sterio
    # -------------------------------------------

    #plt.plot(sound)
    #plt.show()

    # fourier transformation from numpy module
    fourier = np.fft.fft(sound)
    fourier = np.absolute(fourier)
    imax = np.argmax(fourier[0 : int(file_length / 2)])  # index of max element

    #plt.plot(fourier)
    #plt.show()

    # peak detection
    i_begin = -1
    threshold = 0.3 * fourier[imax]
    for i in range(0, imax + 100):
        if fourier[i] >= threshold:
            if i_begin == -1:
                i_begin = i
        if i_begin != -1 and fourier[i] < threshold:
            break
    i_end = i
    imax = np.argmax(fourier[0 : i_end + 100])

    freq = (imax * f_s) / (
        file_length * counter
    )  # formula to convert index into sound frequency

    # frequency database
    note = 0
    name = np.array(NOTES)
    frequencies = np.array(FREQUENCIES)

    # searching for matched frequencies
    for i in range(0, frequencies.size - 1):
        if freq < frequencies[0]:
            note = name[0]
            break
        if freq > frequencies[-1]:
            note = name[-1]
            break
        if freq >= frequencies[i] and frequencies[i + 1] >= freq:
            if freq - frequencies[i] < (frequencies[i + 1] - frequencies[i]) / 2:
                note = name[i]
            else:
                note = name[i + 1]
            break

    return note


if __name__ == "__main__":
    file_name = WAV_FILES_PATH / "d2.wav"
    file_name = r"C:\Users\twitch\Desktop\h.wav"
    audio_file = wave.open(str(file_name))
    Detected_Note = note_detect(audio_file)
    print("\n\tDetected Note = " + str(Detected_Note))
