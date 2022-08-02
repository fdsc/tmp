# Использование итоговой иллюстрации не допускается (используется в книге, указанной выше)
# Автор илллюстрации https://author.today/u/alrtat
# Иллюстрация для https://author.today/reader/166459/1360984 (Влад Лей, "Один", глава 5)

import sys
import os

import bpy
import bmesh
from math import *
from mathutils import *
from random import *


Samples   = 1024
Prefilter = 'ACCURATE'
use_denoising = True

SimpleRendering = False

if SimpleRendering:
	Samples   = 6
	Prefilter = 'FAST'
	# Prefilter = 'NONE'
	use_denoising  = False


blend_dir = os.path.dirname("/Arcs/Repos/tmp/blender/2022/ОктавияКолотилина/")
if blend_dir not in sys.path:
   sys.path.append(blend_dir)


import MaterialProperties
global MatProps

MatProps = MaterialProperties.MaterialProperties()


MatProps.DeleteAllObjects()


class GlobalProperties:
	ВысотаМодуля = 3.5
	ШиринаМодуля = 3.0
	ТолщинаСтенокМодуля   = 0.35
	ПоложениеТочкиЗахвата = 8

GP = GlobalProperties()

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

	H = GP.ВысотаМодуля
	W = GP.ШиринаМодуля
	S = GP.ТолщинаСтенокМодуля
	
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
	
	МатериалКоридора = MatProps.addMaterial(BaseColor=(0.5, 0.5, 0.5), Roughness=1, name="МатериалКоридора",  obj=object)

	
	# Свет в коридоре
	H = GP.ВысотаМодуля
	W = GP.ШиринаМодуля
	T = GP.ТолщинаСтенокМодуля
	R = 0.08

	ВысотаПотолка = H - T

	# bpy.data.objects['Светильник']
	lamp_data = bpy.data.lights.new(name="Светильник", type='POINT')

	lamp_data.energy             = 1e4
	lamp_data.shadow_soft_size   = R		# Размер источника света
	lamp_data.cycles.max_bounces = 8
	lamp_data.color			     = (1, 1, 1)

	lamp_object = bpy.data.objects.new(name="Светильник", object_data=lamp_data)
	bpy.context.collection.objects.link(lamp_object)

	lamp_object.location = (W/2, 6, ВысотаПотолка - R)

	
	return object, mesh, vertices, edjes, faces

