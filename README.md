# tts_decode
A simple tool to read the [7 Days to Die](http://store.steampowered.com/app/251570/) prefab format. Prefab files have the extension tts.

A description of the tts file format can be found [here](https://7daystodie.gamepedia.com/Prefabs).

Written for [Python 3](https://www.python.org/ftp/python/3.6.0/python-3.6.0.exe).
Uses [pygame](http://www.pygame.org/news) to generate prefab images. 

## Usage
Run the python and enter the path to a tts file relative to the current directory. The tool will output an image of the prefab with air blocks invisible and every other block given a random color.
