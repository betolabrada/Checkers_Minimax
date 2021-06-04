#------------------------------------------------------------------------------------------------------------------
#   Real time processing of mobile sensor data.
#------------------------------------------------------------------------------------------------------------------
import time
import socket
import struct
import numpy as np
from scipy import stats
from scipy import signal
import classification

# Socket configuration
UDP_IP = '192.168.1.72'
UDP_PORT = 8000
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind((UDP_IP, UDP_PORT))
sock.settimeout(0.001)

# Processing parameters
fs = 500                            # Sampling rate
win_length = 0.1                    # Window length in seconds
win_samps = int(fs*win_length)      # Number of samples per window

# Data acquisition loop
data_buffer = []

start_time = time.time()
start_time2 = start_time;
update_time = 0.25
while True:
        
    try:
        # Read data from UDP connection
        data, addr = sock.recvfrom(1024*1024)      

        # Decode binary stream. 
        data_string = data.decode('ascii').split(",")

        # Append new sensor data
        nsensors = (len(data_string)-1)/4

        for ind in range(1, len(data_string), 4):
            type =  int(data_string[ind])

            if type == 3:
                data_buffer.append([float(data_string[ind+1]), float(data_string[ind+2]), float(data_string[ind+3])])

    except socket.timeout:
        pass

    ellapsed_time = time.time() - start_time;    
    if ellapsed_time > update_time and len(data_buffer) >= win_samps:

        start_time = time.time()        

        # Get last window
        win_data = np.array(data_buffer[-win_samps:])        
        nsignals = win_data.shape[1]
        #print('Last window', win_data)

        # Calculate features
        # The feature vector contains the following elements:
        # Avex, Stdx, Kurtosisx, Skewnesx, Avey, Stdy, Kurtosisy, Skewnesy, Avez, Stdz, Kurtosisz, Skewnesz
        features = []
        for k in range(nsignals):
            features.append(np.average(win_data[:,k]))
            features.append(np.std(win_data[:,k]))
            features.append(stats.kurtosis(win_data[:,k]))
            features.append(stats.skew(win_data[:,k]))            
            
            #freqs, psd = signal.periodogram(win_data[:,k], fs, 'hamming', scaling='spectrum')            
            #features.extend(psd.tolist())

        #print('Features: ', features)

        x_temp = [0] * classification.data_size
        x = []

        # Map data
        nresults = 4
        i = 0
        for result in range(nresults):
            for signal in range(nsignals):
                x_temp[i] = features[result + (nresults * signal)]
                i = i + 1

        x.append(x_temp)

        x = np.array(x)
        #print("x: ", x)

        x_test = x[[i for i in range(len(x))], :]
        y_pred = classification.clf.predict(x_test)
        print('y_pred', y_pred)
        #time.sleep(5)

#------------------------------------------------------------------------------------------------------------------
#   End of file
#------------------------------------------------------------------------------------------------------------------