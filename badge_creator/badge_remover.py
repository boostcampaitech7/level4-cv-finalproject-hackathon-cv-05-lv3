from rembg import remove

def remove_background_from_image(input_path, output_path):
    """
    rembg 라이브러리를 이용하여 이미지 배경을 제거합니다.
    :param input_path: 원본 이미지 파일 경로
    :param output_path: 배경 제거된 이미지를 저장할 파일 경로
    """
    with open(input_path, 'rb') as i:
        input_data = i.read()
    output_data = remove(input_data)
    with open(output_path, 'wb') as o:
        o.write(output_data)
