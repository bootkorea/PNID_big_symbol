import os
import random
import shutil
from image_aug import merge_directories
from drbg import generate_new_diagram  # 새로 추가한 import

# 데이터셋 폴더 경로
splitset_path = "/Users/bootkorea/Documents/GitHub/big_symbol/dataset/split_big_pnid/"
output_path = "/Users/bootkorea/Documents/GitHub/big_symbol/augmented_dataset/"

# 도메인 랜덤화 경로
dr_path = "/Users/bootkorea/Documents/GitHub/big_symbol/need_aug"  # dr_path 변수 정의

# 중간 과정: .txt 파일에서 심볼 개수 계산
def count_symbols_in_txt_files(txt_dir):
    symbol_counts = {}
    for txt_file in os.listdir(txt_dir):
        if txt_file.endswith(".txt"):
            with open(os.path.join(txt_dir, txt_file), 'r') as file:
                lines = file.readlines()
                for line in lines:
                    parts = line.strip().split()
                    if len(parts) >= 9:
                        class_name = parts[8]
                        symbol_counts[class_name] = symbol_counts.get(class_name, 0) + 1
    return symbol_counts

# 1. 이미지 데이터 증강 (image_aug.py 사용)
output_augmented_path = os.path.join(output_path, "augmented_data")
merge_directories(splitset_path, output_augmented_path)

# 2. 도메인 랜덤화를 적용하기 전에 .txt 파일에서 심볼 개수 계산
txt_dir = os.path.join(output_augmented_path, "annfiles")
symbol_counts = count_symbols_in_txt_files(txt_dir)

# 3. 도메인 랜덤화 적용
generate_new_diagram(os.path.join(output_path, "domain_randomized_data"), dr_path)  # 수정된 부분

# 중간 과정: 도메인 랜덤화 후 .txt 파일에서 다시 심볼 개수 계산
txt_dir_dr = os.path.join(output_path, "domain_randomized_data", "annfiles")
symbol_counts_dr = count_symbols_in_txt_files(txt_dir_dr)

# 4. 심볼 개수가 특정 값 미만인 심볼에 대해서만 복사
min_symbol_count = 5  # 여기에 원하는 최소 심볼 개수를 설정하세요

for class_name, count in symbol_counts_dr.items():
    if count < min_symbol_count:
        # 해당 클래스의 심볼 이미지 개수가 특정 값 미만인 경우에만 복사
        src_txt_file = os.path.join(txt_dir_dr, f"{class_name}.txt")
        dest_txt_file = os.path.join(txt_dir, f"{class_name}.txt")
        shutil.copy(src_txt_file, dest_txt_file)

print("새로운 학습 데이터 생성 완료")
