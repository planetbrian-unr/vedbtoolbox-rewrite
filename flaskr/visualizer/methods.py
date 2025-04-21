# written by matt

# base
import os
from io import BytesIO
import math
from json import dumps

# flask
from flask import request

# pip
import msgpack
import numpy as np
import pandas as pd

# The following two functions were provided to us by Brian Szekely, a UNR PhD student and a former student
# of Paul MacNeilage's Self Motion Lab.
# They work with the pldata files, turning them into readable format for our graphing code
def read_pldata(file_path):    
    try:
        with open(file_path, 'rb') as file:
            unpacker = msgpack.Unpacker(file, raw=False)
            data = []
            for packet in unpacker:
                data.append(packet)
    except OSError:
        print(f'File path: "{file_path}" not found.')
        print(f"Current working directory: {os.getcwd()}")
        raise OSError
    return data

def parse_pldata(data):
    unpacker = msgpack.Unpacker(BytesIO(data), raw=False)
    parsed_data = next(unpacker)

    # flatten nested structures
    flattened = {}
    for key, value in parsed_data.items():
        if isinstance(value, list):
            for i, item in enumerate(value):
                flattened[f"{key}_{i}"] = item
        else:
            flattened[key] = value

    return flattened

# This function was taken from Michelle, an individual who has worked on the VEDB and specifically published some
# information about accessing and visualizing the VEDB, in which this function was found.
# That can be found here: https://github.com/vedb/vedb-demos/blob/main/VEDB_demo_explore_session.ipynb
def load_as_dict(path):
    tmp = np.load(path, allow_pickle=True)
    params = {}
    for k, v in tmp.items():
        if isinstance(v, np.ndarray) and (v.dtype==np.dtype("O")):
            if v.shape==():
              params[k] = v.item()
            else:
              params[k] = v
    return params

# Some data files in the VEDB record NANs when the hardware stops recording (for whatever reason)
def count_nans(vel_list):
    nan_count = sum(1 for value in vel_list if isinstance(value, float) and math.isnan(value))
    print("Nan Count Ratio:", nan_count / len(vel_list))
    print("Nan Count:", nan_count)
    return nan_count

def generate_velocity_graphs(filename_list: list[str]):
    # assuming either 1. both files exist, 2. neither file exists
    global graph_file_list
    for filename in filename_list:
        data = read_pldata(filename)
        df = pd.DataFrame(data)
        linear_vel_0_list = []
        linear_vel_1_list = []
        linear_vel_2_list = []

        angular_velocity_0_list = []
        angular_velocity_1_list = []
        angular_velocity_2_list = []

        timestamp_list = []
        first_timestamp = parse_pldata(df[1].iloc[0])['timestamp']

        for i in range(len(df)):
            data_frame = parse_pldata(df[1].iloc[i])

            data_type_1 = 'linear_velocity_0'
            data_type_2 = 'linear_velocity_1'
            data_type_3 = 'linear_velocity_2'

            data_type_4 = 'angular_velocity_0'
            data_type_5 = 'angular_velocity_1'
            data_type_6 = 'angular_velocity_2'

            if not math.isnan(data_frame[data_type_1]):
                linear_vel_0_list.append(data_frame[data_type_1])
                linear_vel_1_list.append(data_frame[data_type_2])
                linear_vel_2_list.append(data_frame[data_type_3])

                angular_velocity_0_list.append(data_frame[data_type_4])
                angular_velocity_1_list.append(data_frame[data_type_5])
                angular_velocity_2_list.append(data_frame[data_type_6])

                timestamp_list.append(data_frame['timestamp'] - first_timestamp)

        json_timestamp = dumps(timestamp_list)

        json_lin0 = dumps(linear_vel_0_list)
        json_lin1 = dumps(linear_vel_1_list)
        json_lin2 = dumps(linear_vel_2_list)

        json_ang0 = dumps(angular_velocity_0_list)
        json_ang1 = dumps(angular_velocity_1_list)
        json_ang2 = dumps(angular_velocity_2_list)
        # i am leaving behind absolutely horrific legacy code

        json_list = [json_timestamp, json_lin0, json_lin1, json_lin2, json_ang0, json_ang1, json_ang2]
        return json_list

