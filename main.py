import bisect
from statistics import mean
import math
import numpy as np
import os

DATA_DIR = "data/"
FILES = ["a.txt", "b.txt", "c.txt", "d.txt", "e.txt", "f.txt"]
SCHEDULE_FILES = ["a_schedule.txt", "b_schedule.txt", "c_schedule.txt", "d_schedule.txt", "e_schedule.txt", "f_schedule.txt"]
METHOD_DIR = "max-1/"

if not os.path.exists(METHOD_DIR):
	os.mkdir(METHOD_DIR)


def insert_time(intersection, street, total_time):
	if intersection not in intersections_dict:
		intersections_dict[intersection] = {}
	if street not in intersections_dict[intersection]:
		intersections_dict[intersection][street] = {}
	if total_time not in intersections_dict[intersection][street]:
		intersections_dict[intersection][street][total_time] = 0

	total_cars = intersections_dict[intersection][street][total_time]
	intersections_dict[intersection][street].update({total_time: total_cars + 1})


for file_name, schedule_file_name in zip(FILES, SCHEDULE_FILES):
	streets_dict = {}
	intersections_dict = {}

	with open(DATA_DIR + file_name, "r") as file:
		raw_params = file.readline()
		params = [int(i) for i in raw_params.split(" ")]

		for street_row in range(params[2]):
			raw_street = file.readline()
			street = raw_street.split(" ")
			streets_dict.update({street[2]: (int(street[1]), int(street[3]))})

		for car_row in range(params[3]):
			raw_car = file.readline()
			car = raw_car.strip().split(" ")
			car_path = car[1:]

			total_time = 0
			for index, street in enumerate(car_path):
				intersection, street_time = streets_dict[street]
				if index != 0:
					total_time += street_time
				insert_time(intersection, street, total_time)

	with open(METHOD_DIR + schedule_file_name, "w") as schedule_file:
		schedule_file.write(str(len(intersections_dict.keys())) + "\n")
		for intersection in intersections_dict.keys():
			schedule_file.write(str(intersection) + "\n")
			schedule_file.write(str(len(intersections_dict[intersection].keys())) + "\n")

			streets_times = []
			for street in intersections_dict[intersection].keys():
				times = []

				street_times_list = sorted(list(intersections_dict[intersection][street].keys()))

				street_times_array = np.asarray(street_times_list)
				if len(street_times_list) != 1:
					street_times_array = street_times_array[1:] - street_times_array[:-1]

				mean_arrival_difference = min(street_times_array)

				for time in street_times_list:
					times.append(intersections_dict[intersection][street][time])

				light_time = max(1, math.ceil(max(times)) - 1)
				streets_times.append((street_times_list[0], street, light_time))

			sorted_streets_times = sorted(streets_times)
			for start_time, street, light_time in sorted_streets_times:
				schedule_file.write(street + " " + str(light_time) + "\n")
