# program template for Spaceship
import simplegui
import math
import random

# globals for user interface
WIDTH = 800
HEIGHT = 600
score = 0
lives = 3
time = 0

class ImageInfo:
    def __init__(self, center, size, radius = 0, lifespan = None, animated = False):
        self.center = center
        self.size = size
        self.radius = radius
        if lifespan:
            self.lifespan = lifespan
        else:
            self.lifespan = float('inf')
        self.animated = animated

    def get_center(self):
        return self.center

    def get_size(self):
        return self.size

    def get_radius(self):
        return self.radius

    def get_lifespan(self):
        return self.lifespan

    def get_animated(self):
        return self.animated

    
# art assets created by Kim Lathrop, may be freely re-used in non-commercial projects, please credit Kim
    
# debris images - debris1_brown.png, debris2_brown.png, debris3_brown.png, debris4_brown.png
#                 debris1_blue.png, debris2_blue.png, debris3_blue.png, debris4_blue.png, debris_blend.png
debris_info = ImageInfo([320, 240], [640, 480])
debris_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/debris2_blue.png")

# nebula images - nebula_brown.png, nebula_blue.png
nebula_info = ImageInfo([400, 300], [800, 600])
nebula_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/nebula_blue.f2014.png")

# splash image
splash_info = ImageInfo([200, 150], [400, 300])
splash_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/splash.png")

# ship image
ship_info = ImageInfo([45, 45], [90, 90], 35)
ship_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/double_ship.png")

# missile image - shot1.png, shot2.png, shot3.png
missile_info = ImageInfo([5,5], [10, 10], 3, 50)
missile_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/shot2.png")

# asteroid images - asteroid_blue.png, asteroid_brown.png, asteroid_blend.png
asteroid_info = ImageInfo([45, 45], [90, 90], 40)
asteroid_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/asteroid_blue.png")

# animated explosion - explosion_orange.png, explosion_blue.png, explosion_blue2.png, explosion_alpha.png
explosion_info = ImageInfo([64, 64], [128, 128], 17, 24, True)
explosion_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/explosion_alpha.png")

# sound assets purchased from sounddogs.com, please do not redistribute
soundtrack = simplegui.load_sound("http://commondatastorage.googleapis.com/codeskulptor-assets/sounddogs/soundtrack.mp3")
missile_sound = simplegui.load_sound("http://commondatastorage.googleapis.com/codeskulptor-assets/sounddogs/missile.mp3")
missile_sound.set_volume(.5)
ship_thrust_sound = simplegui.load_sound("http://commondatastorage.googleapis.com/codeskulptor-assets/sounddogs/thrust.mp3")
explosion_sound = simplegui.load_sound("http://commondatastorage.googleapis.com/codeskulptor-assets/sounddogs/explosion.mp3")

# helper functions to handle transformations
def angle_to_vector(ang):
    return [math.cos(ang), math.sin(ang)]

def dist(p,q):
    return math.sqrt((p[0] - q[0]) ** 2+(p[1] - q[1]) ** 2)

# Ship class
class Ship:
    def __init__(self, pos, vel, angle, angle_vel, image, info):
        self.pos = [pos[0],pos[1]]
        self.vel = [vel[0],vel[1]]
        self.angle = angle
        self.angle_vel = angle_vel
        self.image = image
        self.image_center = info.get_center()
        self.image_size = info.get_size()
        self.radius = info.get_radius()
        
    def draw(self,canvas):
        canvas.draw_image(self.image, self.image_center, self.image_size, self.pos, self.image_size, self.angle)
        
    def update(self):
        self.angle += self.angle_vel
        self.pos[0] = (self.pos[0]+self.vel[0])%WIDTH
        self.pos[1] = (self.pos[1]+self.vel[1])%HEIGHT
        # create friction
        self.vel[0] = self.vel[0]*0.995; self.vel[1] = self.vel[1]*0.995; 
        
    def power(self, n):
        if n == "on":
            self.image_center[0] +=90
            ship_thrust_sound.play()
        else:
            self.image_center = [45, 45]
            ship_thrust_sound.rewind()
    
    def shoot(self, n):
        if n == "on":
            a_missile.vel[0] = (self.vel[0]+angle_to_vector(self.angle)[0])*3
            a_missile.vel[1] = (self.vel[1]+angle_to_vector(self.angle)[1])*3
            a_missile.pos[0] = self.pos[0]+(angle_to_vector(my_ship.angle)[0]*self.radius)
            a_missile.pos[1] = self.pos[1]+(angle_to_vector(my_ship.angle)[1]*self.radius)
            missile_sound.play()
        else:
            missile_sound.rewind()    
            
