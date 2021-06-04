#------------------------------------------------------------------------------------------------------------------
#   Real-time plot of acceleration data.
#------------------------------------------------------------------------------------------------------------------
import time
import socket
import matplotlib.animation as animation
import matplotlib.pyplot as plt

# Socket configuration
UDP_IP = '192.168.1.83'
UDP_PORT = 8000
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind((UDP_IP, UDP_PORT))
sock.settimeout(0.001)

# Signal properties
samp_count = 0
samp_rate = 50
samps_per_frame = int(samp_rate*2)

# Initialize plots
fig, (ax1, ax2, ax3) = plt.subplots(3)

# Animation function
def animate(i, t, y1, y2, y3):

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
                if type == 3:
                    y1.append(float(data_string[ind+1]))
                    y2.append(float(data_string[ind+2]))
                    y3.append(float(data_string[ind+3]))                    
                    t.append(samp_count/samp_rate)
                    samp_count+=1
                    count+=1
                        
            
        except socket.timeout:
            break;            
    
    if (count > 0): 
        
        # Limit t and y lists        
        t = t[-samps_per_frame:]
        y1 = y1[-samps_per_frame:]
        y2 = y2[-samps_per_frame:]
        y3 = y3[-samps_per_frame:]
        
        # Plot data
        ax1.clear()                
        ax1.plot(t, y1)       
        ax1.set_ylim((-20, 20))
        ax1.set_ylabel('Acc x')

        ax2.clear()
        ax2.plot(t, y2)
        ax2.set_ylim((-20, 20))
        ax2.set_ylabel('Acc y')

        ax3.clear()
        ax3.plot(t, y3)
        ax3.set_ylim((-20, 20))
        ax3.set_ylabel('Acc z')
        ax3.set_xlabel('Time (s)')
            
        fig.suptitle('Acceleration data')

# Run animation
t = []
y1 = []
y2 = []
y3 = []
ani = animation.FuncAnimation(fig, animate, fargs=(t, y1, y2, y3), interval=100)
plt.show()
