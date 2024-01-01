from PIL import Image

MSG_TERMINATOR = "$ovr$"

## Encodes a message inside of an image,
# using the least significant bits algorithm ##
def encode_message(image_path, message):
	img = Image.open(image_path, 'r').convert('RGB')
	image_arr = list(img.getdata())

	total_pixels = len(image_arr) // 3

	message += MSG_TERMINATOR	#	The terminator to mark the end of the message
	bit_message = ''.join([format(ord(i), "08b") for i in message])
	req_pixels = len(bit_message)

	if req_pixels > total_pixels:
		print("Invalid size")
		return None

	index = 0
	for p in range(total_pixels):
		pixel = image_arr[p]
		new_pixel = list(pixel)
		for q in range(0, 3):
			if index < req_pixels:
				new_pixel[q] = int(bin(pixel[q])[2:9] + bit_message[index], 2)
				image_arr[p] = tuple(new_pixel)
				index += 1

	img.putdata(image_arr)
	return img


## Decodes a message that was previously inserted inside of an image
# using the least significant bits algorithm ##
def decode_message(image_path):
	img = Image.open(image_path, 'r').convert('RGB')
	image_arr = list(img.getdata())

	total_pixels = len(image_arr) // 3

	hidden_bits = ""
	for p in range(total_pixels):
		for q in range(0, 3):
			hidden_bits += (bin(image_arr[p][q])[2:][-1])

	hidden_bits = [hidden_bits[i:i+8] for i in range(0, len(hidden_bits), 8)]

	message = ""
	for i in range(len(hidden_bits)):
		if message[-5:] == MSG_TERMINATOR:
			break
		else:
			message += chr(int(hidden_bits[i], 2))

	if MSG_TERMINATOR in message:
		return message[:-5]

	return 'Nothing to see here...'
