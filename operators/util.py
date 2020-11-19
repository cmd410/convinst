from collections import deque
from itertools import chain
from collections import namedtuple

import bpy
from mathutils import Vector


def find_origin_center(objs):
    locations = [i.matrix_world.to_translation() for i in objs]
    s = Vector(
        (
            sum([i[0] for i in locations]),
            sum([i[1] for i in locations]),
            sum([i[2] for i in locations])
        )
    )
    return s / len(objs)


def find_lowest_center(objs):
    s = Vector((0, 0, 0))
    lowest_z = None
    for o in objs:
        bb = o.bound_box
        location, rotation , scale = o.matrix_world.decompose()
        s += location
        ob_z = location.z
        for vert in bb:
            coord = Vector(vert)
            coord[2] *= scale[2]
            coord.rotate(rotation)
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
        bb = o.bound_box
        location, rotation , scale = o.matrix_world.decompose()
        s += location
        ob_z = location.z
        for vert in bb:
            coord = Vector(vert)
            coord[2] *= scale[2]
            coord.rotate(rotation)
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


def resolve_transform(obj, parent):
    """Transfrom object into parent's local space
    """
    if parent.rotation_mode != 'QUATERNION':
        parent_rot = parent.rotation_euler.to_quaternion()
    else:
        parent_rot = parent.rotation_quaternion.copy()
    
    # resolve location
    new_location = obj.location
    new_location[0] *= parent.scale[0]
    new_location[1] *= parent.scale[1]
    new_location[2] *= parent.scale[2]
    new_location.rotate(parent_rot)
    new_location += parent.location
    
    obj.location = new_location
    
    # rotate object as parent
    obj.rotation_mode = 'QUATERNION'
    obj.rotation_quaternion.rotate(parent_rot)
    
    # scale object as parent
    obj.scale[0] *= parent.scale[0]
    obj.scale[1] *= parent.scale[1]
    obj.scale[2] *= parent.scale[2]


def unlink_object(obj):
    for c in obj.users_collection:
        c.objects.unlink(obj)