import bpy

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
        inst_rot = context.object.rotation_euler.to_quaternion()

        collection = context.object.instance_collection
        for obj in collection.all_objects:
            new_obj = obj.copy()
            if self.unlink and obj.type not in {'EMPTY'}:
                new_obj.data = obj.data.copy()

            # Calculate Object position
            new_location = new_obj.location
            new_location.rotate(inst_rot)
            new_location += instance.location
            new_obj.location = new_location

            new_obj.rotation_mode = 'QUATERNION'
            new_obj.rotation_quaternion.rotate(inst_rot)

            for c in new_obj.users_collection:
                c.objects.unlink(new_obj)

            context.collection.objects.link(new_obj)
        bpy.data.objects.remove(instance, do_unlink=True)
        return {'FINISHED'}

    def invoke(self, context, event):
        wm = context.window_manager
        return wm.invoke_props_dialog(self)
