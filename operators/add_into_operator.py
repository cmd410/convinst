import bpy
from mathutils import Euler

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
            for c in obj.users_collection:
                c.objects.unlink(obj)
            new_location = obj.location - inst_pos
            new_location.rotate(inst_rot.inverted())
            
            obj.location = new_location
            obj.rotation_mode = 'QUATERNION'
            obj.rotation_quaternion.rotate(inst_rot.inverted())
            into_collection.objects.link(obj)

        return {'FINISHED'}