def СоздатьОкно(object, location, rotation, size, cleanup=True):
	"""
		size		- 	Ширина и высота окна, глубина окна, радиусы скруглений
	"""
	
	view_layer = bpy.context.view_layer
	bpy.ops.object.select_all(action="DESELECT")

	R = size[3]
	
	objs = []

	for sx in range(2):
		for sy in range(2):
	
			if sx == 0:
				sxm = +1
			else:
				sxm = -1
			if sy == 0:
				sym = +1
			else:
				sym = -1
	
			loc = (location[0] + size[0] * sx + R/2*sxm, location[1] + size[2]/2, location[2] - size[1] * sy - R/2*sym)

			bpy.ops.mesh.primitive_cylinder_add(enter_editmode=False, align='WORLD', location=loc, scale=(1, 1, 1), depth = size[2], radius = R, rotation=rotation)

			sub = view_layer.objects.active
			sub.name = 'ОкноПравойДвериСкругления'
			objs.append(sub)
			view_layer.objects.active = object
			bpy.ops.object.modifier_add(type='BOOLEAN')
			object.modifiers["Boolean"].operation  = "DIFFERENCE"
			object.modifiers["Boolean"].object     = sub # bpy.data.objects[sub.name_full]
			bpy.ops.object.modifier_apply(modifier = "Boolean")
			
			bpy.ops.object.select_all(action="DESELECT")

			# МатериалДверей = MatProps.addMaterial(BaseColor=(1, 0, 0), Roughness=1, name="AAABBB",  obj=sub)

			
	# Первый куб
	loc = (location[0]-R/2, location[1], location[2] - R/2)

	# sz = (size[0]+R, size[2], -size[1])
	sz = (size[0]+R, 0.25, -size[1]+R)
	[sub, _] = MatProps.createCube("ОкноПравойДвериКуб.1", sz, loc)
	objs.append(sub)
	
	view_layer.objects.active = object
	bpy.ops.object.modifier_add(type='BOOLEAN')
	object.modifiers["Boolean"].operation  = "DIFFERENCE"
	object.modifiers["Boolean"].object     = sub # bpy.data.objects[sub.name_full]
	bpy.ops.object.modifier_apply(modifier = "Boolean")

	bpy.ops.object.select_all(action="DESELECT")


	# Второй куб
	loc = (location[0]+R/2, location[1], location[2] + R/2)

	sz = (size[0]-R, size[2], -size[1]-R)
	[sub, _] = MatProps.createCube("ОкноПравойДвериКуб.2", sz, loc)
	objs.append(sub)
	
	view_layer.objects.active = object
	bpy.ops.object.modifier_add(type='BOOLEAN')
	object.modifiers["Boolean"].operation  = "DIFFERENCE"
	object.modifiers["Boolean"].object     = sub # bpy.data.objects[sub.name_full]
	bpy.ops.object.modifier_apply(modifier = "Boolean")
	
	bpy.ops.object.select_all(action="DESELECT")
	
	united = objs[0]
	for obj in objs:
		if united == obj:
			continue

		view_layer.objects.active = united
		bpy.ops.object.modifier_add(type='BOOLEAN')
		united.modifiers["Boolean"].operation  = "UNION"
		united.modifiers["Boolean"].object     = obj # bpy.data.objects[sub.name_full]
		bpy.ops.object.modifier_apply(modifier = "Boolean")

		bpy.ops.object.select_all(action="DESELECT")
		bpy.data.objects.remove(obj)

	united.name = "ОкноПравойДвери"
	
	МатериалОкна = MatProps.addMaterial(BaseColor=(0.0, 0.0, 0.0), Roughness=0.0, Specular=1, name="МатериалОкна",  obj=united)
	
	toRemove = МатериалОкна.node_tree.nodes['Principled BSDF']
	МатериалОкна.node_tree.nodes.remove(toRemove)
	matOutput = МатериалОкна.node_tree.nodes['Material Output']
	
	texImage_node = МатериалОкна.node_tree.nodes.new('ShaderNodeBsdfGlass')

    МатериалОкна.node_tree.links.new(texImage_node.outputs[0], matOutput.inputs[0])
	
	# bpy.data.materials['PlanetMaterial.МатериалТочкиЗахвата'].node_tree.nodes['Checker Texture']
	inp = МатериалОкна.node_tree.nodes['Glass BSDF'].inputs
	inp['Color']    .default_value = (1, 1, 1, 1)
	inp['Roughness'].default_value = 0
	inp['IOR']      .default_value = 1.45
	МатериалОкна.node_tree.nodes['Glass BSDF'].distribution = "SHARP"

	if cleanup:
		# for obj in objs:
		#	bpy.data.objects.remove(obj)
		bpy.data.objects.remove(united)


