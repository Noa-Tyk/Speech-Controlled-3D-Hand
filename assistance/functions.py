import os
import sys
import wave
import pyaudio
import numpy as np
from tqdm import tqdm
from array import array
from struct import pack
from pathlib import Path
from itertools import groupby
import matplotlib.pyplot as plt
from resemblyzer import preprocess_wav, VoiceEncoder

from assistance.params import *

############### for verification model script ################################

## the model ##

def record_audio_train():
    Name =(input("Please Enter Your Name:"))
    Path(os.path.join("audio_files\\training",Name)).mkdir(parents=True, exist_ok=True)
    for count in range(10):
        FORMAT = pyaudio.paInt16
        CHANNELS = 1
        RATE = 44100
        CHUNK = 512
        RECORD_SECONDS = 10
        audio = pyaudio.PyAudio()
        print("----------------------record device list---------------------")
        info = audio.get_host_api_info_by_index(0)
        numdevices = info.get('deviceCount')
        for i in range(0, numdevices):
                if (audio.get_device_info_by_host_api_device_index(0, i).get('maxInputChannels')) > 0:
                    print("Input Device id ", i, " - ", audio.get_device_info_by_host_api_device_index(0, i).get('name'))
        print("-------------------------------------------------------------")
        index = int(input())        
        print("recording via index "+str(index))
        stream = audio.open(format=FORMAT, channels=CHANNELS,
                        rate=RATE, input=True,input_device_index = index,
                        frames_per_buffer=CHUNK)
        print ("recording started")
        Recordframes = []
        for i in range(0, int(RATE / CHUNK * RECORD_SECONDS)):
            data = stream.read(CHUNK)
            Recordframes.append(data)
        print ("recording stopped")
        stream.stop_stream()
        stream.close()
        audio.terminate()
        OUTPUT_FILENAME=Name+"-0"+str(count)+".flac"
        WAVE_OUTPUT_FILENAME=os.path.join("audio_files\\training",Name, OUTPUT_FILENAME)
        waveFile = wave.open(WAVE_OUTPUT_FILENAME, 'wb')
        waveFile.setnchannels(CHANNELS)
        waveFile.setsampwidth(audio.get_sample_size(FORMAT))
        waveFile.setframerate(RATE)
        waveFile.writeframes(b''.join(Recordframes))
        waveFile.close()


def record_audio_test():
    FORMAT = pyaudio.paInt16
    CHANNELS = 1
    RATE = 44100
    CHUNK = 512
    RECORD_SECONDS = 5
    audio = pyaudio.PyAudio()
    print("----------------------record device list---------------------")
    info = audio.get_host_api_info_by_index(0)
    numdevices = info.get('deviceCount')
    for i in range(0, numdevices):
        if (audio.get_device_info_by_host_api_device_index(0, i).get('maxInputChannels')) > 0:
            print("Input Device id ", i, " - ", audio.get_device_info_by_host_api_device_index(0, i).get('name'))
    print("-------------------------------------------------------------")
    index = int(input())        
    print("recording via index "+str(index))
    stream = audio.open(format=FORMAT, channels=CHANNELS,
                    rate=RATE, input=True,input_device_index = index,
                    frames_per_buffer=CHUNK)
    print ("recording started")
    Recordframes = []
    for i in range(0, int(RATE / CHUNK * RECORD_SECONDS)):
        data = stream.read(CHUNK)
        Recordframes.append(data)
    print ("recording stopped")
    stream.stop_stream()
    stream.close()
    audio.terminate()
    
    for count in range(2):
        
        OUTPUT_FILENAME = "test-0"+str(count)+".flac"
        WAVE_OUTPUT_FILENAME=os.path.join("audio_files\\test", OUTPUT_FILENAME)
        waveFile = wave.open(WAVE_OUTPUT_FILENAME, 'wb')
        waveFile.setnchannels(CHANNELS)
        waveFile.setsampwidth(audio.get_sample_size(FORMAT))
        waveFile.setframerate(RATE)
        waveFile.writeframes(b''.join(Recordframes))
        waveFile.close()


## create graphs ##


