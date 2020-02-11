# HarmoAIComposorModule
멜로디 작곡 인공지능 모델

## 참고 소스코드
https://github.com/Re-Coma/Classical-Piano-Composer

### 기존 소스 코드 와 다른점
멜로디만 작곡하는 기존 모델과 다르게 음 길이를 생성하는 모델을 작성하여 두게 다 실행한 다음 두개의 결과물을 하나의 미디 데이터로 합쳐서 출력

## 사용법
1. Config (training.py)
  * COMPOSER_NAME : 작곡가 이름(Chopin, Beethoven, Scarlatti) 중에 하나 선택
  * MAX_SHEET : 학습할 곡의 갯수 지정(아무것도 안하면 최대, 이왕이면 비추천)
  * TIME_SIGNATURE : 2, 3중에 하나를 선택하며, 2는 2/4, 4/4박자 계열, 3/4는 3분의 4박자 계열
  * EPOCHS : 학습 수 (200 이상 권장)
  * BATCH_SIZE : 렘에 올라갈 데이터 양(보통 GPU 사용할때 allocation관련 에러가 뜨면 이 사이즈를 조정)

2. training.py를 실행
  * 멜로디 학습이 완료되었을 경우, 가장 최근에 생성된 hdf 파일의 이름을 note_weight로 수정
  * 길이 학습이 완료되면 가장 최근에 생성된 hdf 파일을 duration_weight로 수정

3. predict.py를 실행해 midi 파일 생성
