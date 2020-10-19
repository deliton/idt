from .smartcrop import SmartCrop
from .longer_side import crop_longer_side
from .shorter_side import crop_shorter_side

def get_resizer(img, target_size, resizer):
	if target_size == 0:
		return img

	if resizer == "smartcrop":
		sc = SmartCrop()
		return sc.run_crop(img, target_size)
	elif resizer == 'shorter_side':
		return crop_shorter_side(img,target_size)
	elif resizer == 'longer_side':
		return crop_longer_side(img, target_size)


