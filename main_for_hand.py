import os
import sys
import wave
import time
import signal
import pyaudio
import warnings
import webrtcvad
import contextlib
import collections
from array import array
import speech_recognition as sr
from pyxdameraulevenshtein import normalized_damerau_levenshtein_distance

from bleak import BleakClient
import asyncio

from assistance.params import *
from assistance.functions import *



async def init_ble(address=hand_address, char_uuid='e0198002-7544-42c1-0001-b24344b6aa70'):

    ble_client = BleakClient(address)
    # connect the Hand
    if await ble_client.connect():
        print('Connected to Device: ' + address)
    # find the Trigger preset characteristic
    char_out = None
    for service in ble_client.services:
        for char in service.characteristics:
            if char.uuid == char_uuid:
                char_out = char.uuid
                print('Trigger char was found')
    if char_out is None:
        print("didn't found the relevant characteristic")
    return ble_client,  char_out


# <<<<<<<<<<<<<<<<<<<<<< send BLE message function  >>>>>>>>>>>>>>>>>>>>>>> #
async def send_ble_message(ble_client, char_write, value_write):
    await ble_client.write_gatt_char(char_write, bytes([value_write]))  # Sending Event via BLE


# <<<<<<<<<<<<<<<<<<<<<< BLE disconnection function  >>>>>>>>>>>>>>>>>>>>>>> #
async def disconnect_ble(ble_client):
    await ble_client.disconnect()

# init BLE connection:
my_device_address = hand_address   # change the address according to your device address
trigger_char_uuid = 'e0198002-7544-42c1-0001-b24344b6aa70'

loop = asyncio.get_event_loop()
client, trigger_char = loop.run_until_complete(init_ble(my_device_address, trigger_char_uuid))

# init main loop
activate_preset_id = 1  # here we activate only preset 1 but you can change it as you please (between 0-11)







r = sr.Recognizer()
m = sr.Microphone(device_index)


FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 16000
CHUNK_DURATION_MS = 30
PADDING_DURATION_MS = 1500
CHUNK_SIZE = int(RATE * CHUNK_DURATION_MS / 1000)
CHUNK_BYTES = CHUNK_SIZE * 2
NUM_PADDING_CHUNKS = int(PADDING_DURATION_MS / CHUNK_DURATION_MS)
NUM_WINDOW_CHUNKS = int(150 / CHUNK_DURATION_MS)
NUM_WINDOW_CHUNKS_END = NUM_WINDOW_CHUNKS * 2
Open_Time = time.time() + 1364
activation = 0

if with_prints == 0:
    blockPrint()
    
with warnings.catch_warnings():
    warnings.simplefilter("ignore", category=RuntimeWarning)
    spk_embeds_train, speaker_wavs_training = train_training_set()

