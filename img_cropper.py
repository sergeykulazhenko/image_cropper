import streamlit as st
from streamlit_cropper import st_cropper
from PIL import Image
from pick_save import pick_random_img, load_file_trough_ftp, save_cropped_img_ftp, create_list_of_files
import ftplib



base_folder = '/app/img600x866'
base_folder_crop = base_folder + '_crop'
st.set_option('deprecation.showfileUploaderEncoding', False)
st.header("Lookies! Cropper")

create_list_of_files()


new_image = st.button("New Image")
crop_button = st.button("Crop!")
list_button = st.button("Index Images")

if new_image:
  img_file = pick_random_img()
aspect_choice = st.radio(label="Aspect Ratio", options=["1:1"])
aspect_dict = {"1:1": (1, 1)}
aspect_ratio = aspect_dict[aspect_choice]



img_file = pick_random_img()

img = Image.open(load_file_trough_ftp(img_file))
cropped_img = st_cropper(img, realtime_update=True, box_color='#0000FF', aspect_ratio=aspect_ratio)
st.image(cropped_img)

if crop_button:
  save_cropped_img_ftp(cropped_img, img_file)
  img_file = pick_random_img()
if list_button:
  create_list_of_files()
