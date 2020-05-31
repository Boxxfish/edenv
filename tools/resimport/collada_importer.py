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

        # Export sub-tree
        joint_node_dict = {}
        root_node = ColladaImporter.process_scene(scene, joint_node_dict)
        node_dict = GraphNode.scene_graph_to_dict(root_node)
        with open(resources_path / f"{root_node.name}.json", "w") as file:
            json.dump(node_dict, file)

        # Process skinned meshes
        skin_data = {}
        node_list = []
        for controller in collada_file.controllers:
            joints = list(controller.sourcebyid[controller.joint_source])

            joint_list = []
            weight_list = []
            for i in range(len(controller.joint_index)):
                joint_indices = controller.joint_index[i]
                vertex_joints = []
                for joint_index in joint_indices:
                    joint_node = joint_node_dict[joints[joint_index]]
                    if joint_node not in node_list:
                        node_list.append(joint_node)
                    vertex_joints.append(node_list.index(joint_node))
                joint_list.append(vertex_joints)

                weight_indices = controller.weight_index[i]
                vertex_weights = []
                for weight_index in weight_indices:
                    vertex_weights.append(list(controller.weights)[weight_index][0].item())
                weight_list.append(vertex_weights)

            skin_data[controller.geometry.id] = {"joints": joint_list, "weights": weight_list}

        # Export meshes
        for geometry in collada_file.geometries:
            # Create new mesh
            new_mesh = {}
            vertex_list = []
            texcoords_list = []
            normals_list = []
            for primitive in geometry.primitives:
                # Set mesh's texture
                if primitive.material in mat_map:
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
                    new_mesh["joints"] = skin_data[geometry.id]["joints"]
                    new_mesh["weights"] = skin_data[geometry.id]["weights"]
                    new_mesh["nodes"] = node_list

            # Add metadata
            new_mesh["metadata"] = {
                "version": "0.2",
                "type": "mesh"
            }

            # Export JSON files
            with open(resources_path / f"{geometry.name}.json", "w") as file:
                json.dump(new_mesh, file)

    # Returns a node representation of the scene
    @staticmethod
    def process_scene(scene_node, joint_node_dict):
        node = GraphNode(scene_node.id, [])

        for child in scene_node.nodes:
            child_node = ColladaImporter.process_node(child, joint_node_dict)
            if child_node is not None:
                node.add_child(child_node)

        return node

    # Returns a node representation of a scene node
    @staticmethod
    def process_node(scene_node, joint_node_dict):
        node = GraphNode("Model Node", [])
        if hasattr(scene_node, "id") and scene_node.id is not None:
            node.name = scene_node.xmlnode.attrib["name"]
            if "type" in scene_node.xmlnode.attrib:
                joint_node_dict[scene_node.xmlnode.attrib["sid"]] = node.name

        # Add the transform of the node
        if hasattr(scene_node, "matrix"):
            node.transform.set_matrix(scene_node.matrix)

        # Add a Position component
        pos_component = EComponent.from_script("components.position")
        pos_component.property_vals["pos_x"] = str((node.transform.trans[0].item() * 1000) / 1000)
        pos_component.property_vals["pos_y"] = str((node.transform.trans[1].item() * 1000) / 1000)
        pos_component.property_vals["pos_z"] = str((node.transform.trans[2].item() * 1000) / 1000)
        pos_component.property_vals["rot_x"] = str((node.transform.rot[0].item() * 1000) / 1000)
        pos_component.property_vals["rot_y"] = str((node.transform.rot[1].item() * 1000) / 1000)
        pos_component.property_vals["rot_z"] = str((node.transform.rot[2].item() * 1000) / 1000)
        pos_component.property_vals["scale_x"] = str((node.transform.scale[0].item() * 1000) / 1000)
        pos_component.property_vals["scale_y"] = str((node.transform.scale[1].item() * 1000) / 1000)
        pos_component.property_vals["scale_z"] = str((node.transform.scale[2].item() * 1000) / 1000)
        node.add_component(pos_component)

        # If scene_node is ExtraNode, return nothing
        if type(scene_node) == collada.scene.ExtraNode:
            return None

        if hasattr(scene_node, "children"):
            for child in scene_node.children:
                # If child holds a mesh, add a MeshGraphic to this node
                if hasattr(child, "controller"):
                    mesh_renderer = EComponent.from_script("components.mesh_graphic")
                    mesh_renderer.property_vals["mesh"] = child.controller.geometry.name
                    node.data.append(mesh_renderer)
                else:
                    # Otherwise, treat it like a normal node
                    child_node = ColladaImporter.process_node(child, joint_node_dict)
                    if child_node is not None:
                        node.add_child(child_node)

        return node
