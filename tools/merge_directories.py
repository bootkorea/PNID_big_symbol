import os
import shutil

def merge_and_rename(directories, destination_dir, new_filename_template="file_{}.jpg"):
    """
    여러 개의 디렉토리 내의 파일들을 하나의 디렉토리로 이동시키고 파일명을 변경하는 함수.

    Parameters:
        directories (list): 파일들이 있는 여러 개의 디렉토리 리스트.
        destination_dir (str): 파일들을 이동시킬 대상 디렉토리.
        new_filename_template (str): 새로운 파일명 템플릿. {} 부분은 숫자로 대체됩니다. 기본값은 'file_{}.jpg'.
    """
    if not os.path.exists(destination_dir):
        os.makedirs(destination_dir)

    for dir_path in directories:
        if not os.path.exists(dir_path):
            print(f"경고: 디렉토리 '{dir_path}'가 존재하지 않습니다.")
            continue

        files = os.listdir(dir_path)
        for index, filename in enumerate(files):
            src_file = os.path.join(dir_path, filename)
            new_filename = new_filename_template.format(index)
            dst_file = os.path.join(destination_dir, new_filename)

            # 파일 이동 및 이름 변경
            shutil.move(src_file, dst_file)

if __name__ == "__main__":
    source_directories = ["/Users/bootkorea/Documents/GitHub/big_symbol/dataset/augmentation/aug_dataset_horizon_flip", \
                          "/Users/bootkorea/Documents/GitHub/big_symbol/dataset/augmentation/aug_dataset_rotate_180", \
                          "/Users/bootkorea/Documents/GitHub/big_symbol/dataset/augmentation/aug_dataset_vertical_flip", \
                          "/Users/bootkorea/Documents/GitHub/big_symbol/dataset/augmentation/aug_datatset_symbol_rotate_180"]
    destination_directory = "/Users/bootkorea/Documents/GitHub/big_symbol/dataset/augmentation/merge_dataset"

    merge_and_rename(source_directories, destination_directory)
