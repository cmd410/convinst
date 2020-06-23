import bpy
from mathutils import Vector


def find_origin_center(objs):
    s = Vector((0, 0, 0))
    for o in objs:
        s += o.location
    return s/len(objs)


def find_lowest_center(objs):
    s = Vector((0, 0, 0))
    lowest_z = None
    for o in objs:
        s += o.location
        ob_z = o.location.z
        bb = o.bound_box
        for vert in [bb[0], bb[3], bb[4], bb[7]]:
            if lowest_z is None:
                lowest_z = vert[2] + ob_z
            elif lowest_z > vert[2] + ob_z:
                lowest_z = vert[2] + ob_z
    s = s/len(objs)
    s[2] = lowest_z
    return s


def validate_extract_target(self, obj):
    collection = bpy.context.object.instance_collection
    return collection in obj.users_collection
