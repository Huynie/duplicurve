bl_info = {
    "name": "Dupli Curve",
    "description": "Make selected object into inexpensive instance array on a curve",
    "author": "Huy Chau",
    "version": (0, 1, 0),
    "blender": (2, 80, 0),
    "location": "View3D > Object",
    "warning": "",
    "wiki_url": "",
    "category": "Object"
    }


import bpy
from bpy.types import (
    AddonPreferences,
    Operator,
    Panel,
    PropertyGroup,
)

class OBJECT_OT_duplicurve(Operator): 
    
    bl_label = "Dupli Curve"
    bl_idname = "object.duplicurve"
    bl_description = "Make selected object into inexpensive instance array on a curve"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_options = {'REGISTER','UNDO'}
    
    @classmethod
    def poll(cls, context):
        return context.object.select_get() and context.object.type in ['MESH']

    def execute(self, context):

        to_dupliarray = []

        for ob in bpy.context.selected_objects:
            to_dupliarray.append(ob)

        for obj in to_dupliarray:
            #Creates a Bezier Curve 
            bpy.ops.curve.primitive_bezier_curve_add(radius=20)
            #Renames Bezier Curve
            c = bpy.context.selected_objects[0]
            c.name = "DupliCurve"
            #use deform bounds and stretch
            c.data.use_deform_bounds = True
            c.data.use_stretch = True
                
            #Creates Plane
            bpy.ops.mesh.primitive_plane_add(size=.01)
            #Renames Plane
            p = bpy.context.selected_objects[0]
            #p.name = "DupliPlane"
            #Set instances to 'Faces'
            p.instance_type = 'FACES'
                    
            #Add Array modifier
            pa = p.modifiers.new("Array", 'ARRAY')
            pa.use_relative_offset = False
            pa.use_constant_offset = True
            pa.constant_offset_displace[0] = 2.0
            pa.fit_type = 'FIT_CURVE'
            pa.curve = c
            
            #Add Curve modifier and pick created Bezier Curve from earlier
            pc = p.modifiers.new("Curve", 'CURVE')
            pc.object = c
                        
            #parents selected obj to DupliPlane
            obj.parent = p
            #Parents DupliPlane to DupliCurve
            p.parent = c
                    
            #clears location of all
            c.select_set(True)
            bpy.ops.object.select_grouped(type='CHILDREN')
            
            bpy.ops.object.select_grouped(type='CHILDREN_RECURSIVE')
            bpy.ops.object.location_clear(clear_delta=False)
                    
            #Hides selected obj
            obj.hide_set(True)
                        
        return {'FINISHED'}

def menu_func(self, context):
    self.layout.operator(OBJECT_OT_duplicurve.bl_idname)
    
def register():
    bpy.utils.register_class(OBJECT_OT_duplicurve)
    bpy.types.VIEW3D_MT_object.append(menu_func)
    
def unresgiter():
    bpy.utils.unregister_class(OBJECT_OT_duplicurve)
    bpy.types.VIEW3D_MT_object.remove(menu_func)
    

if __name__ == "__main__":
    register()