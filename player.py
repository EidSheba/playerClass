import glfw
from OpenGL.GL import *
from OpenGL.GLU import *
import numpy as np
from PIL import Image

class Player:
    def __init__(self):
        self.x = 0.0
        self.y = -0.8
        self.width = 0.2
        self.height = 0.2
        self.speed = 0.05
        self.move_left = False
        self.move_right = False
        self.move_up = False
        self.move_down = False

        # Load texture
        self.texture = self.load_texture("Assets/Player.png")

    def load_texture(self, image_path):
        # OpenGL texture loading from a file using PIL
        img = Image.open(image_path)
        img = img.convert("RGBA")  # Convert to RGBA format for OpenGL

        img_data = np.array(list(img.getdata()), np.uint8)

        texture_id = glGenTextures(1)
        glBindTexture(GL_TEXTURE_2D, texture_id)

        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)

        glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA, img.width, img.height, 0, GL_RGBA, GL_UNSIGNED_BYTE, img_data)

        return texture_id

    def handle_input(self, window):
        # Check for key presses
        if glfw.get_key(window, glfw.KEY_LEFT) == glfw.PRESS:
            self.move_left = True
        else:
            self.move_left = False

        if glfw.get_key(window, glfw.KEY_RIGHT) == glfw.PRESS:
            self.move_right = True
        else:
            self.move_right = False

        if glfw.get_key(window, glfw.KEY_UP) == glfw.PRESS:
            self.move_up = True
        else:
            self.move_up = False

        if glfw.get_key(window, glfw.KEY_DOWN) == glfw.PRESS:
            self.move_down = True
        else:
            self.move_down = False

    def update(self):
        if self.move_left and (self.x - self.width / 2) > -1:
            self.x -= self.speed
        if self.move_right and (self.x + self.width / 2) < 1:
            self.x += self.speed
        if self.move_up and (self.y + self.height / 2) < 1:
            self.y += self.speed
        if self.move_down and (self.y - self.height / 2) > -1:
            self.y -= self.speed

    def draw(self):
        glEnable(GL_TEXTURE_2D)
        glBindTexture(GL_TEXTURE_2D, self.texture)

        glBegin(GL_QUADS)
        glTexCoord2f(0, 0)
        glVertex2f(self.x - self.width / 2, self.y - self.height / 2)

        glTexCoord2f(1, 0)
        glVertex2f(self.x + self.width / 2, self.y - self.height / 2)

        glTexCoord2f(1, 1)
        glVertex2f(self.x + self.width / 2, self.y + self.height / 2)

        glTexCoord2f(0, 1)
        glVertex2f(self.x - self.width / 2, self.y + self.height / 2)
        glEnd()

        glDisable(GL_TEXTURE_2D)

def main():
    if not glfw.init():
        return

    # Create the window
    window = glfw.create_window(800, 600, "OpenGL Player Movement", None, None)
    if not window:
        glfw.terminate()
        return

    glfw.make_context_current(window)

    # Create a player instance
    player = Player()

    while not glfw.window_should_close(window):
        glClear(GL_COLOR_BUFFER_BIT)

        # Handle input
        player.handle_input(window)

        # Update player position
        player.update()

        # Draw player
        player.draw()

        glfw.swap_buffers(window)
        glfw.poll_events()

    glfw.terminate()

if __name__ == "__main__":
    main()
