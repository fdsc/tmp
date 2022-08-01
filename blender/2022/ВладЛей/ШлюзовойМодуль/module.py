# Использование итоговой иллюстрации не допускается
# Автор илллюстрации https://author.today/u/alrtat

import sys
import os

import bpy
import bmesh
from math import *
from mathutils import *
from random import *


Samples   = 1024
Prefilter = 'ACCURATE'
CountOfCarbage = 186*2
use_denoising = True

SimpleRendering = True

if SimpleRendering:
	Samples   = 64
	Prefilter = 'FAST'
	# Prefilter = 'NONE'
	CountOfCarbage = 64
	use_denoising  = False


blend_dir = os.path.dirname("/Arcs/Repos/tmp/blender/2022/ОктавияКолотилина/")
if blend_dir not in sys.path:
   sys.path.append(blend_dir)


import MaterialProperties
global MatProps

MatProps = MaterialProperties.MaterialProperties()


MatProps.DeleteAllObjects()


def addTorus(name, loc0, R, minor_radius, major_segments=0, minor_segments=12):
	
	if major_segments <= 0:
		major_segments = int(R/minor_radius)

	if major_segments < int(R):
		major_segments = int(R)

	if major_segments < 16:
		major_segments = 16

	bpy.ops.mesh.primitive_torus_add(
		location       = (loc0[0], loc0[1], 0),
		major_radius   = R,
		minor_radius   = minor_radius,
		major_segments = major_segments,
		minor_segments = minor_segments
	)

	nm = name + ".torus." + str(len(bpy.data.objects))
	# bpy.data.objects[0].name = nm
	bpy.context.active_object.name = nm
	
	print("!!!" + bpy.context.active_object.name)

	return bpy.context.active_object


#Carbage = 'Ремни'
# Перед созданием коллекции убираем выделение с объектов, чтобы они не добавились по ошибке
#bpy.ops.object.select_all(action='DESELECT')
#CarbageCollection = bpy.data.collections.new(Carbage)
#bpy.context.scene.collection.children.link(CarbageCollection)

#view_layer        = bpy.context.view_layer
#CarbageCollection = bpy.data.collections[0]
# bpy.data.scenes[0].collection.children.link(CarbageCollection)
# view_layer.active_layer_collection.collection.objects.link(CarbageCollection)

# with bpy.context.temp_override(**override2):
#	bpy.ops.object.collection_remove()


# Создаём плоскость, параллельную плоскости XY
def newVert():
	
	vertices = []

	# Посчитаем, что шлюз будет 2.75 метра высотой внутри. Снаружи +0,5 метра сверху
	# Ширина шлюза снаружи 2 метра +0,5 по бокам
	# Таким образом у нас 4 плоскости: 0, 1.083, 2.167, 3.25
	# Вертикальные плоскости: 0, 1, 2, 3

	# Масштабный коэффициент
	k = 1

	def addVerts(hs, hp, vs, vp, k):
		# Наружняя стена
		for i in range(len(hs)):
			h = hs[i]
			for v in vs[i]:
				vertices.append(( v*k+vp,  0, h*k+hp))


	def getHV(H, W, S):
		hs = []
		for i in range(4):
			hs.append(i * H/3 + S)

		vs  = []
		vsi = [[1, 2], [0, 3], [0, 3], [1, 2]]
		for i in range(4):
			vs.append((  vsi[i][0] * W / 3 + S, vsi[i][1] * W / 3 + S  ))

		return hs, vs

	H = 3.5
	W = 3.0
	S = 0.5
	
	[hs, vs] = getHV(H, W, 0.0)
	addVerts(hs, 0, vs, 0, k)
	
	# Внутренняя стена
	# Горизонтальные плоскости: 0+0.5, 0.917+0.5, 1.833+0.5, 2.75+0.5
	# Вертикальные: 0+0.5, 0.667+0.5, 1.333+0.5, 2+0.5

	[hs, vs] = getHV(H-S*2, W-S*2, S)
	addVerts(hs, 0.0, vs, 0.0, k)

	return vertices

def newEdjes():

	faces = [
				(0, 1, 3, 3+8, 1+8, 0+8),
				(3, 5, 7, 7+8, 5+8, 3+8),
				(7, 6, 4, 4+8, 6+8, 7+8),
				(4, 2, 0, 0+8, 2+8, 4+8)
			]

	edjes = []

	eds = [0, 1, 3, 5, 7, 6, 4, 2, 0]
	for i in range(  len(eds)-1  ):
		edjes.append((  eds[i]+0, eds[i+1]+0  ))
		edjes.append((  eds[i]+8, eds[i+1]+8  ))

	return faces, edjes

