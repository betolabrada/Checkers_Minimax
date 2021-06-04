#------------------------------------------------------------------------------------------------------------------
#   PSD analysis of gyro data.
#------------------------------------------------------------------------------------------------------------------
import time
import socket
import matplotlib.animation as animation
import matplotlib.pyplot as plt

from scipy import signal

# Socket configuration
UDP_IP = '192.168.1.83'
UDP_PORT = 8000
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind((UDP_IP, UDP_PORT))
sock.settimeout(0.001)

# Signal properties
samp_count = 0
samp_rate = 16.5
samps_per_frame = int(samp_rate*2)

# Initialize plots
fig, (ax1, ax2) = plt.subplots(2)

# Animation function
def animate(i, t, y):

    # Read data from socket buffer
    global samp_count
    
    count = 0
    while True:
        try:
            data, addr = sock.recvfrom(1024*1024)                     
            data_string = data.decode('ascii').split(",")
            nsensors = (len(data_string)-1)/4          
            
            for ind in range(1, len(data_string), 4):
                type =  int(data_string[ind])
                if type == 4:
                    y.append(float(data_string[ind+1]))               
                    t.append(samp_count/samp_rate)
                    samp_count+=1
                    count+=1
                        
            
        except socket.timeout:
            break;            
    
    if count > 0: 
        
        # Limit t and y lists        
        t = t[-samps_per_frame:]
        y = y[-samps_per_frame:]
        
        # Plot data
        ax1.clear()                
        ax1.plot(t, y)       
        ax1.set_ylim((-10, 10))
        ax1.set_xlabel('Time (s)')
        ax1.set_ylabel('Gyro x')        

        f, psd = signal.periodogram(y, samp_rate, 'flattop', scaling='spectrum')

        ax2.clear()
        ax2.plot(f, psd)
        ax2.set_ylim((0, 40))
        ax2.set_xlabel('Frequency (Hz)')
        ax2.set_ylabel('PSD')
          
        fig.suptitle('PSD analysis of gyroscope Data')

# Run animation
t = []
y = []
ani = animation.FuncAnimation(fig, animate, fargs=(t, y), interval=100)
plt.show()
