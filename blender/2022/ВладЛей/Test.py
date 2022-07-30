# Использование иллюстрации только с согласования с автором иллюстрации
# Автор илллюстрации https://author.today/u/alrtat
# Рисуем иллюстрацию к https://author.today/reader/166459/1360972

import bpy
from math import *
from mathutils import *
from random import *


Samples   = 1024
Prefilter = 'ACCURATE'
CountOfCarbage = 186*2
use_denoising = True

SimpleRendering = False

if SimpleRendering:
	Samples   = 64
	Prefilter = 'FAST'
	# Prefilter = 'NONE'
	CountOfCarbage = 64
	use_denoising  = False



# Удаляем всё, что осталось от предыдущих запусков скриптов или других рисований

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


# Функция добавления планеты (сферы)
def addPlanet(name, distance, radius, rotateInDegree, loc0, BaseColor, minor_radius=0.25, subdivisions=4, Smooth = True, noOrbit = False, Collection = None):
	"""
		name     		- имя планеты
		distance 		- радиус орбиты планеты
		radius   		- радиус самой планеты
		rotateInDegree	- положение планеты на орбите (в градусах)
		loc0            - центр орбиты
		BaseColor       - цвет планеты
		minor_radius    - толщина, которой будет показываться орбита (0 - не показывается)
		subdivisions    - планета рисуется как ico-сфера. Количество рекурсий ico-сферы (чем больше, тем более качественная получится сфера: 4-7 - оптимум).
		Smooth			- если True, то отражения от планеты будут нарисованы сглаженными, так, что не будет видно полигонов
		Collection      - имя коллекции объектов
	"""

	# Вычисляем положение планеты на орбите в глобальных координатах
	rotateInDegree += 90

	x = loc0[0] + distance * sin(rotateInDegree * pi / 180)
	y = loc0[1] + distance * cos(rotateInDegree * pi / 180)

	# Рисуем саму планету
	bpy.ops.mesh.primitive_ico_sphere_add(subdivisions=subdivisions, radius=radius, location=(x, y, 0))

	# bpy.data.objects['Icosphere'].name = name
	# len(bpy.data.objects)-1
	# Похоже, что последний объект добавляется здесь в нулевой индекс
	bpy.data.objects[0].name = name
	# bpy.data.meshes[len(bpy.data.meshes)-1].name = name
	if Smooth:
		bpy.ops.object.shade_smooth()

	# Добавляем на планету слот для материала
	bpy.ops.object.material_slot_add()
	override = bpy.context.copy()

	if Collection:
		# bpy.ops.object.collection_instance_add(name=Carbage)
		bpy.ops.object.collection_link(collection=Collection)

		override2 = bpy.context.copy()
		override2['collection'] =  bpy.data.scenes[0].collection # bpy.data.collections[Collection]

		with bpy.context.temp_override(**override2):
			bpy.ops.object.collection_remove()
			# bpy.ops.object.collection_unlink()

	# distance означает, что мы рисуем звезду
	if distance == 0:

		mat = addMaterial(BaseColor = (255, 255, 0), Specular = 1, Roughness = 1, obj = bpy.data.objects[name], name = "planet." + name)

		inp = mat.node_tree.nodes['Principled BSDF'].inputs

		inp['Specular'] .default_value = 0
		inp['Roughness'].default_value = 1
		inp['Emission'] .default_value[0] = 255
		inp['Emission'] .default_value[1] = 255
		inp['Emission'] .default_value[2] = 0
		inp['Emission'] .default_value[3] = 255
		inp['Emission Strength'].default_value = 0.01

		# mat = bpy.data.objects['Алькари'].material_slots[0].material
		bpy.data.objects[name].material_slots[0].material = mat

		bpy.ops.object.light_add(type='POINT', radius=radius, location=(x, y, 0))
		bpy.data.objects[0].name = 'Свет'
		bpy.data.lights[len(bpy.data.lights)-1].energy = 1e8
		bpy.data.lights[len(bpy.data.lights)-1].shadow_soft_size = radius+0.5
		bpy.data.lights[len(bpy.data.lights)-1].cycles.max_bounces = 5
		bpy.data.objects['Свет'].color[0] = 1
		bpy.data.objects['Свет'].color[2] = 1
		bpy.data.objects['Свет'].color[3] = 1

		return


	# Выбираем материал для обычной планеты. Со звездой мы уже закончили
	with bpy.context.temp_override(**override):
		mat = addMaterial(BaseColor = BaseColor, Specular = 100, Roughness = 1, name = "planet." + name)
		bpy.data.objects[name].material_slots[0].material = mat


	# Рисуем орбиту в виде тора
	if noOrbit:
		return

	if minor_radius <= 0:
		return


	major_segments = int(distance)
	if major_segments < 64:
		major_segments = 64

	bpy.ops.mesh.primitive_torus_add(location=(loc0[0], loc0[1], 0), major_radius=distance, minor_radius=minor_radius, major_segments=major_segments, minor_segments=12)

	# bpy.data.objects['Torus'].name = name
	# bpy.data.meshes[len(bpy.data.meshes)-1].name = name + ".orbit"
	nm = name + ".orbit" + str(len(bpy.data.objects))
	bpy.data.objects[0].name = nm
	
	bpy.ops.object.material_slot_add()
	override = bpy.context.copy()
	

	if Collection != None:
		bpy.ops.object.collection_link(collection=Collection)


	# Создаём материал для орбиты
	# Материал имеет слабое свечение
	if len(torMat) <= 0:
		with bpy.context.temp_override(**override):
			mat = bpy.data.materials.new(name = prefix + "torus")
			mat.use_nodes = True

		mat = bpy.data.materials[len(bpy.data.materials)-1]
		bpy.data.objects[nm].material_slots[0].material = mat
		mat.name = 'PlanetMaterial.orbit.' + name

		inp = mat.node_tree.nodes['Principled BSDF'].inputs
		inp['Base Color'].default_value[0] = 127
		inp['Base Color'].default_value[1] = 127
		inp['Base Color'].default_value[2] = 127
		inp['Base Color'].default_value[3] = 255 # Альфа-канал

		inp['Specular'] .default_value = 0
		inp['Roughness'].default_value = 0
		inp['Emission'].default_value[0] = 127
		inp['Emission'].default_value[1] = 127
		inp['Emission'].default_value[2] = 127
		inp['Emission'].default_value[3] = 255
		inp['Emission Strength'].default_value = 0.001

		torMat.append(mat)
	
	bpy.data.objects[nm].material_slots[0].material = torMat[0]

