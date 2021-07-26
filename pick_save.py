import streamlit as st
import os
import os.path
import ftplib
from pathlib import Path

host = 'ftp4.nska.net'
ftp_user = 'test1@lookies.by'
ftp_password = 'U4hq0oLn'
base_folder = 'img600x866'
base_folder_crop = base_folder + '_crop'

list_of_files = []

def pick_random_img():
    list_of_files = []
    list_of_skip = []
    ftp = ftplib.FTP(host, ftp_user, ftp_password)

    a_file = open("list_to_do.txt", 'r')
    for line in a_file:
        stripped_line = line.strip()
        list_of_files.append(stripped_line)
    a_file.close()

    # removing "skip" files
    try:
        ftp.retrbinary("RETR " + "skip_list.txt", open("skip_list.txt", 'wb').write)
    except:
        print("Error")
    skip_list = open("skip_list.txt", 'r')
    for line in skip_list:
        stripped_line = line.strip()
        list_of_skip.append(stripped_line)
    skip_list.close()

    list_of_files = [x for x in list_of_files if x not in list_of_skip]

    st.text("LEFT TO DO: " + str(len(list_of_files)))
    # pick a file "to do"
    first_line = list_of_files[0]
    #try:
    #    #ftp.retrbinary(f"RETR {file_to_do}", localfile.write)
    #    ftp.retrbinary("RETR " + first_line, open(first_line, 'wb').write)
    #except:
    #    print(first_line)
    #    print("Error")

    ftp.quit()
    return first_line

def load_file_trough_ftp(file_to_do):
    file_to_do_split = file_to_do.split('/')
    filename = file_to_do_split[2]
    localfile = open(filename, "wb")
    ftp = ftplib.FTP(host, ftp_user, ftp_password)
    ftp.retrbinary(f"RETR {file_to_do}", localfile.write)
    localfile.close()
    ftp.quit()
    return filename

def save_cropped_img_ftp(cropped_img, img_file):
    filename_split = img_file.split('/')
    img = cropped_img
    img.save(filename_split[2])
    img = open(filename_split[2], 'rb')
    ftp = ftplib.FTP(host, ftp_user, ftp_password)
    ftp.storbinary('STOR ' + base_folder_crop + '/' + str(filename_split[1]) + '/' + str(filename_split[2]), img)
    ftp.quit()

    #Removing the firs element of todo list
    with open("list_to_do.txt", 'r') as fin:
        data = fin.read().splitlines(True)
    with open("list_to_do.txt", 'w') as fout:
        fout.writelines(data[1:])



def create_list_of_files():
    if os.path.isfile("list_to_do.txt"):
        print(' ')
    else:
        # get the list of images
        img_files_path = []
        ftp = ftplib.FTP(host, ftp_user, ftp_password)
        base_folder_el_list = ftp.nlst(base_folder)
        base_folder_el_list = [x for x in base_folder_el_list if "." not in x]
        for el in base_folder_el_list:
            n_folder_element_list = ftp.nlst(el)
            for i in n_folder_element_list:
                img_files_path.append(i)
        img_files_path = [x.replace(base_folder + '/', '') for x in img_files_path if ".jpg" in x]

        # get the list of cropped files
        croped_img_files_path = []
        base_folder_crop_el_list = ftp.nlst(base_folder_crop)
        base_folder_crop_el_list = [x for x in base_folder_crop_el_list if "." not in x]
        for el in base_folder_crop_el_list:
            n_folder_element_list = ftp.nlst(el)
            for i in n_folder_element_list:
                croped_img_files_path.append(i)
        croped_img_files_path = [x.replace(base_folder_crop + '/', '') for x in croped_img_files_path if ".jpg" in x]

        # get the list of "files to do" by removing cropped files
        files_to_do = [(base_folder + '/' + x) for x in img_files_path if x not in croped_img_files_path]
        textfile = open("list_to_do.txt", "w")

        #write to txt
        for element in files_to_do:
            textfile.write(element + "\n")
        textfile.close()

        ftp.quit()

def skip_file(img_file):
    ftp = ftplib.FTP(host, ftp_user, ftp_password)
    try:
        ftp.retrbinary("RETR " + "skip_list.txt", open("skip_list.txt", 'wb').write)
    except:
        print("Error")

    with open("skip_list.txt", 'a') as fout:
        fout.write("\n")
        fout.write(img_file)

    skip_list = open("skip_list.txt", 'rb')
    ftp.storbinary('STOR ' + "skip_list.txt", skip_list)
    ftp.quit()

def delete_tmp_file(img_file_name):
    print(img_file_name)
    if os.path.exists(img_file_name):
        os.remove(img_file_name)
    else:
        pass

#create_list_of_files()
#first_line = pick_random_img()
#file_name = load_file_trough_ftp(first_line)
