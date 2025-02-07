import cv2
import numpy as np

def extract_dominant_colors(image, k=3):
    """
    입력 이미지에서 k개의 dominant 색상을 K-means 클러스터링을 통해 추출합니다.
    :param image: OpenCV 이미지 (BGR 순)
    :param k: 추출할 색상의 수 (기본값 3)
    :return: dominant_colors (k×3 배열, BGR 순)
    """
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