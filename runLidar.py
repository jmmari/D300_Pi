import sys
from LiDARProcessor import LiDARProcessor

if __name__ == "__main__":

	# LiDARProcessor.run("xyz", "~/Documents/test.txt")
	LiDARProcessor.run_collect_points("xyz", "~/Documents/test.txt", 2000)