import bpy

from ..regutil import bpy_register


@bpy_register
class DisassembleOperator(bpy.types.Operator):
    '''Split collection instance into its components'''
    bl_idname = "convinst.disassemble_operator"
    bl_label = "Disassemble instance"
    bl_options = {'UNDO'}

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
        collection = context.object.instance_collection
        for obj in collection.all_objects:
            new_obj = obj.copy()
            if obj.type not in {'EMPTY'}:
                new_obj.data = obj.data.copy()
            new_obj.location += instance.location
            for c in new_obj.users_collection:
                c.objects.unlink(new_obj)
            context.collection.objects.link(new_obj)
        bpy.data.objects.remove(instance, do_unlink=True)
        return {'FINISHED'}