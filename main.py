import time
import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *
from PIL import Image
import numpy as np
import os
import math
import random

# Mass ranges and their corresponding evolutionary paths
MASS_RANGES = {
    "Very Low Mass": {
        "range": (0.08, 0.4),  # Solar masses
        "stages": [
            {
                "name": "Nebula",
                "duration": 5000,
                "color": (0.6, 0.4, 0.8),
                "radius": 0.0,
                "emission": 0.2,
                "texture": "star_texture.jpg",
                "description": "A vast cloud of gas and dust where stars form",
                "transition_time": 1000,
                "particle_count": 1000,
                "particle_spread": 2.0
            },
            {
                "name": "Brown Dwarf",
                "duration": float('inf'),  # Final stage
                "color": (0.8, 0.4, 0.2),
                "radius": 0.3,
                "emission": 0.1,
                "texture": "NO-TEXTURE",
                "description": "A failed star without enough mass to sustain nuclear fusion",
                "transition_time": 0
            }
        ]
    },
    "Low Mass": {
        "range": (0.4, 2.0),
        "stages": [
            {
                "name": "Nebula",
                "duration": 5000,
                "color": (0.6, 0.4, 0.8),
                "radius": 0.0,
                "emission": 0.2,
                "texture": "star_texture.jpg",
                "description": "A vast cloud of gas and dust where stars form",
                "transition_time": 1000,
                "particle_count": 5000,
                "particle_spread": 2.5
            },
            {
                "name": "Protostar",
                "duration": 3000,
                "color": (1.0, 0.7, 0.3),
                "radius": 0.8,
                "emission": 0.5,
                "texture": "star_texture.jpg",
                "description": "An early stage as gravity pulls matter inward",
                "transition_time": 1000
            },
            {
                "name": "Main Sequence",
                "duration": 8000,
                "color": (1.0, 1.0, 0.8),
                "radius": 1.0,
                "emission": 0.8,
                "texture": "star_texture.jpg",
                "description": "The stable phase, powered by hydrogen fusion",
                "transition_time": 1000
            },
            {
                "name": "Red Giant",
                "duration": 4000,
                "color": (1.0, 0.2, 0.0),
                "radius": 2.0,
                "emission": 0.6,
                "texture": "NO-TEXTURE",
                "description": "An expanded phase as the core depletes hydrogen",
                "transition_time": 1000
            },
            {
                "name": "White Dwarf",
                "duration": float('inf'),
                "color": (0.9, 0.9, 1.0),
                "radius": 0.5,
                "emission": 0.4,
                "texture": "NO-TEXTURE",
                "description": "The final stage - a dense, cooling stellar remnant",
                "transition_time": 0
            }
        ]
    },
    "Medium Mass": {
        "range": (2.0, 8.0),
        "stages": [
            {
                "name": "Nebula",
                "duration": 4000,
                "color": (0.6, 0.4, 0.8),
                "radius": 0.0,
                "emission": 0.2,
                "texture": "star_texture.jpg",
                "description": "A vast cloud of gas and dust where stars form",
                "transition_time": 1000,
                "particle_count": 10000,
                "particle_spread": 3.0
            },
            {
                "name": "Protostar",
                "duration": 2000,
                "color": (1.0, 0.8,  0.4),
                "radius": 1.2,
                "emission": 0.6,
                "texture": "star_texture.jpg",
                "description": "A rapidly contracting pre-stellar object",
                "transition_time": 800
            },
            {
                "name": "Main Sequence",
                "duration": 6000,
                "color": (1.0, 1.0, 1.0),
                "radius": 1.5,
                "emission": 1.0,
                "texture": "star_texture.jpg",
                "description": "A bright, massive star burning hydrogen",
                "transition_time": 1000
            },
            {
                "name": "Red Supergiant",
                "duration": 3000,
                "color": (1.0, 0.1, 0.0),
                "radius": 3.0,
                "emission": 0.7,
                "texture": "NO-TEXTURE",
                "description": "A huge, cool giant nearing the end of its life",
                "transition_time": 1000
            },
            {
                "name": "White Dwarf",
                "duration": float('inf'),
                "color": (1.0, 1.0, 1.0),
                "radius": 0.6,
                "emission": 0.5,
                "texture": "NO-TEXTURE",
                "description": "The exposed core after ejecting outer layers",
                "transition_time": 0
            }
        ]
    },
    "High Mass": {
        "range": (8.0, 50.0),
        "stages": [
            {
                "name": "Nebula",
                "duration": 3000,
                "color": (0.6, 0.4, 0.8),
                "radius": 0.0,
                "emission": 0.2,
                "texture": "star_texture.jpg",
                "description": "A massive cloud of gas and dust",
                "transition_time": 1000,
                "particle_count": 15000,
                "particle_spread": 3.5
            },
            {
                "name": "Protostar",
                "duration": 1500,
                "color": (1.0, 0.9, 0.5),
                "radius": 2.0,
                "emission": 0.8,
                "texture": "star_texture.jpg",
                "description": "A rapidly evolving massive protostar",
                "transition_time": 500
            },
            {
                "name": "Main Sequence",
                "duration": 4000,
                "color": (0.8, 0.8, 1.0),
                "radius": 2.5,
                "emission": 1.2,
                "texture": "star_texture.jpg",
                "description": "A massive, bright, blue star",
                "transition_time": 1000
            },
            {
                "name": "Blue Supergiant",
                "duration": 2000,
                "color": (0.4, 0.4, 1.0),
                "radius": 3.5,
                "emission": 1.0,
                "texture": "NO-TEXTURE",
                "description": "An extremely luminous blue giant",
                "transition_time": 800
            },
            {
                "name": "Red Supergiant",
                "duration": 1500,
                "color": (1.0, 0.0, 0.0),
                "radius": 4.0,
                "emission": 0.8,
                "texture": "NO-TEXTURE",
                "description": "A massive red giant before supernova",
                "transition_time": 500
            },
            {
                "name": "Supernova",
                "duration": 500,
                "color": (1.0, 1.0, 0.0),
                "radius": 5.0,
                "emission": 2.0,
                "texture": "NO-TEXTURE",
                "description": "A massive explosion marking the star's death",
                "transition_time": 200,
                "particle_count": 2000,
                "particle_spread": 6.0
            },
            {
                "name": "Neutron Star",
                "duration": float('inf'),
                "color": (0.9, 0.9, 1.0),
                "radius": 0.2,
                "emission": 0.6,
                "texture": "NO-TEXT",
                "description": "A super-dense stellar remnant after supernova",
                "transition_time": 0
            }
        ]
    }
}

