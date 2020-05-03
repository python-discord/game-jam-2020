import arcade
from arcade.experimental import geometry

# Do the math to figure out our screen dimensions
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
SCREEN_TITLE = "Basic Renderer"


class ColorIsolationWindow(arcade.Window):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)

        self.isolation_color = (0.0, 0.0, 0.0)
        self.threshold = 2.3

        self.fs_program = self.ctx.program(
            vertex_shader="""
            #version 330
            in vec2 in_vert;
            in vec2 in_uv;
            out vec2 v_uv;
            void main() {
                gl_Position = vec4(in_vert, 0.0, 1.0);
                v_uv = in_uv;
            }
            """,
            fragment_shader="""
            #version 330
            
            vec3 rgb2xyz( vec3 c ) {
                vec3 tmp;
                tmp.x = ( c.r > 0.04045 ) ? pow( ( c.r + 0.055 ) / 1.055, 2.4 ) : c.r / 12.92;
                tmp.y = ( c.g > 0.04045 ) ? pow( ( c.g + 0.055 ) / 1.055, 2.4 ) : c.g / 12.92,
                tmp.z = ( c.b > 0.04045 ) ? pow( ( c.b + 0.055 ) / 1.055, 2.4 ) : c.b / 12.92;
                const mat3 mat = mat3(
                    0.4124, 0.3576, 0.1805,
                    0.2126, 0.7152, 0.0722,
                    0.0193, 0.1192, 0.9505
                );
                return 100.0 * (tmp * mat);
            }
            
            vec3 xyz2lab( vec3 c ) {
                vec3 n = c / vec3(95.047, 100, 108.883);
                vec3 v;
                v.x = ( n.x > 0.008856 ) ? pow( n.x, 1.0 / 3.0 ) : ( 7.787 * n.x ) + ( 16.0 / 116.0 );
                v.y = ( n.y > 0.008856 ) ? pow( n.y, 1.0 / 3.0 ) : ( 7.787 * n.y ) + ( 16.0 / 116.0 );
                v.z = ( n.z > 0.008856 ) ? pow( n.z, 1.0 / 3.0 ) : ( 7.787 * n.z ) + ( 16.0 / 116.0 );
                return vec3(( 116.0 * v.y ) - 16.0, 500.0 * ( v.x - v.y ), 200.0 * ( v.y - v.z ));
            }
            
            vec3 rgb2lab( vec3 c ) {
                vec3 lab = xyz2lab( rgb2xyz( c ) );
                return vec3( lab.x / 100.0, 0.5 + 0.5 * ( lab.y / 127.0 ), 0.5 + 0.5 * ( lab.z / 127.0 ));
            }
            
            vec3 lab2xyz( vec3 c ) {
                float fy = ( c.x + 16.0 ) / 116.0;
                float fx = c.y / 500.0 + fy;
                float fz = fy - c.z / 200.0;
                return vec3(
                     95.047 * (( fx > 0.206897 ) ? fx * fx * fx : ( fx - 16.0 / 116.0 ) / 7.787),
                    100.000 * (( fy > 0.206897 ) ? fy * fy * fy : ( fy - 16.0 / 116.0 ) / 7.787),
                    108.883 * (( fz > 0.206897 ) ? fz * fz * fz : ( fz - 16.0 / 116.0 ) / 7.787)
                );
            }
            
            vec3 xyz2rgb( vec3 c ) {
                const mat3 mat = mat3(
                    3.2406, -1.5372, -0.4986,
                    -0.9689, 1.8758, 0.0415,
                    0.0557, -0.2040, 1.0570
                );
                vec3 v = (c / 100.0) * mat;
                vec3 r;
                r.x = ( v.r > 0.0031308 ) ? (( 1.055 * pow( v.r, ( 1.0 / 2.4 ))) - 0.055 ) : 12.92 * v.r;
                r.y = ( v.g > 0.0031308 ) ? (( 1.055 * pow( v.g, ( 1.0 / 2.4 ))) - 0.055 ) : 12.92 * v.g;
                r.z = ( v.b > 0.0031308 ) ? (( 1.055 * pow( v.b, ( 1.0 / 2.4 ))) - 0.055 ) : 12.92 * v.b;
                return r;
            }
            
            vec3 lab2rgb( vec3 c ) {
                return xyz2rgb( lab2xyz( vec3(100.0 * c.x, 2.0 * 127.0 * (c.y - 0.5), 2.0 * 127.0 * (c.z - 0.5)) ) );
            }
            
            
            vec3 rgb2hsv(vec3 c)
            {
                vec4 K = vec4(0.0, -1.0 / 3.0, 2.0 / 3.0, -1.0);
                vec4 p = mix(vec4(c.bg, K.wz), vec4(c.gb, K.xy), step(c.b, c.g));
                vec4 q = mix(vec4(p.xyw, c.r), vec4(c.r, p.yzx), step(p.x, c.r));
            
                float d = q.x - min(q.w, q.y);
                float e = 1.0e-10;
                return vec3(abs(q.z + (q.w - q.y) / (6.0 * d + e)), d / (q.x + e), q.x);
            }
            
            vec3 hsv2rgb(vec3 c)
            {
                vec4 K = vec4(1.0, 2.0 / 3.0, 1.0 / 3.0, 3.0);
                vec3 p = abs(fract(c.xxx + K.xyz) * 6.0 - K.www);
                return c.z * mix(K.xxx, clamp(p - K.xxx, 0.0, 1.0), c.y);
            }
            
            
            float deltaE(vec3 c1, vec3 c2) {
                return  length(c1-c2);   
            }
            
            in vec2 v_uv;
            uniform sampler2D tex;
            uniform vec3 special_color;
            uniform float threshold;
            out vec4 out_color;
            void main() {
                vec3 col = texture(tex, v_uv).xyz;
                if (deltaE(rgb2lab(special_color), rgb2lab(col)) > threshold) {
                    float g = 0.2989 * col.x + 0.5870 * col.y + 0.1140 * col.z;
                    col = vec3(g);
                }
                out_color =  vec4(col, 1.);
            }
            """,
        )

        self.fs_quad = geometry.quad_fs(size=(2.0, 2.0))
        self.ost = self.ctx.texture(self.get_framebuffer_size())
        self.fb = self.ctx.framebuffer(color_attachments=self.ost)

    def on_draw(self) -> None:
        try:
            self.clear()
            # render the scene to a off-screen buffer for processing
            self.fb.use()
            self.render()

            # switch back to the windows fbo
            self.use()
            # bind the texture
            self.ost.use(0)
            self.fs_program["special_color"] = self.isolation_color
            self.fs_program["threshold"] = self.threshold
            # render the effect
            self.fs_quad.render(self.fs_program)

        except Exception as e:
            print(f"Error: {e}")
            exit(1)

    def render(self) -> None:
        """
        Override this function to add your custom drawing code.
        """
        pass

    def set_isolation_color(self, color) -> None:
        self.isolation_color = (color[0] / 255.0, color[1] / 255.0, color[2] / 255.0)

    def set_isolation_threshold(self, threshold):
        self.threshold = threshold


