import bpy
from mathutils import Euler

from ..regutil import bpy_register
from .util import validate_extract_target

@bpy_register
class ExtractOperator(bpy.types.Operator):
    '''Extract single object from collection instance'''
    bl_idname = "convinst.extract_operator"
    bl_label = "Extract from instance"
    bl_options = {'UNDO'}

    @classmethod
    def poll(cls, context):
        return all([
            context.mode == 'OBJECT',
            context.object is not None,
            context.object.type == 'EMPTY',
            context.object.instance_type == 'COLLECTION',
            context.object.instance_collection is not None
        ])

    def execute(self, context):
        target_object = context.scene.convinst_extract.extract_target
        if target_object is None:
            return {'CANCELLED'}
        instance = context.object
        inst_rot = instance.rotation_euler.to_quaternion()

        target_object.location.rotate(inst_rot)
        target_object.location += instance.location
        target_object.rotation_mode = 'QUATERNION'
        target_object.rotation_quaternion.rotate(inst_rot)

        for c in target_object.users_collection:
            c.objects.unlink(target_object)
        
        context.collection.objects.link(target_object)
        context.scene.convinst_extract.extract_target = None
        return {'FINISHED'}

    def draw(self, context):
        layout = self.layout
        layout.prop(context.scene.convinst_extract, 'extract_target')

    def invoke(self, context, event):
        wm = context.window_manager
        return wm.invoke_props_dialog(self)