import os
import secrets
from flask import url_for, current_app
from PIL import Image
from smtplib import SMTP

def save_profile_pictures(profile_picture):
	"""This will take a arg (Format: filename.extension) as form data.
	It will create a thumbnail of size (150, 150)."""
	hex_name = secrets.token_hex(8)
	_, file_extn = os.path.splitext(profile_picture.filename)
	pic_filename = hex_name + file_extn
	pic_directory = os.path.join(current_app.root_path, "static/profile_pics", pic_filename)
	image_size = (150, 150)
	profile_pic = Image.open(profile_picture)
	profile_pic.thumbnail(image_size)
	profile_pic.save(pic_directory)
	return pic_filename


def send_reset_mail(user):
	token = user.generate_reset_token()
	# TODO: Create a mailing function
	with SMTP(host=current_app.config["HOST"], port=587) as connection:
		connection.starttls()
		connection.login(user=current_app.config["SENDER"], password=current_app.config["PASSWORD"])
		connection.sendmail(
			from_addr=current_app.config["SENDER"],
			to_addrs=user.email,
			msg=f"""Subject: Reset password request\n\n 
Please click the following link to reset your password : {url_for("users.reset_password", token=token, _external=True)} 
If the reset was not initiated by you, do not proceed with the link and no changes will be made.
If this message was received to the wrong user, we apologies for the incovinence and confusion."""
)
