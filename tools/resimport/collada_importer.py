"""
Handles importing and exporting Collada files.

@author Ben Giacalone
"""
import json

from tools.envedit.graph_node import GraphNode
from tools.resimport.helper import resources_path
from collada import Collada


class ColladaImporter:

    @staticmethod
    def is_type(file):
        return file.name.split(".")[-1] == "dae"

    @staticmethod
    def export(file):
        # Load scene from file
        collada_file = Collada(file)
        scene = collada_file.scene

        # Extract textures
        mat_map = {}
        for material in collada_file.materials:
            mat_map[material.effect.id] = material.effect.diffuse.sampler.surface.image.path

        # Export meshes
        for geometry in collada_file.geometries:
            # Create new mesh
            new_mesh = {
                "vertices": [],
                "texcoords": [],
                "normals": []
            }
            vertex_list = []
            texcoords_list = []
            normals_list = []

            for primitive in geometry.primitives:
                # Set mesh's texture
                new_mesh["texture"] = mat_map[primitive.material]
                for tri in list(primitive):

                    # Go over vertices, texture coordinates, and normals
                    for vertex in tri.vertices:
                        for coord in vertex:
                            vertex_list.append(coord.item())
                    for texcoord in tri.texcoords:
                        for coord in texcoord[0]:
                            texcoords_list.append(coord.item())
                    for normal in tri.normals:
                        for coord in normal:
                            normals_list.append(coord.item())

                    new_mesh["vertices"] = vertex_list
                    new_mesh["texcoords"] = texcoords_list
                    new_mesh["normals"] = normals_list

            # Add metadata
            new_mesh["metadata"] = {
                "version": "0.1",
                "type": "mesh"
            }

            # Export JSON files
            with open(resources_path / f"{geometry.name}.json", "w") as file:
                json.dump(new_mesh, file)
