
import pandas as pd
import math

import os

# For the MSE formula you can use the equation below. I have
 
#    mse = (wob/bitArea + 120*pi*rpm*torque/rop/bitArea)*6894.76
 
# where the parameters need to be converted in imperial units, see below. The 6894.76 factor multiplied at the end is to get the answer back to SI units (Pascals).
 
#    bitArea = pi*bitDiameter[in]^2/ 4.0
#    wob = df['WOBAVG - N']*0.2248
#    torque = df['TQABAV - kN.m']*737.56
#    rop = df['ROPA - m/h']*3.2808
#    rpm = df['RPMBAVG - rpm']


def computeMechanicalSpecificEnergy(directory_of_drilling_data):
    list_of_drilling_data_csv = os.listdir(directory_of_drilling_data)

    for file_name in list_of_drilling_data_csv:
        if not file_name.startswith('.'):
            df = pd.read_csv(os.path.join(directory_of_drilling_data, file_name), sep=',')
            bitArea =  (pow(df['bit_size (in)'],2))*math.pi/4
            wob = df['Weight On Bit N']*0.2248
            torque = df['SurfaceTorque(N.m)']*737.56/1000
            rop = df['Time Averaged ROP m/h']*3.2808
            rpm = df['Surface RPM c s']*60

            df['mse Pa'] = ((wob/bitArea) + (120*math.pi*rpm*torque/rop/bitArea))*6894.76

            df.to_csv(directory_of_drilling_data+'/'+file_name, sep=',')

            print('added MSE to ' + file_name)



if __name__ == '__main__':
    computeMechanicalSpecificEnergy('all_drill_with_fm_csv')   