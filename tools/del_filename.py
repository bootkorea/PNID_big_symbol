import os

directory1_path = "/Users/bootkorea/Downloads/dr_dataset/aug_dataset_dr_n6/annfiles"  # 첫 번째 디렉토리 경로
directory2_path = "/Users/bootkorea/Downloads/dr_dataset/aug_dataset_dr_n6/images"  # 두 번째 디렉토리 경로

# 첫 번째 디렉토리의 파일명 가져오기
files_in_directory1 = set()
for filename in os.listdir(directory1_path):
    if os.path.isfile(os.path.join(directory1_path, filename)):
        file_name_without_ext = os.path.splitext(filename)[0]
        files_in_directory1.add(file_name_without_ext)

# 두 번째 디렉토리의 파일명 가져오기
files_in_directory2 = set()
for filename in os.listdir(directory2_path):
    if os.path.isfile(os.path.join(directory2_path, filename)):
        file_name_without_ext = os.path.splitext(filename)[0]
        files_in_directory2.add(file_name_without_ext)

# 첫 번째 디렉토리에만 있는 파일 삭제
for filename in files_in_directory1 - files_in_directory2:
    file_path = os.path.join(directory1_path, f"{filename}.txt")
    if os.path.isfile(file_path):
        os.remove(file_path)
        print(f"Deleted file: {file_path}")

# 두 번째 디렉토리에만 있는 파일 삭제
for filename in files_in_directory2 - files_in_directory1:
    file_path = os.path.join(directory2_path, f"{filename}.txt")
    if os.path.isfile(file_path):
        os.remove(file_path)
        print(f"Deleted file: {file_path}")