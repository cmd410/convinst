from collections import deque

import bpy
from mathutils import Euler

from ..regutil import bpy_register
from .util import validate_extract_target, resolve_transform, unlink_object


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

    hierachy: bpy.props.BoolProperty(
        name='Extract children',
        default=False,
        description='If checked the object\'s children will also be extracted and repareted to new object.'
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
        object_remap = dict()
        
        def get_object(original):
            obj = object_remap.get(original)
            if obj is None:
                if self.remove:
                    obj = original
                else:
                    obj = original.copy()
                    if self.unlink:
                        obj.data = original.data.copy()
                object_remap[original] = obj
            return obj

        target_object = get_object(original)
        #target_object.parent = None
        if target_object is None:
            return {'CANCELLED'}
        
        instance = context.object
        collection = instance.instance_collection
        
        resolve_transform(target_object, instance)
        if target_object.parent in [i for i in collection.all_objects]:
            target_object.parent = instance
            target_object.location, target_object.rotation_quaternion, target_object.scale = \
                target_object.matrix_world.decompose()

        if self.hierachy:
            def get_children(obj):
                return [
                    i
                    for i in collection.all_objects
                    if i.parent == obj
                ]
            search = deque([original])
            while search:
                children = get_children(search.popleft())
                for i in children:
                    new_object = get_object(i)
                    new_object.parent = get_object(i.parent)
                search.extend(children)

        # Relink objects
        for i in object_remap.values():
            unlink_object(i)
            context.collection.objects.link(i)
        
        # Cleanup target variable
        context.scene.convinst_extract.extract_target = None
        return {'FINISHED'}

    def draw(self, context):
        layout = self.layout
        layout.prop(context.scene.convinst_extract, 'extract_target')
        layout.prop(self, 'remove')
        layout.prop(self, 'unlink')
        layout.prop(self, 'hierachy')

    def invoke(self, context, event):
        wm = context.window_manager
        return wm.invoke_props_dialog(self)