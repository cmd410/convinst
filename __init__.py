from .regutil import register, unregister  # NOQA
from .custom_props import *  # NOQA
from .operators import *  # NOQA
from .menus import *  # NOQA


bl_info = {
    "name": "Convenient Instances",
    "description": "Creating collection instance assets made easy.",
    "author": "Crystal Melting Dot",
    "version": (1, 1),
    "blender": (2, 80, 0),
    "category": "Object",
    "tracker_url": "https://github.com/cmd410/convinst/issues",
    "location": "View3D -> Object menu -> convinst"
}


if __name__ == '__main__':
    register()