# Добавляем планеты
loc0 = (0, 0)
addPlanet('Алькари',   0, 15,    0,   loc0, BaseColor = None,          minor_radius = 0)
addPlanet('Реквием', 150,  8,   +38,  loc0, BaseColor = (0,   1,   0), minor_radius = 0.02)
addPlanet('Мора',     75,  4,   -18,  loc0, BaseColor = (0,   0,   1), minor_radius = 0.05)
addPlanet('Калидум',  40,  2,  -100,  loc0, BaseColor = (1, 0.5,   0), minor_radius = 0.10)

# Добавляем спутники планет
# Калидум + Клара
ml = bpy.data.objects['Калидум'].location
addPlanet('Клара',  5, 1, -70, (ml[0], ml[1]), BaseColor = (0.7, 0.5, 0), minor_radius = 0.01)

# Мора + Примис + Дейнде
ml = bpy.data.objects['Мора'].location
mk = (ml[0], ml[1])
addPlanet('Примис',  7.8, 1, -158,  mk, BaseColor = (0.25, 0.25, 1), minor_radius = 0.01)
addPlanet('Дейнде',  11,  2,  -77,  mk, BaseColor = (1, 0.25, 0.75), minor_radius = 0.01)

# Добавляем слой обломков
Carbage = 'Кольцо обломков'
# Перед созданием коллекции убираем выделение с объектов, чтобы они не добавились по ошибке
bpy.ops.object.select_all(action='DESELECT')
bpy.ops.collection.create(name=Carbage)
bpy.ops.object.collection_instance_add(name=Carbage)

scale = 5
for i in range(CountOfCarbage):
	addPlanet(
		'Пояс',
		distance       = uniform(5, 6.5),				# Высота орбиты
		radius         = uniform(0.04*scale, 0.01*scale),
		rotateInDegree = uniform(0, 360),
		loc0           = mk,
		BaseColor      = (
							1-uniform(0, 0.1),
							0.25+uniform(-0.05, 0.05),
							0.75+uniform(-0.05, 0.05)
						),
		minor_radius = 0,
		subdivisions = 1 + (i&1),
		Smooth = False,
		Collection = Carbage
	)

# Реквием + Сомниум
ml = bpy.data.objects['Реквием'].location
mk = (ml[0], ml[1])
addPlanet('Сомниум', 18, 1.5, +0,  mk, BaseColor = (0, 1, 0.18), minor_radius = 0.01)


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

