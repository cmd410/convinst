"""Utilities for registering bpy types, menus, etc with decorators"""

from bpy.props import PointerProperty
from bpy.types import Menu
from bpy.utils import register_class, unregister_class


classes = []
menus = []
props = []


def menu(cls):
    '''Adds a draw function to menu class.
    Function must take 2 args (self, context)'''
    def decorator(menu_obj):
        if issubclass(menu_obj, Menu):
            menus.append((cls, menu_obj.menu_draw))
        else:
            menus.append((cls, menu_obj))
        return menu_obj
    return decorator


def custom_prop_group(cls, id: str,):
    def decorator(prop_cls):
        props.append((cls, id, prop_cls,))
        return prop_cls
    return decorator


def bpy_register(cls):
    global classes
    classes.append(cls)
    return cls


def register():
    global classes
    global menus
    global props

    # Register classes
    for c in classes:
        register_class(c)

    # Set custom Property Groups
    for owner, prop_id, prop_cls in props:
        if prop_cls not in classes:
            register_class(prop_cls)
        setattr(owner,
                prop_id,
                PointerProperty(name=prop_id, type=prop_cls))

    # Add draw funcs to menus
    for menu, submenu in menus:
        menu.append(submenu)


def unregister():
    global classes
    global menus
    global props

    # Remove custom Property Groups
    for owner, prop_id, prop_cls in props:
        delattr(owner, prop_id)
        print(f'Deleted GroupProperty {prop_id} of {owner}')
        if prop_cls not in classes:
            unregister_class(prop_cls)

    # Remove draw funcs from menus
    for menu, func in menus:
        menu.remove(func)

    # Unregister classes
    for c in classes:
        unregister_class(c)
