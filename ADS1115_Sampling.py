import time
import sys
import sqlite3
#sys.path.append("/home/pi/Adafruit_Python_ADS1x15/Adafruit_ADS1x15")

#importing Adafruit_ADS1x15 library
import Adafruit_ADS1x15

#establishing the sqlite3 database connection
conn=sqlite3.connect('testing_1.db')
#establishing the cursor for handling connection
c=conn.cursor()
#creating 2 different tables for taking values from input and environment
c.execute("CREATE TABLE IF NOT EXISTS parameter (ID INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT, Ptime DATETIME, Voltage REAL)");
c.execute("CREATE TABLE IF NOT EXISTS environment_light (ID INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT, Etime DATETIME, Light REAL)");


adc=Adafruit_ADS1x15.ADS1115()
#setting GAIN= 1 for voltage between 0 to 4.096V
GAIN=1

while True:
    #Starting ADC for continous conversion with last result
    adc.start_adc(0, gain=GAIN)
    value_volt = adc.get_last_result()
    #converting the digital voltage value to analog value
    v = value_volt*(4.096/32768)
    c.execute("INSERT INTO parameter (Ptime, name, Voltage) VALUES (CURRENT_TIMESTAMP, ?, ?)",('voltage', v))
    conn.commit()

    #printing the voltage value_volt
    print("Voltage value is {0:5.5f}".format(v))
    #giving time sleep for 0.5 seconds to read the values and even datalogging
    time.sleep(0.1)

    adc.start_adc(1, gain=GAIN)
    value_light = adc.get_last_result()
    #converting the digital light value to analog value
    l = value_light*(4.096/32768)
    c.execute("INSERT INTO environment_light (Etime, name, Light) VALUES (CURRENT_TIMESTAMP, ?, ?)",('light', l))
    conn.commit()

    #printing the voltage value_light
    print("Light intesity value is {0:5.5f}".format(l))
    #giving time sleep for 0.5 seconds to read the values and even datalogging
    time.sleep(0.1)

conn.commit()
#closing the db connection with sqlite
conn.close()
