import serial
import matplotlib.pyplot as plt
import datetime

time_window = 5
ser = serial.Serial('COM4', 9600)  
plt.ion() 
fig, ax = plt.subplots()
line, = ax.plot([], [])  #
ax.set_xlabel('Time')  
ax.set_ylabel('Y Label')
ax.set_title('Real-time Plot') 
plt.show()
x_data = []
y_data = []

while True:
    try:
        data = ser.read(4).decode().rstrip()
        ser.timeout = 0.01 
        print(data)
        y= float(data)/8
        x = datetime.datetime.now()
        x_data.append(x)
        y_data.append(y)
        while (x_data[-1] - x_data[0]).total_seconds() > time_window:
            x_data.pop(0)
            y_data.pop(0)
        line.set_data(x_data, y_data)
        ax.relim() 
        ax.autoscale_view(True, True, True)
        plt.draw() 
        plt.pause(0.001)
    except KeyboardInterrupt:
        break
ser.close()
plt.ioff()
plt.close()