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

    remove: bpy.props.BoolProperty(
        name='Remove from collection',
        default=False,
        description='If checked the object will be removed from collection'
    )

    unlink: bpy.props.BoolProperty(
        name='Unlink',
        default=False,
        description='If checked the object will have unique data'
    )

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
        original = context.scene.convinst_extract.extract_target

        if self.remove:
            target_object = original
        else:
            target_object = original.copy()
            if self.unlink:
                target_object.data = original.data.copy()

        if target_object is None:
            return {'CANCELLED'}
        instance = context.object
        inst_rot = instance.rotation_euler.to_quaternion()

        target_object.location[0] *= instance.scale[0]
        target_object.location[1] *= instance.scale[1]
        target_object.location[2] *= instance.scale[2]

        target_object.scale[0] = target_object.scale[0] * instance.scale[0]
        target_object.scale[1] = target_object.scale[1] * instance.scale[1]
        target_object.scale[2] = target_object.scale[2] * instance.scale[2]

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
        layout.prop(self, 'remove')
        layout.prop(self, 'unlink')

    def invoke(self, context, event):
        wm = context.window_manager
        return wm.invoke_props_dialog(self)