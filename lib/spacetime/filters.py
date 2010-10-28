from __future__ import division

import numpy
import scipy.stats

def BGSubtractLineByLine(frame):
	# FIXME: this modifies the frame in-place, I'm not sure if this is desired behaviour
	new = numpy.zeros(frame.image.shape)
	pixels = numpy.arange(frame.image.shape[1])
	for i, line in enumerate(frame.image):
		slope, intercept, r_value, p_value, stderr = scipy.stats.linregress(pixels, line)
		new[i,:] = line - (slope * pixels + intercept)
	frame.image = new
	return frame

def ClipStdDev(number):
	# FIXME: this modifies the frame in-place, I'm not sure if this is desired behaviour
	def clip(frame):
		avg, stddev = frame.image.mean(), frame.image.std()
		frame.image = numpy.clip(frame.image, avg - number * stddev, avg + number * stddev)
		return frame
	return clip

def average(npoints):
	# FIXME: this modifies the frame in-place, I'm not sure if this is desired behaviour
	def avgn(data):
		data.value = numpy.array(map(numpy.mean, numpy.array_split(data.value, numpy.ceil(data.value.size/npoints))))
		data.time = numpy.array(map(numpy.mean, numpy.array_split(data.time, numpy.ceil(data.time.size/npoints))))
		return data
	return avgn