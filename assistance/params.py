device_index = 0   # the microphone index you want to use

recording_for_training = 10  #  the amount of recordings of the training set for each person

len_rec_training = 10  #  the length of each recording for training set

len_rec_test = 5  #  the length of the recording for test set

accuracy = 70 # between 0 to 100, where 0 means without verification

with_prints = 0 # 0-> prints only keywords when activated and verificated. 1-> all prints included

open_time = 10 # the duration of time you don't have to say "okay hand" and it will think you are the user

rec_len = 3 # the maximum duration of each recording that should be transcribed

hand_address= '24:62:AB:F9:72:9E'  #  the address of the controller 

time_between_movements = 1.4  #  the time given to each movement to occure

words = ['close','open','pinch','catch','like',
         'victory','finger','point','pinky','hold']