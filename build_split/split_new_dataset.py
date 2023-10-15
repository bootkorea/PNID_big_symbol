import os
import cv2
import numpy as np
import shutil

# PNID dilation Code
def apply_dilate(img, kernel_size=(2, 2)):
    kernel = np.ones(kernel_size, np.uint8)
    dilate = cv2.erode(img, kernel, iterations=8)
    return dilate

# PNID Resize Code
def apply_resize(img, resize_factor):
    height, width, channels = img.shape
    img_resized = cv2.resize(img, (int(width * resize_factor), int(height * resize_factor)))
    return img_resized

# 데이터셋 폴더 경로
text_path = "/Users/bootkorea/Documents/GitHub/big_symbol/"
dataset_path = "/Users/bootkorea/Documents/GitHub/big_symbol/dataset/new_dataset/"
splitset_path = "/Users/bootkorea/Documents/GitHub/big_symbol/split_big_pnid/"
annfiles_path = os.path.join(dataset_path, "annfiles")
images_path = os.path.join(dataset_path, "images")

# 분할된 데이터셋 경로
train_path = splitset_path + "train/"
test_path = splitset_path + "test/"
val_path = splitset_path + "val/"

# 디렉토리 생성
os.makedirs(test_path, exist_ok=True)
os.makedirs(val_path, exist_ok=True)
os.makedirs(train_path, exist_ok=True)

os.makedirs(train_path + "annfiles", exist_ok=True)
os.makedirs(train_path + "images", exist_ok=True)

os.makedirs(val_path + "annfiles", exist_ok=True)
os.makedirs(val_path + "images", exist_ok=True)

os.makedirs(test_path + "annfiles", exist_ok=True)
os.makedirs(test_path + "images", exist_ok=True)

# big_symbol.txt 파일 읽기
txt_file_path = os.path.join(text_path, "big_symbol.txt")
with open(txt_file_path, 'r') as file:
    lines = file.readlines()

# 클래스명과 파일 리스트로 분할
class_files = {}
current_class = None

for line in lines:
    line = line.strip()
    if line and ".jpg" not in line:
        current_class = line
        class_files[current_class] = set()
    else:
        class_files[current_class].add(line)

# 분할 여부 디버깅을 위한 리스트 생성
train_pop = []
val_pop = []
test_pop = []

# test dataset
for class_name, file_set in class_files.items():
    # 파일 크기를 기준으로 정렬
    sorted_files = sorted(file_set, key=lambda x: os.path.getsize(os.path.join(annfiles_path, os.path.splitext(x)[0] + ".txt")))

    if len(sorted_files) > 0:
        test_file = sorted_files[0]  # 파일 크기가 가장 작은 파일 선택
        test_pop.append(test_file)
        src_path = os.path.join(images_path, test_file)
        dst_path = os.path.join(test_path, "images", test_file)
        shutil.copy(src_path, dst_path)

        # 매칭되는 .txt 파일 찾아서 복사
        txt_file_name = os.path.splitext(test_file)[0] + ".txt"
        src_txt_path = os.path.join(annfiles_path, txt_file_name)
        dst_txt_path = os.path.join(test_path, "annfiles", txt_file_name)

        with open(src_txt_path, 'r') as src_file, open(dst_txt_path, 'w') as dst_file:
            for line in src_file:
                values = line.strip().split(' ')
                if len(values) >= 8:
                    # 좌표값을 0.125배로 축소
                    coordinates = [str(round(float(value) * 0.125)) for value in values[:8]]
                    modified_line = ' '.join(coordinates + values[8:]) + '\n'
                    dst_file.write(modified_line)
                else:
                    dst_file.write(line)


        # 다른 클래스 set에서 test 파일 제거
        for files in class_files.values():
            if test_file in files:
                files.remove(test_file)
    else:
        print(f"Warning: No files available for class '{class_name}' in test set")

# val dataset
for class_name, file_set in class_files.items():
    sorted_files = sorted(file_set, key=lambda x: os.path.getsize(os.path.join(annfiles_path, os.path.splitext(x)[0] + ".txt")))

    if len(sorted_files) > 0:
        val_file = sorted_files[0]  # 파일 크기가 가장 작은 파일 선택
        val_pop.append(val_file)
        src_path = os.path.join(images_path, val_file)
        dst_path = os.path.join(val_path, "images", val_file)
        shutil.copy(src_path, dst_path)

        # 매칭되는 .txt 파일 찾아서 수정된 좌표로 새로운 파일 생성
        txt_file_name = os.path.splitext(val_file)[0] + ".txt"
        src_txt_path = os.path.join(annfiles_path, txt_file_name)
        dst_txt_path = os.path.join(val_path, "annfiles", txt_file_name)

        with open(src_txt_path, 'r') as src_file, open(dst_txt_path, 'w') as dst_file:
            for line in src_file:
                values = line.strip().split(' ')
                if len(values) >= 8:
                    # 좌표값을 0.125배로 축소
                    coordinates = [str(round(float(value) * 0.125)) for value in values[:8]]
                    modified_line = ' '.join(coordinates + values[8:]) + '\n'
                    dst_file.write(modified_line)
                else:
                    dst_file.write(line)


        # 다른 클래스 set에서 val 파일 제거
        for files in class_files.values():
            if val_file in files:
                files.remove(val_file)
    else:
        print(f"Warning: Insufficient files for class '{class_name}' in validation set.")