# Sprite class
class Sprite:
    def __init__(self, pos, vel, ang, ang_vel, image, info, sound = None):
        self.pos = [pos[0],pos[1]]
        self.vel = [vel[0],vel[1]]
        self.angle = ang
        self.angle_vel = ang_vel
        self.image = image
        self.image_center = info.get_center()
        self.image_size = info.get_size()
        self.radius = info.get_radius()
        self.lifespan = info.get_lifespan()
        self.animated = info.get_animated()
        self.age = 0
        if sound:
            sound.rewind()
            sound.play()
   
    def draw(self, canvas):
        canvas.draw_image(self.image, self.image_center, self.image_size, self.pos, self.image_size, self.angle)
        
    def update(self):
        self.angle += self.angle_vel
        self.pos[0] += self.vel[0]
        self.pos[1] += self.vel[1]
        
def draw(canvas):
    global time, score, lives
    
    # animiate background
    time += 1
    wtime = (time / 4) % WIDTH
    center = debris_info.get_center()
    size = debris_info.get_size()
    canvas.draw_image(nebula_image, nebula_info.get_center(), nebula_info.get_size(), [WIDTH / 2, HEIGHT / 2], [WIDTH, HEIGHT])
    canvas.draw_image(debris_image, center, size, (wtime - WIDTH / 2, HEIGHT / 2), (WIDTH, HEIGHT))
    canvas.draw_image(debris_image, center, size, (wtime + WIDTH / 2, HEIGHT / 2), (WIDTH, HEIGHT))
    
    # draw Lives and Score
    canvas.draw_text("Lives", [30, 30], 20, "Yellow", "sans-serif")
    canvas.draw_text(str(lives), [45, 55], 20, "White", "sans-serif")
    canvas.draw_text("Score", [700, 30], 20, "Yellow", "sans-serif")
    canvas.draw_text(str(score), [720, 55], 20, "White", "sans-serif")
    
    # draw ship and sprites
    my_ship.draw(canvas)
    a_rock.draw(canvas)
    a_missile.draw(canvas)
    
    # update ship and sprites
    my_ship.update()
    a_rock.update()
    a_missile.update()
            
# timer handler that spawns a rock    
def rock_spawner():
    a_rock.pos[0] = random.randint(0, WIDTH)
    a_rock.pos[1] = random.randint(0, HEIGHT)
    a_rock.angle_vel = random.randint(-5, 5)*0.02
    a_rock.vel[0] = random.randint(-1, 1)
    a_rock.vel[1] = random.randint(-1, 1)
       
# initialize frame
frame = simplegui.create_frame("Asteroids", WIDTH, HEIGHT)

# initialize ship and two sprites
my_ship = Ship([WIDTH / 2, HEIGHT / 2], [0, 0], 0, 0, ship_image, ship_info)
a_rock = Sprite([WIDTH / 3, HEIGHT / 3], [1, 1], 0, 0.01, asteroid_image, asteroid_info)
a_missile = Sprite([2 * WIDTH / 3, 2 * HEIGHT / 3], [0,0], 0, 0, missile_image, missile_info, missile_sound)

def keydown(key):
    if key == simplegui.KEY_MAP["left"]:
            my_ship.angle_vel = -0.05
    elif key == simplegui.KEY_MAP["right"]:
            my_ship.angle_vel = 0.05     
    elif key == simplegui.KEY_MAP["up"]:
            my_ship.power("on")
            my_ship.vel[0] += angle_to_vector(my_ship.angle)[0]*2.5
            my_ship.vel[1] += angle_to_vector(my_ship.angle)[1]*2.5
    elif key == simplegui.KEY_MAP["down"]:
            my_ship.vel[0] = 0
            my_ship.vel[1] = 0   
    elif key == simplegui.KEY_MAP["space"]:
            my_ship.shoot("on")
           
            
def keyup(key):
    if key == simplegui.KEY_MAP["left"]:
            my_ship.angle_vel = 0
    elif key == simplegui.KEY_MAP["right"]:
            my_ship.angle_vel = 0       
    elif key == simplegui.KEY_MAP["up"]:
            my_ship.power("off")      
    elif key == simplegui.KEY_MAP["space"]:
            my_ship.shoot("off")  
            
# register handlers
frame.set_draw_handler(draw)
frame.set_keydown_handler(keydown)
frame.set_keyup_handler(keyup)
timer = simplegui.create_timer(2000.0, rock_spawner)
label = frame.add_label("Up = Forward")   
label = frame.add_label("Down = Stop")   
label = frame.add_label("Left = Turn counter-clockwise")   
label = frame.add_label("Right = Turn clockwise")   
label = frame.add_label("Space = Fire missiles")   
# get things rolling
timer.start()
frame.start()
