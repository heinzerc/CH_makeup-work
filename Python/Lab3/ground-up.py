import argparse
from glob import glob
import os
import pandas
import sys
import numpy as np

import scipy
from scipy.signal import find_peaks

import matplotlib
import matplotlib.pyplot as plt
matplotlib.use('Agg')

import csv

from sklearn import tree
from sklearn.tree import DecisionTreeClassifier
from sklearn.preprocessing import StandardScaler
from sklearn import metrics
from sklearn.metrics import classification_report
from sklearn.tree import DecisionTreeClassifier
from sklearn.model_selection import GridSearchCV

def extract(file_name: str, test_train: int):
    # return dict of atts and their values

    if test_train == 0:
        name = "Data/Lab3/Train/" + file_name
    elif test_train == 1:
        name = file_name
    elif test_train == 2:
        name = "Data/Lab3/Validation/" + file_name
    f = open(name, "r")

    # skip first line
    line1 = f.readline()

    info = {}
    info['headset_pos_x'] = []
    info['headset_pos_y'] = []
    info['headset_pos_z'] = []
    info['controller_left_vel_x'] = []
    info['controller_left_vel_y'] = []
    info['controller_left_vel_z'] = []
    info['controller_left_angularVel_x'] = []
    info['controller_left_angularVel_y'] = []
    info['controller_left_angularVel_z'] = []
    info['controller_left_pos_x'] = []
    info['controller_left_pos_y'] = []
    info['controller_left_pos_z'] = []
    info['controller_left_rot_x'] = []
    info['controller_left_rot_y'] = []
    info['controller_left_rot_z'] = []
    info['controller_right_vel_x'] = []
    info['controller_right_vel_y'] = []
    info['controller_right_vel_z'] = []
    info['controller_right_angularVel_x'] = []
    info['controller_right_angularVel_y'] = []
    info['controller_right_angularVel_z'] = []
    info['controller_right_pos_x'] = []
    info['controller_right_pos_y'] = []
    info['controller_right_pos_z'] = []
    info['controller_right_rot_x'] = []
    info['controller_right_rot_y'] = []
    info['controller_right_rot_z'] = []

    # data: time,headset_vel.x,headset_vel.y,headset_vel.z,headset_angularVel.x,headset_angularVel.y,headset_angularVel.z,headset_pos.x,headset_pos.y,headset_pos.z,headset_rot.x,headset_rot.y,headset_rot.z,controller_left_vel.x,controller_left_vel.y,controller_left_vel.z,controller_left_angularVel.x,controller_left_angularVel.y,controller_left_angularVel.z,controller_left_pos.x,controller_left_pos.y,controller_left_pos.z,controller_left_rot.x,controller_left_rot.y,controller_left_rot.z,controller_right_vel.x,controller_right_vel.y,controller_right_vel.z,controller_right_angularVel.x,controller_right_angularVel.y,controller_right_angularVel.z,controller_right_pos.x,controller_right_pos.y,controller_right_pos.z,controller_right_rot.x,controller_right_rot.y,controller_right_rot.z
    # want time, controller_left_vel.x, controller_left_vel.y, controller_left_vel.z
    # indices [7,8,9,13, 14, 15]

    for line in f.readlines():
        lst = line.split(",")
        info['headset_pos_x'].append(lst[7])
        info['headset_pos_y'].append(lst[8])
        info['headset_pos_z'].append(lst[9])
        info['controller_left_vel_x'].append(lst[13])
        info['controller_left_vel_y'].append(lst[14])
        info['controller_left_vel_z'].append(lst[15])
        info['controller_left_angularVel_x'].append(lst[16])
        info['controller_left_angularVel_y'].append(lst[17])
        info['controller_left_angularVel_z'].append(lst[18])
        info['controller_left_pos_x'].append(lst[19])
        info['controller_left_pos_y'].append(lst[20])
        info['controller_left_pos_z'].append(lst[21])
        info['controller_left_rot_x'].append(lst[22])
        info['controller_left_rot_y'].append(lst[23])
        info['controller_left_rot_z'].append(lst[24])
        info['controller_right_vel_x'].append(lst[25])
        info['controller_right_vel_y'].append(lst[26])
        info['controller_right_vel_z'].append(lst[27])
        info['controller_right_angularVel_x'].append(lst[28])
        info['controller_right_angularVel_y'].append(lst[29])
        info['controller_right_angularVel_z'].append(lst[30])
        info['controller_right_pos_x'].append(lst[31])
        info['controller_right_pos_y'].append(lst[32])
        info['controller_right_pos_z'].append(lst[33])
        info['controller_right_rot_x'].append(lst[34])
        info['controller_right_rot_y'].append(lst[35])
        info['controller_right_rot_z'].append(lst[36])

    f.close()
    return info

