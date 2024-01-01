from flask import Flask, render_template, request, send_file
from stegano import encode_message, decode_message
from PIL import Image
from io import BytesIO
import os
import tempfile
import base64

app = Flask(__name__, static_folder="public")

# The encoder page
@app.route('/image/encode', methods=['GET', 'POST'])
def encoder_page():
	if request.method == 'POST':
		# Check if the post request has the file and message fields
		if 'file' not in request.files or not request.files['file']:
			return render_template('encode.html', response='Try again.')
		if 'message' not in request.form or not request.form['message']:
			return render_template('encode.html', response='Try again.')

		file = request.files['file']
		message = request.form['message']

		# Save the uploaded file to a temporary location
		temp_dir = tempfile.mkdtemp()
		file_path = os.path.join(temp_dir, file.filename)
		file.save(file_path)

		image = Image.open(file_path, 'r')
		img_format = image.format.lower()

		if img_format != 'png' and img_format != 'bmp':
			return render_template('decode.html', response='Image format not supported.')

		# Encode the message into the image
		encoded_image = encode_message(file_path, message)

		if encoded_image is None:
			return render_template('encode.html', response="Message was too long.")

		# Save the encoded image
		save_path = './public/data'
		if not os.path.exists(save_path):
			os.makedirs(save_path)
		save_filename = os.path.join(save_path, 'encoded.png')
		encoded_image.save(save_filename)

		# Send the encoded image as a binary download
		return send_file(save_filename, as_attachment=True)

	return render_template('encode.html')

# The decoder page
@app.route('/image/decode', methods=['GET', 'POST'])
def decoder_page():
	# Same as for the encoder
	if request.method == 'POST':
		if 'file' not in request.files or not request.files['file']:
			return render_template('decode.html', secret='try again.')

		file = request.files['file']

		temp_dir = tempfile.mkdtemp()
		file_path = os.path.join(temp_dir, file.filename)
		file.save(file_path)

		image = Image.open(file_path, 'r')
		img_format = image.format.lower()

		if img_format != 'png' and img_format != 'bmp':
			return render_template('decode.html', secret='image format not supported.')

		save_path = './public/data'
		if not os.path.exists(save_path):
			os.makedirs(save_path)
		save_filename = os.path.join(save_path, 'decoded.png')
		image.save(save_filename)

		# Decode the message from the image
		message = decode_message(file_path)

		return render_template('decode.html', secret=message)

	return render_template('decode.html', secret='nothing so far :(')

# Latest encoded page
@app.route('/image/last/encoded')
def latest_encoded():
	file_path = './public/data/encoded.png'

	if not os.path.exists(file_path):
		return render_template('last_encoded.html', message='Image not found')

	image = Image.open(file_path, "r")
	img_format = image.format.lower()

	binary_data = BytesIO()
	image.save(binary_data, format=img_format)
	binary_data.seek(0)

	base64_data = base64.b64encode(binary_data.read()).decode('utf-8')

	return render_template('last_encoded.html', image_data=base64_data)

# Latest decoded page
@app.route('/image/last/decoded')
def latest_decoded():
	file_path = './public/data/decoded.png'

	if not os.path.exists(file_path):
		return render_template('last_decoded.html', message='Image not found')

	image = Image.open(file_path, "r")
	img_format = image.format.lower()

	binary_data = BytesIO()
	image.save(binary_data, format=img_format)
	binary_data.seek(0)

	base64_data = base64.b64encode(binary_data.read()).decode('utf-8')

	return render_template('last_decoded.html', image_data=base64_data)

# Home page
@app.route("/")
def index():
	return render_template("index.html")

if __name__ == "__main__":
	app.run(debug=True, port=5000)
