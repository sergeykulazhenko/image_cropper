#import streamlit as st
import os, random
import ftplib
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
    return files_to_do[0]



def save_cropped_img(cropped_img, img_file):
    cropped_img.save('/app/img600x866_crop/' + str(img_file))

pick_random_img()