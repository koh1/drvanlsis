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
    plt.clf()

def plot_user_velocity(data, filename):
    for k,v in data.items():
        plt.plot(v['time'], v['velocity'])
    plt.savefig(filename)
    plt.clf()

def plot_user_paths(data, filename):
    for k,v in data.items():
        plt.plot(v['x'], v['y'])
    plt.savefig(filename)
    plt.clf()

def plot_stats_data(data, filename):
    for k,v in data.items():
        plt.plot(v['v_mean'], v['a_mean'])
    plt.savefig(filename)
    plt.clf()

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

def make_velocity_data(paths_data, stats_data):
    v_data = {}
    stats_data = {}
    for k,v in paths_data.items():
        prev_xy = [0,0]
        time_index = 0
        varray = []
        distance = 0
        for r in v.iterrows():
#            print "%s, %s, %s" % (type(r), r[1]['x'], r[1]['y'])
            d = np.sqrt((r[1]['x'] - prev_xy[0])**2 + (r[1]['y'] - prev_xy[1])**2)
            distance += d
            varray.append([time_index, d])
            prev_xy = [r[1]['x'], r[1]['y']]
            time_index += 1

        v_data[k] = pd.DataFrame(varray, columns=['time','velocity'])
        stats_data[k] = {
            'time': time_index - 1,
            'distance': distance,
            'v_max': v_data[k]['velocity'].max(),
            'v_min': v_data[k]['velocity'].min(),
            'v_mean': v_data[k]['velocity'].mean(),
            'v_median': v_data[k]['velocity'].median(),
            'v_std': v_data[k]['velocity'].std()
        }


    return (v_data,stats_data)
 
def make_acceleration_data(v_data, stats_data):
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
        stats_data[k]['a_max'] = a_data[k]['acceleration'].max()
        stats_data[k]['a_min'] = a_data[k]['acceleration'].min()
        stats_data[k]['a_mean'] = a_data[k]['acceleration'].mean()
        stats_data[k]['a_median'] = a_data[k]['acceleration'].median()
        stats_data[k]['a_std'] = a_data[k]['acceleration'].std()

    return (a_data, stats_data)

if __name__ == '__main__':
    p = sys.argv
    if len(p) < 2:
        print "usage: python %s file_dir" % p[0]
        sys.exit(0)
    data = load_user_paths(p[1])
    plot_user_paths(data, "%s/%s_paths.png" % (p[1],p[1].split('/')[-1]))

    stats_data = {}
    vdata, stats_data = make_velocity_data(data, stats_data)
    plot_user_velocity(vdata, "%s/%s_velocity.png" % (p[1], p[1].split('/')[-1]))

    adata, stats_data = make_acceleration_data(vdata, stats_data)
    plot_user_acceleration(adata, "%s/%s_acceleration.png" % (p[1], p[1].split('/')[-1]))

    plot_stats_data(stats_data, "%s/%s_stats.png" % (p[1], p[1].split('/')[-1]))
