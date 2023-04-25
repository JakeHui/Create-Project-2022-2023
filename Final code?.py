
import time
import stdlib
import board
import adafruit_adxl37x
import busio
import math
import os
#global data
accel = [0, 0, 0, 0, 0]
saveVal = [0]
global height
orient_list = [0,0,0,0,0,0,0,0,0,0,0,0,0,0]

def _get_accel(): #Get the acceleration values
    tempaccel_x = [0] #set arrays to be empty
    tempaccel_y = [0]
    tempaccel_z = [0]
    
    for i in range (0, 10): #read values 10 times
        #read acceleration
        imu_accel_x = accelerometer.raw_x
        imu_accel_y = accelerometer.raw_y
        imu_accel_z = accelerometer.raw_z

        #append acceleration into specific arrays
        tempaccel_x.append(imu_accel_x)
        tempaccel_y.append(imu_accel_y)
        tempaccel_z.append(imu_accel_z)

    return tempaccel_x, tempaccel_y, tempaccel_z

def _read_accel(tempaccel_x, tempaccel_y, tempaccel_z, accel, orient_list):
  
    sumaccel_x = 0 #use to find average accelration out of the x samples
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

    totalaccel = abs(math.sqrt(math.pow(sumaccel_x, 2) + math.pow(sumaccel_y, 2) + math.pow(sumaccel_z, 2))-20) #total acceleration in all directions
    
    orientation = "overhand"
    if (accel[-1] < 10): #if total acceleration is less than gravity, will still be able to read gravity and act like gyroscope
        #finds orientation but only when not moving
        if (abs(sumaccel_x) > abs(sumaccel_y)) and (abs(sumaccel_x) > abs(sumaccel_z)):
              orientation = "side"  #racket side up
        elif (abs(sumaccel_y) > abs(sumaccel_x)) and (abs(sumaccel_y) > abs(sumaccel_z)):
              orientation = "underhand"  #racket face flat
        elif (abs(sumaccel_z) > abs(sumaccel_x)) and (abs(sumaccel_z) > abs(sumaccel_y)):
              orientation = "overhand"  #up and down (default calibraition)          
    
    print (totalaccel, orientation)
    orient_list.append(orientation)

    accel.append(totalaccel)
    
    bool_hit = check_hit(accel, orient_list[-10], orient_list)
    if bool_hit:
        accel.clear()
        accel = [0,0,0,0,0]
        orient_list = [0,0,0,0,0,0,0,0,0,0,0,0,0,0]
        go_menu = input("Press 1 to return to menu or any other key to continue training. ")
        
        if go_menu == "1":
            menu()
            
    return orient_list, accel

#USER INTERFACE
def menu():
    print("\n\n\n\n\n\n\n\n\n\n\n\n")

    print("       Badminton Trainer       ")
    print("                               ")
    print("   Press 1 to start training   ")
    print("   Press 2 for instructions    ")
    print("   Press 3 for past data       ")
    print("   Press 4 to Exit             \n")

    decision = int(input("input: ")) #Get user input
    if decision == 2:
        print("Welcome to Badminton Trainer! This program is intended to assist you in improving your badminton skills by analyzing your hits.") 
        print("When the Trainer starts, the program will display information about the hit, such as speed, type of hit, and estimated distance.")
        print("Simply perform a hit to display data. You then have the option to return to menu and press 3 to view past logged data.")
        input("Press any key to return to menu.")
        menu()
    elif decision == 3:
        input("Press any key to return to menu.")
        menu()
    elif decision == 4:
        print("See you next time!")
        exit()
    
    orient_list = [0,0,0,0,0,0,0,0,0,0,0,0,0,0]
    flag = True
    while flag:
        try:
            height = int(input("What is your height (in centimeters)? "))
            flag = False
        except:
            print("Please type an integer." )
        
    return 0
  
