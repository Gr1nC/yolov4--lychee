from PIL import Image
from PIL.ExifTags import TAGS, GPSTAGS

import piexif
from fractions import Fraction

def add_location_to_exif(image_path, lat, lon):
    """将给定的经纬度信息添加到 JPEG 照片的 EXIF 数据中"""
    # 构造 GPSIFD 字典
    gps_ifd = {
        piexif.GPSIFD.GPSVersionID: (2, 0, 0, 0),
        piexif.GPSIFD.GPSLatitudeRef: 'N' if lat >= 0 else 'S',
        piexif.GPSIFD.GPSLatitude: convert_to_rational(abs(lat)),
        piexif.GPSIFD.GPSLongitudeRef: 'E' if lon >= 0 else 'W',
        piexif.GPSIFD.GPSLongitude: convert_to_rational(abs(lon))
    }
    # 将 GPSIFD 字典添加到 EXIF 数据中
    exif_dict = piexif.load(image_path)
    exif_dict['GPS'] = gps_ifd
    # 将更新后的 EXIF 数据保存到照片中
    exif_bytes = piexif.dump(exif_dict)
    piexif.insert(exif_bytes, image_path)
    
def convert_to_rational(number):
    """将给定的数字转换为有理数"""
    # 将数字转换为带分数的字符串
    fraction = Fraction(number).limit_denominator()
    return (
        (fraction.numerator, fraction.denominator),
        (0, 1),
        (0, 1)
    )

import os



def get_exif_data(image_path):
    """从图像中提取 EXIF 数据"""
    exif_data = {}
    with Image.open(image_path) as img:
        info = img._getexif()
        if info:
            for tag, value in info.items():
                decoded_tag = TAGS.get(tag, tag)
                if decoded_tag == 'GPSInfo':
                    gps_data = {}
                    for t in value:
                        sub_decoded_tag = GPSTAGS.get(t, t)
                        gps_data[sub_decoded_tag] = value[t]
                    exif_data[decoded_tag] = gps_data
                else:
                    exif_data[decoded_tag] = value
    return exif_data

def get_lat_lon(exif_data):
    """从 EXIF 数据中提取经纬度信息"""
    lat = None
    lon = None
    if 'GPSInfo' in exif_data:
        gps_info = exif_data['GPSInfo']
        gps_latitude = _convert_to_degrees(gps_info['GPSLatitude'])
        gps_latitude_ref = gps_info['GPSLatitudeRef']
        gps_longitude = _convert_to_degrees(gps_info['GPSLongitude'])
        gps_longitude_ref = gps_info['GPSLongitudeRef']
        if gps_latitude and gps_latitude_ref and gps_longitude and gps_longitude_ref:
            if gps_latitude_ref == 'N':
                lat = gps_latitude
            else:
                lat = -gps_latitude
            if gps_longitude_ref == 'E':
                lon = gps_longitude
            else:
                lon = -gps_longitude
    return lat, lon

def _convert_to_degrees(value):
    """将经纬度数据从度分秒格式转换为十进制格式"""
    degrees = float(value[0])
    minutes = float(value[1]) / 60.0
    seconds = float(value[2]) / 3600.0
    return degrees + minutes + seconds


# image_folder = 'D:/YOLO/yolov4-pytorch/data/images'
# lat, lon = 113.406273, 23.058386

# for filename in os.listdir(image_folder):
#     if filename.endswith('.jpg'):
#         image_path = os.path.join(image_folder, filename)
#         add_location_to_exif(image_path, lat, lon)
#         print(filename+' DONE')
path = 'D:/YOLO/yolov4-pytorch/data/images/1.jpg'
a = get_exif_data(path)
print(get_lat_lon(a))