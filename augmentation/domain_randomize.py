import os
import cv2
import numpy as np
import random

# 데이터셋 폴더 경로
output_path = "/Users/bootkorea/Documents/GitHub/big_symbol/dr_dataset/"
dr_path = "/Users/bootkorea/Documents/GitHub/big_symbol/need_aug"

# 새로운 데이터셋 경로
output_annfiles_path = os.path.join(output_path, "annfiles")
output_images_path = os.path.join(output_path, "images")

# 디렉토리 생성
os.makedirs(output_annfiles_path, exist_ok=True)
os.makedirs(output_images_path, exist_ok=True)

# 기본 정보 설정
dataset_annfiles_path = os.path.join(dr_path, "annfiles")
dataset_images_path = os.path.join(dr_path, "images")
symbol_size = (1241, 877)  # 새로운 심볼 이미지 크기
n = 6  # 삽입할 심볼 개수
coordinate_margin = 5  # 좌표 이미지 확장 마진

# 기존 .txt 파일과 이미지 파일 대응 여부 확인
annfiles = [file for file in os.listdir(dataset_annfiles_path) if file.endswith(".txt")]
image_files = [file for file in os.listdir(dataset_images_path) if file.endswith(".png")]

# 모든 심볼 정보 저장
all_symbols = []

for annfile in annfiles:
    image_file = annfile.replace(".txt", ".png")

    if image_file in image_files:
        # .txt 파일 읽기
        with open(os.path.join(dataset_annfiles_path, annfile), 'r') as file:
            lines = file.readlines()

        # 심볼 개수만큼 반복하여 이미지 추출 및 저장
        for line in lines:
            values = line.strip().split()
            coordinates = list(map(float, values[:8]))
            class_name = values[8]

            symbol_info = {
                'coordinates': coordinates,
                'class_name': class_name,
                'image_file': image_file
            }

            all_symbols.append(symbol_info)

# 총 심볼 개수
total_symbols = len(all_symbols)

# 이미지 개수 계산
num_images = total_symbols // n
if total_symbols % n != 0:
    num_images += 1

# New diagram image generation
for i in range(num_images):
    # Create a blank image
    new_image = np.ones((symbol_size[1], symbol_size[0], 3), dtype=np.uint8) * 255

    # Starting index
    start_idx = i * n
    # Ending index
    end_idx = min((i + 1) * n, total_symbols)

    # Insert selected symbol images into the new diagram
    inserted_symbols = []  # Keep track of inserted symbols' positions

    for symbol in all_symbols[start_idx:end_idx]:
        coordinates = symbol['coordinates']
        class_name = symbol['class_name']
        image_file = symbol['image_file']

        # Load symbol image
        symbol_image = cv2.imread(os.path.join(dataset_images_path, image_file))

        # Symbol image size
        symbol_width = int(max(coordinates[0:8:2]) - min(coordinates[0:8:2])) + coordinate_margin * 2
        symbol_height = int(max(coordinates[1:8:2]) - min(coordinates[1:8:2])) + coordinate_margin * 2

        # Random coordinates generation (non-overlapping)
        x, y = None, None
        attempts = 0
        max_attempts = 100  # Maximum attempts to find a non-overlapping position

        while attempts < max_attempts:
            x = random.randint(0, symbol_size[0] - symbol_width)
            y = random.randint(0, symbol_size[1] - symbol_height)

            overlap = False
            for inserted_symbol in inserted_symbols:
                inserted_x, inserted_y, inserted_width, inserted_height = inserted_symbol
                if (x < inserted_x + inserted_width and x + symbol_width > inserted_x and
                        y < inserted_y + inserted_height and y + symbol_height > inserted_y):
                    overlap = True
                    break

            if not overlap:
                break
            attempts += 1

        if attempts >= max_attempts:
            print(f"Warning: Could not find non-overlapping position for symbol {class_name}. Skipping...")
            continue

        # Insert the symbol image into the new diagram
        new_image[y:y + symbol_height, x:x + symbol_width] = symbol_image[
            int(min(coordinates[1:8:2])) - coordinate_margin: int(max(coordinates[1:8:2])) + coordinate_margin,
            int(min(coordinates[0:8:2])) - coordinate_margin: int(max(coordinates[0:8:2])) + coordinate_margin
        ]

        # Record the inserted symbol's position for future checks
        inserted_symbols.append((x, y, symbol_width, symbol_height))

        # Adjust coordinate information
        coordinates = [
            x + coordinate_margin, y + coordinate_margin,
            x + symbol_width - coordinate_margin, y + coordinate_margin,
            x + symbol_width - coordinate_margin, y + symbol_height - coordinate_margin,
            x + coordinate_margin, y + symbol_height - coordinate_margin
        ]
        coordinates_str = ' '.join(map(str, coordinates))

        # Save the coordinate information of the new symbol
        new_annfile = f"new_dr_data_{i}.txt"
        new_annfile_path = os.path.join(output_annfiles_path, new_annfile)

        with open(new_annfile_path, 'a') as file:
            file.write(f"{coordinates_str} {class_name} 0\n")

    # Modify the image filename
    new_image_file = f"new_dr_data_{i}.png"

    # Save the new diagram image
    new_image_path = os.path.join(output_images_path, new_image_file)
    cv2.imwrite(new_image_path, new_image)

print("이미지 생성 완료")