class Particle:
    def __init__(self, spread):
        angle = random.uniform(0, 2 * math.pi)
        radius = random.uniform(0, spread)
        self.x = math.cos(angle) * radius
        self.y = math.sin(angle) * radius
        self.z = random.uniform(-spread/2, spread/2)
        self.size = random.uniform(0.02, 0.08)
        self.color = self.generate_nebula_color()
        self.rotation = random.uniform(0, 360)
        self.rotation_speed = random.uniform(-0.5, 0.5)

    def generate_nebula_color(self):
        colors = [
            (0.6, 0.4, 0.8, 0.3),
            (0.3, 0.4, 0.8, 0.3),
            (0.8, 0.4, 0.6, 0.3),
            (0.4, 0.6, 0.8, 0.3),
        ]
        return random.choice(colors)

    def update(self):
        self.rotation += self.rotation_speed
        if self.rotation >= 360:
            self.rotation -= 360

def draw_particle(particle):
    glPushMatrix()
    glTranslatef(particle.x, particle.y, particle.z)
    glRotatef(particle.rotation, 0, 1, 0)

    glEnable(GL_BLEND)
    glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)

    glDisable(GL_LIGHTING)
    glColor4f(*particle.color)

    glBegin(GL_QUADS)
    size = particle.size
    glVertex3f(-size, -size, 0)
    glVertex3f(size, -size, 0)
    glVertex3f(size, size, 0)
    glVertex3f(-size, size, 0)
    glEnd()

    glEnable(GL_LIGHTING)
    glDisable(GL_BLEND)
    glPopMatrix()

def generate_light_map(size=256):
    texture = np.zeros((size, size, 4), dtype=np.uint8)
    for x in range(size):
        for y in range(size):
            height = (np.sin(x / 20.0) * np.cos(y / 25.0) * 0.3 + 0.7) + np.random.rand() * 0.1
            brightness = int(max(0, min(1, height)) * 255)
            texture[x, y] = [brightness, brightness, brightness, 255]
    return texture

