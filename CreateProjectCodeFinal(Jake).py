#Badminton Trainer
import time
import stdlib
import board
import adafruit_adxl37x
import busio
import math
import os
import sys

#global data
accel = [20, 20, 20, 20, 20 ,20 ,20 ,20 ,20, 20, 20, 20, 20] #array for the acceleration data (starts at combined gravity)
global height #height of player (taken as input)
orient_list = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0] #tracks orientation of racket over time
tempaccel_x = [0] #set temporary acceleration arrays to be empty
tempaccel_y = [0]
tempaccel_z = [0]
saved_data = ["N/A"] #array of past hits can be accessed from the menu
maxacl = "N/A" 
ornt = "N/A"
edis = "N/A"
save = "N/A"
orientation = "overhand" 

def _get_accel(): #Get the acceleration values
    tempaccel_x = [0] #set arrays to be empty
    tempaccel_y = [0]
    tempaccel_z = [0]
    imu_accel_x = 0
    imu_accel_y = 0
    imu_accel_z = 0
    for i in range (0, 10): #read values 10 times
        #read acceleration of 3 axis from accelerometer
        imu_accel_x = accelerometer.raw_x 
        imu_accel_y = accelerometer.raw_y
        imu_accel_z = accelerometer.raw_z

        #append acceleration into specific arrays
        tempaccel_x.append(imu_accel_x)
        tempaccel_y.append(imu_accel_y)
        tempaccel_z.append(imu_accel_z)

    return tempaccel_x, tempaccel_y, tempaccel_z



#This Function Done By Partner
#Start
def _read_accel(tempaccel_x, tempaccel_y, tempaccel_z, accel, orient_list, saved_data):
    
    sumaccel_x = 0 #use to find average acceleration out of the x samples
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

    totalaccel = abs(math.sqrt(math.pow(sumaccel_x, 2) + math.pow(sumaccel_y, 2) + math.pow(sumaccel_z, 2))-20) #combine axis
    
    orientation = "overhand" #placeholder value (racket should be calibrated at this)
    if (accel[-1] < 10): #if total acceleration is less than gravity, will still be able to read gravity and act like gyroscope
        #finds orientation with direction gravity is pulling
        if (abs(sumaccel_x) > abs(sumaccel_y)) and (abs(sumaccel_x) > abs(sumaccel_z)):
              orientation = "side"  #racket side up
        elif (abs(sumaccel_y) > abs(sumaccel_x)) and (abs(sumaccel_y) > abs(sumaccel_z)):
              orientation = "underhand"  #racket face flat
        elif (abs(sumaccel_z) > abs(sumaccel_x)) and (abs(sumaccel_z) > abs(sumaccel_y)):
              orientation = "overhand"  #up and down (default calibraition)          
    
    print (totalaccel, str(orientation)) #for the built-in graphing 
    
    orient_list.append(orientation) #list so that the orientation at the beginning of a swing can be accessed
    
    accel.append(totalaccel)

    bool_hit = check_hit(accel, orient_list, saved_data) #check_hit returns true or false based on if it detects a spike in acceleration
    if bool_hit:
        accel.clear() #save memory on Raspberry Pi Pico
        accel = [20, 20, 20, 20, 20 ,20 ,20 ,20 ,20, 20, 20, 20, 20]
        orient_list = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
        print("\n")
        go_menu = input("Press 1 to return to menu or any other key to continue training. ") #ask user if they want to continue
        print("\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n")
    
        if go_menu == "1": #return to menu
            menu(saved_data)
        else:
            go_menu = "0" #continue tracking data
            
    bool_hit = False

    return orient_list, accel, saved_data
#End




#USER INTERFACE
def menu(saved_data):
    print("\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n")

    print("       Badminton Trainer       ")
    print("                               ")
    print("   Press 1 to start training   ")
    print("   Press 2 for instructions    ")
    print("   Press 3 for past data       ")
    print("   Press 4 to Exit             \n")
    
    flag1 = True
    while flag1:
        try:
            decision = int(input("input: ")) #Get user choice
            flag1 = False
        except:
            print("Please type an integer. " )
    
    if decision == 2: #instructions
        print("\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n")
        print("Welcome to Badminton Trainer! This program is intended to assist you in improving your badminton skills by analyzing your hits.") 
        print("When the Trainer starts, the program will display information about the hit, such as speed, type of hit, and estimated distance.")
        print("Simply perform a hit to display data. You then have the option to return to menu and press 3 to view past logged data.")
        input("Press any key to return to menu.")
        menu(saved_data)
        
    elif decision == 3: #display past data
        for i in range(len(saved_data)): 
            print(saved_data[i], "\n")
        input("Press any key to return to menu. ")
        menu(saved_data)
        
    elif decision == 4: #exit program
        print("See you next time!")
        sys.exit("See you next time!")   
    
    orient_list = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
    if decision == 1:
        flag = True
        while flag:
            try:
                time.sleep(0.5)
                height = int(input("What is your height (in centimeters)? ")) #get user height for distance calculations later in check_hit
                flag = False
            except:
                print("Please type an integer. " )
        
    return 0
  
