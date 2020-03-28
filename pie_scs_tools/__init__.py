bl_info = {
    "name": "Pie SCS Blender Tools",
    "description": "Pie Menu to put all panels together",
    "author": "AmirMahdavi (AM)",
    "version": (0, 0, 2),
    "blender": (2, 81, 0),
    "warning": "Alpha",
    "location": "3D View",
    "tracker_url": "https://forum.scssoft.com/viewtopic.php?f=162&t=282487",
    "support": "COMMUNITY",
    "category": "Interface"}

import bpy
from bpy.types import Menu, Panel, AddonPreferences
from bpy.props import EnumProperty
from io_scs_tools.consts import Icons
from io_scs_tools.internals.icons import get_icon
from io_scs_tools.utils import get_scs_globals as scs_globals


######     Addon Preferences    ######

class PIE_PT_SCSPreferences(AddonPreferences):
    bl_idname = __name__

    def draw(self, context):
        layout = self.layout
        layout.label(text="Hotkey - 'Shif+Ctrl+Alt+A'       For change it, go to Keymap, search SCS Blender Tools", icon="INFO")


icon = Icons.Types

######     Main Pie    ######

class PIE_MT_PieSCS(Menu):
    bl_idname = "PIE_MT_PieSCS"
    bl_label = "SCS Blender Tools"

    def draw(self, context):
        layout = self.layout
        pie = layout.menu_pie()

        # 4 - Left
        pie.popover("SCS_TOOLS_PT_Object", text=" Object                     ", icon="OBJECT_DATA")
        # 6 - Right
        pie.popover("SCS_TOOLS_PT_Material", text="Material                 ", icon="MATERIAL")
        # 2 - Down
        pie.operator('scene.scs_tools_export_by_scope', text="Export", icon="EXPORT")
        # 8 - Up
        pie.operator("scs_tools.import_pim", text="Import PIM", icon="IMPORT")
        # 7 - Left Up
        pie.operator("converter_pix_wrapper.import", text="Import PMD", icon="SORT_ASC")
        # 9 - Right Up
        pie.menu("PIE_MT_SCSAddObject", icon_value=get_icon(icon.loc))
        # 1 - Left Down
        pie.operator("scene.scs_tools_run_packing", text="Pack MOD", icon="PACKAGE")
        # 3 - Right Down
        pie.operator("object.scs_tools_relocate_scs_roots", text="Relocate SCS Roots", icon="CON_LOCLIKE")


        pie.separator()
        pie.separator()
        other = pie.column()
        other.scale_x = 1.05
        other.scale_y = 1.3
        gap = other.column()
        gap.separator()
        gap.scale_y = 3.8

        SnapIcon = "SNAP_ON" if scs_globals().use_alternative_bases else "SNAP_OFF"

        other_menu = other.box().column()
        other_menu.menu("PIE_MT_SCSExportScope", icon="SEQ_CHROMA_SCOPE")
        other_menu.popover("PIE_PT_SCSMisc", text="Misc", icon="LAYER_ACTIVE")
        row = other_menu.row(align=True)
        row.popover("SCS_TOOLS_PT_PathSettingsPresets", text="", icon="PRESET")
        row.operator("scene.scs_tools_select_project_path", text="Base Path", icon="FILEBROWSER")
        row.prop(scs_globals(), "use_alternative_bases", icon=SnapIcon, icon_only=True)
        other_menu.operator('scene.scs_tools_select_dir_inside_base', text="DefaultExportPath", icon="FILEBROWSER").type = "DefaultExportPath"
        other_menu.prop(scs_globals(), "base_paint_color", icon_only=True)


        pie.separator()
        pie.separator()
        pie.separator()
        pie.separator()
        other = pie.column()
        other.scale_x = 1.14
        other.scale_y = 1.3
        gap = other.column()
        gap.separator()
        gap.scale_y = 25.9

        other_menu = other.box().column()
        other_menu.popover("PIE_PT_SCSVertexPaint", text="Vertex Paint", icon="VPAINT_HLT")
        other_menu.popover("SCS_TOOLS_PT_LampSwitcher", text="Lamp Switcher", icon="LIGHT")
        other_menu.popover("SCS_TOOLS_PT_LampTool", text="Lamp Tool", icon="OUTLINER_OB_LIGHT")
        other_menu.popover("SCS_TOOLS_PT_ConvexBlDefs", text="Convex", icon_value=get_icon(icon.loc_collider_convex))
        other_menu.prop(scs_globals(), "use_scs_lighting", text="SCS Lighting")


        pie.separator()
        pie.separator()
        pie.separator()
        pie.separator()
        pie.separator()
        pie.separator()
        other = pie.column()
        other.scale_x = 1.06
        other.scale_y = 1.3
        gap = other.column()
        gap.separator()
        gap.scale_y = 25.9

        other_menu = other.box().column()
        other_menu.popover("SCS_TOOLS_PT_ExportPanel", text="Export", icon="EXPORT")
        other_menu.popover("SCS_TOOLS_PT_ConversionHelper", text="Converter", icon="PACKAGE")
        other_menu.popover("SCS_TOOLS_PT_Visibility", text="Visibility", icon="HIDE_OFF")
        other_menu.popover("SCS_TOOLS_PT_DisplayMethods", text="Display Methods", icon_value=get_icon(icon.loc))
        other_menu.prop(scs_globals(), "show_preview_models", text="Preview Models")



