from pynput import mouse
from pynput.mouse import Controller
import Quartz

# HOW TO USE:
# 1. Set desired scrolling sensitivity
# 2. Run script, e.g. python mac-scroll-fix.py
# Recommended to add this script to your startup items

# desired scrolling sensitivity
sensitivityX = -15
sensitivityY = 10


mouseController = Controller()

# Intercept event and modify it if it's mouse scroll
def darwin_intercept(event_type, event):
	# detect if it was mouse scroll event (type 22)
	if event_type == 22:
		# all possible event properties: https://developer.apple.com/documentation/coregraphics/cgeventfield

		# 11/12 - kCGScrollWheelEventDeltaAxis1/2
		# Change in vertical position
		# scroll up values are 0 and higher
		# scroll down values are -1 and lower
		originalDistanceX = Quartz.CGEventGetIntegerValueField(event, 12)
		originalDistanceY = Quartz.CGEventGetIntegerValueField(event, 11)
		
		# 96/97 - kCGScrollWheelEventPointDeltaAxis1/2
		# Pixel-based scrolling distance
		# Used to determine which axis was scrolled, as originalDistanceX/Y can be 0 both
		# when scrolled very small positive distance or when scrolled on dirrent axis
		onAxisX = Quartz.CGEventGetIntegerValueField(event, 97) != 0
		onAxisY = Quartz.CGEventGetIntegerValueField(event, 96) != 0
				
		newDistanceX = 0
		if onAxisX:
			newDistanceX = sensitivityX if originalDistanceX >= 0 else -sensitivityX

		newDistanceY = 0
		if onAxisY:
			newDistanceY = sensitivityY if originalDistanceY >= 0 else -sensitivityY

		# For debugging:
		# print('Axis: {0} original: {1}, new: {2}, 97: {3}, 96: {4}'.format(
		# 	(int(onAxisX), int(onAxisY)),
		# 	(originalDistanceX, originalDistanceY),
		# 	(newDistanceX, newDistanceY),
		# 	Quartz.CGEventGetIntegerValueField(event, 97),
		# 	Quartz.CGEventGetIntegerValueField(event, 96)))
				
		Quartz.CGEventSetIntegerValueField(event, 12, newDistanceX)
		Quartz.CGEventSetIntegerValueField(event, 11, newDistanceY)
		
	return event


with mouse.Listener(darwin_intercept=darwin_intercept) as listener:
    listener.join()
