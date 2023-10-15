import os
import shutil

# 원본 이미지 파일이 있는 디렉토리 경로
source_image_dir = "/Users/bootkorea/Downloads/split_big_pnid/train/images"

# 특정 디렉토리 내의 annfiles 디렉토리 경로
annfiles_dir = "/Users/bootkorea/Documents/GitHub/big_symbol/need_aug/annfiles"

# 특정 디렉토리 내의 images 디렉토리 경로
images_dir = "/Users/bootkorea/Documents/GitHub/big_symbol/need_aug/images"

# annfiles 디렉토리 내의 .txt 파일 목록 가져오기
txt_files = [f for f in os.listdir(annfiles_dir) if f.endswith(".txt")]

# 이미지 파일을 원본 디렉토리에서 찾아서 images 디렉토리로 복사
for txt_file in txt_files:
    image_file_name = os.path.splitext(txt_file)[0]  # .txt 확장자 제거
    source_image_path = os.path.join(source_image_dir, f"{image_file_name}.png")
    destination_image_path = os.path.join(images_dir, f"{image_file_name}.png")
    
    # 이미지 파일 복사
    if os.path.exists(source_image_path):
        shutil.copy2(source_image_path, destination_image_path)
        print(f"이미지 파일 복사 완료: {image_file_name}.png")

print("모든 파일 복사 완료")
