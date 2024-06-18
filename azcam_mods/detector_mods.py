"""
MODS focal plane
"""

# MODS focal plane
detector_mods = {
    "name": "MODS",
    "description": "MODS",
    "ref_pixel": [4080.0, 4080.0],
    "format": [4080, 4, 0, 20, 4080, 0, 0, 0, 0],
    "focalplane": [2, 2, 4, 2, [0, 1, 0, 1]],
    "roi": [1, 4080, 1, 4080, 1, 1],
    "jpg_order": [1, 2, 3, 4],
    "det_number": [1, 1, 2, 2],
    "amp_pixel_position": [
        [1, 1],
        [4080, 1],
        [4081, 1],
        [8160, 1],
    ],
    "det_gap": [
        [0, 0],
        [0, 0],
        [0, 0],
        [0, 0],
    ],
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
    "ext_name": [
        "im1",
        "im2",
        "im3",
        "im4",
    ],
    "ext_number": [1, 2, 3, 4],
}

# test dewar
detector_mods_test_dewar = {
    "name": "MODS test dewar",
    "description": "MODS Test Dewar",
    "ref_pixel": [4080.0, 4080.0],
    "format": [4080 * 2, 4, 0, 20, 4080 * 2, 0, 0, 0, 0],
    "focalplane": [2, 2, 4, 2, [0, 1, 0, 1, 0, 1, 0, 1]],
    "roi": [1, 4080 * 2, 1, 4080 * 2, 1, 1],
    "jpg_order": [1, 2, 3, 4, 5, 6, 7, 8],
    "det_number": [1, 1, 2, 2, 3, 3, 4, 4],
    "amp_pixel_position": [
        [1, 1],
        [4080, 1],
        [4081, 1],
        [8160, 1],
        [1, 8160],
        [4080, 8160],
        [4081, 8160],
        [8160, 8160],
    ],
    "det_gap": [
        [0, 0],
        [0, 0],
        [0, 0],
        [0, 0],
    ],
    # should change both location
    "det_position": [
        [1, 1],
        [1, 1],
        [2, 1],
        [2, 1],
        [1, 2],
        [1, 2],
        [2, 2],
        [2, 2],
    ],
    "ext_position": [
        [1, 1],
        [2, 1],
        [3, 1],
        [4, 1],
        [1, 2],
        [2, 2],
        [3, 2],
        [4, 2],
    ],
    "ext_name": [
        "im1",
        "im2",
        "im3",
        "im4",
        "im5",
        "im6",
        "im7",
        "im8",
    ],
    "ext_number": [1, 2, 3, 4, 5, 6, 7, 8],
}
