import picamera
from PIL import Image
from time import sleep

with picamera.PiCamera() as camera:
    camera.resolution = (1280, 720)
    camera.framerate = 24
    camera.start_preview()

    # Load the arbitrarily sized image
    img = Image.open('overlay-400-240.png')
    # Create an image padded to the required size with
    # mode 'RGB'
    width = ((img.size[0] + 31) // 32) * 32
    height = ((img.size[1] + 15) // 16) * 16
    print("pad size",width,height)
    pad = Image.new('RGBA', (width,height))
    # Paste the original image into the padded one
    pad.paste(img, (0, 0))
    print("img size",img.size)
    # Add the overlay with the padded image as the source,
    # but the original image's dimensions
    #b = img.tobytes('rgba')    
    b = pad.tobytes()
    o = camera.add_overlay(b, size=img.size)
    print(camera)
    # By default, the overlay is in layer 0, beneath the
    # preview (which defaults to layer 2). Here we make
    # the new overlay semi-transparent, then move it above
    # the preview
    #o.alpha = 128
    o.layer = 3

    # Wait indefinitely until the user terminates the script
    while True:
        sleep(1)