"""car01 = extract("CAR_01.csv", 0)
for key, val in car01.items():
    print(key, val)"""

def preprocess(file_name: str, test_train: int):
    # mean, std, number of peaks
    info  = extract(file_name, test_train)

    # initialize results variable
    res = {}
    
    # x, y, and z components of v
    headset_pos_x = list(map(float, info['headset_pos_x']))
    headset_pos_y = list(map(float, info['headset_pos_y']))
    headset_pos_z = list(map(float, info['headset_pos_z']))
    controller_left_vel_x = list(map(float, info['controller_left_vel_x']))
    controller_left_vel_y = list(map(float, info['controller_left_vel_y']))
    controller_left_vel_z = list(map(float, info['controller_left_vel_z']))
    controller_left_angularVel_x = list(map(float, info['controller_left_angularVel_x']))
    controller_left_angularVel_y = list(map(float, info['controller_left_angularVel_y']))
    controller_left_angularVel_z = list(map(float, info['controller_left_angularVel_z']))
    controller_left_pos_x = list(map(float, info['controller_left_pos_x']))
    controller_left_pos_y = list(map(float, info['controller_left_pos_y']))
    controller_left_pos_z = list(map(float, info['controller_left_pos_z']))
    controller_left_rot_x = list(map(float, info['controller_left_rot_x']))
    controller_left_rot_y = list(map(float, info['controller_left_rot_y']))
    controller_left_rot_z = list(map(float, info['controller_left_rot_z']))
    controller_right_vel_x = list(map(float, info['controller_right_vel_x']))
    controller_right_vel_y = list(map(float, info['controller_right_vel_y']))
    controller_right_vel_z = list(map(float, info['controller_right_vel_z']))
    controller_right_angularVel_x = list(map(float, info['controller_right_angularVel_x']))
    controller_right_angularVel_y = list(map(float, info['controller_right_angularVel_y']))
    controller_right_angularVel_z = list(map(float, info['controller_right_angularVel_z']))
    controller_right_pos_x = list(map(float, info['controller_right_pos_x']))
    controller_right_pos_y = list(map(float, info['controller_right_pos_y']))
    controller_right_pos_z = list(map(float, info['controller_right_pos_z']))
    controller_right_rot_x = list(map(float, info['controller_right_rot_x']))
    controller_right_rot_y = list(map(float, info['controller_right_rot_y']))
    controller_right_rot_z = list(map(float, info['controller_right_rot_z']))

    # peaks
    peaks_controller_left_vel_x, _ = find_peaks(controller_left_vel_x)
    peaks_controller_left_vel_y, _ = find_peaks(controller_left_vel_y)
    peaks_controller_left_vel_z, _ = find_peaks(controller_left_vel_z)
    peaks_controller_left_angularVel_x, _ = find_peaks(controller_left_angularVel_x)
    peaks_controller_left_angularVel_y, _ = find_peaks(controller_left_angularVel_y)
    peaks_controller_left_angularVel_z, _ = find_peaks(controller_left_angularVel_z)
    peaks_controller_left_pos_x, _ = find_peaks(controller_left_pos_x)
    peaks_controller_left_pos_y, _ = find_peaks(controller_left_pos_y)
    peaks_controller_left_pos_z, _ = find_peaks(controller_left_pos_z)
    peaks_controller_left_rot_x, _ = find_peaks(controller_left_rot_x)
    peaks_controller_left_rot_y, _ = find_peaks(controller_left_rot_y)
    peaks_controller_left_rot_z, _ = find_peaks(controller_left_rot_z)
    peaks_controller_right_vel_x, _ = find_peaks(controller_right_vel_x)
    peaks_controller_right_vel_y, _ = find_peaks(controller_right_vel_y)
    peaks_controller_right_vel_z, _ = find_peaks(controller_right_vel_z)
    peaks_controller_right_angularVel_x, _ = find_peaks(controller_right_angularVel_x)
    peaks_controller_right_angularVel_y, _ = find_peaks(controller_right_angularVel_y)
    peaks_controller_right_angularVel_z, _ = find_peaks(controller_right_angularVel_z)
    peaks_controller_right_pos_x, _ = find_peaks(controller_right_pos_x)
    peaks_controller_right_pos_y, _ = find_peaks(controller_right_pos_y)
    peaks_controller_right_pos_z, _ = find_peaks(controller_right_pos_z)
    peaks_controller_right_rot_x, _ = find_peaks(controller_right_rot_x)
    peaks_controller_right_rot_y, _ = find_peaks(controller_right_rot_y)
    peaks_controller_right_rot_z, _ = find_peaks(controller_right_rot_z)

    res['peaks_controller_left_vel_x'] = len(peaks_controller_left_vel_x)
    res['peaks_controller_left_vel_y'] = len(peaks_controller_left_vel_y)
    res['peaks_controller_left_vel_z'] = len(peaks_controller_left_vel_z)
    res['peaks_controller_left_angularVel_x'] = len(peaks_controller_left_angularVel_x)
    res['peaks_controller_left_angularVel_y'] = len(peaks_controller_left_angularVel_y)
    res['peaks_controller_left_angularVel_z'] = len(peaks_controller_left_angularVel_z)
    res['peaks_controller_left_pos_x'] = len(peaks_controller_left_pos_x)
    res['peaks_controller_left_pos_y'] = len(peaks_controller_left_pos_y)
    res['peaks_controller_left_pos_z'] = len(peaks_controller_left_pos_z)
    res['peaks_controller_left_rot_x'] = len(peaks_controller_left_rot_x)
    res['peaks_controller_left_rot_y'] = len(peaks_controller_left_rot_y)
    res['peaks_controller_left_rot_z'] = len(peaks_controller_left_rot_z)
    res['peaks_controller_right_vel_x'] = len(peaks_controller_right_vel_x)
    res['peaks_controller_right_vel_y'] = len(peaks_controller_right_vel_y)
    res['peaks_controller_right_vel_z'] = len(peaks_controller_right_vel_z)
    res['peaks_controller_right_angularVel_x'] = len(peaks_controller_right_angularVel_x)
    res['peaks_controller_right_angularVel_y'] = len(peaks_controller_right_angularVel_y)
    res['peaks_controller_right_angularVel_z'] = len(peaks_controller_right_angularVel_z)
    res['peaks_controller_right_pos_x'] = len(peaks_controller_right_pos_x)
    res['peaks_controller_right_pos_y'] = len(peaks_controller_right_pos_y)
    res['peaks_controller_right_pos_z'] = len(peaks_controller_right_pos_z)
    res['peaks_controller_right_rot_x'] = len(peaks_controller_right_rot_x)
    res['peaks_controller_right_rot_y'] = len(peaks_controller_right_rot_y)
    res['peaks_controller_right_rot_z'] = len(peaks_controller_right_rot_z)

    # means
    s_headset_pos_x = pandas.Series(data = headset_pos_x)
    s_headset_pos_y = pandas.Series(data = headset_pos_y)
    s_headset_pos_z = pandas.Series(data = headset_pos_z)
    s_controller_left_vel_x = pandas.Series(data = controller_left_vel_x)
    s_controller_left_vel_y = pandas.Series(data = controller_left_vel_y)
    s_controller_left_vel_z = pandas.Series(data = controller_left_vel_z)
    s_controller_left_angularVel_x = pandas.Series(data = controller_left_angularVel_x)
    s_controller_left_angularVel_y = pandas.Series(data = controller_left_angularVel_y)
    s_controller_left_angularVel_z = pandas.Series(data = controller_left_angularVel_z)
    s_controller_left_pos_x = pandas.Series(data = controller_left_pos_x)
    s_controller_left_pos_y = pandas.Series(data = controller_left_pos_y)
    s_controller_left_pos_z = pandas.Series(data = controller_left_pos_z)
    s_controller_left_rot_x = pandas.Series(data = controller_left_rot_x)
    s_controller_left_rot_y = pandas.Series(data = controller_left_rot_y)
    s_controller_left_rot_z = pandas.Series(data = controller_left_rot_z)
    s_controller_right_vel_x = pandas.Series(data = controller_right_vel_x)
    s_controller_right_vel_y = pandas.Series(data = controller_right_vel_y)
    s_controller_right_vel_z = pandas.Series(data = controller_right_vel_z)
    s_controller_right_angularVel_x = pandas.Series(data = controller_right_angularVel_x)
    s_controller_right_angularVel_y = pandas.Series(data = controller_right_angularVel_y)
    s_controller_right_angularVel_z = pandas.Series(data = controller_right_angularVel_z)
    s_controller_right_pos_x = pandas.Series(data = controller_right_pos_x)
    s_controller_right_pos_y = pandas.Series(data = controller_right_pos_y)
    s_controller_right_pos_z = pandas.Series(data = controller_right_pos_z)
    s_controller_right_rot_x = pandas.Series(data = controller_right_rot_x)
    s_controller_right_rot_y = pandas.Series(data = controller_right_rot_y)
    s_controller_right_rot_z = pandas.Series(data = controller_right_rot_z)

    res['mean_headset_pos_x'] = s_headset_pos_x.mean()
    res['mean_headset_pos_y'] = s_headset_pos_y.mean()
    res['mean_headset_pos_z'] = s_headset_pos_z.mean()
    res['mean_controller_left_vel_x'] = s_controller_left_vel_x.mean()
    res['mean_controller_left_vel_y'] = s_controller_left_vel_y.mean()
    res['mean_controller_left_vel_z'] = s_controller_left_vel_z.mean()
    res['mean_controller_left_angularVel_x'] = s_controller_left_angularVel_x.mean()
    res['mean_controller_left_angularVel_y'] = s_controller_left_angularVel_y.mean()
    res['mean_controller_left_angularVel_z'] = s_controller_left_angularVel_z.mean()
    res['mean_controller_left_pos_x'] = s_controller_left_pos_x.mean()
    res['mean_controller_left_pos_y'] = s_controller_left_pos_y.mean()
    res['mean_controller_left_pos_z'] = s_controller_left_pos_z.mean()
    res['mean_controller_left_rot_x'] = s_controller_left_rot_x.mean()
    res['mean_controller_left_rot_y'] = s_controller_left_rot_y.mean()
    res['mean_controller_left_rot_z'] = s_controller_left_rot_z.mean()
    res['mean_controller_right_vel_x'] = s_controller_right_vel_x.mean()
    res['mean_controller_right_vel_y'] = s_controller_right_vel_y.mean()
    res['mean_controller_right_vel_z'] = s_controller_right_vel_z.mean()
    res['mean_controller_right_angularVel_x'] = s_controller_right_angularVel_x.mean()
    res['mean_controller_right_angularVel_y'] = s_controller_right_angularVel_y.mean()
    res['mean_controller_right_angularVel_z'] = s_controller_right_angularVel_z.mean()
    res['mean_controller_right_pos_x'] = s_controller_right_pos_x.mean()
    res['mean_controller_right_pos_y'] = s_controller_right_pos_y.mean()
    res['mean_controller_right_pos_z'] = s_controller_right_pos_z.mean()
    res['mean_controller_right_rot_x'] = s_controller_right_rot_x.mean()
    res['mean_controller_right_rot_y'] = s_controller_right_rot_y.mean()
    res['mean_controller_right_rot_z'] = s_controller_right_rot_z.mean()

    # stds
    res['std_headset_pos_x'] = s_headset_pos_x.mean()
    res['std_headset_pos_y'] = s_headset_pos_y.mean()
    res['std_headset_pos_z'] = s_headset_pos_z.mean()
    res['std_controller_left_vel_x'] = s_controller_left_vel_x.std()
    res['std_controller_left_vel_y'] = s_controller_left_vel_y.std()
    res['std_controller_left_vel_z'] = s_controller_left_vel_z.std()
    res['std_controller_left_angularVel_x'] = s_controller_left_angularVel_x.std()
    res['std_controller_left_angularVel_y'] = s_controller_left_angularVel_y.std()
    res['std_controller_left_angularVel_z'] = s_controller_left_angularVel_z.std()
    res['std_controller_left_pos_x'] = s_controller_left_pos_x.std()
    res['std_controller_left_pos_y'] = s_controller_left_pos_y.std()
    res['std_controller_left_pos_z'] = s_controller_left_pos_z.std()
    res['std_controller_left_rot_x'] = s_controller_left_rot_x.std()
    res['std_controller_left_rot_y'] = s_controller_left_rot_y.std()
    res['std_controller_left_rot_z'] = s_controller_left_rot_z.std()
    res['std_controller_right_vel_x'] = s_controller_right_vel_x.std()
    res['std_controller_right_vel_y'] = s_controller_right_vel_y.std()
    res['std_controller_right_vel_z'] = s_controller_right_vel_z.std()
    res['std_controller_right_angularVel_x'] = s_controller_right_angularVel_x.std()
    res['std_controller_right_angularVel_y'] = s_controller_right_angularVel_y.std()
    res['std_controller_right_angularVel_z'] = s_controller_right_angularVel_z.std()
    res['std_controller_right_pos_x'] = s_controller_right_pos_x.std()
    res['std_controller_right_pos_y'] = s_controller_right_pos_y.std()
    res['std_controller_right_pos_z'] = s_controller_right_pos_z.std()
    res['std_controller_right_rot_x'] = s_controller_right_rot_x.std()
    res['std_controller_right_rot_y'] = s_controller_right_rot_y.std()
    res['std_controller_right_rot_z'] = s_controller_right_rot_z.std()

    # activity type
    res['user'] = file_name[0:3]

    return res

