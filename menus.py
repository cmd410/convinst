import bpy
from .regutil import menu, bpy_register


@bpy_register
@menu(bpy.types.VIEW3D_MT_object)
class TOPBAR_MT_convinst_menu(bpy.types.Menu):
    bl_label = "ConvInst"

    def draw(self, context):
        layout = self.layout
        layout.operator('convinst.collapse_operator')
        layout.operator('convinst.disassemble_operator')

    def menu_draw(self, context):
        self.layout.menu("TOPBAR_MT_convinst_menu")