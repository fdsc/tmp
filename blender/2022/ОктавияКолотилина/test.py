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


Carbage = 'Ремни'
# Перед созданием коллекции убираем выделение с объектов, чтобы они не добавились по ошибке
bpy.ops.object.select_all(action='DESELECT')
CarbageCollection = bpy.data.collections.new(Carbage)
bpy.context.scene.collection.children.link(CarbageCollection)

view_layer        = bpy.context.view_layer
CarbageCollection = bpy.data.collections[0]
# bpy.data.scenes[0].collection.children.link(CarbageCollection)
# view_layer.active_layer_collection.collection.objects.link(CarbageCollection)



# with bpy.context.temp_override(**override2):
#	bpy.ops.object.collection_remove()

# view_layer = bpy.context.view_layer


def addTor(loc, R, minor_radius, rot, name, collection):

	tor = addTorus(name, (0, 0, 0), 4, 0.1)
	tors.append(tor)
	
	view_layer.objects.active = tor
	collection.objects.link(tor)

	overrideCl = bpy.context.copy()
	overrideCl['collection'] = bpy.context.scene.collection
	with bpy.context.temp_override(**overrideCl):
		bpy.ops.object.collection_remove()


	tor.rotation_euler = rot


tors = []

n = 8
for i in range(n):
	
	addTor((0, 0, 0), 4, 0.1, (i/n*2*pi, 0, 0),    Carbage, CarbageCollection)
	addTor((0, 0, 0), 4, 0.1, (pi*2, i/n*2*pi, 0), Carbage, CarbageCollection)



