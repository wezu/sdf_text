# Signed Distance Field Text for Panda3D
![screenshot](https://github.com/wezu/sdf_text/blob/master/screen.png)

To use the SdfText you will need font files generated with egg-mkfont (shipped with the Panda3D SDK) with the -sdf option. For this demo I used some extra padding around the glyphs so that the outline wont bleed over.
```
egg-mkfont monosb.ttf -sdf -ppu 32 -pm 4 -o mono_font.egg
```
See the code for hint on how to use it, there are few comments, but most functions are self explanatory (like set_outline_color()).
