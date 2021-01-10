import ctypes
import sys
import win32api

import ntplib
import datetime
import time as t

#checks if the program has admin privilages, and if not it gets them
#(they are needed to change the clock)
def is_admin():
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False

if is_admin():
    #getting time info from a server
    client = ntplib.NTPClient()
    response = client.request ('pool.ntp.org', version = 3)

    #converting the time data into format that windows accepts
    time_data = t.gmtime(response.tx_time)
    final_time_data = t.strftime("%Y,%m,%w,%d,%H,%M,%S,0", time_data)
    final_time_data = tuple(map(int,final_time_data.split(",")))

    #passing data to the system
    win32api.SetSystemTime(*final_time_data)
else:
    # Re-run the program with admin rights
    ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, " ".join(sys.argv), None, 1)
