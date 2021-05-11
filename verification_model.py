import warnings
import numpy as np

from assistance.functions import *

np.seterr(divide='ignore', invalid='ignore')
with warnings.catch_warnings():
    warnings.simplefilter("ignore", category=RuntimeWarning)    
       
    while True:
        choice=int(input("\n 1.Record audio for training \n 2.Record audio for testing \n 3.check similarity \n"))
        if(choice==1):
            record_audio_train()
        elif(choice==2):
            record_audio_test()
        elif(choice==3):
            training_testing_set()
        if(choice>3):
            exit()