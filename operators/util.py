from mathutils import Vector


def find_origin_center(objs):
    s = Vector((0, 0, 0))
    for o in objs:
        s += o.location
    return s/len(objs)
