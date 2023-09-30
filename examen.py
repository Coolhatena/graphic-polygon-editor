import tkinter as tk
from PIL import Image, ImageTk
import graflib as gl


class rootApp(tk.Tk):
	def __init__(self):
		tk.Tk.__init__(self)
		self._frame = None
		self.switch_frame(StartPage)

	def switch_frame(self, frame_class):
		# Destroys current frame and replaces it with a new one.
		new_frame = frame_class(self)
		if self._frame is not None:
			self._frame.destroy()
		self._frame = new_frame
		self._frame.pack()


class ScrollableFrame(tk.Frame):
	def __init__(self, container, *args, **kwargs):
		super().__init__(container, *args, **kwargs)
		canvas = tk.Canvas(self)
		canvas.config(
			width=container.master.ancho + 100, height=container.master.alto + 20
		)

		scrollbar = tk.Scrollbar(self, orient="vertical", command=canvas.yview)
		self.scrollable_frame = tk.Frame(canvas)

		self.scrollable_frame.bind(
			"<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
		)

		canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")

		canvas.configure(yscrollcommand=scrollbar.set)

		canvas.pack(side="left", fill="both", expand=True)
		scrollbar.pack(side="right", fill="y")


class StartPage(tk.Frame):
	def __init__(self, master):
		tk.Frame.__init__(self, master)
		master.geometry("400x160")
		tk.Label(
			self, text="Ingrese las medidas del canvas:", font=("Helvetica bold", 15)
		).pack()

		labelTextAncho = tk.StringVar()
		labelTextAncho.set("Ancho (En px):")
		tk.Label(self, textvariable=labelTextAncho).pack()

		self.ancho = tk.StringVar(None)
		self.ancho.set("300")
		tk.Entry(self, textvariable=self.ancho, width=25).pack()

		labelTextAlto = tk.StringVar()
		labelTextAlto.set("Alto (En px):")
		tk.Label(self, textvariable=labelTextAlto).pack()

		self.alto = tk.StringVar(None)
		self.alto.set("300")
		tk.Entry(self, textvariable=self.alto, width=25).pack()

		# tk.Label(self, text="This is the start page").pack(side="top", fill="x", pady=10)
		tk.Button(
			self, text="Continuar", command=lambda: self.assertPoints(master)
		).pack(pady=5)

	def assertPoints(self, master):
		ancho = self.ancho.get()
		alto = self.alto.get()
		if ancho != "" and alto != "":
			master.ancho = int(ancho)
			master.alto = int(alto)
			master.switch_frame(selectPoints)


class selectPoints(tk.Frame):
	def __init__(self, master):
		tk.Frame.__init__(self, master)
		alto = master.alto
		ancho = master.ancho
		puntos = []
		master.geometry(f"{ancho+50}x{alto+90}")
		canva = Image.new("RGB", (ancho, alto), (255, 255, 255))

		tkpic = ImageTk.PhotoImage(canva)
		label = tk.Label(self, image=tkpic)
		label.image = tkpic  # Save reference to image
		label.pack()

		def callback(event):
			color = (0, 0, 0)
			gl.pointAround(canva, event.x, event.y, (ancho, alto), color)
			tkpic = ImageTk.PhotoImage(canva)
			label.config(image=tkpic)
			label.image = tkpic  # Save reference to image
			puntos.append((event.x, event.y))

		label.bind("<Button-1>", callback)

		tk.Button(
			self, text="Volver", command=lambda: master.switch_frame(StartPage)
		).pack(pady=5)

		tk.Button(self, text="Continuar", command=lambda: self.sendData(puntos)).pack(
			pady=5
		)

	def sendData(self, points):
		if len(points) > 2:
			self.master.points = points
			self.master.switch_frame(Polygon)


class Polygon(tk.Frame):
	def __init__(self, master):
		tk.Frame.__init__(self, master)
		master.geometry(f"{master.ancho+120}x{master.alto}")
		canva = Image.new("RGB", (master.ancho, master.alto), (255, 255, 255))
		gl.drawPolygon(
			gl.matrixToCartessian(master.points, master.ancho, master.alto),
			(0, 0, 0),
			canva,
		)

		container = ScrollableFrame(self)

		tkpic = ImageTk.PhotoImage(canva)
		label = tk.Label(container.scrollable_frame, image=tkpic)
		label.image = tkpic  # Save reference to image
		label.pack()

		labelTextRed = tk.StringVar()
		labelTextRed.set("Rojo:")
		tk.Label(container.scrollable_frame, textvariable=labelTextRed).pack()

		red = tk.Scale(
			container.scrollable_frame,
			from_=0,
			to=255,
			tickinterval=20,
			length=380,
			orient=tk.HORIZONTAL,
		)
		red.pack()

		labelTextGreen = tk.StringVar()
		labelTextGreen.set("Verde:")
		tk.Label(container.scrollable_frame, textvariable=labelTextGreen).pack()

		green = tk.Scale(
			container.scrollable_frame,
			from_=0,
			to=255,
			tickinterval=20,
			length=380,
			orient=tk.HORIZONTAL,
		)
		green.pack()

		labelTextBlue = tk.StringVar()
		labelTextBlue.set("Azul:")
		tk.Label(container.scrollable_frame, textvariable=labelTextBlue).pack()

		blue = tk.Scale(
			container.scrollable_frame,
			from_=0,
			to=255,
			tickinterval=20,
			length=380,
			orient=tk.HORIZONTAL,
		)
		blue.pack()

		tk.Button(
			container.scrollable_frame,
			text="Volver",
			command=lambda: master.switch_frame(selectPoints),
		).pack(pady=5)

		tk.Button(
			container.scrollable_frame,
			text="Continuar",
			command=lambda: self.sendData(
				int(red.get()), int(green.get()), int(blue.get())
			),
		).pack(pady=3)

		container.pack(side="left", fill="both", expand=True)

	def sendData(self, r, g, b):
		self.master.color = (r, g, b)
		self.master.switch_frame(gradientPolygon)


class gradientPolygon(tk.Frame):
	def __init__(self, master):
		tk.Frame.__init__(self, master)
		master.geometry(f"{master.ancho+50}x{master.alto+50}")
		canva = Image.new("RGB", (master.ancho, master.alto), (255, 255, 255))
		gl.drawGradientPolygon(
			gl.matrixToCartessian(master.points, master.ancho, master.alto),
			master.color,
			canva,
		)

		tkpic = ImageTk.PhotoImage(canva)
		label = tk.Label(self, image=tkpic)
		label.image = tkpic  # Save reference to image
		label.pack()

		def callback(event):
			centroid = (event.x, event.y)
			canva = Image.new("RGB", (master.ancho, master.alto), (255, 255, 255))
			gl.drawGradientPolygon(
				gl.matrixToCartessian(master.points, master.ancho, master.alto),
				master.color,
				canva,
				centroid,
			)
			tkpic = ImageTk.PhotoImage(canva)
			label.config(image=tkpic)
			label.image = tkpic  # Save reference to image

		label.bind("<Button-1>", callback)

		labelTextInfo = tk.StringVar()
		labelTextInfo.set("Click en la imagen para cambiar el punto de gradiente")
		tk.Label(self, textvariable=labelTextInfo).pack()

		tk.Button(
			self, text="Volver", command=lambda: master.switch_frame(Polygon)
		).pack(pady=3)


if __name__ == "__main__":
	app = rootApp()
	app.title("Paint")
	app.mainloop()
