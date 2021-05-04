# Speech-Controlled-3D-Hand
In this project we create an algorithm which records data and trains a neural network used for speaker identification, and controls a 3D printed prosthetic hand using speech commands set by the user.

## Requirements
This project was ran on a Windows 10 PC and in a Python 3.6+ environment using anaconda.<br/>
To run this project you will need to following libraries:<br/>
* webrtcvad - `pip install webrtcvad`
* pyaudio - `pip install pyaudio`
* pyxDamerauLevenshtein - `pip install pyxDamerauLevenshtein`
* numpy - `pip install numpy`
* SpeechRecognition - `pip install SpeechRecognition`
* matplotlib - `pip install matplotlib`
* resemblyzer - `pip install resemblyzer`

Run `pip install *library name*` for each library mentioned.

## Collect Data And Train The Model
We suggest running the code on the anaconda prompt.<br/>
To record new users - run the file: "python identify_speaker.py" on the anaconda prompt
we suggest that the user will be called **user** in those recordings.
There will be 10 recordings per speaker- one for each preset of a hand movement.<br/>
Notice that each one of the 10 recordings will include the sentence "okay hand *keyword*" multiple times.<br/>

If the user regularly has specific people in his daily environment, we suggest he should record them as well for better speaker verification results.

## Parameter Changes
To change specific parameters- names of movements will be determined in lines __ and __ in the file___. <br/>
Threshold will be in line __ in the file __ .

We would like to thank the following projects which we used and helped us reach our finished project:<br/>
https://github.com/wangshub/python-vad , https://github.com/gfairchild/pyxDamerauLevenshtein , 
https://github.com/VaibhavBhapkar/Speaker-Identification-Using-Machine-Learning , 
https://github.com/Uberi/speech_recognition , 
https://github.com/resemble-ai/Resemblyzer
