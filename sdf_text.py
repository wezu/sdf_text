from panda3d.core import TextNode
from panda3d.core import NodePath
from panda3d.core import Vec2
from panda3d.core import Vec3
from panda3d.core import Vec4
from panda3d.core import Shader
from panda3d.core import TransparencyAttrib


__all__ = ['SdfText']

v_shader='''#version 130
in vec4 p3d_Vertex;
in vec2 p3d_MultiTexCoord0;
in vec4 p3d_Color;
uniform mat4 p3d_ModelViewProjectionMatrix;
out vec2 uv;
out vec4 txt_color;
void main()
    {
    gl_Position = p3d_ModelViewProjectionMatrix * p3d_Vertex;
    uv=p3d_MultiTexCoord0;
    txt_color=p3d_Color;
    }
'''
f_shader='''#version 130

uniform sampler2D p3d_Texture0;
uniform vec4 outline_color;
uniform vec2 outline_offset;
uniform float outline_power;

in vec2 uv;
in vec4 txt_color;

void main()
    {
    float dist = texture(p3d_Texture0, uv).a;
    vec2 width = vec2(0.5-fwidth(dist), 0.5+fwidth(dist));
    float alpha = smoothstep(width.x, width.y, dist);
    //supersampling
    float scale = 0.354; // half of 1/sqrt2 - value from internet(???)
    vec2 duv = scale * (dFdx(uv) + dFdy(uv));
    vec4 box = vec4(uv-duv, uv+duv);
    alpha +=0.5*(smoothstep(width.x, width.y, texture(p3d_Texture0, box.xy).a)
            +smoothstep(width.x, width.y, texture(p3d_Texture0, box.zw).a)
            +smoothstep(width.x, width.y, texture(p3d_Texture0, box.xw).a)
            +smoothstep(width.x, width.y, texture(p3d_Texture0, box.zy).a));
    alpha/=3.0; //weighted average, 1*1 + 4*0.5 = 3, so divide by 3
    //outline
    float outline=pow(texture(p3d_Texture0, uv-outline_offset).a, outline_power);
    gl_FragData[0] =mix(vec4(outline_color.rgb, outline_color.a*outline), txt_color, alpha);
    }
'''

class SdfText:
    def __init__(self, font):
        self.txt_node=TextNode('sdf_text_node')
        self.txt_node.set_font(font)
        self.geom=NodePath(self.txt_node.get_internal_geom())
        self.__txt_color=Vec4(1.0, 1.0, 1.0, 1.0)
        self.__outline_color= Vec4(0.0, 0.0, 0.0, 0.0)
        self.__outline_offset= Vec2(0.0)
        self.__outline_power=1.0
        self.parent=None
        self.__pos=Vec3(0.0)
        self.__hpr=Vec3(0.0)
        self.__scale=Vec3(1.0)
        self.__shader=Shader.make(Shader.SL_GLSL, v_shader, f_shader)
        self._make_geom()

    def _make_geom(self):
        '''Refresh or create the actual geom with the text '''
        self.geom=NodePath(self.txt_node.get_internal_geom())
        self.geom.set_shader(self.__shader, 1)
        self.geom.set_shader_input('outline_color', self.__outline_color)
        self.geom.set_shader_input('outline_offset', self.__outline_offset)
        self.geom.set_shader_input('outline_power', self.__outline_power)
        self.geom.set_transparency(TransparencyAttrib.M_alpha, 1)
        if self.parent:
            self.geom.reparent_to(self.parent)
        self.geom.set_pos_hpr_scale(self.__pos, self.__hpr, self.__scale)

    def set_text(self, text):
        '''Sets text'''
        self.txt_node.set_text(text)
        self._make_geom()

    def reparent_to(self, node):
        '''Reparent the text geom to node (as if for NodePath)'''
        self.geom.reparent_to(node)
        self.parent=node
        self._make_geom()

    def set_hpr(self,*args):
        '''Set rotation (as if for NodePath)'''
        self.geom.set_hpr(*args)
        self.__hpr=self.geom.get_hpr()

    def set_pos(self, *args):
        '''Set position (as if for NodePath)'''
        self.geom.set_pos(*args)
        self.__pos=self.geom.get_pos()

    def set_scale(self, *args):
        '''Set scale (as if for NodePath)'''
        self.geom.set_scale(*args)
        self.__scale=self.geom.get_scale()

    def set_text_color(self, *color):
        '''Sets text color (rgba) '''
        self.__txt_color=Vec4(*color)
        self.txt_node.set_text_color(self.__txt_color)
        self._make_geom()


    def set_outline_color(self, *color):
        '''Sets text outline color (rgba) '''
        self.__outline_color=Vec4(*color)
        self.geom.set_shader_input('outline_color', self.__outline_color)

    def set_outline_strength(self, strength):
        '''Sets outline strength.
        Values smaller than 1.0 will make the outline less prominent
        Values greater than 1.0 will make the outline stronger'''
        self.__outline_power=1.0/strength
        self.geom.set_shader_input('outline_power', self.__outline_power)

    def set_outline_offset(self, x_offset=0, y_offset=0):
        '''Outline offset in pixels.
        Will cause artefacts when larger than the glyph padding in the texture!'''
        tex=self.geom.find_all_textures()[0]
        x=tex.get_x_size()
        y=tex.get_y_size()
        self.__outline_offset=Vec2(x_offset/x, y_offset/y)
        self.geom.set_shader_input('outline_offset', self.__outline_offset)

    #properties:
    @property
    def outline_offset(self):
        return self.__outline_offset

    @outline_offset.setter
    def outline_offset(self, value):
        self.set_outline_offset(value)

    @property
    def outline_strength(self):
        return self.__outline_strength

    @outline_strength.setter
    def outline_strength(self, value):
        self.set_outline_strength(value)

    @property
    def outline_color(self):
        return self.__outline_color

    @outline_color.setter
    def outline_color(self, value):
        self.set_outline_color(value)

    @property
    def text_color(self):
        return self.__text_color

    @text_color.setter
    def text_color(self, value):
        self.set_text_color(value)

    @property
    def scale(self):
        return self.__scale

    @scale.setter
    def scale(self, value):
        self.set_scale(value)

    @property
    def pos(self):
        return self.__pos

    @pos.setter
    def pos(self, value):
        self.set_pos(value)

    @property
    def hpr(self):
        return self.__hpr

    @hpr.setter
    def hpr(self, value):
        self.set_hpr(value)

    @property
    def text(self):
        return self.self.txt_node.get_text()

    @text.setter
    def text(self, value):
        self.set_text(value)
