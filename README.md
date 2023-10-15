# Scripts

## 데이터셋 생성 (build_split)

### 코드 설명

| 코드명               | 설명                                                              |
| -------------------- | ----------------------------------------------------------------- |
| build_new_dataset.py | 원본 데이터셋 중 큰 심볼 보유한 도면만으로 '학습용 데이터셋' 생성 |
| split_new_dataset.py | 생성된 데이터셋에 Dilation, Resize 적용                           |
| big_symbol.txt       | 데이터셋 내 큰 심볼 정보 관련 텍스트 파일                         |

### 코드 실행

위 파일에서 필요한 파라메터 및 경로 지정 후 실행

- common_path(원본 데이터셋) 경로 지정
- new_folder_path(생성 데이터셋 저장 위치) 경로 지정

## 데이터 증강 (augmentation)

- refactor 디렉토리 내에 있는 파일은 아직 수정 진행 중인 내용

### 코드 설명

| 코드명                      | 설명                                                                                        |
| --------------------------- | ------------------------------------------------------------------------------------------- |
| domain_randomize.py         | 배경 없이(흰색 배경) 큰 심볼에 Domain Randomization 적용한 결과 생성                        |
| domain_randomize_with_bg.py | 배경 포함하여 큰 심볼에 Domain Randomization 적용한 결과 생성                               |
| image_aug.py                | 도면 이미지에 Flipping(Vertical / Horizontal), Rotation(180 degree) 적용한 결과 생성 (각각) |
| symbol_aug.py               | 도면 이미지 중, 심볼에만 Rotation(180 degree) 적용한 결과 생성                              |
| aug_pipeline.py             | image_aug.py 와 symbol_aug에 적용되어야 할 내용 한 번에 생성                                |
| a_with_bbox.py              | 증강 적용이 제대로 생성되었는지 bounding_box 표시 (디버깅용)                                |

## etc (tools)

- 큰 심볼 작업 중 필요한 코드 모음

### 코드 설명

| 코드명              | 설명                                                                                                                    |
| ------------------- | ----------------------------------------------------------------------------------------------------------------------- |
| class_count.py      | 클래스별 큰 심볼 개수, 저장된 위치 정보를 .txt 파일로 저장                                                              |
| comp_filename.py    | 정상적으로 데이터셋 생성/증강이 적용되었는지 확인하기 위한 용도 (특정 디렉토리의 annfiles/images 내용 차이 확인 여부)   |
| compare_filename.py | 정상적으로 데이터셋 생성/증강이 적용되었는지 확인하기 위한 용도 (학습용 디렉토리의 annfiles/images 내용 차이 확인 여부) |
| del_filename.py     | annfiles/images 두 디렉토리 중, 한 디렉토리에만 있는 파일 삭제                                                          |
| draw_bbox.py        | 정답 생성                                                                                                               |
