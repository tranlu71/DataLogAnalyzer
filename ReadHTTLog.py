# Note: This code only works for folders that contain:
#   1-run HTT Logs
#   Multiple-run HTT Logs but the runs are approx equal in treatment time and the treatment time must be specified

import time
import pandas as pd
import glob
import os
import numpy as np


def ReadHTT(wd_arg, output_filename_arg, treatment_time_arg, display_variable_list_arg, pattern_arg):
    def find_col_index(subdir_name_arg):
        subdir_name = subdir_name_arg
        joined_csv = glob.glob(subdir_name + '/HTT*') + glob.glob(subdir_name + '/DCCData*')
        df = pd.concat(map(pd.read_csv, joined_csv), ignore_index=True)
        df = df.sort_values('Date')
        df = df.reset_index(drop=True)
        df_cols = df.columns
        col_index = [df_cols.get_loc(name) for name in ['Date', 'LinePressure (kPa)', 'OpticalTemp',
                                                        'LaserStatus', 'LaserTotalPulses', 'LaserTotalTime',
                                                        'LaserPower (W)', 'CoolingState', 'LaserRemoteInterlock',
                                                        'TankPressure (kPa)', 'ProbeType', 'LaserPulseDuration (ms)',
                                                        'LaserPulseDelay (ms)']]
        return col_index

    def HTTDCClog(subdir_name_arg, use_cols_arg):
        output = []
        subdir_name = subdir_name_arg
        joined_csv = glob.glob(subdir_name + '/HTT*') + glob.glob(subdir_name + '/DCCData*')

        def process_csv(file_name):
            print(file_name)
            df_unit = pd.read_csv(file_name).iloc[:, use_cols_arg].reset_index(drop=True)
            col_names = ['Date', 'LinePressure (kPa)', 'OpticalTemp',
                         'LaserStatus', 'LaserTotalPulses', 'LaserTotalTime', 'LaserPower (W)',
                         'CoolingState', 'LaserRemoteInterlock', 'TankPressure (kPa)', 'ProbeType', 'LaserPulseDuration (ms)',
                         'LaserPulseDelay (ms)']
            df_unit = df_unit.rename(columns=dict(zip(df_unit.columns, col_names)))
            return df_unit
        df = pd.concat(map(process_csv, joined_csv), ignore_index=True)
        df = df.sort_values('Date')
        df = df.reset_index(drop=True)
        LinePressure = df['LinePressure (kPa)']
        ProbeTemp = df['OpticalTemp']
        LaserStatus = df['LaserStatus']
        CoolingState = df['CoolingState']
        Interlock = df['LaserRemoteInterlock']
        LaserTotalTime = df['LaserTotalTime']
        probeID = os.path.basename(subdir_name)
        start_laser_index = []
        stop_laser_index = []
        start_cooling_index = []
        start_interlock_index = []
        row_count = 1
        count = 0
        pulse = df['LaserPulseDuration (ms)']
        delay = df['LaserPulseDelay (ms)']

        while row_count < len(df.index):
            for row in range(row_count, len(df.index)):
                if LaserStatus[row] == 'Laser':
                    start_laser_foo = row
                    start_laser_index.append(start_laser_foo)
                    for row_remain in range(start_laser_foo+1, len(df.index)):
                        if LaserStatus[row_remain-1] == 'Laser' and LaserStatus[row_remain] != 'Laser':
                            stop_laser_foo = row_remain-1
                            if treatment_time_arg == '':
                                treatment_laser_on = LaserTotalTime[max([idx for idx in range(start_laser_foo, len(LaserTotalTime)-1) if LaserTotalTime[idx]])]
                                try:
                                    treatment_laser_on_foo = time.strptime(LaserTotalTime[stop_laser_foo], '%H:%M:%S')
                                    treatment_laser_on_foo = treatment_laser_on_foo.tm_hour * 3600 + treatment_laser_on_foo.tm_min * 60 + treatment_laser_on_foo.tm_sec
                                    treatment_laser_on = time.strptime(treatment_laser_on, '%H:%M:%S')
                                    treatment_laser_on = treatment_laser_on.tm_hour * 3600 + treatment_laser_on.tm_min * 60 + treatment_laser_on.tm_sec
                                    if treatment_laser_on_foo + 1 >= treatment_laser_on:
                                        stop_laser_index.append(stop_laser_foo)
                                        treatment_time = treatment_laser_on_foo * (pulse[stop_laser_foo] + delay[stop_laser_foo]) / pulse[stop_laser_foo]/60
                                        break
                                except ValueError:
                                    print("LaserTotalTime does not follow normal format")
                                    return 1
                            else:
                                treatment_laser_on = int(np.floor(float(treatment_time_arg) * pulse[stop_laser_foo] / (pulse[stop_laser_foo] + delay[stop_laser_foo])))
                                try:
                                    if time.strptime(LaserTotalTime[stop_laser_foo], '%H:%M:%S') > time.strptime('00:'+str(treatment_laser_on)+':00', '%H:%M:%S'):
                                        stop_laser_index.append(stop_laser_foo)
                                        break
                                except ValueError:
                                    print("LaserTotalTime does not follow normal format")
                                    return 1
                    break
            if count == len(stop_laser_index):
                break
            row_count = stop_laser_index[count]+1
            count += 1
        for i in range(count):
            if i == 0:
                start_cooling_foo = start_laser_index[0]
                start_interlock_foo = start_laser_index[0]
                for row in range(0, start_laser_index[0]):
                    if row == start_laser_index[0] - 1:
                        start_interlock_index.append(start_interlock_foo)
                        start_cooling_index.append(start_cooling_foo)
                        break
                    if CoolingState[row] == 0 and CoolingState[row + 1] == 1:
                        start_cooling_foo = row + 1
                    if Interlock[row] == 0 and Interlock[row + 1] == 1:
                        start_interlock_foo = row + 1
            else:
                start_cooling_foo = start_cooling_index[i-1]
                start_interlock_foo = start_interlock_index[i-1]
                for row in range(stop_laser_index[i-1]+1, start_laser_index[i]):
                    if row == start_laser_index[i]-1:
                        start_interlock_index.append(start_interlock_foo)
                        start_cooling_index.append(start_cooling_foo)
                        break
                    if CoolingState[row] == 0 and CoolingState[row + 1] == 1:
                        start_cooling_foo = row + 1
                    if Interlock[row] == 0 and Interlock[row + 1] == 1:
                        start_interlock_foo = row + 1

        def extract_data(laser_start, laser_stop, cooling_start, interlock_start):
            laserOnTime = time.strptime(df['LaserTotalTime'][laser_stop], '%H:%M:%S')
            laserOnTime = laserOnTime.tm_hour * 3600 + laserOnTime.tm_min * 60 + laserOnTime.tm_sec
            laserOffTime = delay[laser_stop]/pulse[laser_stop] * laserOnTime
            try:
                coolingOnTime = time.strptime(df['Date'][cooling_start], '%Y-%m-%d %H:%M:%S.%f')
            except ValueError:
                coolingOnTime = time.strptime(df['Date'][cooling_start], '%M:%S.%f')
            try:
                interlockOnTime = time.strptime(df['Date'][interlock_start], '%Y-%m-%d %H:%M:%S.%f')
            except ValueError:
                interlockOnTime = time.strptime(df['Date'][interlock_start], '%M:%S.%f')
            interlock = - (coolingOnTime.tm_hour * 3600 + coolingOnTime.tm_min * 60 + coolingOnTime.tm_sec) + \
                          (interlockOnTime.tm_hour * 3600 + interlockOnTime.tm_min * 60 + interlockOnTime.tm_sec)
            try:
                shotStart = time.strptime(df['Date'][laser_start], '%Y-%m-%d %H:%M:%S.%f')
            except ValueError:
                shotStart = time.strptime(df['Date'][laser_start], '%M:%S.%f')
            stable = - (interlockOnTime.tm_hour * 3600 + interlockOnTime.tm_min * 60 + interlockOnTime.tm_sec) + \
                       (shotStart.tm_hour * 3600 + shotStart.tm_min * 60 + shotStart.tm_sec)

            power = df['LaserPower (W)'][laser_stop]
            tempRange = np.array([ProbeTemp[idx] for idx in range(laser_start, laser_stop) if LaserStatus[idx] == 'Laser'])
            tempRange = '{:.2f} to {:.2f}'.format(tempRange[[idx for idx in range(len(tempRange)) if tempRange[idx] != '']].min(),
                                                  tempRange[[idx for idx in range(len(tempRange)) if tempRange[idx] != '']].max())
            maxPressure = f"{max(LinePressure[laser_start:laser_stop]):.2f}"
            shotStart = df['Date'][laser_start]
            shotEnd = df['Date'][laser_stop]
            try:
                tempSpike = f"{max(ProbeTemp[laser_start-5:laser_start+15]):.2f}"  # one laser pulse is 2400ms, data points are 200s apart
            except ValueError:
                tempSpike = 0
            tempPeak = f"{max(ProbeTemp[laser_stop:laser_stop + 480]):.2f}"
            tankPressure = df['TankPressure (kPa)'][cooling_start+100]
            probeType = df['ProbeType'][laser_start]
            tempInitial = ProbeTemp[cooling_start-1]
            output_unit = {'Probe ID': probeID}
            key_value_pairs = [
                ('Probe Type', probeType, 14),
                ('Laser ON Time (sec)', laserOnTime, 7),
                ('Laser OFF Time (sec)', laserOffTime, 8),
                ('Power (W)', power, 2),
                ('Initial Probe Temp (oC)', tempInitial, 15),
                ('Probe Temp. Cooling Range (oC)', tempRange, 9),
                ('Max Line Pressure (kPa)', maxPressure, 0),
                ('Temp. Spike (oC)', tempSpike, 1),
                ('Post-cooling Max Temp. (oC)', tempPeak, 3),
                ('Interlock (s)', interlock, 4),
                ('Stable (s)', stable, 5),
                ('Start Tank Pressure (kPa)', tankPressure, 6),
                ('Cooling Start', df['Date'][cooling_start], 12),
                ('Interlock Start', df['Date'][interlock_start], 13),
                ('Shot Start', shotStart, 10),
                ('Shot End', shotEnd, 11)
            ]

            # Loop through the key-value pairs
            for key, value, display_variable_index in key_value_pairs:
                # Check if display_variable_list_arg[index] is True
                if display_variable_list_arg[display_variable_index]:
                    # Add the key-value pair only if display_variable_list_arg[index] is True
                    output_unit[key] = value

            # Add the dictionary to the main dictionary
            output.append(output_unit)

        for run in range(len(stop_laser_index)):
            extract_data(start_laser_index[run], stop_laser_index[run], start_cooling_index[run], start_interlock_index[run])
        return output

    if wd_arg is None:
        root_path = 'C:/Users/tlu/PycharmProjects/ReadHTTLog'
    else:
        root_path = wd_arg

    output_df = []
    flag = True
    cols_index = [0, 11, 107, 40, 42, 43, 49, 17, 45, 9, 20, 50, 51]
    for dir_name, sub_dirs, files in os.walk(root_path):
        if pattern_arg in dir_name:
            if not sub_dirs and dir_name:
                print(os.path.basename(dir_name))
                if flag:
                    try:
                        cols_index = find_col_index(dir_name)
                        flag = False
                    except KeyError:
                        print("Log has no header.")
                info_capability = HTTDCClog(dir_name, cols_index)
                if info_capability != 1:
                    for index in range(len(info_capability)):
                        output_df.append(info_capability[index])

    output_df = pd.DataFrame(output_df)
    output_filename_path = wd_arg+"/"+output_filename_arg+".xlsx"
    output_df.to_excel(output_filename_path)
    print(output_filename_path)
