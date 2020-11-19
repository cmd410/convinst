import bpy
from mathutils import Euler

from .util import unlink_object
from ..regutil import bpy_register


@bpy_register
class AddIntoOperator(bpy.types.Operator):
    '''Add selected objects into last active collection instance'''
    bl_idname = "convinst.add_into_operator"
    bl_label = "Add to instance"
    bl_options = {'UNDO'}

    @classmethod
    def poll(cls, context):
        return all([
            context.mode == 'OBJECT',
            context.object is not None,
            context.object.type == 'EMPTY',
            context.object.instance_type == 'COLLECTION',
            context.object.instance_collection is not None,
            len(context.selected_objects) >= 2
        ])

    def execute(self, context):
        instance = context.object
        inst_pos = context.object.location
        inst_rot = context.object.rotation_euler.to_quaternion()

        into_collection = context.object.instance_collection
        for obj in context.selected_objects:
            if obj == instance:
                continue
            
            if obj.parent is None:
                new_location = obj.location - inst_pos
                new_location[0] /= instance.scale[0]
                new_location[1] /= instance.scale[1]
                new_location[2] /= instance.scale[2]
                new_location.rotate(inst_rot.inverted())

                obj.scale[0] = obj.scale[0] / instance.scale[0]
                obj.scale[1] = obj.scale[1] / instance.scale[1]
                obj.scale[2] = obj.scale[2] / instance.scale[2]

                obj.location = new_location
                obj.rotation_mode = 'QUATERNION'
                obj.rotation_quaternion.rotate(inst_rot.inverted())

            unlink_object(obj)
            into_collection.objects.link(obj)

        return {'FINISHED'}
