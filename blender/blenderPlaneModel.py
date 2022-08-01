# Использование итоговой иллюстрации не допускается
# Автор илллюстрации https://author.today/u/alrtat

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



# Удаляем всё, что осталось от предыдущих запусков скриптов или других рисований

if bpy.ops.object.mode_set.poll():
    bpy.ops.object.mode_set(mode="OBJECT")


# Удаляем все mesh
for i in bpy.data.meshes:
	bpy.data.meshes.remove(i)

# Удаляем все камеры
for camera in bpy.data.cameras:
	bpy.data.cameras.remove(camera)

# Удаляем все светящие объекты
for light in bpy.data.lights:
	bpy.data.lights.remove(light)

# Удаляем все коллекции объектов
for coll in bpy.data.collections:
	bpy.data.collections.remove(coll)

# Удаляем все материалы
for mat in bpy.data.materials:
	#if mat.name_full.startswith(prefix):
	bpy.data.materials.remove(mat)

	
# Удаляем все объекты
# Почему-то иногда не работает
bpy.ops.object.select_all()
bpy.ops.object.delete(confirm=False)


class Properties:
	MaterialNumber: int = 0

	def __init__(this):
		this.MaterialNumber = bpy.data.scenes[0].get('PlanetMaterialNumber', 0)
		bpy.data.scenes[0]['PlanetMaterialNumber'] = this.MaterialNumber

	@property
	def getMaterialNumber(this):
		a = this.MaterialNumber
		this.MaterialNumber += 1

		bpy.data.scenes[0]['PlanetMaterialNumber'] = this.MaterialNumber
		
		return a


global torMat, Props

torMat = []
Props  = Properties()
prefix = 'PlanetMaterial.'


def addMaterial(BaseColor = None, Specular = 0, Roughness = 0, obj = None, name=None):

	if name:
		matName = prefix + name
	else:
		matName = prefix + str(Props.getMaterialNumber)

	# bpy.data.materials.new(matName)
	#bpy.ops.material.new()
	mat = bpy.data.materials.new(name=matName)
	mat.use_nodes = True

	#mat = bpy.data.materials[len(bpy.data.materials) - 1]
	#mat.name = matName

	inp = mat.node_tree.nodes['Principled BSDF'].inputs
	if BaseColor:
		inp['Base Color'].default_value[0] = BaseColor[0]
		inp['Base Color'].default_value[1] = BaseColor[1]
		inp['Base Color'].default_value[2] = BaseColor[2]
		inp['Base Color'].default_value[3] = 255 # Альфа-канал

	inp['Specular'] .default_value = Specular
	inp['Roughness'].default_value = Roughness

	return mat


# Создаём плоскость, параллельную плоскости XY
def newPlane_getVericies(loc, size, centerSize):
	
	[x, y, z]                  = (0, 0, 0)
	[sizeX,       sizeY]       = size
	[centerSizeX, centerSizeY] = centerSize

	startCX = x + (sizeX - centerSizeX) / 2
	startCY = y + (sizeY - centerSizeY) / 2
	
	vertices = []
	
	for ix in range(2):
		for iy in range(2):
			vertices.append((x       + sizeX      *ix, y       + sizeY      *iy, z + 0))
			vertices.append((startCX + centerSizeX*ix, startCY + centerSizeY*iy, z + 0))
			
	return vertices

def newPlane_getFacesAndEdjes():

	faces = [
				(1, 3, 7, 5),
				(0, 1, 3, 2), (0, 1, 5, 4), (2, 3, 7, 6), (4, 5, 7, 6)
			]

	edjes = [
				(0, 2), (0, 4), (2, 6), (4, 6),
				(1, 3), (1, 5), (3, 7), (5, 7),
				(0, 1), (2, 3), (4, 5), (6, 7)
			]

	return faces, edjes


