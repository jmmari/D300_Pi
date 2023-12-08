import subprocess
import os
import re
import math
import sys
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from mpl_toolkits.mplot3d import Axes3D
from collections import deque
import numpy as np

class LiDARProcessor:
	path_to_sdk = "/home/user/ldlidar_ws/ldlidar_stl_sdk"
	max_depth = 5000
	#----------------------------------------------------------------------------------------------------------------------
	@staticmethod
	def set_sdk_path(a_path):
		LiDARProcessor.path_to_sdk = a_path

	@staticmethod
	def process_lidar_data(line, mode):
		match = re.search(r'angle:([\d\.]+),distance\(mm\):(\d+),intensity:(\d+)', line)
		if match:
			angle = float(match.group(1))
			distance = int(match.group(2))
			intensity = int(match.group(3))

			if mode == "raw":
				return f"{angle};{distance};{intensity}"
			elif mode == "xyz":
				# Convert to Cartesian coordinates (assuming z=0)
				rad = math.radians(angle)
				x = distance * math.cos(rad)
				y = distance * math.sin(rad)
				z = 0
				return f"{x};{y};{z};{intensity}"
	#----------------------------------------------------------------------------------------------------------------------
	@staticmethod
	def execute_command(product_type, comm_mode, port_path, server_ip_addr, server_port_addr, mode, output_file=None):
		command = []

		if comm_mode == "network":
			command = [f'{LiDARProcessor.path_to_sdk}/build/ldlidar_stl_node', product_type, 'networkcom_tcpclient', server_ip_addr, server_port_addr]
		elif comm_mode == "serial":
			os.system(f'sudo chmod 777 {port_path}')
			command = [f'{LiDARProcessor.path_to_sdk}/build/ldlidar_stl_node', product_type, 'serialcom', port_path]
		else:
			raise ValueError("Input [communication_mode] is error.")

		with subprocess.Popen(command, stdout=subprocess.PIPE, text=True) as proc:
			if output_file:
				output_file = os.path.expanduser(output_file)  # Expands '~' to the user's home directory
				with open(output_file, 'w') as outfile:
					for line in proc.stdout:
						processed_line = LiDARProcessor.process_lidar_data(line, mode)
						if processed_line:
							print(processed_line, file=outfile)
			else:
				for line in proc.stdout:
					processed_line = LiDARProcessor.process_lidar_data(line, mode)
					if processed_line:
						print(processed_line)

	@staticmethod
	def run(mode='raw', filename=None):
		product_type = "LD06"
		comm_mode = "serial"
		port_path = "/dev/ttyUSB0"
		server_ip_addr = "None"
		server_port_addr = "0"

		LiDARProcessor.execute_command(product_type, comm_mode, port_path, server_ip_addr, server_port_addr, mode, filename)
	#----------------------------------------------------------------------------------------------------------------------	
	@staticmethod
	def count_command(product_type, comm_mode, port_path, server_ip_addr, server_port_addr, mode, num_points=None, output_file=None):
		command = []

		if comm_mode == "network":
			command = [f'{LiDARProcessor.path_to_sdk}/build/ldlidar_stl_node', product_type, 'networkcom_tcpclient', server_ip_addr, server_port_addr]
		elif comm_mode == "serial":
			os.system(f'sudo chmod 777 {port_path}')
			command = [f'{LiDARProcessor.path_to_sdk}/build/ldlidar_stl_node', product_type, 'serialcom', port_path]
		else:
			raise ValueError("Input [communication_mode] is error.")


		with subprocess.Popen(command, stdout=subprocess.PIPE, text=True) as proc:
			point_count = 0
			for line in proc.stdout:
				if num_points is not None and point_count >= num_points:
					break

				processed_line = LiDARProcessor.process_lidar_data(line, mode)
				if processed_line:
					if output_file:
						output_file.write(processed_line + '\n')  # Write to file
					else:
						print(processed_line)  # Print to stdout

					point_count += 1

	@staticmethod
	def run_collect_points(mode='raw', filename=None, num_points=None):
		product_type = "LD06"
		comm_mode = "serial"
		port_path = "/dev/ttyUSB0"
		server_ip_addr = "None"
		server_port_addr = "0"

		if filename:
			filename = os.path.expanduser(filename)  # Expands '~' to the user's home directory
			with open(filename, 'w') as outfile:
				LiDARProcessor.count_command(product_type, comm_mode, port_path, server_ip_addr, server_port_addr, mode, num_points, outfile)
		else:
			LiDARProcessor.count_command(product_type, comm_mode, port_path, server_ip_addr, server_port_addr, mode, num_points)

	#----------------------------------------------------------------------------------------------------------------------	
	@staticmethod
	def yield_lidar(product_type, comm_mode, port_path, server_ip_addr, server_port_addr, mode):
		command = []

		if comm_mode == "network":
			command = [f'{LiDARProcessor.path_to_sdk}/build/ldlidar_stl_node', product_type, 'networkcom_tcpclient', server_ip_addr, server_port_addr]
		elif comm_mode == "serial":
			os.system(f'sudo chmod 777 {port_path}')
			command = [f'{LiDARProcessor.path_to_sdk}/build/ldlidar_stl_node', product_type, 'serialcom', port_path]
		else:
			raise ValueError("Input [communication_mode] is error.")
		
		with subprocess.Popen(command, stdout=subprocess.PIPE, text=True) as proc:
			for line in proc.stdout:
				processed_line = LiDARProcessor.process_lidar_data(line, mode)
				if processed_line:
					yield processed_line
	@staticmethod
	def update_plot(num, data_gen, x_data, y_data, z_data, intensity_data, scatter, ax, is_3d):
		try:
			new_point = next(data_gen).split(';')
			x, y, z, intensity = map(float, new_point)
			x_data.append(x)
			y_data.append(y)
			z_data.append(z)
			intensity_data.append(intensity)

			if is_3d:
				scatter._offsets3d = (x_data, y_data, z_data)
				scatter.set_array(np.array(intensity_data))
			else:
				scatter.set_offsets(list(zip(x_data, y_data)))
				scatter.set_array(np.array(intensity_data))
		except StopIteration:
			return
		return scatter,

	@staticmethod
	def animated_lidar_plot(buffer_size=1000, is_3d=False):
		x_data, y_data, z_data, intensity_data = deque(maxlen=buffer_size), deque(maxlen=buffer_size), deque(maxlen=buffer_size), deque(maxlen=buffer_size)

		fig = plt.figure()

		if is_3d:
			ax = fig.add_subplot(111, projection='3d')
			scatter = ax.scatter([], [], [], s=10, c=[], cmap='viridis_r')
		else:
			ax = fig.add_subplot(111)
			scatter = ax.scatter([], [], s=10, c=[], cmap='viridis_r')

		max_depth = 5000
		ax.set_xlim(-max_depth, max_depth)
		ax.set_ylim(-max_depth, max_depth)
		if is_3d:
			ax.set_zlim(-max_depth, max_depth)

		data_gen = LiDARProcessor.yield_lidar("LD06", "serial", "/dev/ttyUSB0", "None", "0", "xyz")

		ani = FuncAnimation(fig, LiDARProcessor.update_plot, fargs=(data_gen, x_data, y_data, z_data, intensity_data, scatter, ax, is_3d), frames=100, interval=50, blit=False)

		plt.colorbar(scatter, ax=ax)
		plt.show()

