import pickle
from PIL import Image
from io import BytesIO
import time
import matplotlib.pyplot as plt

with open('information.pkl', 'rb') as file:
    information = pickle.load(file)

distances = []
time = []
for message in information['information']['sensor_messages']:
    if message['sensor_type'] == 'image':
        img = Image.open(message['sensor_reading'], formats=['JPEG'])
        img.show()
    else:
       distances.append(message['sensor_reading'])
       time.append(message['time'])
       
plt.plot(time, distances, marker='o', linestyle='-')

# Add labels and a title
plt.xlabel('Time')
plt.ylabel('Distance')
plt.title('Distance Sensor Reading')

# Show the plot
plt.show()