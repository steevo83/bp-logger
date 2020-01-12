'''
Created on Mar 14, 2019

@author: Steevo
'''
#*** Using Omron HEM-RML31 cuff for getting BP/Pulse results, digital scale for weight measurements***

#TESTING GIT
# Want to add individual results -- Create new DB for new users and edit personal ones for returning users.


import time as tm
import statistics as st
import datetime as dt
import matplotlib.pyplot as plt
from matplotlib import style
#import matplotlib.dates as mdates
#import pytz
#from pytz.reference import Eastern
from pytz import timezone
from tzlocal import get_localzone
import pandas as pd
from astropy.wcs.docstrings import bp
from twisted.conch.test.test_helper import HEIGHT
pd.set_option("display.max_columns", 20)
#import re

style.use('fivethirtyeight')

'''name=input("Name: ")
dob=input("Date of Birth: ")'''


source = 'Blood_Pressure_Readings.csv'
users = {'Steven Ormosi': source}
bp_reading = {'DateTime':[],
              'Systolic':[],
              'Diastolic':[],
              'Pulse':[],
              'Weight':[],
              'Notes':[],
              }

am_bp = []
pm_bp = []

master = pd.read_csv(source)
master = master.set_index('DateTime', drop=False)

'''def update():
    global bp_reading
    bp_reading = {'DateTime':[],
                  'Systolic':[],
                  'Diastolic':[],
                  'Pulse':[],
                  'Weight':[],
                  'Notes':[],
                  }'''

for x in master['DateTime']:
    bp_reading['DateTime'].append(x)

for x in master['Systolic']:
    bp_reading['Systolic'].append(x)

for x in master['Diastolic']:
    bp_reading['Diastolic'].append(x)

for x in master['Pulse']:
    bp_reading['Pulse'].append(x)

for x in master['Weight']:
    bp_reading['Weight'].append(x)

for x in master['Notes']:
    bp_reading['Notes'].append(x)

'''
!!!MIGHT NEED THIS LATER!!!
    def am_or_pm():
    for x in bp_reading['DateTime']:
        am_pm = re.split('-|:| ', x)
        if(int(am_pm[4]) >= 0 and int(am_pm[4]) <= 12):
            am_bp.append(x)
        elif(int(am_pm[4]) > 12 and int(am_pm[4]) <= 23):
            pm_bp.append(x)
        else:
            print("Error!")


print (am_bp)
am_or_pm()
print (am_bp)
print (pm_bp)
dfam = pd.DataFrame(am_bp)
dfpm = pd.DataFrame(pm_bp)
print(dfam.head(), dfpm.head())



        !!!WIP!!!
        elif(choice == '4'):
            am = df[ (re.split('-|:| ', df.index) <= 12) ] #might need to do this before declaring DateTime the index?
            print(am.head())
!!!MIGHT NEED THIS LATER!!!
'''

