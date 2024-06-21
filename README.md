
## 요약
동영상에서 프레임을 추출하고, [PaddleOCR 라이브러리](https://github.com/PaddlePaddle/PaddleOCR)를 사용하여 한국어 인식 모델로 OCR을 수행한 후, 중복 프레임을 제거하여 OCR 결과를 저장합니다. OCR 결과는 CSV, TXT, JSON 형식으로 저장 가능하며 선택적으로 OCR 결과 이미지를 생성할 수 있습니다.

## 기능 설명
1. 동영상에서 프레임 추출
2. PaddleOCR 라이브러리를 통한 OCR 수행 (korean 인식 모델)
3. 중복 프레임 제거
   - 동영상 화면 기준으로 상단 80%는 자료 화면 영역, 하단 20%는 자막 영역으로 ROI 설정
   - 자료화면 영역과 자막 영역 두 ROI 모두 추출된 텍스트가 이전 프레임의 텍스트와 동일한 비율이 60% 이상일 경우 중복 프레임으로 판단하고 저장하지 않음
4. OCR 결과를 CSV, TXT, JSON 형식으로 저장
5. OCR 결과 이미지 생성 (Optional)


| 파일명                     | 해상도      | 동영상 총 길이 | FPS     | 총 프레임 수 | 중복 제거 후 프레임 수 | 총 실행시간* |
|----------------------------|-------------|----------------|---------|--------------|------------------------|-------------|
| test_video0.mp4            | 1920*1080   | 122.76초       | 29.944  | 3676         | 66                     | 92.32초     |
| test_video1.mp4            | 1920*1080   | 157.09초       | 29.970  | 4708         | 51                     | 72.24초     |
| test_video2.mp4            | 1920*1080   | 168.36초       | 29.970  | 3701         | 41                     | 58.59초     |
| test_video3.mp4            | 1920*1080   | 123.49초       | 29.970  | 7743         | 58                     | 96.52초     |
| test_video4.mp4            | 1920*1080   | 258.36초       | 29.947  | 5042         | 27                     | 63.05초     |
| resize960_test_video0.mp4  | 960*540     | 122.76초       | 29.944  | 3676         | 72                     | 78.07초     |
| resize640_test_video0.mp4  | 640*320     | 122.76초       | 29.944  | 3676         | 74                     | 55.02초     |

총 실행시간은 *Tesla V100 1대* 기준. 

## 개발 환경
- Python>=3.7
- paddlepaddle-gpu=2.5.2
- paddleocr=2.7.0.2

## 구성
```
OCR/
├── run.py
├── draw_ocr.py
├── setup.py
├── test_source/
│ ├── news_video
│ ├── variety_video
│ └── resize_video
├── requirements.txt
└── NanumGothic-Regular.ttf
```

- `run.py`: OCR 실행 모듈
- `draw_ocr.py`: `run.py`에서 `--draw_ocr` 모드를 실행하기 위한 코드
- `test_source`: 테스트 동영상 파일들이 있는 디렉토리
  - `news_video`: 뉴스 동영상 5개
  - `variety_video`: 예능프로그램 자막 테스트를 위한 예능 동영상 2개
  - `resize_video`: 해상도에 따른 실행 시간 테스트를 위한 다양한 해상도의 뉴스 동영상 3개
- `NanumGothic-Regular.ttf`: OCR 수행 결과 표시를 위한 한글 트루타입

## 실행 방법
```bash
git clone git@github.com:yesungKo/ocr.git
cd ocr
pip install -e .
```

### CLI 사용법
```bash
python run.py [VIDEO_PATH] [OUTPUT_PATH] --savefile_type='csv' --draw_ocr
```
- VIDEO_PATH(str): OCR을 수행할 비디오 경로
- OUTPUT_PATH(str): OCR 결과 저장 경로
- savefile_type(str): 중복 제거된 프레임명, OCR 수행 결과 bbox 좌표 정보가 담긴 result 파일의 형식 (csv, json, txt 가능, 기본값은 csv)
- draw_ocr(stored_true): 프레임에 OCR 결과를 그릴지 여부

## Output
```
results/
├── draw_ocr/
│   ├── result_screen_0.png
│   ├── result_screen_29.png
│   ├── ...
│   ├── result_subtitle_1073.png
│   ├── result_subtitle_1189.png
│   └── ...
├── frame_0.png
├── frame_29.png
├── frame_116.png
├── ...
└── ocr_results.csv
```

- frame_{int}.png: 중복 제거된 프레임들
- draw_ocr: drawocr 옵션 설정 시 프레임에 OCR 시각화 (자료화면과 자막 OCR 별도로 저장됨)
    - 자료화면 OCR 결과: result_screen_{int}.png
    - 자막 OCR 결과: result_subtitle_{int}.png
- ocr_result.csv: 이미지 파일명, OCR 결과, bbox 좌표값이 포함된 결과 (json, txt로 변경 가능)