def СоздатьДвери(Коридор):
	[_, _, vert, _, _] = Коридор
	
	Уплотнение   = 0.025
	Зазор        = 0.001
	Смещение     = 0.01
	ТолщинаДвери = 0.25
	
	GP.Смещение  = Смещение
	
	# Правая дверь
	v  = vert[8:]
	x  = (  v[4][0] + v[5][0]  ) / 2
	dx = (v[5][0] - v[4][0]) * 0.1
	x -= dx
	z  = v[4][2]
	v.append((x+Уплотнение, 0, z))

	z  = v[3][2]
	v.append((x+Уплотнение, 0, z))

	# Делаем зазор между дверью и корпусом
	vi   = v[1]
	v[1] = (vi[0], vi[1], vi[2]+Зазор)

	vi   = v[7]
	v[7] = (vi[0], vi[1], vi[2]-Зазор)
	
	for i in [3, 5]:
		vi   = v[i]
		v[i] = (vi[0]-Зазор, vi[1], vi[2])


	f = [(1, 3, 5, 7, 8, 9)]

	name = 'ДверьПравая'
	[object, mesh] = MatProps.createObject(
		name=name, vertices=v, faces=f, edjes=[], loc0=(0, +Смещение, 0)
		)
	
	vr = v

	bpy.ops.object.editmode_toggle()

	bpy.ops.mesh.extrude_context_move(MESH_OT_extrude_context={"use_normal_flip":False, "use_dissolve_ortho_edges":False, "mirror":False}, TRANSFORM_OT_translate={"value":(0, 0, -ТолщинаДвери), "orient_axis_ortho":'X', "orient_type":'NORMAL', "orient_matrix":((-1, 0, 0), (-0, -0, -1), (0, -1, 0)), "orient_matrix_type":'NORMAL', "constraint_axis":(False, False, True), "mirror":False, "use_proportional_edit":False, "proportional_edit_falloff":'SMOOTH', "proportional_size":1, "use_proportional_connected":False, "use_proportional_projected":False, "snap":False, "snap_target":'CLOSEST', "snap_point":(0, 0, 0), "snap_align":False, "snap_normal":(0, 0, 0), "gpencil_strokes":False, "cursor_transform":False, "texture_space":False, "remove_on_cancel":False, "view2d_edge_pan":False, "release_confirm":True, "use_accurate":False, "use_automerge_and_split":False})
	
	bpy.ops.object.mode_set(mode='OBJECT')
	bpy.ops.object.select_all(action="DESELECT")
	
	# Делаем окно в правой двери
	x  = vr[8][0]
	dx = (vr[5][0]-vr[8][0]) / 4
	x += dx
	
	СоздатьОкно(object, (x, +Смещение, vr[8][2]), (90*pi/180, 0, 0), (dx*2, dx*2, ТолщинаДвери, 0.1), cleanup=False)


	МатериалДверей = MatProps.addMaterial(BaseColor=(0.5, 0.5, 0.5), Roughness=1, name="МатериалДверей",  obj=object)

	GP.ПраваяДверь = [object, mesh, МатериалДверей]

	
	# Левая дверь
	v  = vert[8:]
	x  = (  v[4][0] + v[5][0]  ) / 2
	dx = (v[5][0] - v[4][0]) * 0.1
	x -= dx
	z  = v[4][2]
	v.append((x, 0, z))

	z  = v[3][2]
	v.append((x, 0, z))
		
	v[1] = (v[1][0]-Уплотнение, v[1][1], v[1][2])
	v[7] = (v[7][0]-Уплотнение, v[7][1], v[7][2])
	
	# Делаем зазор между дверью и корпусом
	vi   = v[0]
	v[0] = (vi[0], vi[1], vi[2]+Зазор)
	vi   = v[1]
	v[1] = (vi[0], vi[1], vi[2]+Зазор)

	vi   = v[6]
	v[6] = (vi[0], vi[1], vi[2]-Зазор)
	vi   = v[7]
	v[7] = (vi[0], vi[1], vi[2]-Зазор)
	
	vi   = v[2]
	v[2] = (vi[0]+Зазор, vi[1], vi[2])
	vi   = v[4]
	v[4] = (vi[0]+Зазор, vi[1], vi[2])

	
	f = [(0, 1, 9, 8, 7, 6, 4, 2)]

	name = 'ДверьЛевая'
	[object, mesh] = MatProps.createObject(
		name=name, vertices=v, faces=f, edjes=[], loc0=(0, +Смещение, 0)
		)

	vl = v
	
	bpy.ops.object.editmode_toggle()

	bpy.ops.mesh.extrude_context_move(MESH_OT_extrude_context={"use_normal_flip":False, "use_dissolve_ortho_edges":False, "mirror":False}, TRANSFORM_OT_translate={"value":(0, 0, -ТолщинаДвери), "orient_axis_ortho":'X', "orient_type":'NORMAL', "orient_matrix":((-1, 0, 0), (-0, -0, -1), (0, -1, 0)), "orient_matrix_type":'NORMAL', "constraint_axis":(False, False, True), "mirror":False, "use_proportional_edit":False, "proportional_edit_falloff":'SMOOTH', "proportional_size":1, "use_proportional_connected":False, "use_proportional_projected":False, "snap":False, "snap_target":'CLOSEST', "snap_point":(0, 0, 0), "snap_align":False, "snap_normal":(0, 0, 0), "gpencil_strokes":False, "cursor_transform":False, "texture_space":False, "remove_on_cancel":False, "view2d_edge_pan":False, "release_confirm":True, "use_accurate":False, "use_automerge_and_split":False})
	
	bpy.ops.object.mode_set(mode='OBJECT')
	bpy.ops.object.select_all(action="DESELECT")

	bpy.ops.object.material_slot_add()
	object.material_slots[0].material = МатериалДверей
	
	GP.ЛеваяДверь = [object, mesh, МатериалДверей]
	
	
	# Уплотнение между дверями
	v = []
	v.append(vr[1]) # 0 Правые точки уплотнения: низ
	v.append(vr[7]) # 1 Правые точки уплотнения: верх
	v.append(vr[8]) # 2 Правые точки центра: верх
	v.append(vr[9]) # 3 Правые точки центра: низ

	v.append(vl[1])	# 4 Левая точка снизу
	v.append(vl[7])	# 5 Левая точки сверху
	v.append(vl[8])	# 6 Левая тоцка центр: верх
	v.append(vl[9])	# 7 Левая тоцка центр: низ


	# f = [(4, 0, 3, 7), (3, 7, 6, 3), (3, 6, 5, 1)]
	f = [(4, 0, 3, 7), (3, 7, 6, 2), (6, 2, 1, 5)]
	
	name = 'УплотнениеМеждуДверями'
	[object, mesh] = MatProps.createObject(
		name=name, vertices=v, faces=f, edjes=[], loc0=(0, +Смещение, 0)
		)
	
	bpy.ops.object.editmode_toggle()

	bpy.ops.mesh.extrude_context_move(MESH_OT_extrude_context={"use_normal_flip":False, "use_dissolve_ortho_edges":False, "mirror":False}, TRANSFORM_OT_translate={"value":(0, 0, -ТолщинаДвери), "orient_axis_ortho":'X', "orient_type":'NORMAL', "orient_matrix":((-1, 0, 0), (-0, -0, -1), (0, -1, 0)), "orient_matrix_type":'NORMAL', "constraint_axis":(False, False, True), "mirror":False, "use_proportional_edit":False, "proportional_edit_falloff":'SMOOTH', "proportional_size":1, "use_proportional_connected":False, "use_proportional_projected":False, "snap":False, "snap_target":'CLOSEST', "snap_point":(0, 0, 0), "snap_align":False, "snap_normal":(0, 0, 0), "gpencil_strokes":False, "cursor_transform":False, "texture_space":False, "remove_on_cancel":False, "view2d_edge_pan":False, "release_confirm":True, "use_accurate":False, "use_automerge_and_split":False})
	
	bpy.ops.object.mode_set(mode='OBJECT')
	bpy.ops.object.select_all(action="DESELECT")

	МатериалУплотнения = MatProps.addMaterial(BaseColor=(0, 0, 0), Roughness=1, name="МатериалУплотнения",  obj=object)

	GP.УплотнениеМеждуДверями = [object, mesh, МатериалУплотнения]


