import os
import cv2
import numpy as np
import shutil

# 데이터셋 폴더 경로
splitset_path = "/Users/bootkorea/Documents/GitHub/big_symbol/split_big_pnid/"
output_path = "/Users/bootkorea/Documents/GitHub/big_symbol/rotate_image180/"

cnt = 0

# 결과 디렉토리 생성
def merge_directories(splitset_path, output_path):
    os.makedirs(output_path, exist_ok=True)
    output_annfiles_path = os.path.join(output_path, 'annfiles')
    output_images_path = os.path.join(output_path, 'images')
    os.makedirs(output_annfiles_path, exist_ok=True)
    os.makedirs(output_images_path, exist_ok=True)

    # annfiles 파일 병합
    for dir_name in ['train', 'val', 'test']:
        annfiles_dir = os.path.join(splitset_path, dir_name, 'annfiles')
        for file in os.listdir(annfiles_dir):
            shutil.copy(os.path.join(annfiles_dir, file), output_annfiles_path)

    # images 파일 병합
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

# bounding_box 좌표 확장
def expand_coordinates(coords_list, expand_size, image_width, image_height):
    expanded_coords_list = []

    for coords in coords_list:
        expanded_coords = []
        for i in range(0, len(coords), 4):
            x_min, y_min, x_max, y_max = coords[i:i+4]

            # bounding_box 좌표 확장
            x_min = max(0, x_min - expand_size)
            x_max = min(image_width, x_max + expand_size)
            y_min = max(0, y_min - expand_size)
            y_max = min(image_height, y_max + expand_size)

            expanded_coords.extend([x_min, y_min, x_max, y_max])

        expanded_coords_list.append(expanded_coords)

    return expanded_coords_list

# bounding_box 그리기 함수
def draw_bounding_boxes(image, coords_list, class_names):
    for coords, class_name in zip(coords_list, class_names):
        num_points = len(coords) // 2
        x_min, y_min, x_max, y_max = min(coords[0::2]), min(coords[1::2]), max(coords[0::2]), max(coords[1::2])

        # bounding_box 그리기
        color = (0, 255, 0)  # 초록색
        thickness = 2
        cv2.rectangle(image, (x_min, y_min), (x_max, y_max), color, thickness)

        # 클래스 이름 표시
        font = cv2.FONT_HERSHEY_SIMPLEX
        font_scale = 0.5
        font_thickness = 1
        text_size = cv2.getTextSize(class_name, font, font_scale, font_thickness)[0]
        text_x = x_min + 5
        text_y = y_min + text_size[1] + 5
        cv2.putText(image, class_name, (text_x, text_y), font, font_scale, color, font_thickness, cv2.LINE_AA)

# 좌표 변환 함수
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
def apply_image_transform(image_path, txt_path, output_dir, transform_type, expand_size):
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

    if expand_size is not None:
        # 변환된 좌표 확장
        expanded_coords_list = expand_coordinates(transformed_coords_list, expand_size, image_width, image_height)

        # 변환된 이미지에 bounding_box 그리기
        draw_bounding_boxes(transformed_image, expanded_coords_list, class_names)

        # .txt 파일에 저장할 좌표로 변환
        transformed_coords_list = expanded_coords_list

    # 수정된 좌표 정보와 class_name을 새로운 .txt 파일에 저장
    transformed_txt_path = os.path.join(output_dir, f"{os.path.splitext(os.path.basename(txt_path))[0]}.txt")
    with open(transformed_txt_path, 'w') as f:
        for coords, class_name in zip(transformed_coords_list, class_names):
            for i in range(0, len(coords), 4):
                f.write(f"{coords[i]} {coords[i+1]} {coords[i+2]} {coords[i+3]} ")
            f.write(f"{class_name} 0\n")  # class_name과 0을 함께 저장
            global cnt
            cnt += 1

    # 변환된 이미지 저장 (images 디렉토리에 저장)
    output_filename = os.path.splitext(os.path.basename(txt_path))[0]
    transformed_image_path = os.path.join(images_dir, f"{output_filename}.png")
    cv2.imwrite(transformed_image_path, transformed_image)

# 데이터 병합
merge_directories(splitset_path, output_path)

# 이미지 변환 및 좌표 수정 과정
annfiles_dir = os.path.join(output_path, 'annfiles')
images_dir = os.path.join(output_path, 'images')
expand_size = 10  # 원하는 확장 크기 설정

for txt_file in os.listdir(annfiles_dir):
    if txt_file.endswith(".txt"):
        txt_path = os.path.join(annfiles_dir, txt_file)
        image_file = txt_file.replace(".txt", ".png")
        image_path = os.path.join(images_dir, image_file)

        # 이미지 변환 및 좌표 수정 적용
        apply_image_transform(image_path, txt_path, annfiles_dir, "rotate_180", expand_size)

print(cnt)