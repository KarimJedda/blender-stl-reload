bl_info = {
    "name": "STL Watcher",
    "author": "Karim Jedda",
    "version": (0, 1),
    "blender": (2, 80, 0),
    "location": "File > Import > STL Watch",
    "description": "Watches for changes in STL files and updates them in Blender",
    "warning": "",
    "wiki_url": "",
    "category": "Import-Export",
}

import os 
import bpy
import random
import string
import logging
from bpy_extras.io_utils import ImportHelper
from bpy.props import StringProperty, FloatVectorProperty
from bpy.types import Operator


# Can be removed after dev
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
handler = logging.StreamHandler()
handler.setLevel(logging.INFO)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)


class STLReloadOperator(bpy.types.Operator):
    """Operator to reload all STL files"""
    bl_idname = "object.stl_reload"
    bl_label = "Reload STLs"

    def execute(self, context):
        logger.info("Reloading STLs")
        for obj in bpy.data.objects:
            if "stl_filepath" in obj:
                original_materials = [mat for mat in obj.data.materials]
                original_location = obj.location.copy()
                original_rotation = obj.rotation_euler.copy()
                original_scale = obj.scale.copy()

                bpy.ops.import_mesh.stl(filepath=obj["stl_filepath"])
                imported_obj = bpy.context.selected_objects[0]

                # Apply original transformations
                imported_obj.location = original_location
                imported_obj.rotation_euler = original_rotation
                imported_obj.scale = original_scale

                imported_obj.name = obj.name
                imported_obj["stl_filepath"] = obj["stl_filepath"]
                imported_obj.data.materials.clear()

                # Reassign the original materials
                for mat in original_materials:
                    imported_obj.data.materials.append(mat)

                # Delete the old object
                bpy.data.objects.remove(obj)

        return {'FINISHED'}

def update_stl_button(self, context):
    self.layout.operator(STLReloadOperator.bl_idname, text="Update STLs")

class STLToolsPanel(bpy.types.Panel):
    """Creates a Panel in the Object properties window"""
    bl_label = "STL Tools"
    bl_idname = "OBJECT_PT_stl_tools"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'STL Tools' 

    def draw(self, context):
        layout = self.layout
        layout.operator("object.stl_reload", text="Update STLs")


class STLWatcherOperator(Operator, ImportHelper):
    """STL Watcher Operator"""
    bl_idname = "import_mesh.stl_watcher"
    bl_label = "STL Watcher"
    bl_options = {'REGISTER', 'UNDO'}

    filename_ext = ".stl"

    filter_glob: StringProperty(
        default="*.stl",
        options={'HIDDEN'},
    )

    random_string = ''.join(random.choices(string.ascii_letters + string.digits, k=10))
    
    object_name: StringProperty(
        name="Object Name",
        description="Name for the imported object",
        default=random_string
    )

    object_color: FloatVectorProperty(
        name="Object Color",
        description="Color for the imported object",
        default=(0.8, 0.8, 0.8),
        min=0.0,
        max=1.0,
        subtype='COLOR',
        size=3
    )

    def execute(self, context):
        print("Selected STL file:", self.filepath)
        bpy.ops.import_mesh.stl(filepath=self.filepath)

        imported_object = bpy.context.selected_objects[0]
        imported_object["stl_filepath"] = self.filepath

        if self.object_name:
            imported_object.name = self.object_name
        else:
            imported_object.name = "ImportedSTL_" + os.path.basename(self.filepath).split('.')[0]

        unique_mat_name = "Material_" + imported_object.name
        if unique_mat_name in bpy.data.materials:
            mat = bpy.data.materials[unique_mat_name]
        else:
            mat = bpy.data.materials.new(name=unique_mat_name)

        color_with_alpha = tuple(self.object_color) + (1.0,)  # Convert to tuple and add alpha
        mat.diffuse_color = color_with_alpha

        if len(imported_object.data.materials) > 0:
            imported_object.data.materials[0] = mat  # Replace existing material
        else:
            imported_object.data.materials.append(mat)  # Add new material

        return {'FINISHED'}

def menu_func_import(self, context):
    self.layout.operator(STLWatcherOperator.bl_idname, text="STL Watcher (*.stl)")

def register():
    bpy.utils.register_class(STLToolsPanel)
    bpy.utils.register_class(STLReloadOperator)
    bpy.types.VIEW3D_MT_object.append(update_stl_button)

    bpy.utils.register_class(STLWatcherOperator)
    bpy.types.TOPBAR_MT_file_import.append(menu_func_import)

def unregister():
    bpy.utils.unregister_class(STLToolsPanel)

    bpy.utils.unregister_class(STLReloadOperator)
    bpy.types.VIEW3D_MT_object.remove(update_stl_button)

    bpy.utils.unregister_class(STLWatcherOperator)
    bpy.types.TOPBAR_MT_file_import.remove(menu_func_import)

if __name__ == "__main__":
    register()