def load_texture(image_path):
    try:
        if os.path.exists(image_path):
            image = Image.open(image_path).transpose(Image.FLIP_TOP_BOTTOM)
            image_data = image.convert("RGBA").tobytes()
            width, height = image.size
        else:
            texture_data = generate_light_map()
            image_data = texture_data.tobytes()
            width, height = texture_data.shape[:2]

        texture_id = glGenTextures(1)
        glBindTexture(GL_TEXTURE_2D, texture_id)
        glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA, width, height, 0, GL_RGBA, GL_UNSIGNED_BYTE, image_data)

        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_REPEAT)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_REPEAT)

        return texture_id
    except Exception as e:
        print(f"Error loading texture {image_path}: {e}")
        return None

def interpolate_value(start, end, progress):
    cos_progress = (1 - math.cos(progress * math.pi)) / 2
    return start + (end - start) * cos_progress

def interpolate_color(start_color, end_color, progress):
    return tuple(
        interpolate_value(start_color[i], end_color[i], progress)
        for i in range(3)
    )

class TextureManager:
    def __init__(self):
        self.textures = {}

    def get_texture(self, stage):
        if stage["texture"] not in self.textures:
            self.textures[stage["texture"]] = load_texture(stage["texture"])
        return self.textures[stage["texture"]]

class MassController:
    def __init__(self):
        self.current_mass = 1.0
        self.current_range = "Low Mass"
        self .mass_change_speed = 0.1

    def update_mass(self, delta):
        old_range = self.current_range
        self.current_mass = max(0.08, min(50.0, self.current_mass + delta * self.mass_change_speed))

        for range_name, range_data in MASS_RANGES.items():
            if range_data["range"][0] <= self.current_mass <= range_data["range"][1]:
                self.current_range = range_name
                break

        return self.current_range != old_range

    def get_stages(self):
        return MASS_RANGES[self.current_range]["stages"]

class StarLifeCycleRenderer:
    def __init__(self, mass_controller, texture_manager):
        self.mass_controller = mass_controller
        self.texture_manager = texture_manager
        self.current_stage_index = 0
        self.next_stage_index = 1
        self.stage_timer = 0
        self.transition_timer = 0
        self.is_transitioning = False
        self.speed_factor = 1.0
        self.particles = []
        self.initialize_particles()

    def initialize_particles(self):
        stages = self.mass_controller.get_stages()
        current_stage = stages[self.current_stage_index]
        if "particle_count" in current_stage:
            spread = current_stage["particle_spread"]
            self.particles = [Particle(spread) for _ in range(current_stage["particle_count"])]
        else:
            self.particles.clear()

    def handle_mass_change(self):
        stages = self.mass_controller.get_stages()
        self.current_stage_index = 0
        self.next_stage_index = 1
        self.stage_timer = 0
        self.transition_timer = 0
        self.is_transitioning = False
        self.initialize_particles()

    def update(self, delta_time):
        if not self.is_transitioning:
            self.stage_timer += delta_time
            current_stage = self.mass_controller.get_stages()[self.current_stage_index]

            if "particle_count" in current_stage:
                for particle in self.particles:
                    particle.update()

            if self.stage_timer >= current_stage["duration"] / 1000 and current_stage["duration"] != float('inf'):
                self.is_transitioning = True
                self.transition_timer = 0
                self.next_stage_index = self.current_stage_index + 1
        else:
            current_stage = self.mass_controller.get_stages()[self.current_stage_index]
            self.transition_timer += delta_time
            transition_progress = min(1, self.transition_timer / (current_stage["transition_time"] / 1000))

            if transition_progress >= 1:
                self.current_stage_index = self.next_stage_index
                self.stage_timer = 0
                self.is_transitioning = False
                if self.current_stage_index > 0:
                    self.particles.clear()
                return self.get_current_stage_params()

            return self.get_interpolated_stage_params(transition_progress)

        return self.get_current_stage_params()

    def render(self, angle):
        current_stage_info = self.get_current_stage_params()
        current_stage = current_stage_info["stage"]

        glPushMatrix()
        glRotatef(angle, 0, 1, 0)
        texture_id = self.texture_manager.get_texture(current_stage)
        draw_sphere(
            current_stage["radius"],
            current_stage["color"],
            current_stage.get("emission", 0.5),
            texture_id
        )
        glPopMatrix()

        if "particle_count" in current_stage:
            for particle in self.particles:
                draw_particle(particle)

    def get_current_stage_params(self):
        stage = self.mass_controller.get_stages()[self.current_stage_index]
        return {
            "stage": stage,
            "time_in_stage": self.stage_timer
        }

    def get_interpolated_stage_params(self, progress):
        current_stage = self.mass_controller.get_stages()[self.current_stage_index]
        next_stage = self.mass_controller.get_stages()[self.next_stage_index]

        return {
            "stage": {
                "name": f"{current_stage['name']} -> {next_stage['name']}",
                "duration": 1000,
                "color": interpolate_color(current_stage['color'], next_stage['color'], progress),
                "radius": interpolate_value(current_stage['radius'], next_stage['radius'], progress),
                "emission": interpolate_value(current_stage['emission'], next_stage['emission'], progress),
                "texture": current_stage['texture'],
                "description": f"Transitioning from {current_stage['name']} to {next_stage['name']}"
            },
            "time_in_stage": 0.0
        }

