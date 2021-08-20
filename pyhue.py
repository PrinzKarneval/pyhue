import requests
from math import pow
from config import *


def convert_rgb_to_xy(red: int, green: int, blue: int) -> [float, float]:
    # Convert to values from 0 to 1
    red /= 255
    green /= 255
    blue /= 255
    # Gamma correction
    red = pow((red + 0.055) / (1.0 + 0.055), 2.4) if red > 0.04045 else (red / 12.92)
    green = pow((green + 0.055) / (1.0 + 0.055), 2.4) if green > 0.04045 else (green / 12.92)
    blue = pow((blue + 0.055) / (1.0 + 0.055), 2.4) if blue > 0.04045 else (blue / 12.92)
    # Convert RGB to XYZ using the RGB D65 conversion formula
    X = red * 0.649926 + green * 0.103455 + blue * 0.197109
    Y = red * 0.234327 + green * 0.743075 + blue * 0.022598
    Z = red * 0.0000000 + green * 0.053077 + blue * 1.035763
    # Calculate xy from XYZ
    x = X / (X + Y + Z) if X + Y + Z > 0.0 else 0
    y = Y / (X + Y + Z) if X + Y + Z > 0.0 else 0
    return [round(x, 3), round(y, 3)]


def request(method, url, *args):
    methods = {
        "get": requests.get,
        "put": requests.put,
        "post": requests.post,
        "delete": requests.delete
    }
    headers = {'content-type': 'application/json'}
    if args:
        response = methods[method](f"{API_URL}/{url}", data=args[0], headers=headers, verify=False)
    else:
        response = methods[method](f"{API_URL}/{url}", headers=headers, verify=False)
    return response.content

