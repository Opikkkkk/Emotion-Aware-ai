def get_ar_content(materi):
    if materi == "Geometri":
        return {
            "object": "cube.glb",
            "description": "Visualisasi kubus 3D menggunakan AR"
        }
    else:
        return {
            "object": "graph.glb",
            "description": "Visualisasi grafik fungsi sederhana"
        }
