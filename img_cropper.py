import streamlit as st
import s3_store
from streamlit_cropper import st_cropper
from PIL import Image
import random
import os


BUCKET = 'kulazhenko-image-cropper'

st.set_option('deprecation.showfileUploaderEncoding', False)
st.header("Lookies! Cropper")
new_image = st.button("New Image")
crop_button = st.button("Crop!")

if new_image:
  s3_img = os.path.join(
    '/original/',
    s3_store.random_uncroped_filename(BUCKET)
  )
  local_img = s3_store.download_file(s3_img, BUCKET)

aspect_choice = st.radio(label="Aspect Ratio", options=["1:1"])
aspect_dict = {"1:1": (1, 1)}
aspect_ratio = aspect_dict[aspect_choice]

img = Image.open(local_img)
cropped_img = st_cropper(img, realtime_update=True, box_color='#0000FF', aspect_ratio=aspect_ratio)
st.image(cropped_img)

if crop_button:
  cropped_img.save(str(img_file))
