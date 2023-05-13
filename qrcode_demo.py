import cv2
import zbar

# 이미지 파일을 로드합니다.
image = cv2.imread("image.png")

# QR 코드 디코더를 만듭니다.
scanner = zbar.Scanner()

# QR 코드를 이미지에서 스캔합니다.
results = scanner.scan(image)

# QR 코드가 발견되면 데이터를 인쇄합니다.
for result in results:
    print(result.data)
