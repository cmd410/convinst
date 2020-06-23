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
        for vert in bb:
            coord = Vector(vert)
            coord[2] *= o.scale[2]
            coord.rotate(o.rotation_euler.to_quaternion())
            coord = coord[2]
            if lowest_z is None:
                lowest_z = coord + ob_z
            elif lowest_z > coord + ob_z:
                lowest_z = coord + ob_z
    s = s/len(objs)
    s[2] = lowest_z
    return s


def find_highest_center(objs):
    s = Vector((0, 0, 0))
    highest_z = None
    for o in objs:
        s += o.location
        ob_z = o.location.z
        bb = o.bound_box
        for vert in bb:
            coord = Vector(vert)
            coord[2] *= o.scale[2]
            coord.rotate(o.rotation_euler.to_quaternion())
            coord = coord[2]
            if highest_z is None:
                highest_z = coord + ob_z
            elif highest_z < coord + ob_z:
                highest_z = coord + ob_z
    s = s/len(objs)
    s[2] = highest_z
    return s


def validate_extract_target(self, obj):
    collection = bpy.context.object.instance_collection
    return collection in obj.users_collection
