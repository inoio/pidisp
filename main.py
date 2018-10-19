# coding=utf8
import time
import epd7in5
from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont
#import imagedata
from time import gmtime, strftime,localtime
import locale
import urllib2

import foo

locale.setlocale(locale.LC_ALL,"de_DE.UTF-8")
EPD_WIDTH = 640
EPD_HEIGHT = 384

OldState = ""

def main():
    global OldState
    epd = epd7in5.EPD()
    epd.init()
    font = ImageFont.truetype('/usr/share/fonts/truetype/freefont/FreeMonoBold.ttf', 88)
    font2 = ImageFont.truetype('/usr/share/fonts/truetype/freefont/FreeMonoBold.ttf', 65)
    font3 = ImageFont.truetype('/usr/share/fonts/dejavu/DejaVuSansMono-Bold.ttf', 35)
    image = Image.new('1', (EPD_WIDTH, EPD_HEIGHT), 1)    # 1: clear the frame
    draw = ImageDraw.Draw(image)
    draw.text((0, 0), u'LÖSUNGSRAUM', font = font, fill = 0)
    newState= foo.getAll()
    draw.text((10,150),newState,font=font3,fill = 0)
    if OldState!=newState:
        print "Draw image"
        epd.display_frame(epd.get_frame_buffer(image))
    OldState=newState

if __name__ == '__main__':
    main()
    while True:
        try:
            main()
        except:
            print("oups")
        time.sleep(60)
