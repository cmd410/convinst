import bpy
from collections import deque

from ..regutil import bpy_register


@bpy_register
class DisassembleOperator(bpy.types.Operator):
    '''Split collection instance into its components'''
    bl_idname = "convinst.disassemble_operator"
    bl_label = "Disassemble instance"
    bl_options = {'UNDO'}

    unlink: bpy.props.BoolProperty(
        name='Unlink objects',
        description='New objects will have unique data'
    )

    recursive: bpy.props.BoolProperty(
        name='Recursive',
        description='If checked all nested instances will be disassembled as well'
    )

    @classmethod
    def poll(cls, context):
        return all([
            context.mode == 'OBJECT',
            context.object,
            context.object.type == 'EMPTY',
            context.object.instance_type == 'COLLECTION',
            context.object.instance_collection
        ])

    def execute(self, context):
        instance = context.object
        if instance is None:
            return {'CANCELLED'}

        active_collection = context.collection

        decaying_instances = deque()
        decaying_instances.append(instance_decay(instance, unlink=self.unlink))
        while decaying_instances:
            decay = decaying_instances.popleft()
            for new_obj in decay:
                if all([self.recursive,
                        new_obj.type == 'EMPTY',
                        new_obj.instance_type == 'COLLECTION',
                        new_obj.instance_collection]):

                    decaying_instances.append(
                        instance_decay(new_obj, self.unlink))
                    continue
                active_collection.objects.link(new_obj)

        bpy.data.objects.remove(instance, do_unlink=True)
        return {'FINISHED'}

    def invoke(self, context, event):
        wm = context.window_manager
        return wm.invoke_props_dialog(self)


def instance_decay(instance, unlink=False):
    """Generator that yields all objects from instance"""
    if instance.rotation_mode != 'QUATERNION':
        inst_rot = instance.rotation_euler.to_quaternion()
    else:
        inst_rot = instance.rotation_quaternion.copy()
    collection = instance.instance_collection
    for obj in collection.all_objects:
        new_obj = obj.copy()
        if unlink and obj.type not in {'EMPTY'}:
            new_obj.data = obj.data.copy()

        # Calculate Object position
        new_location = new_obj.location
        new_location[0] *= instance.scale[0]
        new_location[1] *= instance.scale[1]
        new_location[2] *= instance.scale[2]
        new_location.rotate(inst_rot)
        new_location += instance.location
        new_obj.location = new_location

        new_obj.rotation_mode = 'QUATERNION'
        new_obj.rotation_quaternion.rotate(inst_rot)

        new_obj.scale[0] = new_obj.scale[0] * instance.scale[0]
        new_obj.scale[1] = new_obj.scale[1] * instance.scale[1]
        new_obj.scale[2] = new_obj.scale[2] * instance.scale[2]

        for c in new_obj.users_collection:
            c.objects.unlink(new_obj)
        yield new_obj