def ДобавитьТочкуЗахвата():
	
	view_layer = bpy.context.view_layer
	
	R = 0.7		# Радиус цилиндра
	H = 0.4		# Высота цилиндра над уровнем коридора
	ВысотаЦилиндра = H + GP.ТолщинаСтенокМодуля
	# Точка захвата расположена на крыше по центру модуля
	position = (GP.ШиринаМодуля/2, GP.ПоложениеТочкиЗахвата, GP.ВысотаМодуля + H/2)

	bpy.ops.mesh.primitive_cylinder_add(vertices=128, radius=R, depth=H, enter_editmode=False, align='WORLD', location=position)

	cyl = view_layer.objects.active
	
	МатериалТочкиЗахвата = MatProps.addMaterial(BaseColor=(1, 1, 1), Roughness=0.0, Specular=1, Metallic=0, name="МатериалТочкиЗахвата",  obj=cyl)

	# Текстура не реагирует на освещение, поэтому я её убрал
	"""
	toRemove = МатериалТочкиЗахвата.node_tree.nodes['Principled BSDF']
	МатериалТочкиЗахвата.node_tree.nodes.remove(toRemove)
	matOutput = МатериалТочкиЗахвата.node_tree.nodes['Material Output']
	
	texImage_node = МатериалТочкиЗахвата.node_tree.nodes.new('ShaderNodeTexChecker')

    МатериалТочкиЗахвата.node_tree.links.new(texImage_node.outputs[0], matOutput.inputs[0])
	
	# bpy.data.materials['PlanetMaterial.МатериалТочкиЗахвата'].node_tree.nodes['Checker Texture']
	inp = МатериалТочкиЗахвата.node_tree.nodes['Checker Texture'].inputs
	inp['Color1'].default_value = (1, 1, 1, 1)
	inp['Color2'].default_value = (0, 0, 0, 1)
	inp['Scale'] .default_value = 3
	"""

	
