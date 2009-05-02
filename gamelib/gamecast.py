from glob import glob
import geom
import random
from math import cos, sin, radians, degrees, atan, atan2, pi, sqrt
from pyglet.image import Animation, AnimationFrame, load
from pymunk.vec2d import Vec2d

from cocos.sprite import NotifierSprite, Sprite

class NotifierSprite(Sprite):
    def register(self, *args):
        pass

from boids import merge, seek, cap, avoid_group
from shapes import BulletShape, RayShape, AgentShape, ZombieShape, WallShape
from tiless_editor.layers.collision import Circle
import sound

# NOTE: select wich class will be used as Zombie near EOF

COLLISION_GROUP_FATHER = 1

def get_animation(anim_name):
    return Animation([AnimationFrame(load(img_file), 0.2)
                      for img_file in  glob('data/img/%s*.png' % anim_name)])


class Agent(NotifierSprite):
    def __init__(self, img, position=(0,0)):
        super(Agent, self).__init__(img, position)
        self.anims = {}
        self.current_anim = 'idle'

        self.shape = AgentShape(self)
        self.just_born = True

    def update_position(self, position):
        # test for collisions
        self.old_position = self.position
        self.updating = True
        collision_layer = self.parent

        self.position = position
        return
        self.collision = None
        collision_layer.step()
        if self.collision:
            if self.just_born:
                self.x += random.choice([-1,1])*70
                self.y += random.choice([-1,1])*70
                self.target = self.position = (self.x, self.y)
                self.target = self.position
                return
            
            self.on_collision(self.collision)
            f = getattr(self.collision, "on_collision", None)
            if f is not None:
                f(self)

            self.position = position[0], self.old_position[1]
            self.collision = None
            collision_layer.step()
            if self.collision:
                self.position = self.old_position[0], position[1]
                self.collision = None
                collision_layer.step()
                if self.collision:
                    self.position = self.old_position
        else:
            if self.just_born:
                self.just_born = False

    def _on_collision(self, other):
        # used internally for collision testing
        if isinstance(other, Bullet):
            self.on_collision(other)
        if not self.updating:
            return
        self.collision = other

    def play_anim(self, anim_name):
        self.image = self.anims[anim_name]
        self.image_anchor = (self.image.frames[0].image.width / 2,
                             self.image.frames[0].image.height / 2)
        self.current_anim = anim_name

    def on_collision(self, other):
        if isinstance(other, Bullet):
            self.die()

    def die(self):
        # only mark it as dead, as I cannot remove the pymunk stuff while within the collision detection phase
        # as segfaults might occur
        game_layer = self.player.game_layer
        game_layer.dead_items.add(self)


class Father(Agent):
    def __init__(self, img, position, game_layer):
        super(Father, self).__init__(img, position)
        self.shape.group = COLLISION_GROUP_FATHER

        self._old_state = {'position': position}
        self.speed = 0
        self.position = position
        self.schedule(self.update)
        self.game_layer = game_layer
        self.acceleration = 0
        self.updating = False
        self.rotation_speed = 0
        self.collision = False
        self.anims = {'idle': get_animation('father_idle'),
                      'walk': get_animation('father_walk'),
                      }
        self.current_anim = 'idle'
        self.family = {}
        self.selected_relative = None
        self.just_born = False

    def on_collision(self, other):
        if isinstance(self.collision, Agent):
            pass#sound.play("player_punch")

    def update(self, dt):
        # update speed
        if self.acceleration != 0 and abs(self.speed) < 130:
            self.speed += self.acceleration*100*dt

        self.rotation += 110 * self.rotation_speed * dt
        # update the position, based on the speed
        nx = (self.x + cos( radians(-self.rotation) ) * self.speed * dt)
        ny = (self.y + sin( radians(-self.rotation) ) * self.speed * dt)
        # FIXME: for some reason the x/y attributes don't update the position attribute correctly
        new_position = (nx, ny)

        self.update_position(new_position)

        # update layer position (center camera)
        self.game_layer.update(dt)

    def look_at(self, px, py):
        # translate mouse position to world
        px = px - self.game_layer.x
        py = py - self.game_layer.y
        self.target = (px, py)
        pl_x, pl_y = self.position[0], self.position[1]
        self.rotation = -(atan2(py - pl_y, px - pl_x) / pi * 180)

    def fire(self):
        bullet = Bullet(get_animation('bullet'), self)
        self.game_layer.add_bullet(bullet)