# val dataset에 부족한 파일 개수 계산
files_needed = len(test_pop) - len(val_pop)
print(files_needed)

# val dataset에 부족한 파일 개수 계산
files_needed = len(test_pop) - len(val_pop)
print(files_needed)

# 부족한 파일 개수만큼 추가로 val dataset에 파일 추가
if files_needed > 0:
    # 현재까지 남아있는 파일이 많은 클래스를 찾음
    classes_with_remaining_files = {class_name: len(file_set) for class_name, file_set in class_files.items()}
    classes_with_remaining_files = dict(sorted(classes_with_remaining_files.items(), key=lambda x: x[1], reverse=True))

    for class_name, remaining_files in classes_with_remaining_files.items():
        if files_needed <= 0:
            break

        # 현재 클래스에서 추가할 파일 선택
        files_to_move = min(files_needed, remaining_files)

        # 파일 크기 기준으로 오름차순 정렬
        sorted_files = sorted(class_files[class_name], key=lambda x: os.path.getsize(os.path.join(images_path, x)))

        # 파일 이동
        files_to_move_list = sorted_files[:files_to_move]
        for file_to_move in files_to_move_list:
            class_files[class_name].remove(file_to_move)
            src_path = os.path.join(images_path, file_to_move)
            dst_path = os.path.join(val_path, "images", file_to_move)
            shutil.copy(src_path, dst_path)

            # 매칭되는 .txt 파일 찾아서 수정된 좌표로 새로운 파일 생성
            txt_file_name = os.path.splitext(file_to_move)[0] + ".txt"
            src_txt_path = os.path.join(annfiles_path, txt_file_name)
            dst_txt_path = os.path.join(val_path, "annfiles", txt_file_name)

            with open(src_txt_path, 'r') as src_file, open(dst_txt_path, 'w') as dst_file:
                for line in src_file:
                    values = line.strip().split(' ')
                    if len(values) >= 8:
                        # 좌표값을 0.125배로 축소
                        coordinates = [str(round(float(value) * 0.125)) for value in values[:8]]
                        modified_line = ' '.join(coordinates + values[8:]) + '\n'
                        dst_file.write(modified_line)
                    else:
                        dst_file.write(line)

            val_pop.append(file_to_move)
            files_needed -= 1

print("Final val dataset size:", len(val_pop))
print("Final test dataset size:", len(test_pop))


# 중복 파일 제거
all_files = set()  # 전체 파일 저장용 set

for file_set in class_files.values():
    all_files.update(file_set)

# train dataset
for class_name, file_set in class_files.items():
    for train_file in file_set:
        if train_file in all_files:
            all_files.remove(train_file)
        else:
            continue

        train_pop.append(train_file)
        src_path = os.path.join(images_path, train_file)
        dst_path = os.path.join(train_path, "images", train_file)
        shutil.copy(src_path, dst_path)

        # 매칭되는 .txt 파일 찾아서 수정된 좌표로 새로운 파일 생성
        txt_file_name = os.path.splitext(train_file)[0] + ".txt"
        src_txt_path = os.path.join(annfiles_path, txt_file_name)
        dst_txt_path = os.path.join(train_path, "annfiles", txt_file_name)

        with open(src_txt_path, 'r') as src_file, open(dst_txt_path, 'w') as dst_file:
            for line in src_file:
                values = line.strip().split(' ')
                if len(values) >= 8:
                    # 좌표값을 0.125배로 축소
                    coordinates = [str(round(float(value) * 0.125)) for value in values[:8]]
                    modified_line = ' '.join(coordinates + values[8:]) + '\n'
                    dst_file.write(modified_line)
                else:
                    dst_file.write(line)

# train 데이터셋 이미지에 dilation과 resizing 적용
train_images_dir = os.path.join(train_path, "images")
for train_file in os.listdir(train_images_dir):
    img_path = os.path.join(train_images_dir, train_file)
    img = cv2.imread(img_path)
    dilate = apply_dilate(img)
    resized = apply_resize(dilate, 0.125)

    save_path = os.path.join(train_path, "images", os.path.splitext(train_file)[0] + ".png")
    cv2.imwrite(save_path, resized)
    os.remove(img_path)

# val 데이터셋 이미지에 dilation과 resizing 적용
val_images_dir = os.path.join(val_path, "images")
for val_file in os.listdir(val_images_dir):
    img_path = os.path.join(val_images_dir, val_file)
    img = cv2.imread(img_path)
    dilate = apply_dilate(img)
    resized = apply_resize(dilate, 0.125)

    save_path = os.path.join(val_path, "images", os.path.splitext(val_file)[0] + ".png")
    cv2.imwrite(save_path, resized)
    os.remove(img_path)

# test 데이터셋 이미지에 dilation과 resizing 적용
test_images_dir = os.path.join(test_path, "images")
for test_file in os.listdir(test_images_dir):
    img_path = os.path.join(test_images_dir, test_file)
    img = cv2.imread(img_path)
    dilate = apply_dilate(img)
    resized = apply_resize(dilate, 0.125)

    save_path = os.path.join(test_path, "images", os.path.splitext(test_file)[0] + ".png")
    cv2.imwrite(save_path, resized)
    os.remove(img_path)

# 디버깅 정보 출력
print("train_pop:", len(train_pop))
print("val_pop:", len(val_pop))
print("test_pop:", len(test_pop))