def СоздатьКоридор():
	vertices       = newVert()
	[faces, edjes] = newEdjes()

	name = 'Коридор'
	[object, mesh] = MatProps.createObject(
		name=name, vertices=vertices, faces=faces, edjes=edjes, loc0=(0, 0, 0)
		)

	bpy.ops.object.mode_set(mode='EDIT')

	bpy.ops.mesh.extrude_context_move(MESH_OT_extrude_context={"use_normal_flip":False, "use_dissolve_ortho_edges":False, "mirror":False}, TRANSFORM_OT_translate={"value":(0, 0, -12.0), "orient_axis_ortho":'X', "orient_type":'NORMAL', "orient_matrix":((-1, 0, 0), (-0, -0, -1), (0, -1, 0)), "orient_matrix_type":'NORMAL', "constraint_axis":(False, False, True), "mirror":False, "use_proportional_edit":False, "proportional_edit_falloff":'SMOOTH', "proportional_size":1, "use_proportional_connected":False, "use_proportional_projected":False, "snap":False, "snap_target":'CLOSEST', "snap_point":(0, 0, 0), "snap_align":False, "snap_normal":(0, 0, 0), "gpencil_strokes":False, "cursor_transform":False, "texture_space":False, "remove_on_cancel":False, "view2d_edge_pan":False, "release_confirm":True, "use_accurate":False, "use_automerge_and_split":False})
	
	bpy.ops.object.mode_set(mode='OBJECT')
	
	return object, mesh, vertices, edjes, faces

def СоздатьДвери(Коридор):
	[_, _, vert, _, _] = Коридор
	
	# Правая дверь
	v  = vert[8:]
	x  = (  v[4][0] + v[5][0]  ) / 2
	dx = (v[5][0] - v[4][0]) * 0.1
	x -= dx
	z  = v[4][2]
	v.append((x, 0, z))

	z  = v[3][2]
	v.append((x, 0, z + dx))
	
	#for i in range(len(v)):
	#	v[i] = (v[i][0], v[i][1]+0.025, v[i][2])

	f = [(1, 3, 5, 7, 8, 9)]

	name = 'ДверьПравая'
	[object, mesh] = MatProps.createObject(
		name=name, vertices=v, faces=f, edjes=[], loc0=(0, 0, 0)
		)


	bpy.ops.object.editmode_toggle()

	bpy.ops.mesh.extrude_context_move(MESH_OT_extrude_context={"use_normal_flip":False, "use_dissolve_ortho_edges":False, "mirror":False}, TRANSFORM_OT_translate={"value":(0, 0, -0.2), "orient_axis_ortho":'X', "orient_type":'NORMAL', "orient_matrix":((-1, 0, 0), (-0, -0, -1), (0, -1, 0)), "orient_matrix_type":'NORMAL', "constraint_axis":(False, False, True), "mirror":False, "use_proportional_edit":False, "proportional_edit_falloff":'SMOOTH', "proportional_size":1, "use_proportional_connected":False, "use_proportional_projected":False, "snap":False, "snap_target":'CLOSEST', "snap_point":(0, 0, 0), "snap_align":False, "snap_normal":(0, 0, 0), "gpencil_strokes":False, "cursor_transform":False, "texture_space":False, "remove_on_cancel":False, "view2d_edge_pan":False, "release_confirm":True, "use_accurate":False, "use_automerge_and_split":False})
	
	bpy.ops.object.mode_set(mode='OBJECT')
	
	
	# Левая дверь
	v  = vert[8:]
	x  = (  v[4][0] + v[5][0]  ) / 2
	dx = (v[5][0] - v[4][0]) * 0.1
	x -= dx
	z  = v[4][2]
	v.append((x, 0, z))

	z  = v[3][2]
	v.append((x, 0, z + dx))
	
	f = [(0, 1, 9, 8, 7, 6, 4, 2)]

	name = 'ДверьЛевая'
	[object, mesh] = MatProps.createObject(
		name=name, vertices=v, faces=f, edjes=[], loc0=(0, 0, 0)
		)

	bpy.ops.object.editmode_toggle()

	bpy.ops.mesh.extrude_context_move(MESH_OT_extrude_context={"use_normal_flip":False, "use_dissolve_ortho_edges":False, "mirror":False}, TRANSFORM_OT_translate={"value":(0, 0, -0.2), "orient_axis_ortho":'X', "orient_type":'NORMAL', "orient_matrix":((-1, 0, 0), (-0, -0, -1), (0, -1, 0)), "orient_matrix_type":'NORMAL', "constraint_axis":(False, False, True), "mirror":False, "use_proportional_edit":False, "proportional_edit_falloff":'SMOOTH', "proportional_size":1, "use_proportional_connected":False, "use_proportional_projected":False, "snap":False, "snap_target":'CLOSEST', "snap_point":(0, 0, 0), "snap_align":False, "snap_normal":(0, 0, 0), "gpencil_strokes":False, "cursor_transform":False, "texture_space":False, "remove_on_cancel":False, "view2d_edge_pan":False, "release_confirm":True, "use_accurate":False, "use_automerge_and_split":False})
	
	bpy.ops.object.mode_set(mode='OBJECT')


Коридор = СоздатьКоридор()
СоздатьДвери(Коридор)