# print(preprocess("CAR_01.csv", 0))

def combine_files(dir: str, file_out: str, test_train: int):
    # create a dataframe from all files in Train

    files = os.listdir("Data/Lab3/Train")
    data_dicts = []

    for file in files:
        data_dict = preprocess(file, test_train)
        data_dicts.append(data_dict)

    # field names
    fields = ['peaks_controller_left_vel_x', 'peaks_controller_left_vel_y', 'peaks_controller_left_vel_z', 'peaks_controller_left_angularVel_x', 'peaks_controller_left_angularVel_y', 'peaks_controller_left_angularVel_z', 'peaks_controller_left_pos_x', 'peaks_controller_left_pos_y', 'peaks_controller_left_pos_z', 'peaks_controller_left_rot_x', 'peaks_controller_left_rot_y', 'peaks_controller_left_rot_z', 'peaks_controller_right_vel_x', 'peaks_controller_right_vel_y', 'peaks_controller_right_vel_z', 'peaks_controller_right_angularVel_x', 'peaks_controller_right_angularVel_y', 'peaks_controller_right_angularVel_z', 'peaks_controller_right_pos_x', 'peaks_controller_right_pos_y', 'peaks_controller_right_pos_z', 'peaks_controller_right_rot_x', 'peaks_controller_right_rot_y', 'peaks_controller_right_rot_z','mean_headset_pos_x', 'mean_headset_pos_y', 'mean_headset_pos_z','mean_controller_left_vel_x', 'mean_controller_left_vel_y', 'mean_controller_left_vel_z','mean_controller_left_angularVel_x', 'mean_controller_left_angularVel_y', 'mean_controller_left_angularVel_z','mean_controller_left_pos_x', 'mean_controller_left_pos_y', 'mean_controller_left_pos_z','mean_controller_left_rot_x', 'mean_controller_left_rot_y', 'mean_controller_left_rot_z','mean_controller_right_vel_x', 'mean_controller_right_vel_y', 'mean_controller_right_vel_z','mean_controller_right_angularVel_x', 'mean_controller_right_angularVel_y', 'mean_controller_right_angularVel_z','mean_controller_right_pos_x', 'mean_controller_right_pos_y', 'mean_controller_right_pos_z','mean_controller_right_rot_x', 'mean_controller_right_rot_y', 'mean_controller_right_rot_z','std_headset_pos_x', 'std_headset_pos_y', 'std_headset_pos_z','std_controller_left_vel_x', 'std_controller_left_vel_y', 'std_controller_left_vel_z','std_controller_left_angularVel_x', 'std_controller_left_angularVel_y', 'std_controller_left_angularVel_z','std_controller_left_pos_x', 'std_controller_left_pos_y', 'std_controller_left_pos_z','std_controller_left_rot_x', 'std_controller_left_rot_y', 'std_controller_left_rot_z','std_controller_right_vel_x', 'std_controller_right_vel_y', 'std_controller_right_vel_z','std_controller_right_angularVel_x', 'std_controller_right_angularVel_y', 'std_controller_right_angularVel_z','std_controller_right_pos_x', 'std_controller_right_pos_y', 'std_controller_right_pos_z','std_controller_right_rot_x', 'std_controller_right_rot_y', 'std_controller_right_rot_z','user']
    
    # name of csv
    filename = file_out

    # write to csv
    with open(filename, 'w') as csvfile:
        # create a csv dict writer object
        writer = csv.DictWriter(csvfile, fieldnames=fields)

        # write header and data rows
        writer.writeheader()
        writer.writerows(data_dicts)

