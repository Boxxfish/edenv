"""
Handles importing and exporting 3D models.

@author Ben Giacalone
"""
from tools.resimport.collada_importer import ColladaImporter


class ModelImporter:

    # Returns True if file is a 3D model
    @staticmethod
    def is_type(file):
        return ColladaImporter.is_type(file)

    # Imports a model and exports it to the correct internal formats
    @staticmethod
    def export(file):
        if ColladaImporter.is_type(file):
            ColladaImporter.export(file)