enablePrint()
print("\n")
try:
    with warnings.catch_warnings():
        warnings.simplefilter("ignore", category=RuntimeWarning)
        while True:
            try:
                    
                START_OFFSET = int(NUM_WINDOW_CHUNKS * CHUNK_DURATION_MS * 0.5 * RATE)
                
                vad = webrtcvad.Vad(3)
                
                pa = pyaudio.PyAudio()
                stream = pa.open(format=FORMAT,
                                 channels=CHANNELS,
                                 rate=RATE,
                                 input=True,
                                 start=False,
                                 input_device_index = device_index,
                                 frames_per_buffer=CHUNK_SIZE)
                
                
                got_a_sentence = False
                leave = False
                
                
                signal.signal(signal.SIGINT, handle_int)
                
                while not leave:
                    ring_buffer = collections.deque(maxlen=NUM_PADDING_CHUNKS)
                    triggered = False
                    voiced_frames = []
                    ring_buffer_flags = [0] * NUM_WINDOW_CHUNKS
                    ring_buffer_index = 0
                
                    ring_buffer_flags_end = [0] * NUM_WINDOW_CHUNKS_END
                    ring_buffer_index_end = 0
                    buffer_in = ''
                    raw_data = array('h')
                    index = 0
                    start_point = 0
                    StartTime = time.time()
                    if with_prints == 1:
                        print("* recording: ")
                    stream.start_stream()
                    
                    count_for_rec = 0
                
                    while not got_a_sentence and not leave:
                        chunk = stream.read(CHUNK_SIZE)
                        raw_data.extend(array('h', chunk))
                        index += CHUNK_SIZE
                        active = vad.is_speech(chunk, RATE)
                
                        ring_buffer_flags[ring_buffer_index] = 1 if active else 0
                        ring_buffer_index += 1
                        ring_buffer_index %= NUM_WINDOW_CHUNKS
                        ring_buffer_flags_end[ring_buffer_index_end] = 1 if active else 0
                        ring_buffer_index_end += 1
                        ring_buffer_index_end %= NUM_WINDOW_CHUNKS_END
                
                        if not triggered:
                            ring_buffer.append(chunk)
                            num_voiced = sum(ring_buffer_flags)
                            if num_voiced > 0.9 * NUM_WINDOW_CHUNKS:
                                triggered = True
                                count_for_rec = count_for_rec + 1
                                if count_for_rec == 1:
                                    stop_rec = time.time()
                                start_point = index - CHUNK_SIZE * 20 
                                ring_buffer.clear()
                        else:
                            ring_buffer.append(chunk)
                            num_unvoiced = NUM_WINDOW_CHUNKS_END - sum(ring_buffer_flags_end)
                            TimeUse = time.time() - stop_rec
                            if num_unvoiced > 0.60 * NUM_WINDOW_CHUNKS_END or TimeUse > rec_len:
                                triggered = False
                                got_a_sentence = True
                
                        sys.stdout.flush()
                    sys.stdout.write('\n')             
                    stream.stop_stream()
                    StartTime = time.time()
                    raw_data.reverse()
                    for index in range(start_point):
                        raw_data.pop()
                    raw_data.reverse()
                    got_a_sentence = False
                    raw_data = normalize(raw_data)
                    for count in range(2):
                        OUTPUT_FILENAME = "test-0"+str(count)+".flac"
                        AUDIO_FILE_NAME = os.path.join("audio_files\\test", OUTPUT_FILENAME)
                        record_to_file(AUDIO_FILE_NAME, raw_data, 2, RATE)
                    with contextlib.closing(wave.open(AUDIO_FILE_NAME,'r')) as f:
                        frames = f.getnframes()
                        rate = f.getframerate()
                        duration = frames / float(rate)
                        if with_prints == 1:
                            print("\n The duration of test is \n", duration, " seconds")
                    a = sr.AudioFile(AUDIO_FILE_NAME)
                    with a as source:
                        audio = r.record(source)

                    sentense = r.recognize_google(audio)
                    sentense = sentense.lower()
                    text_list = sentense.split()
                    list_len = len(text_list)
                    sample = 0
                    key = 0
                    keysam = 0
                    keysam1 = 0
                    over = 0
                    if len(text_list) != 0:
                        Time_so_far = abs(time.time() - Open_Time)
                        if  Time_so_far > open_time:
                            activation = 0
                            check_speaker = 1
                                
                            while (sample < (len(text_list)-1)) and (over == 0):
            
                                if normalized_damerau_levenshtein_distance(text_list[sample], 'okay') < 0.5:
                                    text_list[sample] = 'okay'
                                    text_list.pop(sample)
                                    if len(text_list) == 0:
                                        new_sentense = ' '.join(text_list[:])
                                        break
                                else:
                                    text_list.pop(sample)
                                    if len(text_list) == 0:
                                        new_sentense = ' '.join(text_list[:])
                                        break
                                    continue
                                if normalized_damerau_levenshtein_distance(text_list[sample], 'hand') < 0.5:
                                    text_list[sample] = 'hand'
                                    text_list.pop(sample)
                                    activation = 1
                                    Open_Time = time.time()
                                    if len(text_list) == 0:
                                        new_sentense = ' '.join(text_list[:])
                                        break
                                else:
                                    text_list.pop(sample)
                                    if len(text_list) == 0:
                                        new_sentense = ' '.join(text_list[:])
                                        break
                                over = 1
        
        
        
        
                    if len(text_list) > 0:
                        while keysam < (len(text_list)):
                            keysam = max(keysam, keysam1)
                            keysam1 = keysam
                            use_DL = 1
                            percent_min = 1
                            if_pop = 1  
                            text = text_list[keysam]
                            temptext = text
                            for opt in words:
                                per = normalized_damerau_levenshtein_distance(opt, text)
                                if per < 0.5:
                                    if per < percent_min:
                                        temptext = opt
                                        percent_min = per
                                        key = key + 1
                                        if_pop = 0
                            if if_pop == 0:
                                text_list[keysam] = text
                                keysam1 = keysam + 1
                                if_pop = 2
                            if ((text == 'clothes')):
                                text = 'close'
                                key = key + 1
                                keysam = keysam + 1
                                if_pop = 0
                                use_DL = 0
                            if ((text == 'binge') or(text == 'themes')):
                                text = 'pinch'
                                key = key + 1
                                keysam = keysam + 1
                                if_pop = 0
                                use_DL = 0
                            if ((text == 'bingo')):
                                text = 'finger'
                                key = key + 1
                                keysam = keysam + 1
                                if_pop = 0
                                use_DL = 0
                            if ((text == 'holland')):
                                text = 'hold'
                                key = key + 1
                                keysam = keysam + 1
                                if_pop = 0
                                use_DL = 0
                            if use_DL == 1:
                                text = temptext
                                if if_pop == 2:
                                    text_list[keysam1 - 1] = text
                                else:
                                    text_list.pop(keysam1)
                                if keysam1 == len(text_list):
                                    break
                                continue
                            if if_pop == 0:
                                text_list[keysam - 1] = text
                            elif if_pop == 1:
                               text_list.pop(keysam)
                            if keysam == len(text_list):
                                break 
                            
                    new_sentense = ' '.join(text_list[:])
                    
                    if activation == 0:
                        if with_prints == 1:
                            new_sentense = '----no activation words-----'
                            Timeuse = time.time() - StartTime
                            print("\n you are saying " + str(new_sentense) + "\n processing time is " + str(Timeuse) + " seconds")
                        continue
                    if (key == 0) and (activation == 1):
                        if with_prints == 1:
                            new_sentense = '----no keywords-----'
                            Timeuse = time.time() - StartTime
                            print("\n you said " + str(new_sentense) + "\n processing time is " + str(Timeuse) + " seconds")
                        continue
                    
                    if with_prints == 0:
                        blockPrint()
                    print("\n you said " + str(new_sentense))
                    if check_speaker == 1:
                        a = sr.AudioFile(AUDIO_FILE_NAME)
                        with a as source:
                            audio = r.record(source)
                        if accuracy > 0:
                            speaker_id = speaker_verification(spk_embeds_train, speaker_wavs_training)
                        else:
                            speaker_id = 1
                        if speaker_id == 1:
                            check_speaker = 0
                        Timeuse = time.time() - StartTime

                    if (speaker_id == 0):
                        print("UNKNOWN speaker" + "\n processing time is " + str(Timeuse) + " seconds")                    
                    else:
                        print("You are the user!! HARRAY!!!!!" + "\n processing time is " + str(Timeuse) + " seconds")

                        if with_prints == 1:
                            new_sentense_list = new_sentense.split()
                            for wordi in new_sentense_list:
                                for idx, word in enumerate(words):
                                    if wordi == word:
                                        loop.run_until_complete(send_ble_message(client, trigger_char, idx))  # Sending to BLE
                                        print('event sent! preset: ', idx)
                                        time.sleep(time_between_movements)

                    enablePrint()
                    new_sentense_list = new_sentense.split()
                    if (speaker_id == 1) and (key > 0) and (activation == 1) and (with_prints == 0):
                        print(str(new_sentense))
                        for wordi in new_sentense_list:
                            for idx, word in enumerate(words):
                                if wordi == word:
                                    loop.run_until_complete(send_ble_message(client, trigger_char, idx))  # Sending to BLE
                                    print('event sent! preset: ', idx)
                                    time.sleep(time_between_movements)

                                        

                        
                    leave = True
                stream.close()
            except sr.UnknownValueError:
                    if with_prints == 1:
                        print("Oops! Didn't catch that")
            except sr.RequestError as e:
                    print("Uh oh! Couldn't request results from Google Speech Recognition service; {0}".format(e))
                    
except KeyboardInterrupt:
    pass