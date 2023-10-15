import os
from collections import defaultdict

# 디렉토리 경로 설정
base_dir = "split_big_pnid"
split_dirs = ["train", "val", "test"]
output_file = "symbol_counts.txt"  # 결과를 저장할 파일 이름

# 각 클래스별 심볼 이미지 개수를 저장할 딕셔너리
symbol_counts = defaultdict(int)

# 각 클래스별 train, val, test 디렉토리에서 이미지 개수를 저장할 딕셔너리
image_counts = defaultdict(lambda: defaultdict(int))

# 각 split 디렉토리에서 .txt 파일을 찾아 읽어옴
for split_dir in split_dirs:
    annfiles_dir = os.path.join(base_dir, split_dir, "annfiles")
    
    # annfiles 디렉토리에서 .txt 파일 목록을 가져옴
    txt_files = [f for f in os.listdir(annfiles_dir) if f.endswith(".txt")]
    
    # 각 .txt 파일을 읽어 심볼 이미지 개수를 계산
    for txt_file in txt_files:
        with open(os.path.join(annfiles_dir, txt_file), 'r') as file:
            lines = file.readlines()
            for line in lines:
                parts = line.strip().split()
                if len(parts) >= 9:
                    class_name = parts[8]
                    symbol_counts[class_name] += 1
                    image_counts[class_name][split_dir] += 1

# 결과를 파일에 저장 (count별로 정렬)
with open(output_file, 'w') as output:
    sorted_symbol_counts = sorted(symbol_counts.items(), key=lambda x: x[1])  # count로 정렬
    for class_name, count in sorted_symbol_counts:
        output.write(f"[{class_name}]\n")
        output.write(f"count: {count:02d}\n")
        output.write("pnid:\n")
        
        for split_dir in split_dirs:
            annfiles_dir = os.path.join(base_dir, split_dir, "annfiles")
            txt_files = [f for f in os.listdir(annfiles_dir) if f.endswith(".txt")]
            
            for txt_file in txt_files:
                with open(os.path.join(annfiles_dir, txt_file), 'r') as file:
                    lines = file.readlines()
                    symbol_names = set()
                    for line in lines:
                        parts = line.strip().split()
                        if len(parts) >= 9:
                            file_class_name = parts[8]
                            if file_class_name == class_name:
                                symbol_names.add(os.path.splitext(txt_file)[0])
                    
                    if symbol_names:
                        output.write(f"{split_dir}/{txt_file} ({len(symbol_names)}장)\n")
        
        # 각 클래스별 train, val, test 디렉토리에 이미지 개수 출력
        output.write("Image Counts:\n")
        for split_dir in split_dirs:
            output.write(f"{split_dir}: {image_counts[class_name][split_dir]}장\n")
        
        output.write("\n")