class VCRDistortionWindow(arcade.Window):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)

        self.elapsed_time = 0

        self.fs_program = self.ctx.program(
            vertex_shader="""
            #version 330
            in vec2 in_vert;
            in vec2 in_uv;
            out vec2 v_uv;
            void main() {
                gl_Position = vec4(in_vert, 0.0, 1.0);
                v_uv = in_uv;
            }
            """,
            fragment_shader="""
            #version 330
            float noise(vec2 p, float time)
            {
                vec2 uv = vec2(1.,2.*cos(time))*time*8. + p*1.;
                float s = fract(sin(dot(p.xy ,vec2(12.9898,78.233))) * 43758.5453);
                s *= s;
            
                return s;
            
            }
            
            float onOff(float a, float b, float c, float time)
            {
                return step(c, sin(time + a*cos(time*b)));
            }
            
            float ramp(float y, float start, float end)
            {
                float inside = step(start,y) - step(end,y);
                float fact = (y-start)/(end-start)*inside;
                return (1.-fact) * inside;
            }
            
            float stripes(vec2 uv, float time)
            {
            
                float noi = noise(uv*vec2(0.5,1.) + vec2(1.,3.), time);
                return ramp(mod(uv.y*4. + time/2.+sin(time + sin(time*0.63)),1.),0.5,0.6)*noi;
            }
            
            vec2 getVideoUV(vec2 uv, float time)
            {
                vec2 look = uv;
                float window = 1./(1.+20.*(look.y-mod(time/4.,1.))*(look.y-mod(time/4.,1.)));
                look.x = look.x + sin(look.y*10. + time)/50.*onOff(4.,4.,.3, time)*(1.+cos(time*80.))*window;
                float vShift = 0.4*onOff(2.,3.,.9, time)*(sin(time)*sin(time*20.) +
                                                     (0.5 + 0.1*sin(time*200.)*cos(time)));
                look.y = mod(look.y + vShift, 1.);
                return look;
            }
            
            
            vec2 screenDistort(vec2 uv)
            {
                uv -= vec2(.5,.5);
                uv = uv*1.2*(1./1.2+2.*uv.x*uv.x*uv.y*uv.y);
                uv += vec2(.5,.5);
                return uv;
            }
            
            out vec4 fragColor;
            in vec2 v_uv;
            uniform sampler2D tex;
            uniform float iTime;
            void main() {
                vec2 uv = v_uv;
                //vec3 video = texture(tex, getVideoUV(uv, iTime)).xyz;
                vec3 video = texture(tex, uv).xyz;
                float vigAmt = 3.+.3*sin(iTime + 5.*cos(iTime*50.));
                float vignette = (1.-vigAmt*(uv.y-.5)*(uv.y-.5))*(1.-vigAmt*(uv.x-.5)*(uv.x-.5));
            
                video += stripes(uv, iTime);
                video += noise(uv*2., iTime)/20.;
                video *= vignette;
                video *= (12.+mod(uv.y*30.+iTime,1.))/13.;
            
                fragColor = vec4(video,1.0);
            }
            """,
        )

        self.fs_quad = geometry.quad_fs(size=(2.0, 2.0))
        self.ost = self.ctx.texture(self.get_framebuffer_size())
        self.fb = self.ctx.framebuffer(color_attachments=self.ost)

    def on_draw(self) -> None:
        try:
            self.clear()
            # render the scene to a off-screen buffer for processing
            self.fb.use()
            self.render()

            # switch back to the windows fbo
            self.use()
            # bind the texture
            self.ost.use(0)
            self.fs_program['iTime'] = self.elapsed_time / 2.
            # render the effect
            self.fs_quad.render(self.fs_program)

        except Exception as e:
            print(f"Error: {e}")
            exit(1)

    def render(self) -> None:
        """
        Override this function to add your custom drawing code.
        """
        pass
