# Credit to RisingLeaf for this script. Posted on Discord here: https://discord.com/channels/251118043411775489/769121688503582730/1264212113468035072

# post:
# sharing a script to batch crop landscape images:

```python
#!/usr/bin/env python3
import pillow_avif
from PIL import Image
import os
import sys

outputf = "./out/"
inputf = "./raw/"
outputExt = ".png"
resX = 720
resY = 360

argc = len(sys.argv)

for x in range(0, argc - 1):
    arg = sys.argv[x + 1]
    if arg == "hdpi":
        resX *= 2
        resY *= 2
        outputExt = "@2x.png"



print("ES landscape croper v1.0")

print("Trying to create output folder 'land'...")
try:
    os.mkdir(outputf)
    print("Success")
except:
    print("Folder already exists")

print("Converting all files in " + inputf + " to " + outputf)
for file in os.listdir(inputf):
    with Image.open(inputf + file) as im:
        print("Converting: " + inputf + file)
        width, height = im.size
        ratio = height / width
        cropped = im.resize((720, int(720 * ratio)), Image.LANCZOS)
        cropped = cropped.crop((0, 0, 720, 360))
        new_name = file.split(".")[0]
        cropped.save(outputf + new_name + outputExt,"PNG")
        print("Created: " + outputf + new_name)

print("Finished")
```
# I used it for the Incipias, allows you to save a bunch of good images into the `raw` folder and then use the script to crop them into the `out` folder. The script can also generate `highdpi` versions if you use it with `hdpi` in the command line. The script requires to be placed in the same folder as the raw folder, not inside the raw folder. Only dependency is pillow.