combine_files("Data/Lab3/Train", "train_data_summary.csv", 0)
# combine_files("Data/Lab3/Validation", "train_data_summary.csv")

def create_dtree(train_file: str):
    # create dataframe and ensure all data is numbers
    d = {'CAR': 0, 'QUI': 1, "URU": 2}
    df = pandas.read_csv(train_file)

    df['user'] = df['user'].map(d)

    # separate feature columns from target column
    features = ['peaks_controller_left_vel_x', 'peaks_controller_left_vel_y', 'peaks_controller_left_vel_z', 'peaks_controller_left_angularVel_x', 'peaks_controller_left_angularVel_y', 'peaks_controller_left_angularVel_z', 'peaks_controller_left_pos_x', 'peaks_controller_left_pos_y', 'peaks_controller_left_pos_z', 'peaks_controller_left_rot_x', 'peaks_controller_left_rot_y', 'peaks_controller_left_rot_z', 'peaks_controller_right_vel_x', 'peaks_controller_right_vel_y', 'peaks_controller_right_vel_z', 'peaks_controller_right_angularVel_x', 'peaks_controller_right_angularVel_y', 'peaks_controller_right_angularVel_z', 'peaks_controller_right_pos_x', 'peaks_controller_right_pos_y', 'peaks_controller_right_pos_z', 'peaks_controller_right_rot_x', 'peaks_controller_right_rot_y', 'peaks_controller_right_rot_z','mean_headset_pos_x', 'mean_headset_pos_y', 'mean_headset_pos_z','mean_controller_left_vel_x', 'mean_controller_left_vel_y', 'mean_controller_left_vel_z','mean_controller_left_angularVel_x', 'mean_controller_left_angularVel_y', 'mean_controller_left_angularVel_z','mean_controller_left_pos_x', 'mean_controller_left_pos_y', 'mean_controller_left_pos_z','mean_controller_left_rot_x', 'mean_controller_left_rot_y', 'mean_controller_left_rot_z','mean_controller_right_vel_x', 'mean_controller_right_vel_y', 'mean_controller_right_vel_z','mean_controller_right_angularVel_x', 'mean_controller_right_angularVel_y', 'mean_controller_right_angularVel_z','mean_controller_right_pos_x', 'mean_controller_right_pos_y', 'mean_controller_right_pos_z','mean_controller_right_rot_x', 'mean_controller_right_rot_y', 'mean_controller_right_rot_z','std_headset_pos_x', 'std_headset_pos_y', 'std_headset_pos_z','std_controller_left_vel_x', 'std_controller_left_vel_y', 'std_controller_left_vel_z','std_controller_left_angularVel_x', 'std_controller_left_angularVel_y', 'std_controller_left_angularVel_z','std_controller_left_pos_x', 'std_controller_left_pos_y', 'std_controller_left_pos_z','std_controller_left_rot_x', 'std_controller_left_rot_y', 'std_controller_left_rot_z','std_controller_right_vel_x', 'std_controller_right_vel_y', 'std_controller_right_vel_z','std_controller_right_angularVel_x', 'std_controller_right_angularVel_y', 'std_controller_right_angularVel_z','std_controller_right_pos_x', 'std_controller_right_pos_y', 'std_controller_right_pos_z','std_controller_right_rot_x', 'std_controller_right_rot_y', 'std_controller_right_rot_z']
    
    X = df[features].values
    y  = df['user']

    dtree = DecisionTreeClassifier(criterion='gini', max_depth=1, min_samples_leaf=10, min_samples_split=20)
    dtree.fit(X, y)
    return dtree

    # GridSearchCV stuff
