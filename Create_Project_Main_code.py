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

def _readData():
    spreadsheet = open("values.txt", 'a')
    spreadsheet.write(accel[0], "\t", accel[1], "\t", accel[2], "\n")


def _get_accel(): #Get the acceleration values
    tempaccel_x = [0] #set arrays to be empty
    tempaccel_y = [0]
    tempaccel_z = [0]
    gx = 0
    gy = 0
    gz = 0
    
    for i in range (0, 10): #read values 20 times
        #read acceleration
#         gx = 0.6 * gx + 0.4 * accelerometer.raw_x #low pass filter that removes gravity from acceleration (x)
        imu_accel_x = accelerometer.raw_x - gx
#         gy = 0.6 * gy + 0.4 * accelerometer.raw_y #low pass filter that removes gravity from acceleration (y)
        imu_accel_y = accelerometer.raw_y - gy
#         gz = 0.6 * gz + 0.4 * accelerometer.raw_z #low pass filter that removes gravity from acceleration (z)
        imu_accel_z = accelerometer.raw_z - gz

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

    totalaccel = math.sqrt(math.pow(sumaccel_x, 2) + math.pow(sumaccel_y, 2) + math.pow(sumaccel_z, 2))  #calculate total acceleration
    
    orientation = 0
    #finds orientation
    if (abs(sumaccel_x) > abs(sumaccel_y)) and (abs(sumaccel_x) > abs(sumaccel_z)):
        orientation = 0  #racket side up
    elif (abs(sumaccel_y) > abs(sumaccel_x)) and (abs(sumaccel_y) > abs(sumaccel_z)):
        orientation = -50  #racket face flat
    elif (abs(sumaccel_z) > abs(sumaccel_x)) and (abs(sumaccel_z) > abs(sumaccel_y)):
        orientation = 50  #up and down (default calibraition)
                                                  
    print(sumaccel_x, sumaccel_y, sumaccel_z,orientation)

        
    return sumaccel_x, sumaccel_y, sumaccel_z #return variables


def _check_hit(accel):
    #check using math wheter the thing has been hit or not
    #MATH
    if ():
        return True
    else:
        return False

Flag = False
while Flag == False: # repeats getting acceleration until hit is recorded
    sumx, sumy, sumz = _get_accel() #outputs: x, y, z, total
    tempsum = [sumx, sumy, sumz]
    accel.append(tempsum)
    Flag = _check_hit(accel)
 
#when hit leave loop and check other things
#GOOD HIT / BAD HIT USING MATH
#WHAT KIND OF HIT USING GRAVITY (always accelerating downwards at 9.8m/s^2)
#plot hit with acceleration and time
    




