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
#  along with this program; if not, write to the Free Software Foundation,
#  Inc., 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301, USA.
#
# ##### END GPL LICENSE BLOCK #####

bl_info = {
    "name": "Moleculos",
    "author": "Maxim Seliverstoff",
    "version": (1, 0),
    "blender": (2, 65, 0),
    "location": "View3D > Add > Mesh > New Object",
    "description": "Adds a new Mesh Object",
    "warning": "",
    "wiki_url": "",
    "category": "Add Mesh"}


import bpy, bmesh, mathutils, bl_ui


from bpy.app.handlers import persistent

@persistent
def update_handler(self):
    
    for obj in self.objects:
        if obj.moleculos.use:
            particle = bpy.data.objects[obj.moleculos.emiter]
            Update(obj, particle)
           
bpy.app.handlers.frame_change_post.append(update_handler)

def updateMoleculos(self, context):
    obj = bpy.data.objects[context.object.name]
    global_obj = obj
    ml = obj.moleculos
    particle = bpy.data.objects[obj.moleculos.emiter]
    if ml.auto_update:
        Update(obj, particle)


class MoleculosSettings(bpy.types.PropertyGroup):
    
    use = bpy.props.BoolProperty(
                        name        = "Use Properties",
                        description = "Use Properties Description",
                        default     = False
                        )
                        
    max = bpy.props.FloatProperty(
                        name        = "Max",
                        description = "Max distance relations",
                        default     = 0.8,
                        min         = 0.0,
                        max         = 10.0,
                        soft_min    = 0.001,
                        soft_max    = 10.0,
                        step        = 5,
                        precision   = 3,
                        update      = updateMoleculos
                        )
                        
    min = bpy.props.FloatProperty(
                        name        = "Min",
                        description = "Min distance relations",
                        default     = 0.001,
                        min         = 0.0,
                        max         = 10.0,
                        soft_min    = 0.001,
                        soft_max    = 10.0,
                        step        = 5,
                        precision   = 3,
                        update      = updateMoleculos
                        )
    
    emiter = bpy.props.StringProperty(
                        name="Emiter",
                        description=""
    )
    
                        
    particle = bpy.props.StringProperty(
                        name="Target particle",
                        description=""
    )      
    
    relations_variable_use = bpy.props.BoolProperty(
                        name        = "Use relation variable width",
                        description = "Use relation variable width",
                        default     = False,
                        update      = updateMoleculos
                        )
                        
    vertex_color_use = bpy.props.BoolProperty(
                        name        = "Use vertex color",
                        description = "Use relation vertex color variable",
                        default     = False,
                        update      = updateMoleculos
                        )
                        
    auto_update = bpy.props.BoolProperty(
                        name        = "Auto Update",
                        description = "Auto Update",
                        default     = False,
                        update      = updateMoleculos
                        )                                                
    
    relations_width = bpy.props.FloatProperty(
                        name        = "Relations width",
                        description = "Relations width",
                        default     = 0.001,
                        min         = 0.0,
                        max         = 10.0,
                        soft_min    = 0.001,
                        soft_max    = 10.0,
                        step        = 5,
                        precision   = 3,
                        update      = updateMoleculos
                        )
                        
    variable_sensitivity = bpy.props.FloatProperty(
                        name        = "Sensitivity",
                        description = "Variable Sensitivity",
                        default     = 0.001,
                        min         = 0.0,
                        max         = 10.0,
                        soft_min    = 0.001,
                        soft_max    = 10.0,
                        step        = 5,
                        precision   = 3,
                        update      = updateMoleculos
                        )
                        
    color_sensitivity = bpy.props.FloatProperty(
                        name        = "Sensitivity",
                        description = "Color Sensitivity",
                        default     = 0.001,
                        min         = 0.0,
                        max         = 10.0,
                        soft_min    = 0.001,
                        soft_max    = 10.0,
                        step        = 5,
                        precision   = 3,
                        update      = updateMoleculos
                        )                                                                                     

bpy.utils.register_class(MoleculosSettings)
bpy.types.Object.moleculos = bpy.props.PointerProperty(type=MoleculosSettings)