def generate_gaze_graph(filename_list):
    for filename in filename_list:
        gaze_dict = load_as_dict(filename)
        left_gaze = gaze_dict['left']
        right_gaze = gaze_dict['right']

        left_timestamps = []
        right_timestamps = []
        left_norm_pos_x = []
        left_norm_pos_y = []
        right_norm_pos_x = []
        right_norm_pos_y = []

        left_first_timestamp = left_gaze['timestamp'][0]
        # for value in left_gaze['timestamp']:
        #     left_timestamps.append(value - left_first_timestamp)
        counter = 0
        for value in left_gaze['norm_pos']:
            if value[0] < 1.0 and value[0] > -0.1 and value[1] < 1.0 and value[1] > -0.1:
                left_norm_pos_x.append(value[0])
                left_norm_pos_y.append(value[1])
                left_timestamps.append(left_gaze['timestamp'][counter] - left_first_timestamp)
                counter = counter + 1

        right_first_timestamp = right_gaze['timestamp'][0]
        # for value in  right_gaze['timestamp']:
        #     right_timestamps.append(value - right_first_timestamp)
        counter = 0
        for value in  right_gaze['norm_pos']:
            if value[0] < 1.0 and value[0] > -0.1 and value[1] < 1.0 and value[1] > -0.1:
                right_norm_pos_x.append(value[0])
                right_norm_pos_y.append(value[1])
                right_timestamps.append(right_gaze['timestamp'][counter] - right_first_timestamp)
                counter = counter + 1

        # NON DOWN SAMPLED TIMESTAMPS (around 82000 left or 78000 right), removed <0 and >1, i think those are out of bounds
        # json_left_timestamp = dumps(left_timestamps)
        # json_left_norm_pos_x = dumps(left_norm_pos_x)
        # json_left_norm_pos_y = dumps(left_norm_pos_y)
        #
        # json_right_timestamp = dumps(right_timestamps)
        # json_right_norm_pos_x = dumps(right_norm_pos_x)
        # json_right_norm_pos_y = dumps(right_norm_pos_y)

        # DOWN SAMPLED TIMESTAMPS, these have 1/10 of the original value so around 8200 left or 7800 right
        sampled_left_x = left_norm_pos_x[::10]
        sampled_left_y = left_norm_pos_y[::10]
        sampled_right_x = right_norm_pos_x[::10]
        sampled_right_y = right_norm_pos_y[::10]

        sampled_left_time = left_timestamps[::10]
        sampled_right_time = right_timestamps[::10]

        json_left_timestamp = dumps(sampled_left_time)
        json_left_norm_pos_x = dumps(sampled_left_x)
        json_left_norm_pos_y = dumps(sampled_left_y)

        json_right_timestamp = dumps(sampled_right_time)
        json_right_norm_pos_x = dumps(sampled_right_x)
        json_right_norm_pos_y = dumps(sampled_right_y)

        gaze_json = [json_left_timestamp, json_left_norm_pos_x, json_left_norm_pos_y, json_right_timestamp, json_right_norm_pos_x, json_right_norm_pos_y]
        return gaze_json

# Loads the visualizer once files have been correctly uploaded
def load_visualizer():
    if request.method == 'POST':
        if not show_form1 and not show_form2:
            if get_is_folder(2):
                file_to_graph = "flaskr/" + get_folder_name(2) + "/odometry.pldata"
            else:
                file_to_graph = "odometry.pldata"

            # This returns a JSON_list, in the refactor this will go to the frontend JS for graph generation, in the form of lists not graphs
            vel_data = generate_velocity_graphs([file_to_graph])
            if get_is_folder(2):
                file_to_graph = "flaskr/" + get_folder_name(2) + "/gaze.npz"
            else:
                file_to_graph = "gaze.npz"
            gaze_data = generate_gaze_graph([file_to_graph])

            return render_template("visualizer/visualizer.html", velocity_timestamps = vel_data[0], linear_0 = vel_data[1],
                                   linear_1 = vel_data[2], linear_2 = vel_data[3], angular_0 = vel_data[4], angular_1 = vel_data[5], angular_2 = vel_data[6],
                                   left_gaze_timestamps = gaze_data[0], left_norm_pos_x = gaze_data[1], left_norm_pos_y = gaze_data[2],
                                   right_gaze_timestamps = gaze_data[3], right_norm_pos_x = gaze_data[4], right_norm_pos_y = gaze_data[5])
        else:
            raise Exception(f"Invalid Action") #how did it get here

def download_graphs():
    linear_graph = request.args.get('linearGraph')
    angular_graph = request.args.get('angularGraph')
    gaze_graph = request.args.get('gazeGraph')

    linear_file_name = request.args.get('linearFileName')
    angular_file_name = request.args.get('angularFileName')
    gaze_file_name = request.args.get('gazeFileName')

    if not os.path.exists("graphs"):
        os.mkdir("graphs")

    linear_graph.write_image("images" + linear_file_name + ".png")
    angular_graph.write_image("images" + angular_file_name + ".png")
    gaze_graph.write_image("images" + gaze_file_name + ".png")

#Function ran when the viewer's exit viewer button is clicked
def new_files():
    global video_file_list
    global data_file_list

    delete_files_in_list(video_file_list)
    delete_files_in_list(data_file_list)

    delete_folders()
    clear_lists()