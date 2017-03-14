"""
7 Days to Die TTS decoder
Copyright (C) 2017 Liam Brandt <brandt.liam@gmail.com>

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.
"""

import struct
import time
import pygame
import random

def unpack(bin_file, data_type, length_arg=0):
    #integer or unsigned integer
    if data_type == "i" or data_type == "I":
        return int(struct.unpack(data_type, bin_file.read(4))[0])
    #short or unsigned short
    elif data_type == "h" or data_type == "H":
        return int(struct.unpack(data_type, bin_file.read(2))[0])
    #string
    elif data_type == "s":
        return struct.unpack(str(length_arg) + data_type, bin_file.read(length_arg))[0]
    #char
    elif data_type == "c":
        return struct.unpack(data_type, bin_file.read(1))[0]
    #byte or unsigned byte
    elif data_type == "b" or data_type == "B":
        return int(struct.unpack(data_type, bin_file.read(1))[0])

def draw_prefab(prefab):
    colors = {}

    block_size = (10, 10, 3)

    image_size_x = ( (1*prefab["size_x"]*block_size[0]) + (prefab["size_z"]*block_size[2]) + block_size[0])
    image_size_y = ( (1*prefab["size_y"]*block_size[1]) + (prefab["size_z"]*block_size[2]) + block_size[1])
    image = pygame.surface.Surface((image_size_x, image_size_y))

    z = 0
    for each_layer in prefab["layers"]:
        y = 0
        for each_row in each_layer:
            x = 0
            for each_block in each_row:
                if each_block != 0:
                    if each_block not in colors:
                        colors[each_block] = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
                    draw_color = colors[each_block]
                    draw_x = (x*block_size[0]) + (z*block_size[2])
                    draw_y = (-y*block_size[1]) + (z*block_size[2]) + prefab["size_y"]*block_size[1]
                    draw_rect = (draw_x, draw_y, block_size[0], block_size[1])

                    pygame.draw.rect(image, draw_color, draw_rect, 0)
                    pygame.draw.rect(image, (0, 0, 0), draw_rect, 1)
                x += 1
            y += 1
        z += 1

    print("Block ids and colors: " + str(colors))
    pygame.image.save(image, "output.png")


def main():
    file_name = input("TTS FILE?: ")
    bin_file = open(file_name, "rb")

    prefab = {}

    prefab["header"] = unpack(bin_file, "s", 4)
    prefab["version"] = unpack(bin_file, "I")
    prefab["size_x"] = unpack(bin_file, "H")
    prefab["size_y"] = unpack(bin_file, "H")
    prefab["size_z"] = unpack(bin_file, "H")

    print("Prefab version: " + str(prefab["version"]))
    print("Dimensions: " + str(prefab["size_x"]) + "x" + str(prefab["size_y"]) + "x" + str(prefab["size_z"]))

    prefab["layers"] = []

    for layer_index in range(prefab["size_z"]):
        prefab["layers"].append([])
        for row_index in range(prefab["size_y"]):
            prefab["layers"][layer_index].append([])
            for block_index in range(prefab["size_x"]):
                prefab["layers"][layer_index][row_index].append(None)
                value = unpack(bin_file, "I")
                #get rid of flags, block id can only be less than 2048
                block_id = value & 2047
                flags = value >> 11

                prefab["layers"][layer_index][row_index][block_index] = block_id

    draw_prefab(prefab)

main()
