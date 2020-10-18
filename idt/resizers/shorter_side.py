from PIL import Image

def crop_shorter_side(img, size):
	width, height = img.size
	if width < size or height < size:
		return img.thumbnail(size, Image.ANTIALIAS)
	elif width > height:
		ratio = float(width) / float(height)
		new_width = int(size * ratio)
		return img.resize((new_width, size), Image.ANTIALIAS)
	else:
		ratio = float(height) / float(width)
		new_height = int(size * ratio)
		return img.resize((width_size, size), Image.ANTIALIAS)