"""
    # Define the parameter grid
    param_grid = {'criterion':["gini","entropy"],
    'max_depth': [2, 3, 4, 5],
    'min_samples_leaf': [10, 20, 30],
    'min_samples_split': [20, 30, 40]}

    grid_search = GridSearchCV(dtree, param_grid, cv=5)
    grid_search.fit(X, y)
    print("Best hyperparameters: ", grid_search.best_params_)
    # Best hyperparameters:  {'criterion': 'gini', 'max_depth': 2, 'min_samples_leaf': 10, 'min_samples_split': 20}"""

    # print(dtree.predict([[21, 23, 36, 0.013482798090909078, -0.04247224632085562, -0.05696568897192513, 1.9615210787122295, 3.170571856589989, 0.6929715271035114]]))

# create_dtree("train_data_summary.csv")

def predict_shallow(sensor_data: str) -> str:
    dtree = create_dtree("train_data_summary.csv")

    input = preprocess(sensor_data, 1)
    input_vals = [val for key, val in input.items() if key != 'user']
    # print(input_vals)
    print(dtree.predict_proba([input_vals]))

    user = dtree.predict([input_vals])
    result = 100    # garbage value

    if (user == 0):
        result = "CAR"
    elif (user == 1):
        result = "QUI"
    elif (user == 2):
        result = "URU"
    
    return result

