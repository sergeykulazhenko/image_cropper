#import streamlit as st
import os, random
import ftplib
from PIL import Image
import shutil

host = 'ftp4.nska.net'
ftp_user = 'test1@lookies.by'
ftp_password = 'U4hq0oLn'
ftp = ftplib.FTP(host, ftp_user, ftp_password)


base_folder = 'img600x866'
base_folder_crop = base_folder + '_crop'

def pick_random_img():
    # get the list of images
    img_files_path = []
    base_folder_el_list = ftp.nlst(base_folder)
    base_folder_el_list = [x for x in base_folder_el_list if "." not in x]
    for el in base_folder_el_list:
        n_folder_element_list = ftp.nlst(el)
        for i in n_folder_element_list:
            img_files_path.append(i)
    img_files_path = [x.replace('img600x866/', '') for x in img_files_path if ".jpg" in x ]
    print("TOTAL IMAGES: " + str(len(img_files_path)))

    # get the list of cropped files
    croped_img_files_path = []
    base_folder_crop_el_list = ftp.nlst(base_folder_crop)
    base_folder_crop_el_list = [x for x in base_folder_crop_el_list if "." not in x]
    for el in base_folder_crop_el_list:
        n_folder_element_list = ftp.nlst(el)
        for i in n_folder_element_list:
            croped_img_files_path.append(i)
    croped_img_files_path = [x.replace('img600x866_crop/', '') for x in croped_img_files_path if ".jpg" in x]
    print(croped_img_files_path)
    print("CROPPED IMAGES: " + str(len(croped_img_files_path)))

    # get the list of "files to do"
    files_to_do = [('img600x866/' + x) for x in img_files_path if x not in croped_img_files_path]

    print("LEFT TO DO: " + str(len(files_to_do)))
    #st.text("LEFT TO DO: " + str(len(files_to_do)))

    # pick a random file "to do"
    print(files_to_do[0])
    try:
        ftp.retrbinary("RETR " + files_to_do[0], open(A, 'wb').write)
    except:
        print("Error")
    print(files_to_do[0])
    return files_to_do[0]

def load_file_trough_ftp(file_to_do):
    file_to_do_split = file_to_do.split('/')
    filename = file_to_do_split[2]
    localfile = open(filename, "wb")
    ftp.retrbinary(f"RETR {file_to_do}", localfile.write)
    localfile.close()
    return filename

def save_cropped_img_ftp():
    #filename_split = img_file.split('/')
    img = Image.open('AD093EMJLZE4_11419934_4_v1_2x.jpg')
    img.save('22AD093EMJLZE4_11419934_4_v1_2x.jpg')
    img = open('22AD093EMJLZE4_11419934_4_v1_2x.jpg', 'rb')
    ftp.storbinary('STOR tmp/AD093EMJLZE4_11419934_4_v1_2x.jpg', img)
    #cropped_img.save('/app/img600x866_crop/' + str(img_file))


#load_file_trough_ftp(pick_random_img())
#save_cropped_img_ftp()