import numpy as np
import pandas as pd

import os
import sys
import re
import math

import matplotlib.pyplot as plt

def plot_user_acceleration(data, filename):
    for k,v in data.items():
        plt.plot(v['time'], v['acceleration'])
    plt.savefig(filename)

def plot_user_velocity(data, filename):
    for k,v in data.items():
        plt.plot(v['time'], v['velocity'])
    plt.savefig(filename)

def plot_user_paths(data, filename):
    for k,v in data.items():
        plt.plot(v['x'], v['y'])
    plt.savefig(filename)

def load_user_paths(src_dir=""):
    files = os.listdir("%s/" % src_dir)
    pattern = re.compile(r"^(.+)\.csv$")
    data = {}
    for f in files:
        reobj =  re.match(pattern, f)
        if not reobj == None:
            num = int(reobj.group(1))
            item_name = "path_%04d" % num
            data[item_name] = pd.read_csv("%s/%s" % (src_dir, f))
    return data

def make_velocity_data(paths_data):
    v_data = {}
    for k,v in paths_data.items():
        prev_xy = [0,0]
        time_index = 0
        varray = []
        for r in v.iterrows():
#            print "%s, %s, %s" % (type(r), r[1]['x'], r[1]['y'])
            d = np.sqrt((r[1]['x'] - prev_xy[0])**2 + (r[1]['y'] - prev_xy[1])**2)
            varray.append([time_index, d])
            prev_xy = [r[1]['x'], r[1]['y']]
            
            time_index += 1

        v_data[k] = pd.DataFrame(varray, columns=['time','velocity'])

    return v_data
 
def make_acceleration_data(v_data):
    a_data = {}
    for k,v in v_data.items():
        prev_v = 0
        time_index = 0
        aarray = []
        for r in v.iterrows():
            dv = r[1]['velocity'] - prev_v
            aarray.append([time_index, dv])
            prev_v = r[1]['velocity']
            
            time_index += 1
        
        a_data[k] = pd.DataFrame(aarray, columns=['time', 'acceleration'])

    return a_data

if __name__ == '__main__':
    p = sys.argv
    if len(p) < 2:
        print "usage: python %s file_dir" % p[0]
        sys.exit(0)
    data = load_user_paths(p[1])
#    plot_user_paths(data, "%s_paths.png" % p[1])
    vdata = make_velocity_data(data)
    adata = make_acceleration_data(vdata)
#    plot_user_velocity(vdata, "%s_velocity.png" % p[1])
    plot_user_acceleration(adata, "%s_acceleration.png" % p[1])