def draw_sphere(radius, color, emission, texture_id):
    glEnable(GL_TEXTURE_2D)
    glBindTexture(GL_TEXTURE_2D, texture_id)

    ambient = [x * 0.1 for x in color]
    diffuse = [x * 0.3 for x in color]
    emission_color = [x * emission for x in color]

    glMaterialfv(GL_FRONT, GL_AMBIENT, [*ambient, 1.0])
    glMaterialfv(GL_FRONT, GL_DIFFUSE, [*diffuse, 1.0])
    glMaterialfv(GL_FRONT, GL_SPECULAR, [0.2, 0.2, 0.2, 1.0])
    glMaterialfv(GL_FRONT, GL_EMISSION, [*emission_color, 1.0])
    glMaterialf(GL_FRONT, GL_SHININESS, 10.0)

    quad = gluNewQuadric()
    gluQuadricTexture(quad, GL_TRUE)
    gluQuadricNormals(quad, GLU_SMOOTH)
    gluSphere(quad, radius, 64, 64)
    gluDeleteQuadric(quad)

    glDisable(GL_TEXTURE_2D)

def render_text(screen, stage, time_in_stage, speed_factor, mass_controller):
    text_surface = pygame.Surface((800, 600), pygame.SRCALPHA)
    font = pygame.font.Font(None, 36)

    mass_text = f"Star Mass: {mass_controller.current_mass:.2f} solar masses ({mass_controller.current_range})"
    mass_surface = font.render(mass_text, True, (255, 255, 255))
    text_surface.blit(mass_surface, (10, 10))

    name_surface = font.render(f"Stage: {stage['name']}", True, (255, 255, 255))
    text_surface.blit(name_surface, (10, 50))

    words = stage['description'].split()
    line = []
    y = 90
    for word in words:
        line.append(word)
        line_surface = font.render(' '.join(line), True, (255, 255, 255))
        if line_surface.get_width() > 780:
            line.pop()
            line_surface = font.render(' '.join(line), True, (255, 255, 255))
            text_surface.blit(line_surface, (10, y))
            line = [word]
            y += 30
    if line:
        line_surface = font.render(' '.join(line), True, (255, 255, 255))
        text_surface.blit(line_surface, (10, y))

    time_remaining = (stage['duration'] / 1000) / speed_factor - time_in_stage
    time_surface = font.render(f"Time until next stage: {time_remaining:.1f}s", True, (255, 255, 255))
    text_surface.blit(time_surface, (10, 550))

    screen.blit(text_surface, (0, 0))

