import os
import cv2
import numpy as np
import shutil

# 데이터셋 폴더 경로
text_path = "/Users/bootkorea/Documents/GitHub/big_symbol/"
splitset_path = "/Users/bootkorea/Documents/GitHub/big_symbol/split_big_pnid/"
output_path = "/Users/bootkorea/Documents/GitHub/big_symbol/aug_big_pnid/"

# 새로운 데이터셋 경로
output_annfiles_path = os.path.join(output_path, "annfiles")
output_images_path = os.path.join(output_path, "images")

# 디렉토리 생성
os.makedirs(output_annfiles_path, exist_ok=True)
os.makedirs(output_images_path, exist_ok=True)

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

# 이미지를 주어진 각도에 맞게 회전시키는 함수
def rotate_image(image, angle):
    height, width = image.shape[:2]
    center = (width / 2, height / 2)

    rotation_matrix = cv2.getRotationMatrix2D(center, angle, 1.0)
    rotated_image = cv2.warpAffine(image, rotation_matrix, (width, height))

    return rotated_image

# 좌표를 원하는 각도로 회전시키는 함수
def rotate_coordinates(coordinates, angle, center):
    # 회전하는 행렬 생성
    theta = np.radians(angle)
    rotation_matrix = np.array([[np.cos(theta), -np.sin(theta)], [np.sin(theta), np.cos(theta)]])

    # 회전된 좌표 계산
    rotated_coordinates = []
    for i in range(0, len(coordinates), 2):
        x = coordinates[i] - center[0]
        y = coordinates[i + 1] - center[1]
        rotated_x, rotated_y = np.dot(rotation_matrix, np.array([x, y]))
        rotated_coordinates.extend([int(rotated_x + center[0]), int(rotated_y + center[1])])

    return rotated_coordinates

# annfiles 디렉토리에 있는 big_symbol 좌표 정보 수정
for dataset_folder in ["train", "val", "test"]:
    dataset_annfiles_path = os.path.join(splitset_path, dataset_folder, "annfiles")
    dataset_images_path = os.path.join(splitset_path, dataset_folder, "images")
    output_annfiles_path = os.path.join(output_path, "annfiles")
    output_images_path = os.path.join(output_path, "images")

    os.makedirs(output_annfiles_path, exist_ok=True)
    os.makedirs(output_images_path, exist_ok=True)

    for annfile in os.listdir(dataset_annfiles_path):
        if annfile.endswith(".txt"):
            txt_file_path = os.path.join(dataset_annfiles_path, annfile)
            new_txt_file_path = os.path.join(output_annfiles_path, os.path.splitext(annfile)[0] + ".txt")
            shutil.copy(txt_file_path, new_txt_file_path)

            with open(new_txt_file_path, 'r') as file:
                lines = file.readlines()

            # 이미지 파일 경로
            image_file = os.path.splitext(annfile)[0] + ".png"
            image_path = os.path.join(dataset_images_path, image_file)

            # 이미지 로드
            image = cv2.imread(image_path)

            symbol_count = 1

            with open(new_txt_file_path, 'w') as file:
                for line in lines:
                    values = line.strip().split()
                    coordinates = list(map(float, values[:8]))
                    class_name = values[8]
                    angle = 180  # 회전할 각도 설정
                    expand_size = 5  # 좌표를 늘릴 크기

                    # bounding box 좌표 추출
                    x_min = int(min(coordinates[0:8:2])) - expand_size
                    x_max = int(max(coordinates[0:8:2])) + expand_size
                    y_min = int(min(coordinates[1:8:2])) - expand_size
                    y_max = int(max(coordinates[1:8:2])) + expand_size

                    # bounding box 영역 이미지 추출
                    symbol_area = image[max(0, y_min):min(image.shape[0], y_max), max(0, x_min):min(image.shape[1], x_max)]

                    # bounding box의 중점 계산
                    center_x = (x_min + x_max) // 2
                    center_y = (y_min + y_max) // 2

                    # 좌표를 원하는 각도로 회전
                    rotated_coordinates = rotate_coordinates(coordinates, angle, (center_x, center_y))

                    # 좌표 정보를 정수 형태로 반올림하여 저장
                    rotated_coordinates = [round(coord) for coord in rotated_coordinates]

                    # 심볼 이미지 회전
                    rotated_symbol = rotate_image(symbol_area, angle)

                    # 회전된 bounding box의 좌표 계산
                    rotated_x_min = center_x - (x_max - x_min) // 2
                    rotated_x_max = center_x + (x_max - x_min) // 2
                    rotated_y_min = center_y - (y_max - y_min) // 2
                    rotated_y_max = center_y + (y_max - y_min) // 2

                    # 심볼 이미지 크기를 맞춤
                    resized_rotated_symbol = cv2.resize(rotated_symbol, (rotated_x_max - rotated_x_min, rotated_y_max - rotated_y_min))

                    # 심볼 이미지를 symbol_area에 삽입
                    symbol_height, symbol_width, _ = resized_rotated_symbol.shape
                    symbol_area_height, symbol_area_width, _ = symbol_area.shape

                    # 삽입할 영역의 좌표 계산
                    insert_x_min = max(rotated_x_min, x_min)
                    insert_x_max = min(rotated_x_max, x_max)
                    insert_y_min = max(rotated_y_min, y_min)
                    insert_y_max = min(rotated_y_max, y_max)

                    # 삽입할 영역의 크기 계산
                    insert_height = insert_y_max - insert_y_min
                    insert_width = insert_x_max - insert_x_min

                    # symbol_area에 삽입할 위치 계산
                    symbol_x_min = insert_x_min - rotated_x_min
                    symbol_x_max = symbol_x_min + insert_width
                    symbol_y_min = insert_y_min - rotated_y_min
                    symbol_y_max = symbol_y_min + insert_height

                    # symbol_area에 삽입
                    symbol_area[symbol_y_min:symbol_y_max, symbol_x_min:symbol_x_max] = resized_rotated_symbol[:insert_height, :insert_width]

                    # 좌표 정보를 문자열로 변환
                    rotated_coordinates_str = ' '.join(map(str, rotated_coordinates))

                    # 좌표 정보 및 클래스명을 파일에 쓰기
                    file.write(f"{rotated_coordinates_str} {class_name} 0\n")

                    symbol_count += 1

            # 이미지 파일명 수정
            rotated_image_file = os.path.splitext(image_file)[0] + ".png"

            # 새로운 디렉토리에 이미지 저장
            output_image_path = os.path.join(output_images_path, rotated_image_file)
            cv2.imwrite(output_image_path, image)
