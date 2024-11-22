"""
MODS focal plane
"""

detector_mods = {
    "name": "MODS",
    "description": "MODS",
    "ref_pixel": [4096.0, 1536.0],
    "format": [8192, 4, 0, 0, 3072, 8, 0, 0, 0],
    "focalplane": [1, 1, 2, 2, [0, 1, 0, 1]],
    "roi": [1, 8192, 1, 3072, 1, 1],
    "ext_position": [[1, 1], [2, 1], [1, 2], [2, 2]],
    "jpg_order": [1, 2, 3, 4],
    "ext_number": [1, 2, 3, 4],
    "det_number": [1, 1, 1, 1],
    "det_position": [
        [1, 1],
        [1, 1],
        [1, 1],
        [1, 1],
    ],
    "amp_position": [
        [1, 1],
        [2, 1],
        [1, 2],
        [2, 2],
    ],
    "amp_pixel_position": [
        [1, 1],
        [4080, 1],
        [1, 4080],
        [4080, 1],
    ],
    "ext_name": [
        "im1",
        "im2",
        "im3",
        "im4",
    ],
}