def main():
    pygame.init()
    width, height = 800, 600
    angle = 0
    zoom_level = 1
    first_zoom = -10.0
    second_zoom = -5.0
    last_zoom = -2.5
    current_zoom = second_zoom

    pygame.display.set_mode((width, height), DOUBLEBUF | OPENGL)
    pygame_surface = pygame.Surface((width, height), pygame.SRCALPHA)

    pygame.display.set_caption("Interactive Star Life Cycle Simulation")

    gluPerspective(45, (width / height), 0.1, 50.0)
    glTranslatef(0.0, 0.0, current_zoom)

    glEnable(GL_DEPTH_TEST)
    glEnable(GL_LIGHTING)
    glEnable(GL_LIGHT0)
    glLightfv(GL_LIGHT0, GL_POSITION, [0.0, 0.0, 2.0, 1.0])
    glLightfv(GL_LIGHT0, GL_DIFFUSE, [0.3, 0.3, 0.3, 1.0])
    glLightModelfv(GL_LIGHT_MODEL_AMBIENT, [0.05, 0.05, 0.05, 1.0])

    clock = pygame.time.Clock()
    texture_manager = TextureManager()
    mass_controller = MassController()
    star_renderer = StarLifeCycleRenderer(mass_controller, texture_manager)
    paused = False

    while True:
        for event in pygame.event.get():
            if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
                return

            if event.type == KEYDOWN:
                if event.key == K_UP:
                    star_renderer.speed_factor = min(4.0, star_renderer.speed_factor * 1.5)
                elif event.key == K_DOWN:
                    star_renderer.speed_factor = max(0.1, star_renderer.speed_factor / 1.5)
                elif event.key == K_SPACE:
                    paused = not paused

        keys = pygame.key.get_pressed()
        if keys[K_LEFT]:
            if mass_controller.update_mass(-0.1):
                star_renderer.handle_mass_change()
        if keys[K_RIGHT]:
            if mass_controller.update_mass(0.1):
                star_renderer.handle_mass_change()

        if keys[K_z]:
            if zoom_level == 2:
                zoom_level = 1
                current_zoom = first_zoom
                glMatrixMode(GL_PROJECTION)
                glLoadIdentity()
                gluPerspective(45, (width / height), 0.1, 50.0)
                glMatrixMode(GL_MODELVIEW)
                glLoadIdentity()
                glTranslatef(0.0, 0.0, current_zoom)
                time.sleep(1)
            elif zoom_level == 3:
                zoom_level = 2
                current_zoom = second_zoom
                glMatrixMode(GL_PROJECTION)
                glLoadIdentity()
                gluPerspective(45, (width / height), 0.1, 50.0)
                glMatrixMode(GL_MODELVIEW)
                glLoadIdentity()
                glTranslatef(0.0, 0.0, current_zoom)
                time.sleep(1)
        if keys[K_x]:
            if zoom_level == 1:
                zoom_level = 2
                current_zoom = second_zoom
                glMatrixMode(GL_PROJECTION)
                glLoadIdentity()
                gluPerspective(45, (width / height), 0.1, 50.0)
                glMatrixMode(GL_MODELVIEW)
                glLoadIdentity()
                glTranslatef(0.0, 0.0, current_zoom)
                time.sleep(1)
            elif zoom_level == 2:
                zoom_level = 3
                current_zoom = last_zoom
                glMatrixMode(GL_PROJECTION)
                glLoadIdentity()
                gluPerspective(45, (width / height), 0.1, 50.0)
                glMatrixMode(GL_MODELVIEW)
                glLoadIdentity()
                glTranslatef(0.0, 0.0, current_zoom)
                time.sleep(1)

        if not paused:
            delta_time = clock.get_time() / 1000 * star_renderer.speed_factor
            current_stage_info = star_renderer.update(delta_time)
            current_stage = current_stage_info["stage"]
            stage_timer = current_stage_info["time_in_stage"]

        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        glClearColor(0.0, 0.0, 0.02, 1.0)

        star_renderer.render(angle)

        glMatrixMode(GL_PROJECTION)
        glPushMatrix()
        glLoadIdentity()
        glOrtho(0, width, height, 0, -1, 1)
        glMatrixMode(GL_MODELVIEW)
        glPushMatrix()
        glLoadIdentity()

        glDisable(GL_DEPTH_TEST)
        glDisable(GL_LIGHTING)

        pygame_surface.fill((0, 0, 0, 0))
        render_text(pygame_surface, current_stage, stage_timer, star_renderer.speed_factor, mass_controller)

        text_data = pygame.image.tostring(pygame_surface, 'RGBA', True)
        glEnable(GL_BLEND)
        glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
        glDrawPixels(width, height, GL_RGBA, GL_UNSIGNED_BYTE, text_data)
        glDisable(GL_BLEND)

        glMatrixMode(GL_PROJECTION)
        glPopMatrix()
        glMatrixMode(GL_MODELVIEW)
        glPopMatrix()
        glEnable(GL_DEPTH_TEST)
        glEnable(GL_LIGHTING)

        pygame.display.flip()
        clock.tick(60)
        angle += 0.5

if __name__ == "__main__":
    main()
    pygame.quit()