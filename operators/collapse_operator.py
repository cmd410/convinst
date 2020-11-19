import bpy

from ..regutil import bpy_register
from .util import (
    find_origin_center,
    find_lowest_center,
    find_highest_center)


@bpy_register
class CollapseOperator(bpy.types.Operator):
    '''Collapses selected meshes into one collection and spawns its instance here.'''  # NOQA
    bl_idname = "convinst.collapse_operator"
    bl_label = "Collapse objects into instance"
    bl_options = {'UNDO'}

    collection_name: bpy.props.StringProperty(
        name='Collection name',
        description='A name for new collection to collapse objects into'
    )

    pivot: bpy.props.EnumProperty(
        name='Set pivot to',
        items=[
            ('CENTER', 'Origin center', 
            'Set pivot to origin center of objects', 1),
            ('LOWEST', 'Lowest center', 
            'Set pivot to lowest center of objects', 2),
            ('HIGHEST', 'Highest center', 
            'Set pivot to highest center of objects', 3),
            ('ACTIVE', 'Active object', 
            'Set pivot to active object', 4),
        ]
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

        if self.pivot == 'CENTER':
            offset = find_origin_center(objs)
        elif self.pivot == 'LOWEST':
            offset = find_lowest_center(objs)
        elif self.pivot == 'HIGHEST':
            offset = find_highest_center(objs)
        elif self.pivot == 'ACTIVE':
            offset = context.object.location.copy()

        bpy.ops.collection.objects_remove_all()

        scene_coll = scene.collection
        new_coll = bpy.data.collections.new(self.collection_name)
        scene_coll.children.link(new_coll)

        instance_parent = None
        for o in objs:
            new_coll.objects.link(o)
            if o.parent is None:
                o.location = o.location - offset
            elif o.parent not in objs:
                o.location, o.rotation_quaternion, o.scale = \
                    o.matrix_world.decompose()
                o.location -= offset
                instance_parent = o.parent
                o.parent = None

        current_scene = bpy.context.scene


        instance = bpy.data.objects.new(new_coll.name, None)
        instance.instance_type = 'COLLECTION'
        instance.instance_collection = new_coll
        instance.location = offset
        
        bpy.context.collection.objects.link(instance)
        # FIXME setting parent to instance messes with its location
        # need to find a way to negate it
        # instance.parent = instance_parent
        
        for obj in current_scene.collection.all_objects:
            if not obj.parent:
                continue
            if obj in objs:
                continue
            if obj.parent in objs:
                obj.parent = instance
                obj.location, obj.rotation_quaternion, obj.scale = \
                    obj.matrix_world.decompose()
                obj.location -= instance.location
                obj.rotation_quaternion.rotate(
                    instance.rotation_euler.to_quaternion()
                    )

        return {'FINISHED'}

    def invoke(self, context, event):
        wm = context.window_manager
        return wm.invoke_props_dialog(self)
