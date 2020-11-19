import bpy
from collections import deque

from .util import resolve_transform, unlink_object
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
                        instance_decay(new_obj, self.unlink)
                    )
                    continue
                unlink_object(new_obj)
                active_collection.objects.link(new_obj)

        bpy.data.objects.remove(instance, do_unlink=True)
        return {'FINISHED'}

    def invoke(self, context, event):
        wm = context.window_manager
        return wm.invoke_props_dialog(self)


def instance_decay(instance, unlink=False):
    """Generator that yields all objects from instance"""
    collection = instance.instance_collection
    processed_objects = set()

    object_remap = dict()
    for obj in collection.all_objects:
        # check if object already been copied
        if obj in processed_objects:
            continue
        processed_objects.add(obj)
        new_obj = object_remap.get(obj) or obj.copy()
        object_remap[obj] = new_obj
        
        # Unlink object data if needed
        if unlink and obj.type not in {'EMPTY'}:
            new_obj.data = obj.data.copy()
        
        if obj.parent is not None:
            new_parent = object_remap.get(obj.parent)
            if new_parent is None:
                new_parent = obj.parent.copy()
                object_remap[obj.parent] = new_parent

                yield new_parent
            new_obj.parent = new_parent
        else:
            resolve_transform(new_obj, instance)
        yield new_obj
