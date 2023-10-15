import os
import cv2

# annfiles와 images 디렉토리 경로 설정
annfiles_dir = "/Users/bootkorea/Documents/GitHub/big_symbol/test/annfiles"
images_dir = "/Users/bootkorea/Documents/GitHub/big_symbol/test/images"

# bounding_box 그리기 함수
def draw_bounding_boxes(image, coords_list):
    for coords in coords_list:
        # 좌표 정보 파싱
        x_coords = coords[:8:2]
        y_coords = coords[1:8:2]
        label = coords[8]  # index 8에 있는 내용

        # 각 좌표쌍을 선으로 연결하여 그리기
        for j in range(4):
            x1, y1 = x_coords[j], y_coords[j]
            x2, y2 = x_coords[(j + 1) % 4], y_coords[(j + 1) % 4]
            cv2.line(image, (x1, y1), (x2, y2), (50, 200, 40), 2)

        # bounding box 주위에 라벨 표시
        cv2.putText(image, label, (x_coords[0], y_coords[0] - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (50, 200, 50), 2)

# annfiles 디렉토리 내의 .txt 파일 목록 가져오기
txt_files = [file for file in os.listdir(annfiles_dir) if file.endswith(".txt")]

# .txt 파일을 순회하며 bbox 그리기
for txt_file in txt_files:
    txt_path = os.path.join(annfiles_dir, txt_file)
    image_file = txt_file.replace(".txt", ".png")
    image_path = os.path.join(images_dir, image_file)

    # 이미지 로드
    image = cv2.imread(image_path)

    # .txt 파일에서 좌표 정보 읽기
    with open(txt_path, "r") as f:
        lines = f.readlines()
        coords_list = []
        for line in lines:
            data = line.strip().split()
            coords = list(map(int, data[:8]))  # x1 y1 x2 y2 x3 y3 x4 y4 좌표 정보 파싱
            label = data[8]  # index 8에 있는 내용
            coords.append(label)  # 좌표 정보 뒤에 label 추가
            coords_list.append(coords)

        # bounding box 그리기 함수 호출
        draw_bounding_boxes(image, coords_list)
        
        # 이미지에 그려진 bbox 저장
        output_image_path = os.path.join(images_dir, image_file)
        os.makedirs(os.path.dirname(output_image_path), exist_ok=True)
        cv2.imwrite(output_image_path, image)
        
        # 터미널에 현재 심볼 처리 결과 출력
        print(f"Processed: {image_file}")

print("bbox 그리기 완료!")
