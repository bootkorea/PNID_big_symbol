import os

directory1_path = "/Users/bootkorea/Documents/GitHub/big_symbol/aug_dataset_vertical_flip/annfiles"
directory2_path = "/Users/bootkorea/Documents/GitHub/big_symbol/aug_dataset_vertical_flip/images"
new_name_prefix = "vertical_flip"

# # 파일명 접두사 추가
# 첫 번째 디렉토리의 파일명 변경
for filename in os.listdir(directory1_path):
    old_name = os.path.join(directory1_path, filename)
    new_name = os.path.join(directory1_path, new_name_prefix + filename)
    os.rename(old_name, new_name)

# 두 번째 디렉토리의 파일명 변경
for filename in os.listdir(directory2_path):
    old_name = os.path.join(directory2_path, filename)
    new_name = os.path.join(directory2_path, new_name_prefix + filename)
    os.rename(old_name, new_name)

# # 파일명 접두사 삭제
# # 첫 번째 디렉토리의 파일명 변경
# for filename in os.listdir(directory1_path):
#     old_name = os.path.join(directory1_path, filename)
#     new_name = os.path.join(directory1_path, filename[1:])
#     os.rename(old_name, new_name)

# # 두 번째 디렉토리의 파일명 변경
# for filename in os.listdir(directory2_path):
#     old_name = os.path.join(directory2_path, filename)
#     new_name = os.path.join(directory2_path, filename[1:])
#     os.rename(old_name, new_name)