def getPlaneWithSubdivideCenter(loc, size, centerSize, subdivide=4):

	#Define vertices, faces, edges
	vertices       = newPlane_getVericies(loc, size, centerSize)
	[faces, edjes] = newPlane_getFacesAndEdjes()

	name = "Plane"

	#Define mesh and object
	mesh   = bpy.data.meshes.new(name)
	object = bpy.data.objects.new(name, mesh)

	#Set location and scene of object
	object.location = loc # bpy.context.scene.cursor_location
	#bpy.context.scene.objects.link(object)
	view_layer = bpy.context.view_layer
	view_layer.active_layer_collection.collection.objects.link(object)

	#Create mesh
	mesh.from_pydata(vertices, edjes, faces)
	mesh.update(calc_edges=False)


	object.select_set(True)
	view_layer.objects.active = object

	bpy.ops.object.mode_set(mode='EDIT')
	bpy.ops.mesh.normals_make_consistent(inside=False)

	bm = bmesh.from_edit_mesh(mesh)
	for face in bm.faces:
		face.select = False

	bm.faces[0].select = True

	for i in range(subdivide):
		bpy.ops.mesh.subdivide()


	bpy.ops.object.mode_set(mode='OBJECT')

	# bpy.data.objects[name].select_set(True)
	object.select_set(True)
	view_layer.objects.active = object




def addCylinder(name, loc, radius, len, XYRot = True):
	
	if XYRot:
		rot = (90*pi/180, 0, 0)
	else:
		rot = (0, 90*pi/180, 0)

	loc = (loc[0], loc[1], loc[2] + radius)

	bpy.ops.mesh.primitive_cylinder_add(vertices=12, radius=radius, depth=2, end_fill_type='NGON', calc_uvs=False, enter_editmode=False, align='WORLD', location=loc, rotation=rot, scale=(1, 1, len/2))

	# Похоже, что последний объект добавляется здесь в нулевой индекс
	if name:
		bpy.data.objects[0].name = name

	bpy.ops.object.modifier_add(type="COLLISION")

len = 5
rad = 0.1
for x in range(len+1):
	addCylinder(None, (x,    len/2, 0), rad, len, True)

for y in range(len+1):
	addCylinder(None, (len/2, y,    0), rad, len, False)


#bpy.ops.mesh.primitive_plane_add(size=len*3, calc_uvs=False, location=(len/2, len/2, rad*2))
#bpy.ops.object.mode_set(mode="EDIT")

#for i in range(2):
#	bpy.ops.mesh.subdivide()

#bpy.ops.object.mode_set(mode="OBJECT")

k = 1.1

loc = (-(len*k-len)/2, -(len*k-len)/2, rad*2)
getPlaneWithSubdivideCenter(loc, (len*k, len*k), (len, len), 5)


bpy.ops.object.modifier_add(type="SOFT_BODY")
bpy.data.objects["Plane"].modifiers["Softbody"].settings.use_goal = False
bpy.data.objects["Plane"].modifiers["Softbody"].settings.use_edge_collision = True

# Устанавливаем, что на объектах нет текстуры
for obj in bpy.data.objects:
	obj.display_type = 'SOLID' # TEXTURED
# bpy.data.objects['Алькари'].display_type = 'SOLID'


# Добавляем камеру
bpy.ops.object.camera_add()
bpy.data.objects['Camera'].location = Vector((200, 20, 150))
bpy.data.objects['Camera'].rotation_euler = Euler((50*pi/180,   0*pi/180, 100*pi/180), 'XYZ')
bpy.data.cameras[0].lens = 25

# bpy.context.view_layer.view_camera()

# Добавляем настройки рендера
bpy.data.scenes[0].render.engine = 'CYCLES'
bpy.data.scenes[0].cycles.samples = Samples
# bpy.data.scenes[0].cycles.seed = 0
bpy.data.scenes[0].cycles.denoising_prefilter = Prefilter
bpy.data.scenes[0].cycles.use_denoising = use_denoising
# Эта штука позволяет сделать сцену более освещённой при рендеринге
bpy.data.scenes[0].cycles.volume_step_rate = 0.01
# bpy.data.scenes[0].cycles.adaptive_threshold = 0
# bpy.ops.render.view_show()
# bpy.ops.render.render()

try:
	bpy.data.worlds["World"].node_tree.nodes.remove(bpy.data.worlds["World"].node_tree.nodes["Background"])
except:
	None

# bpy.data.worlds["World"].node_tree.nodes["Background"].inputs['Color'].default_value[0] = 0
# bpy.data.worlds["World"].node_tree.nodes["Background"].inputs['Color'].default_value[1] = 0
# bpy.data.worlds["World"].node_tree.nodes["Background"].inputs['Color'].default_value[2] = 0

