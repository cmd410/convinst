import bpy

from ..regutil import bpy_register
from .util import find_origin_center


@bpy_register
class CollapseOperator(bpy.types.Operator):
    '''Collapses selected meshes into one collection and spawns its instance here.'''  # NOQA
    bl_idname = "convinst.collapse_operator"
    bl_label = "Collapse objects into collection"
    bl_options = {'UNDO'}

    collection_name: bpy.props.StringProperty(
        name='Collection name',
        description='A name for new collection to collapse objects into'
    )

    @classmethod
    def poll(cls, context):
        return all([
            context.mode == 'OBJECT',
            len(context.selected_objects),
        ])

    def execute(self, context):
        scene = bpy.data.scenes.new(self.collection_name)
        scene.convinst_settings.is_asset = True
        scene.convinst_settings.is_edited = False

        objs = context.selected_objects

        offset = find_origin_center(objs)

        bpy.ops.collection.objects_remove_all()

        scene_coll = scene.collection
        new_coll = bpy.data.collections.new(self.collection_name)
        scene_coll.children.link(new_coll)

        for o in objs:
            new_coll.objects.link(o)
            o.location = o.location - offset

        bpy.ops.object.collection_instance_add(
            collection=new_coll.name,
            location=offset)

        return {'FINISHED'}

    def invoke(self, context, event):
        wm = context.window_manager
        return wm.invoke_props_dialog(self)
