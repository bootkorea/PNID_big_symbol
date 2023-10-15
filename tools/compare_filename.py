import os

directory_path = "/Users/bootkorea/Documents/GitHub/big_symbol/split_big_pnid"  # train/val/test 디렉토리가 있는 경로로 변경해주세요.

subdirectories = ["train", "val", "test"]
directories_to_compare = ["annfiles", "images"]

files_in_directories = {}

# 디렉토리 내의 파일명 가져오기
for subdir in subdirectories:
    files_in_directories[subdir] = {}
    for directory_to_compare in directories_to_compare:
        current_directory = os.path.join(directory_path, subdir, directory_to_compare)
        files_in_directories[subdir][directory_to_compare] = set()
        for filename in os.listdir(current_directory):
            if os.path.isfile(os.path.join(current_directory, filename)):
                file_name_without_ext = os.path.splitext(filename)[0]
                files_in_directories[subdir][directory_to_compare].add(file_name_without_ext)

# 파일명 비교하여 한 디렉토리에만 존재하는 파일명 출력
for subdir in subdirectories:
    print(f"Comparison results for {subdir} directory:")
    for directory_to_compare in directories_to_compare:
        other_directories = [d for d in directories_to_compare if d != directory_to_compare]
        other_files = set()
        for other_directory in other_directories:
            other_files.update(files_in_directories[subdir][other_directory])
        files_only_in_directory = files_in_directories[subdir][directory_to_compare] - other_files
        num_files_compared = len(files_in_directories[subdir][directory_to_compare]) + len(other_files)
        num_files_only_in_directory = len(files_only_in_directory)
        print(f"Directory: {directory_to_compare}")
        print(f"Total files compared: {num_files_compared}")
        print(f"Files only in directory: {num_files_only_in_directory}")
        print("Files:")
        for filename in files_only_in_directory:
            print(os.path.join(directory_path, subdir, directory_to_compare, filename))
        print()
