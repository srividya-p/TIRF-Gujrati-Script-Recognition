from PIL import Image

image = Image.open('/home/pika/Desktop/TIFR/Tests/TNR12.png')

# image.show()

print(image.format)
print(image.mode) 
print(image.size) 
print(image.palette)

fixed_height = 500
height_percent = (fixed_height / float(image.size[1]))
width_size = int((float(image.size[0]) * float(height_percent)))
image = image.resize((width_size, fixed_height), Image.NEAREST)
image.save('TNR12-rs.png')