# print(predict_shallow("CAR_14.csv"))

def predict_shallow_folder(data_folder: str, output: str):
    # Run the model's prediction on all the sensor data in data_folder, writing labels
    # in sequence to an output text file.

    data_files = sorted(glob(f"{data_folder}/*.csv"))
    labels = map(predict_shallow, data_files)

    # actual values
    actual = []
    for file in data_files:
        # print(file)
        actual.append(file[21:24])

    actual_vals = []

    for el in actual:
        if ("CAR" in el):
            actual_vals.append(0)
        elif ("QUI" in el):
            actual_vals.append(1)
        elif ("URU" in el):
            actual_vals.append(2)

    # predicted values
    predicted_vals = []
    for label in labels:
        if ("CAR" in label):
            predicted_vals.append(0)
        elif ("QUI" in label):
            predicted_vals.append(1)
        elif ("URU" in label):
            predicted_vals.append(2)

    # print(predicted_vals)
    # print(actual_vals)

    with open(output, "w+") as output_file:
        output_file.write("\n".join(labels))

    target_names = ["CAR", "QUI", "URU"]
    # print(classification_report(actual_vals, predicted_vals))

if __name__ == "__main__":
    # Parse arguments to determine whether to predict on a file or a folder
    # You should not need to modify the below starter code, but feel free to
    # add more arguments for debug functions as needed.
    parser = argparse.ArgumentParser()

    sample_input = parser.add_mutually_exclusive_group(required=True)
    sample_input.add_argument(
        "sample", nargs="?", help="A .csv sensor data file to run predictions on"
    )
    sample_input.add_argument(
        "--label_folder",
        type=str,
        required=False,
        help="Folder of .csv data files to run predictions on",
    )

    parser.add_argument(
        "--output",
        type=str,
        default="Data/Lab3/ground-up-lab3.txt",
        help="Output filename of labels when running predictions on a directory",
    )

    args = parser.parse_args()

    if args.sample:
        print(predict_shallow(args.sample))

    elif args.label_folder:
        predict_shallow_folder(args.label_folder, args.output)



