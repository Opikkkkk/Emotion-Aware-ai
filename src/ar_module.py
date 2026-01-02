# ar_module.py

def get_ar_content(materi):
    # Logika sederhana penentuan objek 3D
    if "Geometri" in materi:
        return {
            "object_file": "cube.glb",
            "description": "Visualisasi Kubus 3D (AR Interactable)",
            "type": "3D Model"
        }
    elif "Aljabar" in materi:
        return {
            "object_file": "graph.glb",
            "description": "Visualisasi Grafik Fungsi Linear",
            "type": "Graph"
        }
    else:
        return {
            "object_file": "star.glb",
            "description": "Bintang Penghargaan (Visualisasi Default)",
            "type": "Reward"
        }