def ДобавитьПанельУправленияДверями(Коридор, Enabled=True):

	[_, _, vert, _, _] = Коридор
	size = (0.3, 0.01, 0.5)
	loc0 = (
			vert[11][0] + (vert[3][0] - vert[11][0] - size[0])/2,
			vert[11][1],
			vert[11][2] + (vert[13][2] - vert[11][2])/4
			)

	cube = MatProps.createCube("ПанельУправленияДверями", size, loc0 = loc0)
	
	# Панель может быть включена или выключена
	МатериалПанелиУправленияДверями = MatProps.addMaterial(BaseColor=(0, 0, 0), Roughness=0.0, Specular=1, Metallic=0, name="МатериалПанелиУправленияДверями",  obj=cube[0])

	inp = МатериалПанелиУправленияДверями.node_tree.nodes['Principled BSDF'].inputs
	inp['Emission'] .default_value[0] = 0
	inp['Emission'] .default_value[1] = 255
	inp['Emission'] .default_value[2] = 0
	inp['Emission'] .default_value[3] = 255

	if Enabled:
		inp['Emission Strength'].default_value = 0.001
	else:
		inp['Emission Strength'].default_value = 0.0

	inp['Base Color']       .default_value = (  255,  255,    255, 255)
	inp['Subsurface']       .default_value = 10.0
	inp['Subsurface Color'] .default_value = (    0,    0,      0, 255)
	inp['Subsurface Radius'].default_value = (0.001, 0.001, 0.001)
	inp['Subsurface IOR']   .default_value = 1.0
	

# -------------------------------------------------------------------------------------
# -------------------------------------------------------------------------------------

view_layer = bpy.context.view_layer

# Добавляем камеру
bpy.ops.object.camera_add()
bpy.data.objects['Camera'].location = Vector((+6.0, -10, 6.5))
bpy.data.objects['Camera'].rotation_euler = Euler((70*pi/180,   0*pi/180, +18*pi/180), 'XYZ')
bpy.data.cameras[0].lens     = 37  # Фокусное расстояние объектива
bpy.data.cameras[0].clip_end = 40  # Дальность отрисовки

# Добавляем освещение

# Свет от Моры
bpy.ops.object.light_add(type='SUN', location=(-10, -10, -10), rotation=(180*pi/180, 30*pi/180, 15*pi/180))
MoraObj = view_layer.objects.active
MoraL   = bpy.data.lights[len(bpy.data.lights)-1]
MoraObj.name = 'Свет Моры'
MoraL.energy = 1
# MoraL.angle  = 0.5*pi/180
MoraL.angle  = 90*pi/180
MoraL.cycles.max_bounces = 5

# Устанавливаем свет с синеватым отливом, чтобы источник был примерно как у Моры
MoraL.color = (0.58, 0.58, 1)

# Свет от Солнца (будет идти сверху-справа)
bpy.ops.object.light_add(type='SUN', location=(-10, -10, -10), rotation=(31*pi/180, 0*pi/180, 75*pi/180))
SunObj = view_layer.objects.active
SunL   = bpy.data.lights[len(bpy.data.lights)-1]
SunObj.name = 'Солнце'
SunL.energy = 3
SunL.angle  = 0.5*pi/180
SunL.cycles.max_bounces = 5

# Устанавливаем свет с синеватым отливом, чтобы источник был примерно как у Моры
SunL.color = (1, 1, 0.98)

# -------------------------------------------------------------------------------------
# -------------------------------------------------------------------------------------

# Создаём основные объекты сцены
Коридор = СоздатьКоридор()
СоздатьДвери(Коридор)
ДобавитьТочкуЗахвата()
ДобавитьПанельУправленияДверями(Коридор, False)

# -------------------------------------------------------------------------------------
# -------------------------------------------------------------------------------------

# Устанавливаем, что на объектах нет текстуры
for obj in bpy.data.objects:
	# obj.display_type = 'SOLID' # TEXTURED
	obj.display_type = 'TEXTURED'

# Добавляем настройки рендера
bpy.data.scenes[0].render.engine = 'CYCLES'
bpy.data.scenes[0].cycles.preview_samples = 16
bpy.data.scenes[0].cycles.samples = Samples
# bpy.data.scenes[0].cycles.seed = 0
bpy.data.scenes[0].cycles.denoising_prefilter = Prefilter
bpy.data.scenes[0].cycles.use_denoising = use_denoising
# Эта штука позволяет сделать сцену более освещённой при рендеринге
bpy.data.scenes[0].cycles.volume_step_rate = 0.01


try:
	bpy.data.worlds["World"].node_tree.nodes.remove(bpy.data.worlds["World"].node_tree.nodes["Background"])
except:
	None
