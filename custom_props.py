import bpy

from .regutil import custom_prop_group
from .operators.util import validate_extract_target


@custom_prop_group(bpy.types.Scene, "convinst_settings")
class ConvinstSettings(bpy.types.PropertyGroup):
    is_asset: bpy.props.BoolProperty()
    is_edited: bpy.props.BoolProperty()


# This is a hack for operators not being able to contain PointerProperty
@custom_prop_group(bpy.types.Scene, "convinst_extract")
class ExtractSettings(bpy.types.PropertyGroup):
    extract_target: bpy.props.PointerProperty(
        type=bpy.types.Object,
        name='Object',
        poll=validate_extract_target,
        description='Object to be extracted'
    )
