# Speech-Controlled-3D-Hand
in this project we create an algorithm which records, trains and controls by speech a 3D printed hand.

# Requirements
this project was on a windows 10, Python 3 environment using anaconda. to run this project we suggest you download and run the txt file we provide.

# collect data and train the model
we suggest running the code on the anaconda prompt.
to record new users - run the file: "python identify_speaker.py" we suggest that the user will be called "user" in those recording and that for each preset of a hand movement, each one of the 10 recordings will include the sentence "okay hand *keyword*" multiple times.
if the user usually has specific people in his environment, he should record them as well for better speaker verification results.

# parameter changes
to change specific parameters- names of movements will be determined in lines __ and __ in the file___. 
threshold will be in line __ in the file __ .

we would like to thank the following projects which we used and attributed to our finished project:
https://github.com/wangshub/python-vad
https://github.com/gfairchild/pyxDamerauLevenshtein
https://github.com/VaibhavBhapkar/Speaker-Identification-Using-Machine-Learning
https://github.com/Uberi/speech_recognition
https://github.com/resemble-ai/Resemblyzer
