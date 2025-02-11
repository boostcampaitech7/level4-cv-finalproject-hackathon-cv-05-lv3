import cv2
import numpy as np
import requests
from io import BytesIO
from PIL import Image

def load_image(image_path):
    """
    이미지 경로가 URL이면 다운로드하여 OpenCV 형식 (numpy array)로 변환하고,
    로컬 파일이면 cv2.imread()를 사용하여 불러옵니다.
    """
    if image_path.startswith("http"):  # URL인지 확인
        try:
            response = requests.get(image_path, timeout=5)
            response.raise_for_status()  # 요청 실패 시 예외 발생
            image = Image.open(BytesIO(response.content)).convert("RGB")  # PIL 이미지 변환
            image = np.array(image)  # numpy 배열 변환
            image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)  # OpenCV BGR 형식 변환
        except requests.exceptions.RequestException as e:
            raise ValueError(f"이미지를 다운로드할 수 없습니다: {e}")
    else:
        image = cv2.imread(image_path)  # 로컬 파일 불러오기
        if image is None:
            raise ValueError(f"이미지를 불러올 수 없습니다: {image_path}")
    
    return image

def extract_dominant_colors(image_path, k=3):
    """
    입력 이미지에서 k개의 dominant 색상을 K-means 클러스터링을 통해 추출합니다.
    :param image: OpenCV 이미지 (BGR 순)
    :param k: 추출할 색상의 수 (기본값 3)
    :return: dominant_colors (k×3 배열, BGR 순)
    """
    image = load_image(image_path)
    pixels = image.reshape((-1, 3)).astype("float32")
    criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 10, 1.0)
    attempts = 10
    _, labels, centers = cv2.kmeans(pixels, k, None, criteria, attempts, cv2.KMEANS_RANDOM_CENTERS)
    centers = np.uint8(centers)
    _, counts = np.unique(labels, return_counts=True)
    sorted_idx = np.argsort(-counts)
    dominant_colors = centers[sorted_idx]
    return dominant_colors

def create_central_circle_image(dominant_colors, canvas_size=1024, circle_diameter=512):
    """
    canvas_size×canvas_size 흰색 배경 이미지 중앙에 circle_diameter 크기의 원을 생성합니다.
    원은 3개의 파이 섹터로 나뉘며, 각 섹터에 dominant_colors의 색상을 채웁니다.
    :param dominant_colors: dominant 색상 배열 (BGR 순, 길이 3 이상)
    :param canvas_size: 캔버스 크기 (기본값 1024)
    :param circle_diameter: 원의 지름 (기본값 512)
    :return: 결과 이미지 (OpenCV 이미지, BGR 순)
    """
    image = np.ones((canvas_size, canvas_size, 3), dtype=np.uint8) * 255
    center = (canvas_size // 2, canvas_size // 2)
    radius = circle_diameter // 2
    sectors = [(0, 120), (120, 240), (240, 360)]
    for i, (start_angle, end_angle) in enumerate(sectors):
        color = tuple(int(c) for c in dominant_colors[i].tolist())
        cv2.ellipse(image, center, (radius, radius), 0, start_angle, end_angle, color, thickness=-1)
    return image