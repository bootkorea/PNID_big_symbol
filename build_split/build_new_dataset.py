import os
import shutil

common_path = "/Users/bootkorea/Documents/GitHub/big_symbol/dataset/entire_dataset/"
new_folder_path = "/Users/bootkorea/Documents/GitHub/big_symbol/dataset/new_dataset/"
annfile_list = os.listdir(common_path + "annfiles")
imgfile_list = os.listdir(common_path + "images")

os.makedirs(new_folder_path + "annfiles", exist_ok=True)
os.makedirs(new_folder_path + "images", exist_ok=True)

count = 0
for name in annfile_list:
    annfile_path = common_path + "annfiles/" + name
    annfile = open(annfile_path, 'r')

    lines = annfile.readlines()

    new_annfile = open(os.path.join(new_folder_path + "annfiles", name), 'w+')

    for ind, l in enumerate(lines):
        points = l.split()
        
        x = int(points[0]) - int(points[4])
        y = int(points[1]) - int(points[5])

        x_dist = abs(x)
        y_dist = abs(y)

        # Big Symbol 판별
        if x_dist > 600 or y_dist > 600:
            if points[8] != 'text' :
                new_annfile.write(l)
                count += 1

# 0바이트인 txt 파일 삭제
txt_files = [file for file in os.listdir(new_folder_path + "annfiles") if file.endswith(".txt")]

for txt_file in txt_files:
    txt_file_path = os.path.join(new_folder_path + "annfiles", txt_file)
    if os.path.getsize(txt_file_path) == 0:
        os.remove(txt_file_path)

# .jpg 파일을 new_images_path로 복사
new_txt_files = [file for file in os.listdir(new_folder_path + "annfiles") if file.endswith(".txt")]
jpg_files = [file for file in os.listdir(common_path + "images") if file.endswith(".jpg")]

for jpg_file in jpg_files:
    txt_file_name = jpg_file[:-4] + ".txt"

    if txt_file_name in new_txt_files:
        src_jpg_path = os.path.join(common_path + "images", jpg_file)
        dst_jpg_path = os.path.join(new_folder_path + "images", jpg_file)
        shutil.copy(src_jpg_path, dst_jpg_path)

# Finish Message
print("Job Finished!")
print("Big Symbol Counts:", count)