"""
MODS focal plane
"""

detector_mods = {
    "name": "MODS",
    "description": "MODS",
    "ref_pixel": [4080.0, 4080.0],
    "format": [8192, 4, 0, 48, 3072, 8, 0, 0, 0],
    "focalplane": [1, 1, 2, 2, [0, 1, 0, 1]],
    "roi": [1, 8192, 1, 3072, 1, 1],
    "jpg_order": [1, 2, 3, 4],
    "det_number": [1, 1, 2, 2],
    "det_position": [
        [1, 1],
        [1, 1],
        [2, 1],
        [2, 1],
    ],
    "ext_position": [
        [1, 1],
        [2, 1],
        [3, 1],
        [4, 1],
    ],
    "ext_number": [1, 2, 3, 4],
}
