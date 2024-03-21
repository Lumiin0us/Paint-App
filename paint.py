import Tkinter as tk 
import math


def polygon(sides):
	angle = 2 * math.pi / sides
	return [
		(
			math.sin(angle * i), - math.cos(angle * i)
		)
		for i in range(sides)
	]

def star(sides):
	sides = sides * 2
	angle = 2 * math.pi / sides
	return [
		(
			math.sin(angle * i), - math.cos(angle * i)
		) if i%2 == 0 else (
			math.sin(angle * i)/2.5, - math.cos(angle * i)/2.5
		)
		for i in range(sides)
	]

def transform_points(start_x, start_y, end_x, end_y, points):
	width = end_x - start_x
	height = end_y - start_y
	return [
		(start_x + width/2 + point[0] * width/2, start_y + height/2 + point[1] * height/2)
		for point in points
	]

class PaintApp():
	def __init__(self):
		paint_window = tk.Tk() # Tk is name of class in tk/Tkinter library
		paint_window.title('PaintApp')

		settings_frame = tk.Frame(paint_window) # this new frame exists in paint_window container

		tk.Label(settings_frame, text="Mode:").pack(side=tk.LEFT) # the new label should exist in settings_frame container and is aligned to the left side
		mode = tk.StringVar()
		mode.set("draw")
		mode_dropdown = tk.OptionMenu(settings_frame, mode, "draw", "erase", "delete")
		mode_dropdown.pack(side=tk.LEFT)

		tk.Label(settings_frame, text="Shape:").pack(side=tk.LEFT)
		shape = tk.StringVar()
		shape.set("line")
		shape_dropdown = tk.OptionMenu(settings_frame, shape, "line", "rectangle", "oval",
			"star (5)", "star (6)", "pentagon", "hexagon", "triangle")
		shape_dropdown.pack(side=tk.LEFT)

		tk.Label(settings_frame, text="Line Style:").pack(side=tk.LEFT)
		line_style = tk.StringVar()
		line_style.set("normal")
		line_style_dropdown = tk.OptionMenu(settings_frame, line_style, "normal", "dotted", "dashed")
		line_style_dropdown.pack(side=tk.LEFT)

		tk.Label(settings_frame, text="Color:").pack(side=tk.LEFT)
		color = tk.StringVar()
		color.set("black")
		color_dropdown = tk.OptionMenu(settings_frame, color, "red", "green", "blue", "yellow", "black", "white")
		color_dropdown.pack(side=tk.LEFT)

		tk.Label(settings_frame, text="Fill:").pack(side=tk.LEFT)
		fill = tk.StringVar()
		fill.set("false")
		fill_dropdown = tk.OptionMenu(settings_frame, fill, "true", "false")
		fill_dropdown.pack(side=tk.LEFT)

		canvas = tk.Canvas(paint_window, width=800, height=500) # passing paint_window, width and height in canvas's object (python creates/initializes by __inti__ a new object whenever a class is called)
		canvas.config(highlightthickness = 1, highlightbackground = "black")
		canvas.bind("<ButtonPress-1>", self.mouse_pressed)
		canvas.bind("<ButtonRelease-1>", self.mouse_released)

		# layout and sizing for our window
		settings_frame.pack()
		canvas.pack()

		# make some variables available by self, so other functions can access them
		self.c = canvas
		self.shape = shape
		self.line_style = line_style
		self.color = color
		self.fill = fill
		self.mode = mode
		self.paint_window = paint_window

	def run(self):
		self.paint_window.mainloop() # special tkinter function that starts the GUI

	def mouse_pressed(self, event):
		print("Mouse pressed", event.x, event.y)
		# store mouse position, so we can use it in mouse_released function
		self.start_x = event.x
		self.start_y = event.y

	def mouse_released(self, event):
		print("Mouse released", self.start_x, self.start_y, event.x, event.y)

		if (self.mode.get() == "delete"):
			self.c.delete("current")
		else:
			if self.line_style.get() == "normal":
				dash = None
			elif self.line_style.get() == "dotted":
				dash = (1, 3)
			elif self.line_style.get() == "dashed":
				dash = (10, 5)

			line_color = self.color.get()
			fill_color = ''
			if self.fill.get() == "true":
				fill_color = line_color

			if self.mode.get() == "erase":
				line_color = "white"
				fill_color = "white"

			if self.shape.get() == "line":
				self.c.create_line(self.start_x, self.start_y, event.x, event.y,
					dash = dash,
					fill = line_color)
			elif self.shape.get() == "rectangle":
				self.c.create_rectangle(self.start_x, self.start_y, event.x, event.y,
					dash = dash,
					fill = fill_color, outline = line_color)
			elif self.shape.get() == "oval":
				self.c.create_oval(self.start_x, self.start_y, event.x, event.y,
					dash = dash,
					fill = fill_color, outline = line_color)
			else:
				if self.shape.get() == "star (5)": points = star(5)
				if self.shape.get() == "star (6)": points = star(6)
				if self.shape.get() == "pentagon": points = polygon(5)
				if self.shape.get() == "hexagon": points = polygon(6)
				if self.shape.get() == "triangle": points = polygon(3)
				self.c.create_polygon(
					transform_points(self.start_x, self.start_y, event.x, event.y, points),
					dash = dash,
					fill = fill_color, outline = line_color)


a = PaintApp() # create object of class PaintApp (this calls __init__)
a.run()