class bp_reader(object):

    def Mod(self):
        #update()
        opts = []

        for num, name in enumerate(bp_reading, 1): #Get tuples of index location and items in bp_reading
            print("["+str(num)+"]", name)
            opts.append(name)
        print("[E] Exit to Main Menu")
        mod = input("What would you like to modify? (Enter Number) >> ")
        if(mod.lower() == 'e'):
            self.main()
        elif(int(mod) <= len(bp_reading) and int(mod) > 0):
            chosen = opts[int(mod)-1]
            temp_cols = {"Date": bp_reading['DateTime'], chosen: bp_reading[chosen]}
            temp_df = pd.DataFrame(temp_cols)
            print(temp_df)
            tm.sleep(1.5)
            adj = input("Using the above given indexes, please indicate which number row you would like to adjust. >> ")
            adjint = int(adj)
            if(adjint <= len(bp_reading[chosen])):
                swap = input("What do you want to change (("+chosen+": "+str(bp_reading[chosen][adjint])+")) to? >> ")
                y_n = input("Are you sure that "+swap+" is the correct change for position "+adj+" in the "+chosen+" column?")
                if(y_n.lower() == 'y' or y_n.lower() == 'yes'):
                    if(chosen == "Systolic" or chosen == "Diastolic" or chosen == "Pulse" or chosen == "Weight"):
                        try:
                            swapint = float(swap)
                            bp_reading[chosen][adjint] = swapint
                            print(bp_reading[chosen][adjint])

                        except:
                            print("Error. Go back to beginning and try again.")
                            self.main()
                    elif(chosen == "Notes"):
                        bp_reading[chosen][adjint] = swap
                        print(bp_reading[chosen][adjint])

                    else:
                        print("Error. Go back to beginning and try again.")
                        self.main()
                    df = pd.DataFrame(bp_reading)
                    df.set_index('DateTime', inplace=True)
                    df.fillna(value="", inplace=True)
                    df.to_csv(source)
                    self.main()

                #NOT UPDATING AFTER COMPLETION#
            else:
                print("Not within proper boundaries.")
                self.Mod()
        else:
            print("Invalid choice.")





    #Mod()
    #print(bp_reading['DateTime'])
    #print(len(bp_reading))
    #print(enumerate(bp_reading))
    #print(max(enumerate(bp_reading, 1)))
    #print(master['Systolic'])



    def Systolic(self):
        Sys = input("Systolic >> ")
        y_nInput="Is " + Sys + " correct for your SYSTOLIC reading? (y/n) >> "
        y_n = input(y_nInput)
        if(y_n == 'y'):
            bp_reading['Systolic'].append(int(Sys))
        else:
            self.Systolic()

    def Diastolic(self):
        Dia = input("Diastolic >> ")
        y_nInput="Is " + Dia + " correct for your DIASTOLIC reading? (y/n) >> "
        y_n = input(y_nInput)
        if(y_n == 'y'):
            bp_reading['Diastolic'].append(int(Dia))
        else:
            self.Diastolic()

    def Pulse(self):
        Pul = input("Pulse >> ")
        y_nInput="Is " + Pul + " correct for your PULSE reading? (y/n) >> "
        y_n = input(y_nInput)
        if(y_n == 'y'):
            bp_reading['Pulse'].append(int(Pul))
        else:
            self.Pulse()

    def reading(self):
        fmt = '(%a) %Y-%m-%d %H:%M'
        go=input("Input reading? (y/n) >> ")
        if(go.lower()=='y'):
            now_utc = dt.datetime.now(timezone('UTC'))
            now_local = now_utc.astimezone(get_localzone())
            bp_reading['DateTime'].append(now_local.strftime(fmt))
            self.Systolic()
            self.Diastolic()
            self.Pulse()
            self.Weight()
            self.Notes()
            df = pd.DataFrame(bp_reading)
            df.set_index('DateTime', inplace=True)
            df.fillna(value="", inplace=True)
            df.to_csv(source)
            print(df.tail(20))
            tm.sleep(2)
            self.main()
        else:
            self.main()

    def info(self):
        print("\n## BLOOD PRESSURE INFORMATION ##\n")
        print("    Low Blood Pressure (Hypotension): <90 Systolic OR <60 Diastolic")
        print("    Normal Blood Pressure: 90-120 Systolic AND 60-80 Diastolic")
        print("    Prehypertension: 120-139 Systolic OR 80-89 Diastolic")
        print("    High Blood Pressure (Hypertension Stage 1): 140-159 Systolic OR 90-99 Diastolic")
        print("    High Blood Pressure (Hypertension Stage 2): >160 Systolic OR >100 Diastolic")
        print("    High Blood Pressure Crisis (Seek Emergency Care): >180 Systolic OR  >110 Diastolic")
        tm.sleep(2)
        print("\n## HEART RATE/PULSE INFORMATION ##")
        print('''\n    A normal resting heart rate for adults ranges from 60 to 100 beats per minute.
    Generally, a lower heart rate at rest implies more efficient heart function and better cardiovascular fitness. 
    For example, a well-trained athlete might have a normal resting heart rate closer to 40 beats per minute.''')
        tm.sleep(2)
        print("\n## BMI/WEIGHT INFORMATION ##")
        print('''
    If your BMI is less than 18.5, it falls within the underweight range.
    If your BMI is 18.5 to 24.9, it falls within the normal or Healthy Weight range.
    If your BMI is 25.0 to 29.9, it falls within the overweight range.
    If your BMI is 30.0 or higher, it falls within the obese range.\n''')
        self.main()

    def Weight(self):
        weiInput= 'Weight (leave blank to repeat last entry of '+ str(bp_reading['Weight'][-1])  +') >> '
        wei = input(weiInput)
        if (wei == ""):
            y_nInput="Is " + str(bp_reading['Weight'][-1]) + " correct for your WEIGHT reading? (y/n) >> "
            same = input(y_nInput)
            if(same.lower() == 'y'):
                bp_reading['Weight'].append(bp_reading['Weight'][-1])
            else:
                self.Weight()
        else:
            y_nInput="Is " + wei + " correct for your WEIGHT reading? (y/n) >> "
            y_n = input(y_nInput)
            if(y_n.lower() == 'y'):
                bp_reading['Weight'].append(float(wei))
            else:
                self.Weight()

    def Notes(self):
        note=input("Any additional notes you'd like to include? \n")
        print(note)
        y_n=input("Is this note ok? (y/n) >> ")
        if(y_n.lower() == "y"):
            bp_reading['Notes'].append(note)
        else:
            self.Notes()

    def avg(self):
        #Include Highest and Lowest recorded weights
        #Include full list of readings
        #Add moving averages
        if (bp_reading['Systolic'] != [] and bp_reading['Diastolic'] != [] and bp_reading['Pulse'] != [] and bp_reading['Weight'] != []):
            avgS=st.mean(bp_reading['Systolic'])
            avgD=st.mean(bp_reading['Diastolic'])
            avgP=st.mean(bp_reading['Pulse'])
            difW=round(bp_reading['Weight'][0] - bp_reading['Weight'][-1], 2)

            avg10S=st.mean(bp_reading['Systolic'][-10:])
            avg10D=st.mean(bp_reading['Diastolic'][-10:])
            avg10P=st.mean(bp_reading['Pulse'][-10:])
            difW10=round(bp_reading['Weight'][-10] - bp_reading['Weight'][-1], 2)




            '''
            - Compare am vs. pm and weekdays to weekends(Mon-Thu vs. Fri-Sun)
            --- See Pytz.py in Sandbox for how to break DateTime into chunks (don't forget to import re!)
            - View movement through time (set up rolling already but could use more)
             '''

            df = pd.DataFrame(bp_reading)
            df.set_index('DateTime', inplace=True)
            df.fillna(value="", inplace=True)
            #print(len(df.index))
            #print(df['Weight'][26-11])
            #print(df['Weight'][26-1])
            df['Sys10']=df['Systolic'].rolling(10).mean()
            df['Dia10']=df['Diastolic'].rolling(10).mean()
            df['Pul10']=df['Pulse'].rolling(10).mean()
            #weiDif = len(df.index)
            df['Wei10']=df['Weight'].rolling(10).max() - df['Weight'].rolling(10).min()
            df['Wei30']=df['Weight'].rolling(30).max() - df['Weight'].rolling(30).min()

            #df2 = df.resample('1D').mean()
            print('''
    [1] Print All Readings
    [2] Print Last 10 Readings
    [3] Plot a Graph (Systolic/Diastolic/Pulse/Weight)
    [E] Exit to Main Menu\n''')
            choice=input("What would you like to do? >> ")
            if(choice == '1'):
                print(df)
                print(len(df.index), 'total entries:')
                print("Avg Blood Pressure:", str(int(avgS)) + "/" + str(int(avgD)), ":: Avg Pulse:", str(int(avgP)))
                if(difW > 0):
                    print("You have lost", difW, "pounds since", bp_reading['DateTime'][0] + ".")
                elif(difW < 0):
                    print("You have gained", abs(difW), "pounds since", bp_reading['DateTime'][0] + ".")
                elif(difW == 0):
                    print("Your weight is the same as it was on", bp_reading['DateTime'][0] + ".")
                else:
                    print("Calculation Error")
            elif(choice == '2'):
                print(df.tail(10))
                print("Avg Blood Pressure (Last 10 Readings):", str(int(avg10S)) + "/" + str(int(avg10D)), ":: Avg Pulse (Last 10 Readings):", str(int(avg10P)))
                if(difW10 > 0):
                    print("You have lost", difW10, "pounds since", bp_reading['DateTime'][-10] + ".")
                elif(difW10 < 0):
                    print("You have gained", abs(difW10), "pounds since", bp_reading['DateTime'][-10] + ".")
                elif(difW10 == 0):
                    print("Your weight is the same as it was on", bp_reading['DateTime'][-10] + ".")
                else:
                    print("Calculation Error")
            elif(choice == '3'):
                #ax1=plt.subplot2grid((1,1), (0,0))
                #give choice of what to plot
                df['Systolic'].plot()
                df['Diastolic'].plot()
                df['Pulse'].plot()
                df['Weight'].plot()

                '''ax1.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))
                for label in ax1.xaxis.get_ticklabels():
                    label.set_rotation(45) ###Unable to convert date column to date'''

                plt.legend()
                plt.show()
            elif(choice.lower() == 'e'):
                self.main()
            else:
                print("Not an option.")
        else:
            print("Need complete readings.")
            self.main()
        tm.sleep(2)
        self.avg()
        
    def bmiCalc(self, height):
        return round((bp_reading['Weight'][-1] / height**2)*703, 2)
    
    def bmiClass(self, bmi):
        if bmi < 18.5:
            return "underweight"
        elif bmi >= 18.5 and bmi < 25:
            return "healthy weight"
        elif bmi >= 25 and bmi < 30:
            return "overweight"
        elif bmi >= 30:
            return "obese"
        else:
            raise ValueError
        
    def weightToLose(self, height):
        #heightInt = int(height)
        bmiActual = self.bmiCalc(height)
        classActual = self.bmiClass(bmiActual)
        weightActual = bp_reading['Weight'][-1]
        obeseUp = (30*(height**2))/703
        overweightUp = (25*(height**2))/703
        healthyUp = (18.5*(height**2))/703
        underweightDown = (18.5*(height**2))/703
        healthyDown = (24.9*(height**2))/703
        overweightDown =  (29.9*(height**2))/703
        if classActual == "obese":
            print(f'Lose {round(weightActual-overweightDown, 2)} lbs to achieve "overweight".')
            print(f'Lose {round(weightActual-healthyDown, 2)} lbs to achieve "healthy weight".')
            print(f'If you lose {round(weightActual-underweightDown, 2)} lbs you will be "underweight".')
        if classActual == "overweight":
            print(f'Lose {round(weightActual-healthyDown, 2)} lbs to achieve "healthy weight".')
            print(f'Lose {round(weightActual-underweightDown, 2)} lbs and you will be "underweight".')
            print(f'If you gain {round(obeseUp - weightActual, 2)} lbs you will be "obese"')
        if classActual == "healthy weight":
            print(f'If you lose {round(weightActual-underweightDown, 2)} lbs you will be "underweight".')
            print(f'If you gain {round(overweightUp-weightActual, 2)} lbs you will be "overweight".')
            print(f'If you gain {round(obeseUp-weightActual, 2)} lbs you will be "obese".')
        if classActual == "underweight":
            print(f'Gain {round(healthyUp-weightActual, 2)} lbs to achieve "healthy weight".')
            print(f'If you gain {round(overweightUp-weightActual, 2)} lbs you will be "overweight".')
            print(f'If you gain {round(obeseUp-weightActual, 2)} lbs you will be "obese".')
        tm.sleep(2)
        print('''
    *** Remember that these are only guidelines and everyone's body is different. ***
        ''')
            
    ## Add calculations to show how many lbs needed to lose (or gain) to get to "healthy weight" ##
    
    def bmi(self):
        hInput = input("What is your height in inches?  ")
        bmiActual = self.bmiCalc(int(hInput))
        print(f'Based on your previous weight measurement, your current BMI is: {bmiActual}, which is {self.bmiClass(bmiActual)}.\n')
        self.weightToLose(int(hInput))
        tm.sleep(2)
        self.main()
    

    def main(self):
        #update()
        print("Welcome to your Blood Pressure Helper! \n")
        tm.sleep(1)
        print("[1] Enter a Record")
        print("[2] View Averages")
        print("[3] See Health Information")
        print("[4] Modify an Old Entry")
        print("[5] Calculate my BMI")
        choice=input("\n What would you like to do? ")
        if (choice == '1'):
            self.reading()
        elif (choice == '2'):
            self.avg()
        elif (choice == '3'):
            self.info()
        elif (choice == '4'):
            self.Mod()
        elif (choice == '5'):
            self.bmi()
        else:
            print("Invalid choice.")
            self.main()


reader=bp_reader()
reader.main()




#df.to_csv(source)
