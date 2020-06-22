import bpy

from .regutil import custom_prop_group


@custom_prop_group(bpy.types.Scene, "convinst_settings")
class ConvinstSettings(bpy.types.PropertyGroup):
    is_asset: bpy.props.BoolProperty()
    is_edited: bpy.props.BoolProperty()