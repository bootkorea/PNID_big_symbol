import os
import cv2
import numpy as np
import shutil

# 데이터셋 폴더 경로
splitset_path = "/Users/bootkorea/Documents/GitHub/big_symbol/dataset/split_big_pnid/"
output_path = "/Users/bootkorea/Documents/GitHub/big_symbol/aug_dataset_horizontal_flip/"

cnt = 0

def merge_directories(splitset_path, output_path):
    # Create output directories if they don't exist
    os.makedirs(output_path, exist_ok=True)
    output_annfiles_path = os.path.join(output_path, 'annfiles')
    output_images_path = os.path.join(output_path, 'images')
    os.makedirs(output_annfiles_path, exist_ok=True)
    os.makedirs(output_images_path, exist_ok=True)

    # Merge annfiles files
    for dir_name in ['train', 'val', 'test']:
        annfiles_dir = os.path.join(splitset_path, dir_name, 'annfiles')
        for file in os.listdir(annfiles_dir):
            shutil.copy(os.path.join(annfiles_dir, file), output_annfiles_path)

    # Merge images files
    for dir_name in ['train', 'val', 'test']:
        images_dir = os.path.join(splitset_path, dir_name, 'images')
        for file in os.listdir(images_dir):
            shutil.copy(os.path.join(images_dir, file), output_images_path)

# 이미지 수평 뒤집기
def horizontal_flip(image):
    return cv2.flip(image, 1)

# 이미지 수직 뒤집기
def vertical_flip(image):
    return cv2.flip(image, 0)

# 이미지 180도 회전
def rotate_180(image):
    return cv2.rotate(image, cv2.ROTATE_180)

def draw_bounding_boxes(image, coords_list, class_names):
    for coords, class_name in zip(coords_list, class_names):
        num_points = len(coords) // 2
        points = [(coords[i], coords[i + 1]) for i in range(0, len(coords), 2)]

        # Draw the bounding box
        color = (0, 255, 0)  # Green color for the bounding box
        thickness = 2
        for i in range(num_points - 1):
            cv2.line(image, points[i], points[i + 1], color, thickness)
        cv2.line(image, points[num_points - 1], points[0], color, thickness)

        # Put the class name on the bounding box
        font = cv2.FONT_HERSHEY_SIMPLEX
        font_scale = 0.5
        font_thickness = 1
        text_size = cv2.getTextSize(class_name, font, font_scale, font_thickness)[0]
        text_x = min(points[0][0], points[1][0]) + 5
        text_y = min(points[0][1], points[3][1]) + text_size[1] + 5
        cv2.putText(image, class_name, (text_x, text_y), font, font_scale, color, font_thickness, cv2.LINE_AA)


def transform_coordinates(coords_list, image_width, image_height, transform_type):
    transformed_coords_list = []
    
    for coords in coords_list:
        transformed_coords = []
        if transform_type == "vertical_flip":
            for i in range(0, len(coords), 2):
                x = coords[i]
                y = image_height - coords[i + 1]
                transformed_coords.extend([x, y])

        elif transform_type == "horizontal_flip":
            for i in range(0, len(coords), 2):
                x = image_width - coords[i]
                y = coords[i + 1]
                transformed_coords.extend([x, y])

        elif transform_type == "rotate_180":
            for i in range(0, len(coords), 2):
                x = image_width - coords[i]
                y = image_height - coords[i + 1]
                transformed_coords.extend([x, y])

        transformed_coords_list.append(transformed_coords)

    return transformed_coords_list

# 이미지 변환 및 좌표 수정 함수
def apply_image_transform(image_path, txt_path, output_dir, transform_type):
    # 이미지 로드
    image = cv2.imread(image_path)

    # 이미지 변환
    if transform_type == "vertical_flip":
        transformed_image = vertical_flip(image)
    elif transform_type == "horizontal_flip":
        transformed_image = horizontal_flip(image)
    elif transform_type == "rotate_180":
        transformed_image = rotate_180(image)

    # 좌표 정보 및 class_name 가져오기
    coords_list = []
    class_names = []
    with open(txt_path, 'r') as f:
        for line in f:
            coords = [int(coord) for coord in line.split()[:-2]]
            class_name = line.split()[-2]
            coords_list.append(coords)
            class_names.append(class_name)

    # 이미지 크기
    image_height, image_width, _ = transformed_image.shape

    # 좌표 정보 변환
    transformed_coords_list = transform_coordinates(coords_list, image_width, image_height, transform_type)

    # 수정된 좌표 정보와 class_name을 새로운 .txt 파일에 저장
    transformed_txt_path = os.path.join(output_dir, f"{os.path.splitext(os.path.basename(txt_path))[0]}.txt")
    with open(transformed_txt_path, 'w') as f:
        for coords, class_name in zip(transformed_coords_list, class_names):
            for i in range(0, len(coords), 2):
                f.write(f"{coords[i]} {coords[i+1]} ")
            f.write(f"{class_name} 0\n")  # class_name과 0을 함께 저장
            global cnt
            cnt += 1

    # 변환된 이미지 저장 (images 디렉토리에 저장)
    output_filename = os.path.splitext(os.path.basename(txt_path))[0]
    transformed_image_path = os.path.join(images_dir, f"{output_filename}.png")
    cv2.imwrite(transformed_image_path, transformed_image)

merge_directories(splitset_path, output_path)

# 이미지 변환 및 좌표 수정 과정
annfiles_dir = os.path.join(output_path, 'annfiles')
images_dir = os.path.join(output_path, 'images')

for txt_file in os.listdir(annfiles_dir):
    if txt_file.endswith(".txt"):
        txt_path = os.path.join(annfiles_dir, txt_file)
        image_file = txt_file.replace(".txt", ".png")
        image_path = os.path.join(images_dir, image_file)

        # 이미지 변환 및 좌표 수정 적용
        apply_image_transform(image_path, txt_path, annfiles_dir, "horizontal_flip")

print("Symbol Count:", cnt)