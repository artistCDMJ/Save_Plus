# -*- coding: utf8 -*-
# python
# ##### BEGIN GPL LICENSE BLOCK #####
#
#  This program is free software; you can redistribute it and/or
#  modify it under the terms of the GNU General Public License
#  as published by the Free Software Foundation; either version 2
#  of the License, or (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software
#  Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
#  MA 02110-1301, USA.
#
# ##### END GPL LICENSE BLOCK #####

# <pep8 compliant>


bl_info = {
    'name': 'Save Plus',
    'author': 'artistCDMJ',
    'version': (1, 0, 0),
    'blender': (4, 2, 0),
    'location': 'File > Save+',
    'warning': '',
    'description': 'Save File and Save/Pack Images in One Operation',
    'wiki_url': '',
    'tracker_url': '',
    'category': 'Window'}








import bpy
import os
from bpy.types import Header, Menu, Panel

####### pack all images into file
class SAVE_OT_SavePlus(bpy.types.Operator):  
    """Save All Modified Images or Pack them if Unsaved before File Save"""
    bl_description = "Save all modified images or pack them if unsaved before saving the file"
    bl_idname = "save.plus"
    bl_label = "Save+"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        # Save or pack all modified images before saving the file
        for image in bpy.data.images:
            if image.is_dirty:
                if image.filepath:
                    try:
                        image.save()
                        self.report({'INFO'}, f"Saved image: {image.name}")
                    except Exception as e:
                        self.report({'ERROR'}, f"Failed to save image {image.name}: {str(e)}")
                else:
                    image.pack()
                    self.report({'INFO'}, f"Packed image: {image.name}")

        # Check if the file has been saved at least once
        if not bpy.data.filepath:
            # No filepath, so prompt user with the "Save As" dialog
            self.report({'WARNING'}, "File has not been saved yet. Using 'Save As' to set a filepath.")
            bpy.ops.wm.save_as_mainfile('INVOKE_DEFAULT')
        else:
            # Save the main file normally
            bpy.ops.wm.save_mainfile()

        return {'FINISHED'}

############ menu addition
def menu_func(self, context):
    self.layout.operator(SAVE_OT_SavePlus.bl_idname)

# Function to register the keymap
def register_keymap():
    wm = bpy.context.window_manager
    km = wm.keyconfigs.addon.keymaps.new(name='Window', space_type='EMPTY')  # More global context

    # Add a keymap entry for the 'Ctrl+Shift+S' key (or any key you prefer)
    kmi = km.keymap_items.new(SAVE_OT_SavePlus.bl_idname, 'S', 'PRESS', ctrl=True, shift=True)
    
    return km

# Unregister keymap
def unregister_keymap(km):
    wm = bpy.context.window_manager
    wm.keyconfigs.addon.keymaps.remove(km)

# Register/Unregister Classes
classes = [SAVE_OT_SavePlus]

addon_keymaps = []

def register():
    for cls in classes:
        bpy.utils.register_class(cls)
    
    # Add the operator to the File menu
    bpy.types.TOPBAR_MT_file.append(menu_func)
    
    # Register the keymap
    km = register_keymap()
    addon_keymaps.append(km)

def unregister():
    for cls in classes:
        bpy.utils.unregister_class(cls)
    
    # Remove the operator from the File menu
    bpy.types.TOPBAR_MT_file.remove(menu_func)
    
    # Unregister the keymap
    for km in addon_keymaps:
        unregister_keymap(km)
    addon_keymaps.clear()

if __name__ == "__main__":
    register()
