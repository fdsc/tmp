import bpy
import bmesh

# Создаём куб


#Define vertices, faces, edges
verts = [(0,0,0),(0,5,0),(5,5,0),(5,0,0),(0,0,5),(0,5,5),(5,5,5),(5,0,5)]
faces = [(0,1,2,3), (4,5,6,7), (0,4,5,1), (1,5,6,2), (2,6,7,3), (3,7,4,0)]

name = "Cube"

#Define mesh and object
mesh = bpy.data.meshes.new(name)
object = bpy.data.objects.new(name, mesh)

#Set location and scene of object
object.location = (0, 0, 0) # bpy.context.scene.cursor_location
#bpy.context.scene.objects.link(object)
view_layer = bpy.context.view_layer
view_layer.active_layer_collection.collection.objects.link(object)

#Create mesh
mesh.from_pydata(verts,[],faces)
mesh.update(calc_edges=True)

bpy.data.objects['Cube'].select_set(True)
object.select_set(True)
view_layer.objects.active = object

#Enter edit mode to extrude
bpy.ops.object.mode_set(mode='EDIT')
bpy.ops.mesh.normals_make_consistent(inside=False)

bm = bmesh.from_edit_mesh(mesh)
for face in bm.faces:
    face.select = False
bm.faces[1].select = True

# Show the updates in the viewport
bmesh.update_edit_mesh(mesh, destructive=True)

#bpy.ops.mesh.extrude_faces_move(MESH_OT_extrude_faces_indiv={"mirror":False}, TRANSFORM_OT_shrink_fatten={"value":-5, "use_even_offset":True, "mirror":False, "proportional":'DISABLED', "proportional_edit_falloff":'SMOOTH', "proportional_size":1, "snap":False, "snap_target":'CLOSEST', "snap_point":(0, 0, 0), "snap_align":False, "snap_normal":(0, 0, 0), "release_confirm":False})

# bpy.ops.object.mode_set(mode='OBJECT')
