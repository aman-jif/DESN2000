import pandas as pd
import matplotlib.pyplot as graph
import numpy as np

try:
    data_xlsx = 'water_quality_data.xlsx'
    active_wks = pd.read_excel(data_xlsx)
except FileNotFoundError:
    df = pd.DataFrame(data = {(0)})
    df.plot(title = 'Excel sheet not found!')
    graph.show()
    exit()
except Exception:
    df = pd.DataFrame(data = {(0)})
    df.plot(title = 'An error has occured.')
    graph.show()
    exit()

time_list = active_wks['Timestamp'].tolist()

temp_list = active_wks['Temperature (Sensor 1)'].tolist()
ph_list = active_wks['pH (Sensor 2)'].tolist()
cond_list = active_wks['Conductivity (Sensor 3)'].tolist()
nitr_list = active_wks['Nitrates (Sensor 4)'].tolist()

temp_values = {'Temperature': temp_list, 'Time': time_list}
temp_df = pd.DataFrame(data = temp_values)
temp_df.plot(title = 'Temperature vs Time', xlabel='Time (dd/mm/yy hh:mm:ss)', 
             ylabel= 'Temperature', x = 'Time')
graph.show()

ph_values = {'pH': ph_list, 'Time': time_list}
temp_df = pd.DataFrame(data = ph_values)
temp_df.plot(title = 'pH vs Time', xlabel='Time (dd/mm/yy hh:mm:ss)', 
             ylabel= 'pH', x = 'Time')
graph.show()

cond_values = {'Conductivity': cond_list, 'Time': time_list}
temp_df = pd.DataFrame(data = cond_values)
temp_df.plot(title = 'Conductivity vs Time', xlabel='Time (dd/mm/yy hh:mm:ss)', 
             ylabel= 'Conductivity', x = 'Time')
graph.show()

nitr_values = {'Nitrates': nitr_list, 'Time': time_list}
temp_df = pd.DataFrame(data = nitr_values)
temp_df.plot(title = 'Nitrates vs Time', xlabel='Time (dd/mm/yy hh:mm:ss)', 
             ylabel= 'Nitrates', x = 'Time')
graph.show()

# # time values from 3 to 6 inclusive in steps of 0.01 (use 6.01 to include 6)
# t = np.arange(3, 6.01, 0.01)  # t for time
# # Use NumPy array operations to compute distance and speed at all time values (i.e. x axis)
# distance = (t**2/2 - np.cos(5*t) - 7)
# speed = (t + 5*np.sin(5*t))
# values = {'Distance': distance, 'Speed': speed, 'Time': t}  # x is time t
# df = pd.DataFrame(data= values)
# df.plot(title='Distance and speed', xlabel='Time (hours)', ylabel='Distance (km) / Speed (km/h)', x='Time')
# graph.show()