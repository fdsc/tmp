# Использование итоговой иллюстрации не допускается
# Автор илллюстрации https://author.today/u/alrtat

# filename = "/Arcs/Repos/tmp/blender/2023/Площадь/stone.py"
# exec(compile(open(filename).read(), filename, 'exec'))

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


blend_dir = os.path.dirname("/Arcs/Repos/tmp/blender/2023/Площадь/")
if blend_dir not in sys.path:
   sys.path.append(blend_dir)


import MaterialProperties
global MatProps

MatProps = MaterialProperties.MaterialProperties()

MatProps.DeleteAllObjects()


StonesCollectionName = 'Камень'
# Перед созданием коллекции убираем выделение с объектов, чтобы они не добавились по ошибке
bpy.ops.object.select_all(action='DESELECT')
StonesCollection = bpy.data.collections.new(StonesCollectionName)
bpy.context.scene.collection.children.link(StonesCollection)

view_layer        = bpy.context.view_layer
# StonesCollection  = bpy.data.collections[0] # Зачем?

# bpy.data.scenes[0].collection.children.link(StonesCollection)
# view_layer.active_layer_collection.collection.objects.link(StonesCollection)


# Создаём плоскость, параллельную плоскости XY
def newVert():
	
	vertices = []

	# Масштабный коэффициент
	k = 1

	vertices.append([-1.0, -1.0, -1.0]);
    vertices.append([+1.0, -1.0, -1.0]);
    vertices.append([-1.0, -1.0, +1.0]);
    vertices.append([+1.0, -1.0, +1.0]);
    
	return vertices

def newEdjes():

	faces = [
				(0, 1, 2, 3)
			]

	edjes = []

	eds = [0, 1, 2, 3]
	for i in range(  len(eds)-1  ):
		edjes.append((  eds[i]+0, eds[i+1]+0  ))

	return faces, edjes


def СоздатьКамень():
    vertices       = newVert()
    [faces, edjes] = newEdjes()

    name = 'Камень'
    [object, mesh] = MatProps.createObject(
        name=name, vertices=vertices, faces=faces, edjes=edjes, loc0=(0, 0, 0)
        )

    