def check_hit(accel, orientation, orient_list):
    max_accel = 0
    if accel[-1] > (accel[-5] + 50):#if acceleration is past 20m/s
        #read accelerometer data to get data after contact
        temp_x, temp_y, temp_z = _get_accel()
        orient_list, accel = _read_accel(temp_x, temp_y, temp_z, accel, orient_list)
        
        #determine maximum acceleration during hit (maximum acceleration in the entire array)
        for i in range(len(accel)):
            temp_max_accel = accel[i]
            if temp_max_accel > max_accel:
                max_accel = temp_max_accel
          
        
        
        #determine distance
        shoulder_height = 0.83333333*(height) #ratio of total height to shoulder height
        racket_length = 39 
        arm_length = 0.33333*(height) #ratio of total height to arm length
        
        #IN CENTIMETERS
        if orientation == "overhand":
            if max_accel > 30: #if smashing going down at a lower angle, smashing requires more speed
                h = shoulder_height + (racket_length + arm_length)*math.sin(math.pi/6)
                theta = 30
                dist = (math.pow(max_accel, 2) * math.pow(math.cos(theta*(math.pi)/180), 2) * math.tan(theta*(math.pi)/180) + math.sqrt(math.pow(max_accel, 4) * math.pow(math.cos(theta*(math.pi)/180), 4) * math.pow(math.tan(theta*(math.pi)/180), 2) - 64 * h * math.pow(max_accel, 2) * math.pow(math.cos(theta), 2))/32)
                dist1 = (math.pow(max_accel, 2) * math.pow(math.cos(theta*(math.pi)/180), 2) * math.tan(theta*(math.pi)/180) - math.sqrt(math.pow(max_accel, 4) * math.pow(math.cos(theta*(math.pi)/180), 4) * math.pow(math.tan(theta*(math.pi)/180), 2) - 64 * h * math.pow(max_accel, 2) * math.pow(math.cos(theta), 2))/32)
                if dist < dist1:
                    estimated_distance = dist
                elif dist > dist1:
                    estimated_distance = dist1
                else:
                    estimated_distance = (dist + dist1)/2
              
            else:
                h = shoulder_height + (racket_length + arm_length)*math.sin(15*(math.pi)/180)
                theta = 15
                dist = (math.pow(max_accel, 2) * math.pow(math.cos(theta*(math.pi)/180), 2) * math.tan(theta*(math.pi)/180) + math.sqrt(math.pow(max_accel, 4) * math.pow(math.cos(theta*(math.pi)/180), 4) * math.pow(math.tan(theta*(math.pi)/180), 2) - 64 * h * math.pow(max_accel, 2) * math.pow(math.cos(theta), 2))/32)
                dist1 = (math.pow(max_accel, 2) * math.pow(math.cos(theta*(math.pi)/180), 2) * math.tan(theta*(math.pi)/180) - math.sqrt(math.pow(max_accel, 4) * math.pow(math.cos(theta*(math.pi)/180), 4) * math.pow(math.tan(theta*(math.pi)/180), 2) - 64 * h * math.pow(max_accel, 2) * math.pow(math.cos(theta), 2))/32)
                if dist > dist1:
                    estimated_distance = dist
                elif dist < dist1:
                    estimated_distance = dist1
                else:
                    estimated_distance = (dist + dist1) / 2
          
        if orientation == "underhand":
            h = shoulder_height - (arm_length + racket_length)*math.sin(40*(math.pi)/180)
            theta = 40
            dist = (math.pow(max_accel, 2) * math.pow(math.cos(theta*(math.pi)/180), 2) * math.tan(theta*(math.pi)/180) + math.sqrt(math.pow(max_accel, 4) * math.pow(math.cos(theta*(math.pi)/180), 4) * math.pow(math.tan(theta*(math.pi)/180), 2) - 64 * h * math.pow(max_accel, 2) * math.pow(math.cos(theta), 2))/32)
            dist1 = (math.pow(max_accel, 2) * math.pow(math.cos(theta*(math.pi)/180), 2) * math.tan(theta*(math.pi)/180) - math.sqrt(math.pow(max_accel, 4) * math.pow(math.cos(theta*(math.pi)/180), 4) * math.pow(math.tan(theta*(math.pi)/180), 2) - 64 * h * math.pow(max_accel, 2) * math.pow(math.cos(theta), 2))/32)
            if dist > dist1:
                estimated_distance = dist
            elif dist < dist1:
                estimated_distance = dist1
            else:
                estimated_distance = (dist + dist1) / 2
          
        if orientation == "side":
            h = shoulder_height
            theta = 0
            dist = (math.pow(max_accel, 2) * math.pow(math.cos(theta*(math.pi)/180), 2) * math.tan(theta*(math.pi)/180) + math.sqrt(math.pow(max_accel, 4) * math.pow(math.cos(theta*(math.pi)/180), 4) * math.pow(math.tan(theta*(math.pi)/180), 2) - 64 * h * math.pow(max_accel, 2) * math.pow(math.cos(theta), 2))/32)
            dist1 = (math.pow(max_accel, 2) * math.pow(math.cos(theta*(math.pi)/180), 2) * math.tan(theta*(math.pi)/180) - math.sqrt(math.pow(max_accel, 4) * math.pow(math.cos(theta*(math.pi)/180), 4) * math.pow(math.tan(theta*(math.pi)/180), 2) - 64 * h * math.pow(max_accel, 2) * math.pow(math.cos(theta), 2))/32)
            if dist  > dist1:
                estimated_distance = dist
            elif dist < dist1:
                estimated_distance = dist1
            else:
                estimated_distance = (dist + dist1) / 2
          
        #print data for user
        try:
          print("Maximum Acceleration During Hit: ", max_accel)
          print("Type of Hit: ", orientation)
          print("Estimated distance: ") 
        except:
          print("Maximum Acceleration During Hit: N/A")
          print("Type of Hit: N/A")
          print("Estimated distance: N/A")

        #saveVal.append(max_accel, orientation, estimated_distance) #record data for user to view later
        accel.clear() #clears the array of read values to prevent overload
        accel = [0,0,0,0,0]
    
        return True 
    else:
        return False #if else do nothing and loop again


#INITIALIZE
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
    
#THE FIRST CALL (ORIENTATION = FLAT) (ACCELERATION ISNT MOVING)
_get_accel()
orient_list, accel = _read_accel(tempaccel_x, tempaccel_y, tempaccel_z, accel, orient_list)
if orient_list[-1] is not "side":
  	print("Please calibrate with racket flat. ")
orient_list = [0,0,0,0,0,0,0,0,0,0,0,0,0,0]

#MAIN CODE
height = 0
while 1:
    menu()
    Flag = False
    while Flag == False: 
        #LOOP FOR READING VALUES
        #ONLY VALUES GO IN LOOP
        temp_x, temp_y, temp_z = _get_accel() #outputs: x, y, z
        #acceleration values = sumx, sumy, sumz
        orient_list, accel = _read_accel(temp_x, temp_y, temp_z, accel, orient_list)
#     Flag = running_menu() #print current values for user
     
#when hit leave loop and check other things
#GOOD HIT / BAD HIT USING MATH
#WHAT KIND OF HIT USING GRAVITY (always accelerating downwards at 9.8m/s^2)
#plot hit with acceleration and time
    









