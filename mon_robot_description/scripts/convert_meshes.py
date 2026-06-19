#!/usr/bin/env python3
"""
Script pour convertir les fichiers STEP/SLDPRT en formats compatibles avec Gazebo
Necessite FreeCAD d'etre installe ou utiliser des services en ligne
"""

import os
import subprocess
import sys
from pathlib import Path

# Installations recommandees :
# Ubuntu: sudo apt-get install freecad python3-freecad
# Windows: Installer FreeCAD depuis https://www.freecadweb.org/

def convert_step_to_stl_freecad(step_file, output_dir):
    """Convertit STEP en STL en utilisant FreeCAD en mode batch"""
    try:
        import FreeCAD
        import Import
    except ImportError:
        print("FreeCAD non trouve. Installez-le d'abord:")
        print("  Ubuntu: sudo apt-get install freecad python3-freecad")
        print("  Windows: https://www.freecadweb.org/")
        return False

    try:
        doc = FreeCAD.open(step_file)
        base_name = Path(step_file).stem
        output_file = os.path.join(output_dir, f"{base_name}.stl")

        Import.export(doc.Objects, output_file)
        print(f"Converti: {step_file} -> {output_file}")
        return True
    except Exception as e:
        print(f"Erreur conversion {step_file}: {e}")
        return False

def convert_using_meshlab(step_file, output_dir):
    """Utilise MeshLab si disponible (alternative)"""
    try:
        base_name = Path(step_file).stem
        output_file = os.path.join(output_dir, f"{base_name}.obj")

        subprocess.run([
            'meshlabserver',
            '-i', step_file,
            '-o', output_file
        ], check=True)
        print(f"Converti avec MeshLab: {step_file} -> {output_file}")
        return True
    except (subprocess.CalledProcessError, FileNotFoundError):
        print("MeshLab non disponible")
        return False

def main():
    repo_root = Path(__file__).resolve().parent.parent.parent
    solidworks_dir = repo_root / "Solidworks"
    meshes_output = Path(__file__).resolve().parent.parent / "meshes"

    meshes_output.mkdir(parents=True, exist_ok=True)

    step_files = list(solidworks_dir.glob("*.step")) + list(solidworks_dir.glob("*.stp"))

    if not step_files:
        print("Aucun fichier STEP trouve dans le dossier Solidworks/")
        return 1

    print(f"Trouve {len(step_files)} fichier(s) STEP")

    success_count = 0
    for step_file in step_files:
        print(f"\nTraitement: {step_file.name}")

        if convert_step_to_stl_freecad(str(step_file), str(meshes_output)):
            success_count += 1
        elif convert_using_meshlab(str(step_file), str(meshes_output)):
            success_count += 1

    print(f"\n{'='*50}")
    print(f"Conversion reussie: {success_count}/{len(step_files)}")
    print(f"Fichiers generes dans: {meshes_output}")

    return 0 if success_count == len(step_files) else 1

if __name__ == "__main__":
    sys.exit(main())
