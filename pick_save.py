import streamlit as st
import os, random
import shutil
#os.remove('/Users/sergeykulazhenko/PycharmProjects/pythonProject/croper/img600x866_crop/.DS_Store')
base_folder = '/Users/sergeykulazhenko/PycharmProjects/pythonProject/croper/img600x866'
base_folder_crop = base_folder + '_crop'
def pick_random_img():
    # get the list of images
    img_files_path = []
    for el in os.listdir(base_folder):
        n_folder_path = os.path.join(base_folder, el)
        n_folder_element_list = os.listdir(n_folder_path)
        for i in n_folder_element_list:
            current_img = os.path.join(el, i)
            img_files_path.append(current_img)
    print("TOTAL IMAGES: " + str(len(img_files_path)))

    # get the list of cropped files
    croped_img_files_path = []
    for el in os.listdir(base_folder_crop):
        n_folder_path = os.path.join(base_folder_crop, el)
        n_folder_element_list = os.listdir(n_folder_path)
        for i in n_folder_element_list:
            current_img = os.path.join(el, i)
            croped_img_files_path.append(current_img)
    #print("CROPPED IMAGES: " + str(len(croped_img_files_path)))

    # get the list of "files to do"
    files_to_do = list(set(img_files_path) - set(croped_img_files_path))
    #print("LEFT TO DO: " + str(len(files_to_do)))
    st.text("LEFT TO DO: " + str(len(files_to_do)))
    # pick a random file "to do"

    return files_to_do[0]

def save_cropped_img(cropped_img, img_file):
    cropped_img.save('/Users/sergeykulazhenko/PycharmProjects/pythonProject/croper/img600x866_crop/' + str(img_file))
