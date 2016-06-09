import time, random, pygame, sys

pygame.init()

screen = pygame.display.set_mode([1000, 1000])

block_colors = {
	"0": (0, 0, 0),
}

SETTINGS = {
	"version": 0,
	"tile_size": 8,
}

INFO = {
	"xMultiplier": 0,
	"yMultiplier": 0,
	"xOffset": 0,
	"yOffset": 200,
	"layer": 0,
}

class Prefab(object):
	def __init__(self, size):
		self.size = size
		
		self.current_layer = 0
		self.y = self.size[0]*SETTINGS["tile_size"]
		self.x = self.size[2]*SETTINGS["tile_size"]
		
		self.layers = [Layer(0)]
		
	def add_block(self, id):
		new_block = Block([self.x, self.y], id)
	
		#try to add block to appropriate layer, if non-existent, make a new layer
		try:
			self.layers[self.current_layer].blocks.append(new_block)
		except:
			self.layers.append(Layer(self.current_layer))
			self.layers[self.current_layer].blocks.append(new_block)

		self.y -= SETTINGS["tile_size"]
		if self.y <= 0:
			self.y = self.size[0]*SETTINGS["tile_size"]
			self.x -= SETTINGS["tile_size"]
			
		if self.x <= 0:
			self.y = self.size[0]*SETTINGS["tile_size"]
			self.x = self.size[2]*SETTINGS["tile_size"]
			self.current_layer += 1
			
	def draw(self, index):
		screen.fill([0, 0, 0])
	
		#print("drawing layer " + str(index))
		self.layers[index].draw()
	
	def draw3d(self):
		screen.fill([0, 0, 0])
		for each_layer in self.layers:
			if each_layer.index <= INFO["layer"]:
				each_layer.draw()
	
class Layer(object):
	def __init__(self, index):
		self.index = index
	
		self.blocks = []
		
	def draw(self):
		#print("layer drawing " + str(len(self.blocks)) + " different blocks")
	
		for each_block in self.blocks:
			each_block.draw(self.index*INFO["xMultiplier"] + INFO["xOffset"], self.index*INFO["yMultiplier"] + INFO["yOffset"])
	
class Block(object):
	def __init__(self, pos, id):
		self.pos = pos
		self.id = id
	
	def draw(self, offsetX, offsetY):
		if self.id != "0":
			pygame.draw.rect(screen, block_colors[self.id], (self.pos[0] + offsetX, self.pos[1] + offsetY, SETTINGS["tile_size"], SETTINGS["tile_size"]), 0)
			pygame.draw.rect(screen, (0, 0, 0), (self.pos[0] + offsetX, self.pos[1] + offsetY, SETTINGS["tile_size"], SETTINGS["tile_size"]), 1)
	
def read_integer(file, size):
	bin_int = file.read(size)
	
	bin_int = ":".join("{0:x}".format(ord(c)) for c in bin_int)
	
	bytes = bin_int.split(":")
		
	i = -1
	for each_byte in bytes:
		i += 1
		#pads hex values with zeros
		if len(each_byte) == 1:
			bytes[i] = "0" + each_byte

	#reverse order of the bytes
	bytes = bytes[::-1]
	
	#make hex string of bytes
	int_string = "0x"
	for each_byte in bytes:
		int_string += each_byte

	#converts hex string to dec int
	return int(int_string, 0)
	
	
def main():
	dim_list = []

	file_name = raw_input("tts file to display: ")
	
	print("loading file...")
	tts_file = open(file_name + ".tts", "rb")
	
	#tts in ascii
	tts_file.read(4)
	
	#version
	SETTINGS["version"] = read_integer(tts_file, 4)
	print("FILE VERSION " + str(SETTINGS["version"]))
	
	#dimensions
	for each_dim in range(3):
		dim_list.append(read_integer(tts_file, 2))
		
	print("DIMENSIONS: " + str(dim_list))
	
	#extra header data
	tts_file.read(2)
	
	#old version of prefabs
	if SETTINGS["version"] == 4 or SETTINGS["version"] == 3:
		prefab = Prefab((dim_list[1], dim_list[0], dim_list[2]))
	#up to date version
	else:
		prefab = Prefab((dim_list[0], dim_list[2], dim_list[1]))
	
	#read blocks and add them to prefab
	reading = True
	while(reading):
		#try to read next block, if cannot be read, stop reading
		try:
			block_id = str(read_integer(tts_file, 4))
		except:
			reading = False
			break
			
		#add new block color if block has never been seen before
		if block_id not in block_colors:
			block_colors[block_id] = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
			#print("Added new block color for ID: " + hex(int(block_id)) + ", COLOR: " + str(block_colors[block_id]))

		#add the block to the prefab
		prefab.add_block(block_id)
		
	#flip prefab layers because prefab is read inverted
	prefab.layers = prefab.layers[::-1]
		
	INFO["layer"] = len(prefab.layers) - 1
	
	print("loaded!")
	
	prefab.draw3d()
	pygame.display.flip()
	
	while(True):
		mouse_pressed = pygame.mouse.get_pressed()
		mouse_rel = pygame.mouse.get_rel()
		if mouse_pressed[0]:
			INFO["xOffset"] += mouse_rel[0]
			INFO["yOffset"] += mouse_rel[1]

			prefab.draw3d()
			pygame.display.flip()
	
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				sys.exit(0)
			if event.type == pygame.KEYDOWN:
				if event.key == pygame.K_LEFT:
					INFO["xMultiplier"] -= 1
				if event.key == pygame.K_RIGHT:
					INFO["xMultiplier"] += 1
				if event.key == pygame.K_UP:
					INFO["yMultiplier"] -= 1
				if event.key == pygame.K_DOWN:
					INFO["yMultiplier"] += 1
					
				if event.key == pygame.K_w:
					if INFO["layer"] > 0:
						INFO["layer"] -= 1
				if event.key == pygame.K_s:
					INFO["layer"] += 1
				if event.key == pygame.K_a:
					INFO["xOffset"] -= SETTINGS["tile_size"]
				if event.key == pygame.K_d:
					INFO["xOffset"] += SETTINGS["tile_size"]
					
				#only redraw if a key was pressed, meaning the image likely changed
				prefab.draw3d()
				pygame.display.flip()
			
main()