class ManualUpdate(bpy.types.Operator):
    bl_idname = "moleculos.update"
    bl_label = "Update Current Frame"

    def execute(self, context):
        object = bpy.data.objects[context.object.name]
        emiter = bpy.data.objects[object.moleculos.emiter]
        Update(object, emiter)
        return {'FINISHED'}

bpy.utils.register_class(ManualUpdate)

class Moleculos(bpy.types.Panel):
    """Creates a Panel in the Object properties window"""
    bl_label = "Moleculos"
    bl_idname = "OBJECT_PT_moleculos"
    bl_space_type = 'PROPERTIES'
    bl_region_type = 'WINDOW'
    bl_context = "object"
    

    def draw_header(self, context):
        cont = context.object.moleculos
        self.layout.prop(cont, "use", text="")  

    def draw(self, context):
        cont = context.object.moleculos
        layout = self.layout
        
        if cont.use:
            
            split = layout.split()
            split.prop_search(cont, 'emiter',
            bpy.data,       'objects', text="Target Object")
            
            split = layout.split()
            split.prop_search(cont, 'particle',
            bpy.data,       'particles', text="Target Object")
            
            split = layout.split()
            row = layout.row()
            row.prop(cont, "max")
            row.prop(cont, "min")

            row = layout.row()
            row.prop(cont, "relations_width")

            row = layout.row()
            row.prop(cont, "relations_variable_use")
        
            if cont.relations_variable_use:
                row.prop(cont, "variable_sensitivity")
            
            split = layout.split()
            row = layout.row()
            row.prop(cont, "vertex_color_use")
                
            if cont.vertex_color_use:
                row.prop(cont, "color_sensitivity")
                
            split = layout.split()
            row = layout.row()
            row.prop(cont, "auto_update")
            
            if cont.auto_update == False:
                split = layout.split()
                split.operator("moleculos.update", icon="FILE_REFRESH")  



def swap_dump(p):
    if p[0] > p[1]:
        swap = (p[1], p[0])
    else:    
        swap = (p[0], p[1])
    return swap

    
def Update(object, particle):
    
    obj = object
    me = obj.data
        
    points = particle.particle_systems[0].particles
    point_dump = []
    v_colors = []

    max = object.moleculos.max
    min = object.moleculos.min
    w   = object.moleculos.relations_width

    bm = bmesh.new()  

       
    if not bm.loops.layers.color:
        vertexColor = bm.loops.layers.color.new("ColorForOpacity")
    else:
        vertexColor = bm.loops.layers.color["ColorForOpacity"]
          
    red = [1.0, 0.0, 0.0]

    for i, p in enumerate(points):
        for i_t, p_t in enumerate(points):
            if i != i_t:
                distance = p.location - p_t.location
                if distance.length < max and distance.length > min and swap_dump((i, i_t)) not in point_dump:
                    point_dump.append(swap_dump((i, i_t)))
                    
                    m = object.moleculos
                    d = distance.length
                    p1 = p.location
                    p2 = p_t.location

                    if m.relations_variable_use:
                        size = (m.relations_width/100)
                        max_p = m.max/100
                        c_p = 100-(d/max_p)
                        size = c_p*size
                    else:
                        size = m.relations_width
                        
                    if m.vertex_color_use:
                        c_p = 1-(distance.length/(m.max - m.min))
                        v_colors.append(mathutils.Color((c_p, c_p, c_p)))

                    vec = mathutils.Vector((0.0, 0.0, size))

                    bm.verts.new(p1-vec/2)
                    bm.verts.new(p2+vec/2)
                    bm.verts.new(p2-vec/2)
                    bm.verts.new(p1+vec/2)    
    
                    set_of_verts = set(bm.verts[i] for i in range(-4,0))
                    bm.faces.new(set_of_verts)
                    
    
    if m.vertex_color_use:
        for i, f in enumerate(bm.faces):
            for L in f.loops:
                L[vertexColor] = v_colors[i]

    
    bm.to_mesh(me)
    bm.free()  
    
    try:
        bpy.ops.object.mode_set(mode='EDIT')
        bmesh.update_edit_mesh(me)
        bpy.ops.object.mode_set(mode='OBJECT')
    except RuntimeError:
        print("RenderMode")



def register():
    bpy.utils.register_class(Moleculos)


def unregister():
    bpy.utils.unregister_class(Moleculos)


if __name__ == "__main__":
    register()