"""
Handles importing and exporting Collada files.

@author Ben Giacalone
"""
import json
import os
import shutil
import string
from pathlib import Path

import numpy as np
from collada.scene import Scene

from components.armature import Armature
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

        # Create folder to store resources
        folder_path = resources_path / Path(file.name).stem
        if not folder_path.exists():
            os.mkdir(folder_path)

        # Export textures
        mat_map = {}
        model_folder_path = Path(file.name).parent
        for material in collada_file.materials:
            if hasattr(material.effect.diffuse, "sampler"):
                mat_path = model_folder_path / Path(material.effect.diffuse.sampler.surface.image.path)
                shutil.copy(mat_path, folder_path / mat_path.name)
                mat_map[material.effect.id] = Path(file.name).stem + "/" + mat_path.name

        # Process skinned meshes
        skin_data = {}
        node_list = []
        bind_mats = []
        for controller in collada_file.controllers:
            joints = list(controller.sourcebyid[controller.joint_source])
            joint_list = []
            weight_list = []
            for i in range(len(controller.joint_index)):
                joint_indices = controller.joint_index[i]
                vertex_joints = []

                for joint_index in joint_indices:
                    joint_node = joints[joint_index]
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
            joints_list = []
            weights_list = []
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

                    # Go over weights
                    if geometry.id in skin_data:
                        for index in tri.indices:
                            joints_list.append(skin_data[geometry.id]["joints"][index])
                            weights_list.append(skin_data[geometry.id]["weights"][index])

                        new_mesh["joints"] = joints_list
                        new_mesh["weights"] = weights_list

                new_mesh["vertices"] = vertex_list
                new_mesh["texcoords"] = texcoords_list
                new_mesh["normals"] = normals_list

            # Add metadata
            new_mesh["metadata"] = {
                "version": "0.2",
                "type": "mesh"
            }

            # Export JSON files
            with open(folder_path / f"{geometry.name}.json", "w") as mesh_file:
                json.dump(new_mesh, mesh_file)

        # Export sub-tree
        joint_node_dict = {}
        root_node = ColladaImporter.process_node(scene, np.identity(4), joint_node_dict, node_list, Path(file.name).stem)
        node_dict = GraphNode.scene_graph_to_dict(root_node)
        with open(folder_path / f"{Path(file.name).stem}.json", "w") as scene_file:
            json.dump(node_dict, scene_file)

    # Returns a node representation of a scene node
    @staticmethod
    def process_node(scene_node, parent_mat, joint_node_dict, node_list, folder_name):
        node = GraphNode("Model Node", [])
        if "name" in scene_node.xmlnode.attrib:
            node.name = scene_node.xmlnode.attrib["name"]

        # Register joint
        if "type" in scene_node.xmlnode.attrib and scene_node.xmlnode.attrib["type"].lower() == "joint":
            bind_mat = np.linalg.inv(parent_mat.dot(scene_node.matrix))
            bind_array = []
            for y in range(4):
                for x in range(4):
                    bind_array.append(str(bind_mat[y][x]))
            joint_node_dict[scene_node.xmlnode.attrib["sid"]] = {"name": node.name, "bind_mat": ",".join(bind_array)}

        # Add the transform of the node
        if hasattr(scene_node, "matrix"):
            node.transform.set_matrix(scene_node.matrix)

        # Add a Position component
        pos_component = EComponent.from_script("components.position")
        pos_component.property_vals["pos_x"] = str(int(node.transform.trans[0].item() * 1000) / 1000)
        pos_component.property_vals["pos_y"] = str(int(node.transform.trans[1].item() * 1000) / 1000)
        pos_component.property_vals["pos_z"] = str(int(node.transform.trans[2].item() * 1000) / 1000)
        pos_component.property_vals["rot_x"] = str(int(node.transform.rot[0].item() * 1000) / 1000)
        pos_component.property_vals["rot_y"] = str(int(node.transform.rot[1].item() * 1000) / 1000)
        pos_component.property_vals["rot_z"] = str(int(node.transform.rot[2].item() * 1000) / 1000)
        pos_component.property_vals["scale_x"] = str(int(node.transform.scale[0].item() * 1000) / 1000)
        pos_component.property_vals["scale_y"] = str(int(node.transform.scale[1].item() * 1000) / 1000)
        pos_component.property_vals["scale_z"] = str(int(node.transform.scale[2].item() * 1000) / 1000)
        node.add_component(pos_component)

        # Propagate to children
        if hasattr(scene_node, "children") or hasattr(scene_node, "nodes"):
            children = scene_node.nodes if isinstance(scene_node, Scene) else scene_node.children
            for child in children:

                child_node = ColladaImporter.process_node(child, parent_mat if not hasattr(scene_node, "matrix") else parent_mat.dot(scene_node.matrix), joint_node_dict, node_list, folder_name)

                if child_node is not None:

                    # If child is ExtraNode or LightNode, skip the child
                    if isinstance(child, collada.scene.ExtraNode) or isinstance(child, collada.scene.LightNode):
                        continue

                    # If child holds a mesh, add a MeshGraphic to node and skip the child
                    if hasattr(child, "controller"):
                        mesh_renderer = EComponent.from_script("components.mesh_graphic")
                        mesh_renderer.property_vals["mesh"] = folder_name + "/" + child.controller.geometry.name
                        mesh_renderer.property_vals["armature_node"] = joint_node_dict[child.controller.sourcebyid[child.controller.joint_source][0]]["name"]
                        node.data.append(mesh_renderer)
                        continue

                    # If child is a joint and this node isn't, add an armature to the child
                    parent_attrib = scene_node.xmlnode.attrib
                    child_attrib = child.xmlnode.attrib
                    if ("type" not in parent_attrib or parent_attrib["type"].lower() != "joint") and ("type" in child_attrib and child_attrib["type"].lower() == "joint"):
                        armature = EComponent.from_script("components.armature")
                        armature.property_vals["nodes"] = [joint_node_dict[joint_name]["name"] for joint_name in node_list]
                        armature.property_vals["bind_matrices"] = [joint_node_dict[joint_name]["bind_mat"] for joint_name in node_list]
                        child_node.data.append(armature)

                    node.add_child(child_node)

        return node
