import serial
import time
from sds011lib import SDS011QueryReader	
from Adafruit_IO import Client

print("starting to collect data!")

aio = Client('muldy07', 'INSERT ADAFRUIT SECRET CODE HERE') # set aio client
feed_twofive = aio.feeds('airsensor-feed') # this is the key for the database?
feed_ten = aio.feeds('aberoomten')  # PM 10 pollutant

# Create a query mode reader.
reader = SDS011QueryReader('/dev/ttyUSB0')

# Set the working period to every 2 minutes
reader.set_working_period(2) # sensor will turn on and retrieve data  every 2 minutes, much better solution for turning off
#  dont think data points are that conclusive

time.sleep(30) # let the sensor get up to speed
print("starting data collection")

# Query for some data
result = reader.query()
queue = reader.query()
print(f"PM 2.5: {result.pm25}")
print(f"PM 10: {result.pm10}")

# Check the current working period
result_period = reader.get_working_period()
print(result_period.interval)

i =  0
while  True:
	result = reader.query()
	# print(f"PM 2.5: {result.pm25}")
	# print(f"PM 10: {result.pm10}")
	
	# test the queue
	# print(f"QUEUE: PM 2.5: {queue.pm25}")
	# print(f"QUEUE: PM 10: {queue.pm10}")
	
	
	if result == queue: # test if there is a new data  point
		print("no new data:", i)
		time.sleep(30) # wait for new data
		i = i + 1
		continue
	
	i =  0 	
	# print the new data
	print(f"PM 2.5: {result.pm25}")	# print the new data point
	print(f"PM 10: {result.pm10}")
	queue = reader.query()
	
	# send the data  to Adafruit
	print("sending Adafruit data")
	pmtwofive = float(result.pm25) # easy to send data, just needs to be a number
	aio.send_data(feed_twofive.key, pmtwofive) # this is a different command now
	pmten = float(result.pm10)
	aio.send_data(feed_ten.key, pmten)
	time.sleep(2)
	


