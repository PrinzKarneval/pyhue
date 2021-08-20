from json import dumps
from pyhue import request, convert_rgb_to_xy
import json


def multiple(ids: list, action, *options):
    for id in ids:
        if options:
            action(id, *options)
        else:
            action(id)


def get(id: int = None):
    """
    Gets the attributes and state of a given light.

    :param id:
    :return:
    """
    if id:
        return request("get", f"lights/{id}")
    return request("get", "lights")


def put(id: int, options: dict):
    """Update a bulb"""
    return request("put", f"lights/{id}", dumps(options))


def put_state(id: int, options: dict):
    """Update state of bulb"""
    return request("put", f"lights/{id}/state", dumps(options))


def name(id, value: str):
    """Rename bulb"""
    if len(value) > 32:
        raise Warning("Max length is 32")
    put(id, {"name": value[:32]})


def on(id: int):
    """Turn bulb on"""
    return put_state(id, {"on": True})


def off(id: int):
    """Turn bulb off"""
    return put_state(id, {"on": False})


def turn_all_on():
    """Turn all bulbs on"""
    response = get()
    r_json = json.loads(response)
    for k in r_json.keys():
        on(int(k))


def turn_all_off():
    """Turn all bulbs off"""
    response = get()
    r_json = json.loads(response)
    for k in r_json.keys():
        off(int(k))


def bri(id: int, value: int):
    """
    The brightness value to set the light to.
    Brightness is a scale from 1 (the minimum the light is capable of) to 254 (the maximum).
    Note: a brightness of 1 is not off.
    e.g. “brightness”: 60 will set the light to a specific brightness


    :param id:
    :param value:
    :return:
    """
    return put_state(id, {"bri": value})


def hue(id: int, value: int):
    """
    The hue value to set light to.The hue value is a wrapping value between 0 and 65535.
    Both 0 and 65535 are red, 25500 is green and 46920 is blue.
    e.g. “hue”: 50000 will set the light to a specific hue.

    :param id:
    :param value:
    :return:
    """
    return put_state(id, {"hue": value})


def sat(id: int, value: int):
    """
    Saturation of the light. 254 is the most saturated (colored) and 0 is the least saturated (white).

    :param id:
    :param value:
    :return:
    """
    return put_state(id, {"sat": value})


def xy(id: int, x: float, y: float):
    """
    The x and y coordinates of a color in CIE color space.
    The first entry is the x coordinate and the second entry is the y coordinate.
    Both x and y must be between 0 and 1.
    If the specified coordinates are not in the CIE color space, the closest color to the coordinates will be chosen.

    :param id:
    :param x:
    :param y:
    :return:
    """
    return put_state(id, {"xy": [x, y]})


def ct(id: int, value: int):
    """
    The Mired color temperature of the light.
    2012 connected lights are capable of 153 (6500K) to 500 (2000K).

    :param id:
    :param value:
    :return:
    """
    return put_state(id, {"ct": value})


def rgb(id: int, red: int, green: int, blue: int):
    """Set color by rgb"""
    x, y = convert_rgb_to_xy(red, green, blue)
    return xy(id, x, y)


def brightness_linear_inc(id, duration, start: int = 0, end: int = 254):
    """Increase brightness of bulb from [start] to [end] over [duration]-seconds"""
    if start >= end:
        raise ValueError("Start must be smaller than end")
    put_state(id, {"bri": int(start)})
    put_state(id, {"bri": int(end), "transitiontime": duration * 10})


def alert(id, value: str = "none"):
    """
    The alert effect,is a temporary change to the bulb’s state, and has one of the following values:
    “none” – The light is not performing an alert effect.
    “select” – The light is performing one breathe cycle.
    “lselect” – The light is performing breathe cycles for 15 seconds or until an "alert": "none" command is received.
    Note that this contains the last alert sent to the light and not its current state.
    i.e. After the breathe cycle has finished the bridge does not reset the alert to “none“.

    :param id:
    :param value:
    :return:
    """
    put_state(id, {"alert": value})


def effect(id, state: str):
    """
    The dynamic effect of the light. Currently “none” and “colorloop” are supported.
    Other values will generate an error of type 7.
    Setting the effect to colorloop will cycle through all hues using the current brightness and saturation settings.

    :param id:
    :param state:
    :return:
    """
    put_state(id, {"effect": "colorloop" if state else "none"})


def transitiontime(id: int, value: int):
    """
    The duration of the transition from the light’s current state to the new state.
    This is given as a multiple of 100ms and defaults to 4 (400ms).
    For example, setting transitiontime:10 will make the transition last 1 second.

    :param id:
    :param value:
    :return:
    """
    put_state(id, {"transitiontime": value})


def bri_inc(id: int, value: int):
    """
    Increments or decrements the value of the brightness.
    bri_inc is ignored if the bri attribute is provided.
    Any ongoing bri transition is stopped.
    Setting a value of 0 also stops any ongoing transition.
    The bridge will return the bri value after the increment is performed.

    :param id:
    :param value:
    :return:
    """
    put_state(id, {"bri_inc": value})


def sat_inc(id: int, value: int):
    """
   Increments or decrements the value of the sat.
   sat_inc is ignored if the sat attribute is provided.
   Any ongoing sat transition is stopped.
   Setting a value of 0 also stops any ongoing transition.
   The bridge will return the sat value after the increment is performed.

    :param id:
    :param value:
    :return:
    """
    put_state(id, {"sat_inc": value})


def hue_inc(id: int, value: int):
    """
    Increments or decrements the value of the hue.
    hue_inc is ignored if the hue attribute is provided.
    Any ongoing color transition is stopped.
    Setting a value of 0 also stops any ongoing transition.
    The bridge will return the hue value after the increment is performed.
    Note if the resulting values are < 0 or > 65535 the result is wrapped.
    For example:
        {"hue_inc":  1} on a hue value of 65535 results in a hue of 0.
        {"hue_inc":  -2} on a hue value of 0 results in a hue of 65534

    :param id:
    :param value:
    :return:
    """
    put_state(id, {"hue_inc": value})


def ct_inc(id: int, value: int):
    """
    Increments or decrements the value of the ct.
    ct_inc is ignored if the ct attribute is provided.
    Any ongoing color transition is stopped.
    Setting a value of 0 also stops any ongoing transition.
    The bridge will return the ct value after the increment is performed.
    :param id:
    :param value:
    :return:
    """
    put_state(id, {"ct_inc": value})


def xy_inc(id: int, value: int):
    """
    Increments or decrements the value of the xy.
    xy_inc is ignored if the xy attribute is provided. Any ongoing color transition is stopped.
    Setting a value of 0 also stops any ongoing transition.
    Will stop at it’s gamut boundaries.
    The bridge will return the xy value after the increment is performed.
    Max value [0.5, 0.5].

    :param id:
    :param value:
    :return:
    """
    put_state(id, {"xy_inc": value})


def delete(id):
    """Delete a light form the bridge"""
    return request("delete", f"lights/{id}")