######     Panel & Menu    ######

class PIE_PT_SCSVertexPaint(Panel):
    bl_space_type = "TEXT_EDITOR"
    bl_region_type = "UI"
    bl_category = "SCS TEMP"
    bl_label = "SCS Vertex Paint"

    @classmethod
    def poll(cls, context):
        return context.vertex_paint_object

    def draw(self, context):
        if not self.poll(context):
            self.layout.label(text="Not in 'Vertex Paint' mode!", icon="INFO")
            return

        layout = self.layout
        col = layout.column(align=True)
        row = col.row(align=True)

        ups = context.tool_settings.unified_paint_settings
        ptr = ups if ups.use_unified_color else context.tool_settings.vertex_paint.brush

        row.operator("paint.vertex_color_set", text="Set", icon="BRUSH_DATA")
        row.prop(ptr, "color", icon_only=True)
        col.operator("paint.vertex_color_dirt", text="Dirty Color")
        col.separator()
        col.operator("mesh.scs_tools_wrap_vertex_colors", text="Wrap Selected").wrap_type = "selected"
        col.operator("mesh.scs_tools_wrap_vertex_colors", text="Wrap All").wrap_type = "all"
        col.separator()
        col.operator("mesh.scs_tools_print_vertex_colors_stats")


class PIE_PT_SCSMisc(Panel):
    bl_space_type = "TEXT_EDITOR"
    bl_region_type = "UI"
    bl_category = "SCS TEMP"
    bl_label = "Misc"

    def draw(self, context):
        layout = self.layout
        col = layout.column(align=True)

        col.label(text="Materials", icon="MATERIAL")
        row = col.row(align=True)
        row.operator("material.scs_tools_reload_materials", text="Reload", icon="FILE_REFRESH")
        row.operator("material.scs_tools_merge_materials", text="Merge", icon="AUTOMERGE_ON")
        col.operator("mesh.scs_tools_start_vcoloring", text="VColoring", icon="GROUP_VCOL")
        col.label(text="Objects", icon="OBJECT_DATA")
        col.operator("object.scs_tools_fix_model_locator_hookups", text="Fix Hookups Names", icon_value=get_icon(icon.loc))
        col.operator("object.scs_tools_search_degenerated_polys", text="Check Geometry", icon="ZOOM_SELECTED")


class PIE_MT_SCSAddObject(Menu):
    bl_idname = "PIE_MT_SCSAddObject"
    bl_label = "Add SCS Object"
  
    def draw(self, context):
        layout = self.layout
        col = layout.column(align=True)

        col.operator("object.scs_tools_create_scs_root", text="Root Locator", icon_value=get_icon(icon.scs_root))
        col.operator("object.scs_tools_create_scs_root", text="Root Locator +", icon_value=get_icon(icon.scs_root)).use_dialog = True
        col.separator()
        col.operator("object.scs_tools_add_object", text="Model Locator", icon_value=get_icon(icon.loc_model)).new_object_type = "Model Locator"
        col.operator("object.scs_tools_add_object", text="Prefab Locator", icon_value=get_icon(icon.loc_prefab)).new_object_type = "Prefab Locator"
        col.operator("object.scs_tools_add_object", text="Collision Locator", icon_value=get_icon(icon.loc_collider)).new_object_type = "Collision Locator"



class PIE_MT_SCSExportScope(Menu):
    bl_idname = "PIE_MT_SCSExportScope"
    bl_label = "Export Scope"
    
    def draw(self, context):
        layout = self.layout

        layout.prop(scs_globals(), "export_scope", expand=True)



classes = (
    PIE_PT_SCSPreferences,
    PIE_MT_PieSCS,
    PIE_PT_SCSVertexPaint,
    PIE_PT_SCSMisc,
    PIE_MT_SCSAddObject,
    PIE_MT_SCSExportScope,
    )

addon_keymaps = []


def register():
    for cls in classes:
        bpy.utils.register_class(cls)

    wm = bpy.context.window_manager
    if wm.keyconfigs.addon:
        km = wm.keyconfigs.addon.keymaps.new(name="3D View", space_type="VIEW_3D")
        kmi = km.keymap_items.new("wm.call_menu_pie", "A", "PRESS", shift=True, ctrl=True, alt=True)
        kmi.properties.name = "PIE_MT_PieSCS"
        addon_keymaps.append((km, kmi))

def unregister():
    for cls in classes:
        bpy.utils.unregister_class(cls)

        for km, kmi in addon_keymaps:
            km.keymap_items.remove(kmi)
        addon_keymaps.clear()


if __name__ == "__main__":
    register()
