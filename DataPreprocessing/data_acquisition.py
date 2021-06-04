#------------------------------------------------------------------------------------------------------------------
#   Data acquisition program.
#------------------------------------------------------------------------------------------------------------------
import time
import socket
import struct
import random
import numpy as np

# Experiment configuration
conditions = [('Left', 1), ('Right', 2), ('Up', 3), ('Down', 4)]
n_trials = 4

fixation_cross_time = 5
preparation_time = 2
training_time = 30
rest_time = 5

# Experiment stages
trials = n_trials*conditions
random.shuffle(trials)

experiment = []
for tr in trials:
    experiment.append( ("*********", fixation_cross_time, 0) )
    experiment.append( (tr[0], preparation_time, 0) )
    experiment.append( ('', training_time, tr[1]) )
    experiment.append( ('Rest', rest_time, -1) )

# Socket configuration
UDP_IP = '192.168.1.72'
UDP_PORT = 8000
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind((UDP_IP, UDP_PORT))
sock.settimeout(0.001)

# Data acquisition loop
acc_data = []
acc_trials = []
acc_start = 0

gyro_data = []
gyro_trials = []
gyro_start = 0

mag_data = []
mag_trials = []
mag_start = 0

trial_id = 0

update_time = 0

step = -1

start_time = time.time()
while True:
        
    ellapsed_time = time.time() - start_time;    
    if ellapsed_time >= update_time:

        step = step + 1        

        if step < len(experiment):
            start_time = time.time()        
            print(experiment[step][0])
            update_time = experiment[step][1]

            if experiment[step][2] > 0:
                trial_id = experiment[step][2]
                acc_start = len(acc_data)
                gyro_start = len(gyro_data)
                mag_start = len(mag_data)

            elif experiment[step][2] == -1:                
                acc_trials.append([trial_id, acc_start, len(acc_data)])
                gyro_trials.append([trial_id, gyro_start, len(gyro_data)])
                mag_trials.append([trial_id, mag_start, len(mag_data)])

        else:
            break

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
                acc_data.append([float(data_string[ind+1]), float(data_string[ind+2]), 
                                 float(data_string[ind+3])])
            elif type == 4:
                gyro_data.append([float(data_string[ind+1]), float(data_string[ind+2]), 
                                 float(data_string[ind+3])])
            elif type == 5:
                mag_data.append([float(data_string[ind+1]), float(data_string[ind+2]), 
                                 float(data_string[ind+3])])
                
    except socket.timeout:
        pass

print('end')    

np.savetxt('acc_trials.txt', np.array(acc_trials), fmt='%d')
np.savetxt('gyro_trials.txt', np.array(gyro_trials), fmt='%d')
np.savetxt('mag_trials.txt', np.array(mag_trials), fmt='%d')

np.savetxt('acc_data.txt', np.array(acc_data))
np.savetxt('gyro_data.txt', np.array(gyro_data))
np.savetxt('mag_data.txt', np.array(mag_data))

input()