import sys
import os

import bpy
import bmesh
from math import *
from mathutils import *
from random import *



class MaterialProperties:
	MaterialNumber: int = 0
	prefix        : str = 'PlanetMaterial.'

	def __init__(this):
		this.MaterialNumber = bpy.data.scenes[0].get('PlanetMaterialNumber', 0)
		bpy.data.scenes[0]['PlanetMaterialNumber'] = this.MaterialNumber

		this.torMat = []

	@property
	def getMaterialNumber(this):
		a = this.MaterialNumber
		this.MaterialNumber += 1

		bpy.data.scenes[0]['PlanetMaterialNumber'] = this.MaterialNumber
		
		return a


	def addMaterial(this, BaseColor = None, Specular = 0, Roughness = 0, obj = None, name=None):

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


	def DeleteAllObjects(this):

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

	def createObject(name, vertices, faces, edjes, loc0 = (0, 0, 0)):

		#Define mesh and object
		mesh   = bpy.data.meshes.new(name)
		object = bpy.data.objects.new(name, mesh)

		#Set location and scene of object
		object.location = loc0 # bpy.context.scene.cursor_location

		view_layer = bpy.context.view_layer
		view_layer.active_layer_collection.collection.objects.link(object)

		#Create mesh
		mesh.from_pydata(vertices, edjes, faces)
		mesh.update(calc_edges=False)

		object.select_set(True)
		view_layer.objects.active = object
		
		return object, mesh