def training_testing_set():
    
    encoder = VoiceEncoder()

    wav_fpaths_train = list(Path("audio_files\\training").glob("**/*.flac"))

    speaker_wavs_training = {speaker: list(map(preprocess_wav, wav_fpaths_train)) for speaker, wav_fpaths_train in
                    groupby(tqdm(wav_fpaths_train, "Preprocessing flacs", len(wav_fpaths_train), unit="flacs"), 
                            lambda wav_fpath_train: wav_fpath_train.parent.stem)}


    spk_embeds_training = np.array([encoder.embed_speaker(wavs[:]) \
                             for wavs in speaker_wavs_training.values()])
        
    wav_fpaths_test = list(Path("audio_files\\test").glob("**/*.flac"))

    speaker_wavs_testing = {speaker: list(map(preprocess_wav, wav_fpaths_test)) for speaker, wav_fpaths_test in
                    groupby(tqdm(wav_fpaths_test, "Preprocessing flacs", len(wav_fpaths_test), unit="flacs"), 
                            lambda wav_fpath_test: wav_fpath_test.parent.stem)}


    spk_embeds_testing = np.array([encoder.embed_speaker(wavs[:]) \
                            for wavs in speaker_wavs_testing.values()])
        
        
    train_test_sim = np.inner(spk_embeds_testing, spk_embeds_training)
    similarity_percent = train_test_sim * 100
    labels = ["%s" % i for i in speaker_wavs_training.keys()]
    print("\nSimilarity precentages between training-set and test are:\n")
    for i in range(len(labels)):
        print("\n",labels[i], "-->", similarity_percent[0,i], "%")
    print("\n")
    
    mask = np.eye(len(train_test_sim), dtype=np.bool)
    labels_a = ["%s" % i for i in speaker_wavs_testing.keys()]
    labels_b = ["%s" % i for i in speaker_wavs_training.keys()]
    

    fig, ax = plt.subplots()
    ax.barh(labels_b,similarity_percent[0,:])
    plt.axvline(accuracy, color = 'red')
    ax.invert_yaxis()
    ax.set_xlabel('Percentage')
    ax.set_title('Similarity percentage to test')
    plt.show()
    
    
    

################### for main script ################################


def speaker_verification(spk_embeds_train, speaker_wavs_training):
    
    encoder = VoiceEncoder()

    wav_fpaths = list(Path("audio_files\\test").glob("**/*.flac"))
    
    if with_prints == 1:
        speaker_wavs = {speaker: list(map(preprocess_wav, wav_fpaths)) for speaker, wav_fpaths in
                        groupby(tqdm(wav_fpaths, "Preprocessing flacs", len(wav_fpaths), unit="flacs"), 
                                lambda wav_fpath: wav_fpath.parent.stem)}

    else:
        speaker_wavs = {speaker: list(map(preprocess_wav, wav_fpaths)) for speaker, wav_fpaths in
                        groupby(tqdm(wav_fpaths, len(wav_fpaths), disable=True))}


    spk_embeds_test = np.array([encoder.embed_speaker(wavs[:]) \
                             for wavs in speaker_wavs.values()])
        
    train_test_sim = np.inner(spk_embeds_test, spk_embeds_train)
    
    similarity_precent = train_test_sim * 100
    labels = ["%s" % i for i in speaker_wavs_training.keys()]
    print("\nSimilarity precentages between training-set and test are:\n")
    for i in range(len(labels)):
        print("\n",labels[i], "-->", similarity_precent[0,i], "%")
    print("\n")
    if np.max(similarity_precent) > accuracy:
        speaker_index = np.argmax(train_test_sim)
        if 'user' == labels[speaker_index]:
            speaker = 1
        else:
            speaker = 0
    else:
        speaker = 0
    
    
    return speaker





def train_training_set():
    
    encoder = VoiceEncoder()
    
    wav_fpaths = list(Path("audio_files\\training").glob("**/*.flac"))
    

    speaker_wavs = {speaker: list(map(preprocess_wav, wav_fpaths)) for speaker, wav_fpaths in
                    groupby(tqdm(wav_fpaths, "Preprocessing flacs", len(wav_fpaths), unit="flacs"), 
                            lambda wav_fpath: wav_fpath.parent.stem)}


    spk_embeds_train = np.array([encoder.embed_speaker(wavs[:]) \
                             for wavs in speaker_wavs.values()])
        
    return spk_embeds_train, speaker_wavs


def handle_int(sig, chunk):
    global leave, got_a_sentence
    leave = True
    got_a_sentence = True


def record_to_file(path, data, sample_width, RATE):
    data = pack('<' + ('h' * len(data)), *data)
    wf = wave.open(path, 'wb')
    wf.setnchannels(1)
    wf.setsampwidth(sample_width)
    wf.setframerate(RATE)
    wf.writeframes(data)
    wf.close()


def normalize(snd_data):
    MAXIMUM = 32767
    times = float(MAXIMUM) / max(abs(i) for i in snd_data)
    r = array('h')
    for i in snd_data:
        r.append(int(i * times))
    return r


def blockPrint():
    sys.stdout = open(os.devnull, 'w')


def enablePrint():
    sys.stdout = sys.__stdout__

