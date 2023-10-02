# Libreria personalizada de funciones graficas
import math
import numpy as np


def matrixToCartessian(matrix_points, width, height):
	cartessian_points = []
	for point in matrix_points:
		x = point[0] - width/2 # x = x' - Cw/2
		y = -point[1] + height/2 # y = Ch/2 + y
		cartessian_points.append((int(x), int(y)))
	return cartessian_points


def pointAround(canvas, x, y, canvas_size, color):
	for i in range(0, 5):
		if x-i >= 0:
			canvas.putpixel((x-i, y), color)
		
		if x+i <= canvas_size[0]:
			canvas.putpixel((x+i, y), color)

		if y-i >= 0:
			canvas.putpixel((x, y-i), color)
		
		if x+i <= canvas_size[1]:
			canvas.putpixel((x, y+i), color)
	

def drawPoint(x,y,color,canvas):
	width, height = canvas.size
	xn=int(width/2+x)
	yn=int(height/2-y)
	canvas.putpixel((xn, yn),color)


def swap(P0,P1):
	return P1, P0


def interpolate(i0,d0,i1,d1):
	if i0 == i1:
		return [d0 for i in range(i0,i1+1)]
	values = []
	a = (d1 - d0) / (i1 - i0)
	d = d0
	for i in range(i0, i1+1):
		values.append(d)
		d = d + a
	return values


def drawLine(P0,P1,color,canvas):
	x0=P0[0]
	y0=P0[1]
	x1=P1[0]
	y1=P1[1]
	if abs(P1[0]-P0[0])>abs(P1[1]-P0[1]):
		#Horizonal linex
		if P0[0]>P1[0]:
			(x0,y0), (x1,y1) = swap(P0,P1)
		ys = interpolate(x0, y0, x1, y1)
		for x in range(x0,x1+1):
			drawPoint(x, ys[x - x0], color,canvas)
	else:
		#Vertical lines   
		if P0[1]>P1[1]:
			(x0,y0), (x1,y1) = swap(P0,P1)
		xs = interpolate(y0, x0, y1, x1)
		for y in range(y0,y1+1):
			drawPoint(xs[y - y0],y, color,canvas)


def drawFilledTriangle(P0, P1, P2, color, canvas):
	if P1[1] < P0[1]:
		P1, P0 = swap(P1, P0)

	if P2[1] < P0[1]:
		P2, P0 = swap(P2, P0)

	if P2[1] < P1[1]:
		P2, P1 = swap(P2, P1)

	x0, y0 = P0
	x1, y1 = P1
	x2, y2 = P2


	x01 = interpolate(y0, x0, y1, x1)
	x02 = interpolate(y0, x0, y2, x2)
	x12 = interpolate(y1, x1, y2, x2)

	x012 = x01 + x12

	m = math.floor(len(x012) / 2)
	if x02[m] < x012[m]:
		x_left = x02
		x_right = x012
	else:
		x_left = x012
		x_right = x02

	for y in range(y0, y2):
		for x in range(int(x_left[y - y0]), int(x_right[y - y0])):
			drawPoint(x, y, color, canvas)

def drawShadedTriangle(P0, P1, P2, color, canvas):
    # Sort the points so that y0 <= y1 <= y2
    h0=1
    h1=0
    h2=0
    c=	P0
    if P1[1] < P0[1]:
        P1, P0 = swap(P1, P0)
    if P2[1] < P0[1]:
        P2, P0 = swap(P2, P0)
    if P2[1] < P1[1]:
        P2, P1 = swap(P2, P1)

    if c==P0:
        h1 = 0
        h0 = 1
        h2 = 0
    if c==P1:
        h1 = 1
        h0 = 0
        h2 = 0
    if c==P2:
        h1 = 0
        h0 = 0
        h2 = 1

    x0 = P0[0]
    y0 = P0[1]
    x1 = P1[0]
    y1 = P1[1]
    x2 = P2[0]
    y2 = P2[1]

    # Compute the x coordinates and h values of the triangle edges
    x01 = interpolate(y0, x0, y1, x1)
    h01 = interpolate(y0, h0, y1, h1)

    x12 = interpolate(y1, x1, y2, x2)
    h12 = interpolate(y1, h1, y2, h2)

    x02 = interpolate(y0, x0, y2, x2)
    h02 = interpolate(y0, h0, y2, h2)

    # Concatenate the short sides
    x012 = x01 + x12

    h012 = h01 + h12

    # Determine which is left and which is right
    m = math.floor(len(x012) / 2)
    if x02[m] < x012[m]:
        x_left = x02
        h_left = h02

        x_right = x012
        h_right = h012
    else:
        x_left = x012
        h_left = h012

        x_right = x02
        h_right = h02

    # Draw the horizontal segments
    for y in range(y0, y2):
        xl = round(x_left[y - y0])
        hl = h_left[y - y0]

        xr = round(x_right[y - y0])
        hr = h_right[y - y0]

        h_segment = interpolate(xl, hl, xr, hr)

        for x in range(xl, xr):
            sh_color0 = round(color[0] * h_segment[x - xl])
            sh_color1 = round(color[1] * h_segment[x - xl])
            sh_color2 = round(color[2] * h_segment[x - xl])
            shaded_color = (sh_color0, sh_color1, sh_color2)
            drawPoint(int(x), int(y), shaded_color, canvas)


def drawPolygon(points, color, canvas):
	if len(points) < 3:
		print("No es un poligono")
		return

	for i in range(-1, len(points)-1):
		drawLine(points[i], points[i+1], color, canvas)


def drawFilledPolygon(points, color, canvas):
	if len(points) < 3:
		print("No es un poligono")
		return

	for i in range(1, len(points)-1):
		drawFilledTriangle(points[0], points[i], points[i+1], color, canvas)
	drawFilledTriangle(points[-1], points[-2], points[-3], color, canvas)


def drawGradientPolygon(points, color, canvas, centroid = None):
	k=len(points)
	i=0
	if centroid is None:
		cx=int(np.sum([point[0] for point in points])/k)
		cy=int(np.sum([point[1] for point in points])/k)
		centralPoint=(cx,cy)
	else:
		x, y = canvas.size
		centralPoint = matrixToCartessian([(centroid[0], centroid[1])], x, y)[0]


	while i < k-1:
		drawShadedTriangle(centralPoint, points[i], points[i + 1], color, canvas)
		i=i+1
		
	drawShadedTriangle(centralPoint,points[i],points[0],color,canvas)