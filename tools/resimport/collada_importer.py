"""
Handles importing and exporting Collada files.

@author Ben Giacalone
"""
import json
import shutil
from pathlib import Path

from tools.envedit.edenv_component import EComponent
from tools.envedit.graph_node import GraphNode
from tools.resimport.helper import resources_path
from collada import Collada
import collada


class ColladaImporter:

    @staticmethod
    def is_type(file):
        return file.name.split(".")[-1] == "dae"

    @staticmethod
    def export(file):
        # Load scene from file
        collada_file = Collada(file)
        scene = collada_file.scene

        # Export textures
        mat_map = {}
        model_folder_path = Path(file.name).parent
        for material in collada_file.materials:
            mat_path = model_folder_path / Path(material.effect.diffuse.sampler.surface.image.path)
            shutil.copy(mat_path, resources_path / mat_path.name)
            mat_map[material.effect.id] = mat_path.name

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
                        for coord in texcoord:
                            texcoords_list.append(coord[0].item())
                            texcoords_list.append(coord[1].item())
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

        # Export sub-tree
        root_node = ColladaImporter.process_scene(scene)
        node_dict = GraphNode.scene_graph_to_dict(root_node)
        with open(resources_path / f"{root_node.name}.json", "w") as file:
            json.dump(node_dict, file)

    # Returns a node representation of the scene
    @staticmethod
    def process_scene(scene_node):
        node = GraphNode(scene_node.id, [])

        for child in scene_node.nodes:
            child_node = ColladaImporter.process_node(child)
            if child_node is not None:
                node.add_child(child_node)

        return node

    # Returns a node representation of a scene node
    @staticmethod
    def process_node(scene_node):
        node = GraphNode("Model Node", [])
        if hasattr(scene_node, "id") and scene_node.id is not None:
            node.name = scene_node.id

        # Add the transform of the node
        if hasattr(scene_node, "matrix"):
            node.transform.set_matrix(scene_node.matrix)

        # Add a Position component
        pos_component = EComponent()
        pos_component.set_script("components.position")
        pos_component.property_vals["pos_x"] = str(node.transform.trans[0].item())
        pos_component.property_vals["pos_y"] = str(node.transform.trans[1].item())
        pos_component.property_vals["pos_z"] = str(node.transform.trans[2].item())
        pos_component.property_vals["rot_x"] = str(node.transform.rot[0].item())
        pos_component.property_vals["rot_y"] = str(node.transform.rot[1].item())
        pos_component.property_vals["rot_z"] = str(node.transform.rot[2].item())
        pos_component.property_vals["scale_x"] = str(node.transform.scale[0].item())
        pos_component.property_vals["scale_y"] = str(node.transform.scale[1].item())
        pos_component.property_vals["scale_z"] = str(node.transform.scale[2].item())
        node.add_component(pos_component)

        # If scene_node holds a mesh, add a MeshGraphic
        if hasattr(scene_node, "controller"):
            mesh_renderer = EComponent()
            mesh_renderer.set_script("components.mesh_graphic")
            mesh_renderer.property_vals["mesh"] = scene_node.controller.geometry.name
            node.data.append(mesh_renderer)

        # If scene_node is ExtraNode, return nothing
        if type(scene_node) == collada.scene.ExtraNode:
            return None

        if hasattr(scene_node, "children"):
            for child in scene_node.children:
                child_node = ColladaImporter.process_node(child)
                if child_node is not None:
                    node.add_child(child_node)

        return node
