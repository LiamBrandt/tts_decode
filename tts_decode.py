import struct, time

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
	import pygame, random

	colors = {}

	rect_size = 10

	image = pygame.surface.Surface((2*prefab["size_x"]*rect_size+(prefab["size_z"]*rect_size), 2*prefab["size_y"]*rect_size+(prefab["size_z"]*rect_size)))

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
					draw_rect = (x*rect_size + (z*rect_size), -y*rect_size + (z*rect_size) + prefab["size_y"]*rect_size, rect_size, rect_size)

					pygame.draw.rect(image, draw_color, draw_rect, 0)
					pygame.draw.rect(image, (0, 0, 0), draw_rect, 1)
				x += 1
			y += 1
		z += 1

	pygame.image.save(image, "output.png")


def main():
	file_name = raw_input("TTS FILE?: ")
	bin_file = open(file_name, "rb")

	prefab = {}

	prefab["header"] = unpack(bin_file, "s", 8)
	prefab["size_z"] = unpack(bin_file, "H")
	prefab["size_y"] = unpack(bin_file, "H")
	prefab["size_x"] = unpack(bin_file, "H")

	dimensions = [prefab["size_x"], prefab["size_y"], prefab["size_z"]]

	prefab["layers"] = []

	for layer_index in range(dimensions[0]):
		prefab["layers"].append([])
		for row_index in range(dimensions[1]):
			prefab["layers"][layer_index].append([])
			for block_index in range(dimensions[2]):
				prefab["layers"][layer_index][row_index].append(None)
				value = unpack(bin_file, "I")
				prev_value = prefab["layers"][layer_index][row_index][block_index]

				prefab["layers"][layer_index][row_index][block_index] = value

				#print("prev_value: " + str(prev_value) + " value: " + str(value) + " index: [" + str(layer_index) + "][" + str(row_index) + "][" + str(block_index) + "]")

	draw_prefab(prefab)

main()