class Relative(Agent):
    def __init__(self, img, position, player):
        super(Relative, self).__init__(img, position)
        self._old_state = {}
        self.speed = 100
        self.schedule(self.update)
        self.player = player
        self.updating = False
        self.collision = False
        self.current_anim = 'idle'
        self.target = self.position

    def update(self, dt):
        # move to designated target or stay and fight

        # save old position
        self._old_state = {'position': self.position, 'rotation': self.rotation}

        locals = []
        goal = seek(self.x, self.y, self.target[0], self.target[1])

        delta = geom.angle_rotation(radians(self.rotation), radians(goal))
        delta = degrees(delta)
        max_r = 270
        delta = cap(delta, -max_r, max_r) * dt
        self.rotation += delta

        # FIXME: for some reason the x/y attributes don't update the position attribute correctly
        self.position = (self.x, self.y)
        self.rotation = self.rotation % 360
        # update position
        a = -self.rotation
        nx = (self.x + cos( radians(a) ) * self.speed * dt)
        ny = (self.y + sin( radians(a) ) * self.speed * dt)

        self.update_position((nx, ny))

        if self.position != self.old_position:
            self.play_anim('walk')

        else:
            if self.current_anim != 'idle':
                self.play_anim('idle')


class Boy(Relative):
    def __init__(self, img, position, player):
        super(Boy, self).__init__(img, position, player)
        self.anims = {'idle': get_animation('boy_idle'),
                      'walk': get_animation('boy_walk'),
                      }
        self.sounds = {}
        player.family['boy'] = self


class Girl(Relative):
    def __init__(self, img, position, player):
        super(Girl, self).__init__(img, position, player)
        self.anims = {'idle': get_animation('girl_idle'),
                      'walk': get_animation('girl_walk'),
                      }
        self.sounds = {}
        player.family['girl'] = self


class Mother(Relative):
    def __init__(self, img, position, player):
        super(Mother, self).__init__(img, position, player)
        self.anims = {'idle': get_animation('mother_idle'),
                      'walk': get_animation('mother_walk'),
                      }
        self.sounds = {}
        player.family['mother'] = self


# ZombieBoid , the old zombie class
class ZombieBoid(Agent):
    def __init__(self, img, player):
        super(Zombie, self).__init__(img)
        self._old_state = {}
        self.speed = 100
        self.schedule(self.update)
        self.player = player
        self.updating = False
        self.collision = False
        self.anims = {'idle': get_animation('zombie1_idle'),
                      'walk': get_animation('zombie1_walk'),
                      }
        self.current_anim = 'idle'
        self.shape = ZombieShape(self)

    def update(self, dt):
        # save old position
        self._old_state = {'position': self.position, 'rotation': self.rotation}

        locals = []
        b = self
        goal = seek(b.x, b.y, self.player.x, self.player.y)
        #print "GOAL", goal
        escape, danger = avoid_group(b.x, b.y, locals)
        #print "danger", danger, escape
        if danger < 50:
            #print "escape"
            chosen = escape
        elif danger > 100:
            #print "goal"
            chosen = goal
        else:
            d = (danger-50)/50
            chosen = merge([(goal, d), (escape, 1-d)])

        delta = geom.angle_rotation(radians(b.rotation), radians(chosen))
        delta = degrees(delta)
        max_r = 270
        delta = cap(delta, -max_r, max_r) * dt
        b.rotation += delta

        # FIXME: for some reason the x/y attributes don't update the position attribute correctly
        b.position = (b.x, b.y)
        b.rotation = b.rotation % 360
        # update position
        a = -b.rotation
        nx = (b.x + cos( radians(a) ) * b.speed * dt)
        ny = (b.y + sin( radians(a) ) * b.speed * dt)

        self.update_position((nx, ny))

        if self.position != self.old_position:
            self.play_anim('walk')

        else:
            if self.current_anim != 'idle':
                self.play_anim('idle')

