import os

# 입력 디렉토리 설정
input_dir = '/Users/bootkorea/Documents/GitHub/big_symbol/test_results/aug_s2anet_epoch30'  # 입력 디렉토리 경로
output_dir = '/Users/bootkorea/Documents/GitHub/big_symbol/Detection_annfiles/'  # 출력 디렉토리 경로

# 결과 디렉토리 생성
os.makedirs(output_dir, exist_ok=True)

# 입력 디렉토리 내의 모든 파일에 대해 처리
for filename in os.listdir(input_dir):
    if filename.startswith('Task1_') and filename.endswith('.txt'):
        class_name = filename[len('Task1_'):-len('.txt')]  # 클래스명 추출
        
        with open(os.path.join(input_dir, filename), 'r') as file:
            lines = file.readlines()
        
        for line in lines:
            parts = line.strip().split()
            if len(parts) >= 10:
                image_name = parts[0].split('.')[0]  # 도면명 추출
                coordinates = ' '.join(parts[2:10])  # 좌표 정보 추출
                symbol_name = class_name  # 심볼명
                output_filename = os.path.join(output_dir, f"{image_name}.txt")
                
                with open(output_filename, 'a') as output_file:
                    output_file.write(f"{coordinates} {symbol_name}\n")