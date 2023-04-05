#by Aaron Yang and Jake Hui
import time
import stdlib
import board
import adafruit_adxl37x
import busio
import math
#Initialize
dir(board)
i2c = busio.I2C(board.GP21, board.GP20)
accelerometer = adafruit_adxl37x.ADXL375(i2c)
accelerometer.offset = 0, 0, 0

#CALIBRATION
print("Hold accelerometer flat to set offsets to 0, 0, and -1g...") #ask user to lay down thing face up to zero values
time.sleep(2)
x = accelerometer.raw_x
y = accelerometer.raw_y
z = accelerometer.raw_z
print("Raw x: ", x)
print("Raw y: ", y)
print("Raw z: ", z)

accelerometer.offset = (
    round(-x / 4),
    round(-y / 4),
    round(-(z - 20) / 4),  # Z should be '20' at 1g (49mg per bit)
)
print("Calibrated offsets: ", accelerometer.offset) #change the calibrated offsets 

#global data
accel = [[0,0,0,0]]
global gx
global gy
global gz
gx = 0
gy = 0
gz = 0

def _readData():
    spreadsheet = open("values.txt", 'a')
    spreadsheet.write(accel[0], "\t", accel[1], "\t", accel[2], "\n")


def _get_accel(): #Get the acceleration values
    tempaccel_x = [0] #set arrays to be empty
    tempaccel_y = [0]
    tempaccel_z = [0]
    
    for i in range (0, 10): #read values 20 times
        #read acceleration
        imu_accel_x = accelerometer.raw_x
        imu_accel_y = accelerometer.raw_y
        imu_accel_z = accelerometer.raw_z

        #append acceleration into specific arrays
        tempaccel_x.append(imu_accel_x)
        tempaccel_y.append(imu_accel_y)
        tempaccel_z.append(imu_accel_z)

    sumaccel_x = 0 #weird idk but use to find average accelration out of the x samples
    for i in range(len(tempaccel_x)):
      sumaccel_x = sumaccel_x + tempaccel_x[i] #For x
    sumaccel_x = sumaccel_x/len(tempaccel_x)

    sumaccel_y = 0
    for i in range(len(tempaccel_y)):
      sumaccel_y = sumaccel_y + tempaccel_y[i] #For y
    sumaccel_y = sumaccel_y/len(tempaccel_y)

    sumaccel_z = 0
    for i in range(len(tempaccel_z)):
      sumaccel_z = sumaccel_z + tempaccel_z[i] #For z
    sumaccel_z = sumaccel_z/len(tempaccel_z)

    return sumaccel_x, sumaccel_y, sumaccel_z
    
def total_acceleration(sumx, sumy, sumz, gx, gy, gz):
    #for total acceleration must read original values to remove gravity
    for i in range (0, 20): #take average of multiple values
        gx = 0.9 * gx + 0.1 * accelerometer.raw_x #low pass filter that removes gravity from acceleration (x)
        imu_accel_x = accelerometer.raw_x - gx
        gy = 0.9 * gy + 0.1 * accelerometer.raw_y #low pass filter that removes gravity from acceleration (y)
        imu_accel_y = accelerometer.raw_y - gy
        gz = 0.9 * gz + 0.1 * accelerometer.raw_z #low pass filter that removes gravity from acceleration (z)
        imu_accel_z = accelerometer.raw_z - gz
    totalaccel = abs(math.sqrt(math.pow(sumx, 2) + math.pow(sumy, 2) + math.pow(sumz, 2))-18)
    return totalaccel
    

def find_orientation (sumx, sumy, sumz):
    orientation = 0
    #finds orientation but only when not moving
    if (abs(sumx) > abs(sumy)) and (abs(sumx) > abs(sumz)):
        orientation = 0  #racket side up
    elif (abs(sumy) > abs(sumx)) and (abs(sumy) > abs(sumz)):
        orientation = -50  #racket face flat
    elif (abs(sumz) > abs(sumx)) and (abs(sumz) > abs(sumy)):
        orientation = 50  #up and down (default calibraition)
                          
    # if acceleration is greater than gravity in any direction minus excess acceleration from current one to find orientation
#     print(orientation)
    
    return orientation


Flag = False
while Flag == False: # repeats getting acceleration until hit is recorded
    #LOOP FOR READING VALUES
    #ONLY VALUES GO IN LOOP
    sumx, sumy, sumz = _get_accel() #outputs: x, y, z
    #acceleration values = sumx, sumy, sumz
    sumaccel = total_acceleration(sumx, sumy, sumz, gx, gy, gz) #total acceleration
    #total acceleration is different because must remove gravity
    orientation = find_orientation(sumx, sumy, sumz)
    print (sumaccel, orientation)
    
    tempsum = [sumx, sumy, sumz]
    accel.append(tempsum)
 
#when hit leave loop and check other things
#GOOD HIT / BAD HIT USING MATH
#WHAT KIND OF HIT USING GRAVITY (always accelerating downwards at 9.8m/s^2)
#plot hit with acceleration and time
    



