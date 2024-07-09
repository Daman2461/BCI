import tkinter as tk
from math import cos, sin, radians
class LightToggleApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Light Toggle App")
        
        # Set the background color to black
        self.canvas = tk.Canvas(root, width=400, height=300, bg='black')
        self.canvas.pack()

        self.light_on = False
        self.light_off_color = "grey"
        self.light_on_color = "yellow"
        self.light_radius = 30
        self.light_x = 200
        self.light_y = 120
        
        # Draw the bulb (combination of an oval and a rectangle)
        self.bulb_oval = self.canvas.create_oval(
            self.light_x - self.light_radius, 
            self.light_y - self.light_radius, 
            self.light_x + self.light_radius, 
            self.light_y + self.light_radius, 
            fill=self.light_off_color, outline=''
        )
        
        self.bulb_rect = self.canvas.create_rectangle(
            self.light_x - self.light_radius // 2, 
            self.light_y + self.light_radius, 
            self.light_x + self.light_radius // 2, 
            self.light_y + self.light_radius * 1.5, 
            fill='#C0C0C0', outline=''
        )
        
        self.button = tk.Button(root, text="Toggle Light", command=self.toggle_light)
        self.button.pack(pady=20)

    def toggle_light(self):
        self.light_on = not self.light_on
        new_color = self.light_on_color if self.light_on else self.light_off_color
        self.canvas.delete("ray")
        
        if self.light_on:
            self.draw_light_rays()
        self.canvas.itemconfig(self.bulb_oval, fill=new_color)
        self.canvas.itemconfig(self.bulb_rect, fill='#C0C0C0')
        self.canvas.delete("ray")
        
        if self.light_on:
            self.draw_light_rays()
    def draw_light_rays(self):
        for angle in range(0, 360, 45):  # Light rays every 45 degrees
            x_end = self.light_x + 60 * cos(radians(angle))
            y_end = self.light_y + 60 * sin(radians(angle))
            self.canvas.create_line(
                self.light_x, self.light_y, x_end, y_end,
                fill='#FFFF66', width=2, tags="ray"
            )

if __name__ == "__main__":
    root = tk.Tk()
    app = LightToggleApp(root)
    root.mainloop()
