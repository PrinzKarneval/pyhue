"""Groups API"""
from json import dumps

from pyhue import request


def get(id: int = None):
    """
    Gets a list of all groups that have been added to the bridge.
    A group is a list of lights that can be created, modified and deleted by a user.
    """
    if id:
        return request("get", "groups")
    return request("get", f"groups/{id}")


def create(body):
    """
    Creates a new group containing the lights specified and optional name.
    A new group is created in the bridge with the next available id.
    """
    request("post", "groups", body)


def put(id: int, options: dict):
    """
    Allows the user to modify the name, light and class membership of a group.

    :param id:
    :param options:
    :return:
    """
    return request("put", f"groups/{id}", dumps(options))


def put_state(id: int, options: dict):
    """
    Modifies the state of all lights in a group.
    User created groups will have an ID of 1 or higher;
    however a special group with an ID of 0 also exists containing all the lamps known by the bridge.

    :param id:
    :param options:
    :return:
    """
    return request("put", f"groups/{id}/action", dumps(options))


def on(id):
    """Set state of the light to on."""
    return put_state(id, {"on": True})


def off(id):
    """Set state of the light to off."""
    return put_state(id, {"on": False})


def bri(id, value):
    """
    Brightness is a scale from 0 (the minimum the light is capable of) to 254 (the maximum).
    Note: a brightness of 0 is not off.

    :param id:
    :param value:
    :return:
    """
    return put_state(id, {"bri": value})


def hue(id, value):
    """
    The hue value is a wrapping value between 0 and 65535.
    Both 0 and 65535 are red, 25500 is green and 46920 is blue.

    :param id:
    :param value:
    :return:
    """
    return put_state(id, {"hue": value})


def sat(id, value):
    """
    Saturation of the light. 254 is the most saturated (colored) and 0 is the least saturated (white).
    :param id:
    :param value:
    :return:
    """
    return put_state(id, {"sat": value})


def xy(id, x, y):
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


def ct(id, value):
    """
    The Mired Color temperature of the light. 2012 connected lights are capable of 153 (6500K) to 500 (2000K).

    :param id:
    :param value:
    :return:
    """
    return put_state(id, {"ct": value})


def alert(id, value):
    """
    The alert effect, which is a temporary change to the bulb’s state, and has one of the following values:
    “none” – The light is not performing an alert effect.
    “select” – The light is performing one breathe cycle.
    “lselect” – The light is performing breathe cycles for 15 seconds or until an "alert": "none" command is received.
    Note that this contains the last alert sent to the light and not its current state.
    i.e. After the breathe cycle has finished the bridge does not reset the alert to “none“.

    :param id:
    :param value:
    :return:
    """
    return put_state(id, {"alert": value})


def effect(id, value):
    """
    The dynamic effect of the light, currently “none” and “colorloop” are supported.
    Other values will generate an error of type 7.
    Setting the effect to colorloop will cycle through all hues using the current brightness and saturation settings.

    :param id:
    :param value:
    :return:
    """
    return put_state(id, {"effect": value})


def transitiontime(id, value):
    """
    The duration of the transition from the light’s current state to the new state.
    This is given as a multiple of 100ms and defaults to 4 (400ms).
    For example, setting transitiontime:10 will make the transition last 1 second.

    :param id:
    :param value:
    :return:
    """
    return put_state(id, {"transitiontime": value})


def bri_inc(id, value):
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
    return put_state(id, {"bri_inc": value})


def sat_inc(id, value):
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
    return put_state(id, {"sat_inc": value})


def hue_inc(id, value):
    """
    Increments or decrements the value of the hue.
    hue_inc is ignored if the hue attribute is provided.
    Any ongoing color transition is stopped. Setting a value of 0 also stops any ongoing transition.
     The bridge will return the hue value after the increment is performed.
     Note if the resulting values are < 0 or > 65535 the result is wrapped.
     For example:
        {"hue_inc":  1} on a hue value of 65535 results in a hue of 0.
        {"hue_inc":  -2} on a hue value of 0 results in a hue of 65534.

    :param id:
    :param value:
    :return:
    """
    return put_state(id, {"hue_inc": value})


def ct_inc(id, value):
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
    return put_state(id, {"ct_inc": value})


def xy_inc(id, value):
    """
    Increments or decrements the value of the xy.
    xy_inc is ignored if the xy attribute is provided.
    Any ongoing color transition is stopped.
    Will stop at it’s gamut boundaries.
    Setting a value of 0 also stops any ongoing transition.
    The bridge will return the xy value after the increment is performed.

    :param id:
    :param value:
    :return:
    """
    return put_state(id, {"xy_inc": value})


def scene(id, value):
    """
    The scene identifier if the scene you wish to recall.

    :param id:
    :param value:
    :return:
    """
    return put_state(id, {"scene": value})


def delete(id):
    """
    Deletes the specified group from the bridge.

    :param id:
    :return:
    """
    return request("delete", f"delete/{id}")
