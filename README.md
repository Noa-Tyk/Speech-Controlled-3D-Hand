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
To download the libraries manually, run the following lines:
* pyaudio - `pip install pyaudio`
* pyxDamerauLevenshtein - `pip install pyxDamerauLevenshtein`
* SpeechRecognition - `pip install SpeechRecognition`
* resemblyzer - `pip install resemblyzer`
* tqdm - `pip install tqdm`
* pathlib - `pip install pathlib`
* matplotlib - `pip install matplotlib`
* asyncio - `pip install asyncio`
* bleak - `pip install bleak`

## Collect Data And Train The Model
We suggest running the code on the anaconda prompt.<br/>
run the line: `python verification_model.py` on the anaconda prompt

**there are 3 options when running the code:**
1) Press '1' - "Record audio for training" - To record new people and add them to the train-set.<br/>
we suggest that the user will be called **user** in those recordings.<br/>
There will be 10 recordings per speaker- one for each preset of a hand movement.<br/>
Notice that each one of the 10 recordings will include the sentence "okay hand *keyword*" multiple times. In other words, for every recording you should say the phrase "okay hand *keyword*" for multiple times (until the recording is over) with the same keyword, where *keyword* means a keyword from the list, so that for each recording you use a different keyword from the list.<br/>
If the user regularly has specific people in his daily environment, we suggest he should record them as well for better speaker verification results.
2) Press '2' - "Record audio for testing" - To record a test recording.<br/> There can only be one test recording and it will automatically change to the latest one recorded. You can use it to check the speaker verification algorithm. The `main.py` and `main_for_hand.py` scripts replace the test recording too after running them, so we recommend recording new test recording for each time you wamt to check its effectiveness.
3) Press '3' - "Check similarity" - To check the similarity of the test recording with each one of the people on the train-set. calculates and then returns a histogram of the similarity precentage for the test with each one of the people on the train-set.

## Run The Program
To run the main script without the hand - run this line: `python main.py`.<br/>
To run the main script with the hand - run this line: `python main_for_hand.py`.<br/>

## Parameter Changes
To change specific parameters- enter the `params.py` file and save your changes. <br/>

We would like to thank the following projects which we used and helped us reach our finished project:<br/>
https://github.com/wangshub/python-vad , 
https://github.com/VaibhavBhapkar/Speaker-Identification-Using-Machine-Learning , 
https://github.com/Uberi/speech_recognition , 
https://github.com/resemble-ai/Resemblyzer
