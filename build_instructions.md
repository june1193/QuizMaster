# 정처기 퀴즈 프로그램 빌드 가이드

## 프로그램 실행
```bash
python quiz_program.py
```

## PyInstaller로 EXE 파일 생성

### 1. PyInstaller 설치
```bash
pip install pyinstaller
```

### 2. 기본 빌드 명령어
```bash
pyinstaller --onefile --windowed quiz_program.py
```

### 3. 고급 빌드 옵션 (권장)
```bash
pyinstaller --onefile --windowed --name "정처기퀴즈" --icon=icon.ico quiz_program.py
```

### 4. 빌드 옵션 설명
- `--onefile`: 단일 실행 파일로 생성
- `--windowed`: 콘솔 창을 표시하지 않음 (GUI 프로그램용)
- `--name`: 생성될 실행 파일의 이름 지정
- `--icon`: 아이콘 파일 지정 (선택사항)

### 5. 빌드 결과
- `dist` 폴더에 실행 파일이 생성됩니다
- `정처기퀴즈.exe` 파일을 실행하면 프로그램이 시작됩니다

### 6. 배포 시 주의사항
- 생성된 exe 파일과 같은 폴더에 `quiz_data.json` 파일이 생성됩니다
- 문제 데이터는 이 JSON 파일에 저장되므로 함께 배포해야 합니다

## 문제 해결
- 빌드 시 오류가 발생하면 `--debug all` 옵션을 추가하여 디버그 정보를 확인하세요
- 바이러스 백신 프로그램이 실행 파일을 차단할 수 있으니 예외 처리하세요
