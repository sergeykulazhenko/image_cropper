import streamlit as st
import os, random
import os.path
import ftplib
from PIL import Image
import shutil

host = 'ftp4.nska.net'
ftp_user = 'test1@lookies.by'
ftp_password = 'U4hq0oLn'
ftp = ftplib.FTP(host, ftp_user, ftp_password)


base_folder = 'img600x866'
base_folder_crop = base_folder + '_crop_t'

list_of_files = []
a_file = open('list_to_do.txt', "r")
for line in a_file:
    stripped_line = line.strip()
    print(stripped_line)
    list_of_files.append(stripped_line)
a_file.close()

def pick_random_img():

    #print("LEFT TO DO: " + str(len(files_to_do)))
    #st.text("LEFT TO DO: " + str(len(files_to_do)))

    # pick a random file "to do"
    #print(files_to_do[0])

    first_line = list_of_files[0]
    try:
        ftp.retrbinary("RETR " + first_line, open(A, 'wb').write)
    except:
        print("Error")
    return first_line

def load_file_trough_ftp(file_to_do):
    file_to_do_split = file_to_do.split('/')
    filename = file_to_do_split[2]
    localfile = open(filename, "wb")
    ftp.retrbinary(f"RETR {file_to_do}", localfile.write)
    localfile.close()
    return filename

def save_cropped_img_ftp(cropped_img, img_file):
    filename_split = img_file.split('/')
    img = cropped_img
    img.save(filename_split[2])
    img = open(filename_split[2], 'rb')
    ftp.storbinary('STOR ' + base_folder_crop + '/' + str(filename_split[1]) + '/' + str(filename_split[2]), img)
    del list_of_files[0]
    textfile = open("list_to_do.txt", "w")
    # write to txt
    for element in list_of_files:
        textfile.write(element + "\n")
    textfile.close()


def create_list_of_files():
    if os.path.isfile("list_to_do.txt") == True:
        print("True")
    else:
        # get the list of images
        img_files_path = []
        base_folder_el_list = ftp.nlst(base_folder)
        base_folder_el_list = [x for x in base_folder_el_list if "." not in x]
        for el in base_folder_el_list:
            n_folder_element_list = ftp.nlst(el)
            for i in n_folder_element_list:
                img_files_path.append(i)
        img_files_path = [x.replace(base_folder + '/', '') for x in img_files_path if ".jpg" in x]
        print("TOTAL IMAGES: " + str(len(img_files_path)))

        # get the list of cropped files
        croped_img_files_path = []
        base_folder_crop_el_list = ftp.nlst(base_folder_crop)
        base_folder_crop_el_list = [x for x in base_folder_crop_el_list if "." not in x]
        for el in base_folder_crop_el_list:
            n_folder_element_list = ftp.nlst(el)
            for i in n_folder_element_list:
                croped_img_files_path.append(i)
        croped_img_files_path = [x.replace(base_folder_crop + '/', '') for x in croped_img_files_path if ".jpg" in x]
        print("CROPPED IMAGES: " + str(len(croped_img_files_path)))

        # get the list of "files to do"
        files_to_do = [(base_folder + '/' + x) for x in img_files_path if x not in croped_img_files_path]
        textfile = open("list_to_do.txt", "w")

        #write to txt
        for element in files_to_do:
            textfile.write(element + "\n")
        textfile.close()

def test():
    a_file = open('list_to_do.txt', "r")
    for line in a_file:
        stripped_line = line.strip()
        print(stripped_line)
        break
    #line_list = stripped_line.split()
    #list_of_lists.append(line_list)
    a_file.close()
    #print(list_of_lists)


    #print(first_line)

#pick_random_img()
#encoding="utf-8"