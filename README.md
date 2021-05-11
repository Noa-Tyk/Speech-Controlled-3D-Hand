# Speech-Controlled-3D-Hand
In this project we create an algorithm which records data and trains a neural network used for speaker identification, and controls a 3D printed prosthetic hand using speech commands set by the user.

## Requirements
This project was ran on a Windows 10 PC and in a Python 3.6+ environment using anaconda.<br/>
To create the environment follow the code:<br/>
`conda create --name env_name python=3.6` (change "env_name" to the name you want for the environment you are creating)<br/>
`conda activate env_name`<br/>
`pip install -r requirements.txt`<br/>
<br/>
To run this project you will need the following libraries (which are included in the requierments.txt file)<br/>
To download on your own run the following lines:
* pyaudio - `pip install pyaudio`
* pyxDamerauLevenshtein - `pip install pyxDamerauLevenshtein`
* SpeechRecognition - `pip install SpeechRecognition`
* resemblyzer - `pip install resemblyzer`
* tqdm - `pip install tqdm`
* pathlib - `pip install pathlib`
* matplotlib - `pip install matplotlib`

## Collect Data And Train The Model
We suggest running the code on the anaconda prompt.<br/>
To record new users - run the line: `python verification_model.py` on the anaconda prompt and add them to the train-set.<br/>
we suggest that the user will be called **user** in those recordings.<br/>
There will be 10 recordings per speaker- one for each preset of a hand movement.<br/>
Notice that each one of the 10 recordings will include the sentence "okay hand *keyword*" multiple times.<br/>

If the user regularly has specific people in his daily environment, we suggest he should record them as well for better speaker verification results.

## Run The Program 
To run the main script - run this line: `python main.py`.<br/>

## Parameter Changes
To change specific parameters- enter the `params.py` file and save your changes. <br/>

We would like to thank the following projects which we used and helped us reach our finished project:<br/>
https://github.com/wangshub/python-vad , 
https://github.com/VaibhavBhapkar/Speaker-Identification-Using-Machine-Learning , 
https://github.com/Uberi/speech_recognition , 
https://github.com/resemble-ai/Resemblyzer