def check_hit(accel, orient_list, saved_data): 
    orientation = orient_list[-20] #reference the orientation at the beginning of the hit
    max_accel = 0 
    estimated_distance = 0 
    if accel[-1] > (accel[-5] + 40): #if acceleration is past 40m/s
        time.sleep(0.25) #buffer to prevent pyStack overload
        
        #read accelerometer data to get data after contact
        temp_x, temp_y, temp_z = _get_accel()
        orient_list, accel, saved_data = _read_accel(temp_x, temp_y, temp_z, accel, orient_list, saved_data)
        
        #determine maximum acceleration during hit (maximum acceleration in the entire array)
        for i in range(len(accel)):
            temp_max_accel = accel[i]
            if temp_max_accel > max_accel:
                max_accel = temp_max_accel
          
        #determine distance
        shoulder_height = 0.83333333*(height) #ratio of total height to shoulder height
        racket_length = 39 
        arm_length = 0.33333*(height) #ratio of total height to arm length
        
        #Type of hit
        if orientation == "overhand":
            if max_accel > 200: #if smashing going down at a lower angle, smashing requires more speed
                orientation = "overhand smash"
                h = shoulder_height + (racket_length + arm_length)*math.sin(math.pi/6)
                theta = 80
                #parmetric calculations
                dist = round((math.pow(max_accel, 2) * math.pow(math.cos(theta*(math.pi)/180), 2) * math.tan(theta*(math.pi)/180) + math.sqrt(math.pow(max_accel, 4) * math.pow(math.cos(theta*(math.pi)/180), 4) * math.pow(math.tan(theta*(math.pi)/180), 2) - 64 * h * math.pow(max_accel, 2) * math.pow(math.cos(theta), 2))/32))
                dist1 = round((math.pow(max_accel, 2) * math.pow(math.cos(theta*(math.pi)/180), 2) * math.tan(theta*(math.pi)/180) - math.sqrt(math.pow(max_accel, 4) * math.pow(math.cos(theta*(math.pi)/180), 4) * math.pow(math.tan(theta*(math.pi)/180), 2) - 64 * h * math.pow(max_accel, 2) * math.pow(math.cos(theta), 2))/32))
                if dist < dist1: #formula returns 2 values, find greater of the 2
                    estimated_distance = dist /20
                elif dist > dist1:
                    estimated_distance = dist1 /20
                else:
                    estimated_distance = (dist + dist1)/2
              
            else:
                h = shoulder_height + (racket_length + arm_length)*math.sin(15*(math.pi)/180)
                theta = 20
                dist = round((math.pow(max_accel, 2) * math.pow(math.cos(theta*(math.pi)/180), 2) * math.tan(theta*(math.pi)/180) + math.sqrt(math.pow(max_accel, 4) * math.pow(math.cos(theta*(math.pi)/180), 4) * math.pow(math.tan(theta*(math.pi)/180), 2) - 64 * h * math.pow(max_accel, 2) * math.pow(math.cos(theta), 2))/32))
                dist1 = round((math.pow(max_accel, 2) * math.pow(math.cos(theta*(math.pi)/180), 2) * math.tan(theta*(math.pi)/180) - math.sqrt(math.pow(max_accel, 4) * math.pow(math.cos(theta*(math.pi)/180), 4) * math.pow(math.tan(theta*(math.pi)/180), 2) - 64 * h * math.pow(max_accel, 2) * math.pow(math.cos(theta), 2))/32))
                if dist > dist1:
                    estimated_distance = dist /6
                elif dist < dist1:
                    estimated_distance = dist1 /6
                else:
                    estimated_distance = (dist + dist1) / 2
          
        if orientation == "underhand":
            h = shoulder_height - (arm_length + racket_length)*math.sin(40*(math.pi)/180)
            theta = 15
            dist = round((math.pow(max_accel, 2) * math.pow(math.cos(theta*(math.pi)/180), 2) * math.tan(theta*(math.pi)/180) + math.sqrt(math.pow(max_accel, 4) * math.pow(math.cos(theta*(math.pi)/180), 4) * math.pow(math.tan(theta*(math.pi)/180), 2) - 64 * h * math.pow(max_accel, 2) * math.pow(math.cos(theta), 2))/32))
            dist1 = round((math.pow(max_accel, 2) * math.pow(math.cos(theta*(math.pi)/180), 2) * math.tan(theta*(math.pi)/180) - math.sqrt(math.pow(max_accel, 4) * math.pow(math.cos(theta*(math.pi)/180), 4) * math.pow(math.tan(theta*(math.pi)/180), 2) - 64 * h * math.pow(max_accel, 2) * math.pow(math.cos(theta), 2))/32))
            if dist > dist1:
                estimated_distance = dist /6
            elif dist < dist1:
                estimated_distance = dist1 /6
            else:
                estimated_distance = (dist + dist1) / 2
          
        if orientation == "side":
            h = shoulder_height
            theta = 5
            dist = round((math.pow(max_accel, 2) * math.pow(math.cos(theta*(math.pi)/180), 2) * math.tan(theta*(math.pi)/180) + math.sqrt(math.pow(max_accel, 4) * math.pow(math.cos(theta*(math.pi)/180), 4) * math.pow(math.tan(theta*(math.pi)/180), 2) - 64 * h * math.pow(max_accel, 2) * math.pow(math.cos(theta), 2))/32))
            dist1 = round((math.pow(max_accel, 2) * math.pow(math.cos(theta*(math.pi)/180), 2) * math.tan(theta*(math.pi)/180) - math.sqrt(math.pow(max_accel, 4) * math.pow(math.cos(theta*(math.pi)/180), 4) * math.pow(math.tan(theta*(math.pi)/180), 2) - 64 * h * math.pow(max_accel, 2) * math.pow(math.cos(theta), 2))/32))
            if dist  > dist1:
                estimated_distance = dist /1.8
            elif dist < dist1:
                estimated_distance = dist1 /1.8
            else:
                estimated_distance = (dist + dist1) / 2
          
        estimated_distance = estimated_distance/100
        #print data for user
        try:
          print("\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n")
          maxacl = "Maximum Acceleration During Hit: " + str(max_accel) + "m/s" #concatenate string for user interface
          print(maxacl)
          ornt = "Type of Hit: "+ str(orientation)
          print(ornt)
          edis = "Estimated distance: "+ str(estimated_distance)+ " Meters"
          print(edis)
        
          save = maxacl + "\n" + ornt + "\n" + edis + "\n"
          saved_data.append(save) #array that is returned to menu and can be accessed to view past logs
          
        except: #if there is no data
          print("Maximum Acceleration During Hit: N/A")
          print("Type of Hit: N/A")
          print("Estimated distance: N/A")
     
        accel.clear() #clears the array of read values to prevent overload
        accel = [20, 20, 20, 20, 20 ,20 ,20 ,20 ,20, 20, 20, 20, 20]
        return True 
    else:
        return False #if else do nothing and loop again

#INITIALIZE
dir(board)
i2c = busio.I2C(board.GP21, board.GP20)
accelerometer = adafruit_adxl37x.ADXL375(i2c)
accelerometer.offset = 0, 0, 0

#CALIBRATION (Used documentation from adafruit adxl 375 library for this part)
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
    
    
    
#THE FIRST CALL
_get_accel()
orient_list, accel, saved_data = _read_accel(tempaccel_x, tempaccel_y, tempaccel_z, accel, orient_list, saved_data)

#CHECK THAT (ORIENTATION = FLAT) (ACCELERATION ISNT MOVING)
if (orient_list[-1] is not "overhand") and (check_hit(accel, orientation, orient_list, saved_data) == False): 
    print("Please calibrate with racket flat and not moving. ")
orient_list = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]


#MAIN CODE
height = 0
while 1: 
    menu(saved_data)
    #LOOP TO CONTINUOUSLY READ VALUES
    Flag = False
    while Flag == False:  
        #ONLY VALUES GO IN LOOP
        temp_x, temp_y, temp_z = _get_accel() #outputs: x, y, z
        #acceleration values = sumx, sumy, sumz
        orient_list, accel, saved_data = _read_accel(temp_x, temp_y, temp_z, accel, orient_list, saved_data)