# actualmente es copia de ZombieBoid, esto es preparacion para implantar
class ZombieWpt(Agent):
    def __init__(self, img, player):
        super(Zombie, self).__init__(img)
        self._old_state = {}
        self.speed = 100
        self.schedule(self.update)
        self.player = player
        self.updating = False
        self.collision = False
        self.anims = {'idle': get_animation('zombie1_idle'),
                      'walk': get_animation('zombie1_walk'),
                      }
        self.current_anim = 'idle'
        self.shape = ZombieShape(self)

    def update(self, dt):
        # save old position
        self._old_state = {'position': self.position, 'rotation': self.rotation}

        locals = []
        b = self
        goal = seek(b.x, b.y, self.player.x, self.player.y)
        #print "GOAL", goal
        escape, danger = avoid_group(b.x, b.y, locals)
        #print "danger", danger, escape
        if danger < 50:
            #print "escape"
            chosen = escape
        elif danger > 100:
            #print "goal"
            chosen = goal
        else:
            d = (danger-50)/50
            chosen = merge([(goal, d), (escape, 1-d)])

        delta = geom.angle_rotation(radians(b.rotation), radians(chosen))
        delta = degrees(delta)
        max_r = 270
        delta = cap(delta, -max_r, max_r) * dt
        b.rotation += delta

        # FIXME: for some reason the x/y attributes don't update the position attribute correctly
        b.position = (b.x, b.y)
        b.rotation = b.rotation % 360
        # update position
        a = -b.rotation
        nx = (b.x + cos( radians(a) ) * b.speed * dt)
        ny = (b.y + sin( radians(a) ) * b.speed * dt)

        self.update_position((nx, ny))

        if self.position != self.old_position:
            self.play_anim('walk')

        else:
            if self.current_anim != 'idle':
                self.play_anim('idle')
    def on_collision(self, other):
        #print 'Zombie on_collision', other
        #if isinstance(self.collision, Bullet):
        #    import pdb; pdb.set_trace()
        #elif isinstance(other.shape, Bullet):
        if isinstance(other, Bullet):
            print 'Zombie hit at position', self.position
            self.die(other)

    def die(self, bullet):
        # only mark it as dead, as I cannot remove the pymunk stuff while within the collision detection phase
        # as segfaults might occur
        game_layer = self.player.game_layer
        game_layer.dead_items.add(self)


class Bullet(NotifierSprite):
    def __init__(self, img, agent):
        super(Bullet, self).__init__(img, agent.position, agent.rotation, agent.scale)

        self.anims = {}
        self.agent = agent

        position = agent.position
        WEAPON_RANGE = 200

        offset = Vec2d(WEAPON_RANGE, 0).rotated(-self.rotation)
        target = offset+position
        shape = BulletShape(self, position, target)
        shape.group = agent.shape.group
        self.shape = shape


class Ray(NotifierSprite):
    def __init__(self, agent, target):
        super(Ray, self).__init__('img/bullet.png', agent.position, agent.rotation, agent.scale)
        shape = RayShape(self, agent.position, target)
        shape.group = agent.shape.group
        self.shape = shape


class Wall(NotifierSprite):
    def __init__(self, child):
        img = {'filename': child.path, 'position': child.position,
               'rotation': child.rotation, 'scale': child.scale,
               'opacity': child.opacity, 'rect': child.rect}
        super(Wall, self).__init__(str(img['filename']), img['position'],
                                   img['rotation'], img['scale'],
                                   img['opacity'])
        self.label = None
        self.path = img['filename']
        self.rect = img['rect']
        self.shape = WallShape(self)


#select here wich Zombie class
Zombie = ZombieBoid