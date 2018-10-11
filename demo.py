from panda3d.core import *
from direct.showbase.DirectObject import DirectObject
load_prc_file_data("", "sync-video 0")
load_prc_file_data("", "show-frame-rate-meter  1")
load_prc_file_data('','textures-power-2 None')
from direct.showbase import ShowBase

from sdf_text import SdfText

class App(DirectObject):
    def __init__(self):
        base = ShowBase.ShowBase()
        font=loader.load_font('mono_font.egg')
        txt=SdfText(font)
        txt.set_text('The quick brown fox jumped over the lazy dog.')
        txt.reparent_to(pixel2d)
        txt.set_pos(0,0,-100)
        txt.set_scale(100)

        txt2=SdfText(font)
        txt2.set_text('The quick brown fox jumped over the lazy dog.')
        txt2.reparent_to(pixel2d)
        txt2.set_pos(0,0,-200)
        txt2.set_scale(50)

        txt3=SdfText(font)
        txt3.set_text('The quick brown fox jumped over the lazy dog.')
        txt3.reparent_to(pixel2d)
        txt3.set_pos(0,0,-250)
        txt3.set_scale(25)

        txt4=SdfText(font)
        txt4.set_text('The quick brown fox jumped over the lazy dog.')
        txt4.reparent_to(pixel2d)
        txt4.set_pos(0,0,-275)
        txt4.set_scale(16)

        txt5=SdfText(font)
        txt5.set_text('You can even have color!')
        txt5.reparent_to(pixel2d)
        txt5.set_pos(0,0,-300)
        txt5.set_scale(32)
        txt5.set_hpr(0,0,35)
        txt5.set_text_color(1.0, 0.0, 0.0, 1.0)
        txt5.set_outline_color(1.0, 1.0, 0.0, 1.0)

        txt6=SdfText(font)
        txt6.set_text('Have cool shadow!')
        txt6.reparent_to(pixel2d)
        txt6.set_pos(160,0,-320)
        txt6.set_scale(32)
        txt6.set_outline_strength(0.5)
        txt6.set_outline_color(0.0, 0.0, 0.0, 1.0)
        txt6.set_outline_offset(-2, -4)

        txt7=SdfText(font)
        txt7.set_text('...or an outline')
        txt7.reparent_to(pixel2d)
        txt7.set_pos(180,0,-352)
        txt7.set_scale(32)
        txt7.set_outline_color(0.0, 0.0, 0.0, 1.0)

        txt8=SdfText(font)
        txt8.set_text('...or subtel outline')
        txt8.reparent_to(pixel2d)
        txt8.set_pos(200,0,-384)
        txt8.set_scale(32)
        txt8.set_outline_strength(0.8)
        txt8.set_outline_color(0.0, 0.0, 0.0, 1.0)

        txt9=SdfText(font)
        txt9.set_text('...or very subtel outline')
        txt9.reparent_to(pixel2d)
        txt9.set_pos(220,0,-416)
        txt9.set_scale(32)
        txt9.set_outline_strength(0.5)
        txt9.set_outline_color(0.0, 0.0, 0.0, 1.0)

        #also like this
        txt10=SdfText(font)
        txt10.text='...or NOT subtel at all!!!'
        txt10.reparent_to(pixel2d)
        txt10.pos=(245,0,-455)
        txt10.scale=32
        txt10.outline_strength=5.0
        txt10.outline_color=(0.0, 0.0, 0.0, 1.0)

#Run it
app=App()
base.run()
