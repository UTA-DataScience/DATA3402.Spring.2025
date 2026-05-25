class Canvas:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.data = [[' '] * width for i in range(height)]

    def set_pixel(self, row, col, char='*'):
        if 0 <= row < self.height and 0 <= col < self.width:
            self.data[row][col] = char

    def get_pixel(self, row, col):
        return self.data[row][col]
    
    def clear_canvas(self):
        self.data = [[' '] * self.width for i in range(self.height)]
    
    def v_line(self, x, y, w, char='*'):
        for i in range(x, x + w):
            self.set_pixel(i, y, char)

    def h_line(self, x, y, h, char='*'):
        for i in range(y, y + h):
            self.set_pixel(x, i, char)
            
    def line(self, x1, y1, x2, y2, char='*'):
        if x2 == x1:
            for y in range(y1, y2 + 1):
                self.set_pixel(y, x1, char)
        else:
            slope = (y2 - y1) / (x2 - x1)
            for x in range(x1, x2 + 1):
                y = int(y1 + slope * (x - x1))
                self.set_pixel(y, x, char)
            
    def display(self):
        print("\n".join(["".join(row) for row in self.data]))

from abc import ABC, abstractmethod # Importing again to avoid potential errors in runnning this cell before previous cells.
## Reusing the Shape class from the previous exercise
class Shape(ABC):
    @abstractmethod
    def compute_area(self):
        """Compute the area of the shape."""
        pass

    @abstractmethod
    def compute_perimeter(self):
        """Compute the perimeter of the shape."""
        pass

    @abstractmethod
    def get_center(self):
        """Get the center of the shape."""
        pass

    @abstractmethod
    def get_corners(self):
        """Get the corners of the shape, if applicable."""
        pass
## This is the new method addded to the Shape class to return the perimeter points of the the object.
    @abstractmethod
    def get_perimeter_points(self, num_points=16):
        """Return up to 16 (x, y) points along the perimeter of the shape."""
        pass
## This is the new method to determine if a set of coordinates are inside of the object. 
    @abstractmethod
    def contains_point(self, x, y):
        """Check if a given (x, y) point is inside the shape."""
        pass
## This is the new method to determine if the object overlaps with another object.
    @abstractmethod
    def overlaps_with(self, other: "Shape") -> bool:
        """Determine if this shape overlaps with another shape."""
        pass
    @abstractmethod
    def __repr__(self):
        """Return a string that can be used to recreate the object."""
        pass

class Rectangle(Shape):
    def __init__(self, length, width, x=0, y=0, char = "#"):
        self.__length = length
        self.__width = width
        self.__x = x
        self.__y = y
        self.char = char
## The @property decorator is used to define properties in Python. This puts it in a read only property, which is useful for this exercise.
    @property
    def length(self):
        # Dynamically compute length based on the function of x and y
        return self.__length_function(self.__length, self.__width, self.__x, self.__y)

    @property
    def width(self):
        # Dynamically compute width based on the function of x and y
        return self.__width_function(self.__length, self.__width, self.__x, self.__y)

    @property
    def x(self):
        return self.__x

    @x.setter
    def x(self, value):
        if value < 0:
            raise ValueError("x cannot be negative")
        self.__x = value

    @property
    def y(self):
        return self.__y

    @y.setter
    def y(self, value):
        if value < 0:
            raise ValueError("y cannot be negative")
        self.__y = value

    def set_origin(self, origin_x, origin_y):
        """Update x and y based on a new origin."""
        self.__x = origin_x
        self.__y = origin_y

    def compute_area(self):
        return self.length * self.width

    def compute_perimeter(self):
        return 2 * (self.length + self.width)

    def get_corners(self): # Function to conpute the corners of the rectangle given the length and width and corresponding origin, simplifying the code.
        """Returns the coordinates of the rectangle's corners based on (x, y) as the bottom-left corner."""
        return {
            "bottom_left": (self.__x, self.__y),
            "bottom_right": (self.__x + self.width, self.__y),
            "top_left": (self.__x, self.__y + self.length),
            "top_right": (self.__x + self.width, self.__y + self.length)
        }
     # Implementing abstract methods from Shape
    def compute_area(self):
        return self.length * self.width

    def compute_perimeter(self):
        return 2 * (self.length + self.width)

    def get_center(self):
        return (self.__x, self.__y)

    def get_corners(self):
        return {
            "bottom_left": (self.__x, self.__y),
            "bottom_right": (self.__x + self.width, self.__y),
            "top_left": (self.__x, self.__y + self.length),
            "top_right": (self.__x + self.width, self.__y + self.length)
        }
    ## This is the new method added to the Rectangle class to return the perimeter points of the rectangle.
    def get_perimeter_points(self, num_points=16):
        """Generate up to 16 points along the perimeter of the rectangle."""
        corners = self.get_corners()
        points = []
        
        # Extract corner points
        bl = corners["bottom_left"]
        br = corners["bottom_right"]
        tr = corners["top_right"]
        tl = corners["top_left"]

        # Calculate the points along each edge
        edge_points = num_points // 4 # Utilizing integer division (floor division operator //) to get the number of points per edge
        
        # Bottom edge
        for i in range(edge_points):
            t = i / edge_points
            points.append((bl[0] + t * (br[0] - bl[0]), bl[1]))

        # Right edge
        for i in range(edge_points):
            t = i / edge_points
            points.append((br[0], br[1] + t * (tr[1] - br[1])))

        # Top edge
        for i in range(edge_points):
            t = i / edge_points
            points.append((tr[0] - t * (tr[0] - tl[0]), tr[1]))

        # Left edge
        for i in range(edge_points):
            t = i / edge_points
            points.append((tl[0], tl[1] - t * (tl[1] - bl[1])))

        return points[:num_points]
    ## This is the new method added to the Rectangle class to determine if a given point is inside the rectangle.
    def contains_point(self, x, y):
        """Check if the point (x, y) is inside the rectangle."""
        return self.__x <= x <= self.__x + self.width and self.__y <= y <= self.__y + self.length
    ## This is the new method added to the Rectangle class to determine if the rectangle overlaps with another shape.

    def overlaps_with(self, other: Shape) -> bool:
        """Determine if this rectangle overlaps with another shape."""
        if isinstance(other, Rectangle):
            # Check if there is no overlap
            if (self.__x + self.__width < other.__x or
                other.__x + other.__width < self.__x or
                self.__y + self.__length < other.__y or
                other.__y + other.__length < self.__y):
                return False
            return True
        else:
            # Check if any perimeter point of either shape is inside the other
            for point in self.get_perimeter_points():
                if other.contains_point(*point):
                    return True
            for point in other.get_perimeter_points():
                if self.contains_point(*point):
                    return True
        return False
    def paint(self, canvas: Canvas):
        for i in range(self.__length):
            canvas.h_line(self.__y + i, self.__x, self.__width, char=self.char)
    def __repr__(self):
        return f"Rectangle({self.__length}, {self.__width}, x={self.__x}, y={self.__y}, char={repr(self.char)})"

class Circle(Shape):
    def __init__(self, radius, x =0, y = 0, char = '@'):
        self.__radius = radius
        self.__x = x
        self.__y = y
        self.char = char
    def area(self): # compute the area using the formula pi * r^2
        return 3.14 * self.__radius ** 2
    def circumfrence(self): # compute the perimeter using the formula 2 * pi * r
        return round(2 * 3.14 * self.__radius, 2)
    def get_center(self):
        return self.__x, self.__y
    def get_radius(self):
        return self.__radius
    def get_circumfrence(self):
        return self.circumfrence()
    def get_area(self):
        return self.area()
    def return_all(self):
        print(f"Area: {self.area()}")
        print(f"Circumfrence: {self.circumfrence()}")
        print(f"Center: {self.get_center()}")
        print(f"Radius: {self.get_radius()}")
        return self.area(), self.circumfrence(), self.get_center(), self.get_radius()
        # Implementing abstract methods from Shape
    def compute_area(self):
        return 3.14 * self.__radius ** 2

    def compute_perimeter(self):
        return round(2 * 3.14 * self.__radius, 2)

    def get_center(self):
        return (self.__x, self.__y)

    def get_corners(self):
        """Circles do not have corners, return None."""
        return None

    def get_radius(self):
        return self.__radius
    ## This is the new method added to the Circle class to return the perimeter points of the circle.
    def get_perimeter_points(self, num_points=16):
        """Generate up to 16 points along the perimeter of the circle."""
        points = []
        for i in range(num_points):
            angle = 2 * math.pi * (i / num_points)
            x = self.__x + self.__radius * math.cos(angle)
            y = self.__y + self.__radius * math.sin(angle)
            points.append((round(x, 2), round(y, 2)))
        return points
    ## This is the new method added to the Circle class to determine if a given point is inside the circle.
    def contains_point(self, x, y):
        """Check if the point (x, y) is inside the circle."""
        distance = math.sqrt((x - self.__x) ** 2 + (y - self.__y) ** 2)
        return distance <= self.__radius
    ## This is the new method added to the Circle class to determine if the circle overlaps with another shape.
    def overlaps_with(self, other: Shape) -> bool:
        """Determine if this circle overlaps with another shape."""
        if isinstance(other, Circle):
            distance = math.sqrt((self.__x - other.__x) ** 2 + (self.__y - other.__y) ** 2)
            return distance < (self.__radius + other.__radius)
        else:
            # Check perimeter points of both shapes for containment
            for point in self.get_perimeter_points():
                if other.contains_point(*point):
                    return True
            for point in other.get_perimeter_points():
                if self.contains_point(*point):
                    return True
        return False
    def paint(self, canvas: Canvas):
        aspect_ratio = canvas.height / canvas.width
        for angle in range(0, 360, 10):
            rad = math.radians(angle)
            px = int(self.__x + self.__radius * math.cos(rad))
            py = int(self.__y + self.__radius * math.sin(rad) * aspect_ratio)
            canvas.set_pixel(py, px, char=self.char)
    def __repr__(self):
        return f"Circle({self.__radius}, x={self.__x}, y={self.__y}, char={repr(self.char)})"

import math # import the math module to use the sqrt function
# Simplified Triangle class using Heron's formula
class Triangle(Shape):
    def __init__(self, a, b, c, x=0, y=0, char = '*'):
        # Validate if the sides can form a triangle
        if not (a + b > c and a + c > b and b + c > a):
            raise ValueError("The provided sides do not form a valid triangle.")
        
        self.__a = a
        self.__b = b
        self.__c = c
        self.__x = x
        self.__y = y
        self.char = char

    # Implementing abstract methods from Shape
    def compute_area(self):
        """Compute the area using Heron's formula."""
        s = self.compute_perimeter() / 2  # Semi-perimeter
        area = math.sqrt(s * (s - self.__a) * (s - self.__b) * (s - self.__c))
        return round(area, 2)

    def compute_perimeter(self):
        """Compute the perimeter as the sum of all sides."""
        return round(self.__a + self.__b + self.__c, 2)

    def get_center(self):
        """Return the centroid of the triangle (average of corners)."""
        corners = self.get_corners()
        centroid_x = sum([p[0] for p in corners.values()]) / 3
        centroid_y = sum([p[1] for p in corners.values()]) / 3
        return (round(centroid_x, 2), round(centroid_y, 2))

    def get_corners(self):
        """Assume (x, y) is the bottom-left corner and calculate other corners."""
        # Simple placement of the triangle along the base a
        return {
            "bottom_left": (self.__x, self.__y),
            "bottom_right": (self.__x + self.__a, self.__y),
            "top_vertex": (self.__x + self.__a / 2, self.__y + self.get_approximate_height())
        }
    def get_approximate_height(self):
        """Compute the approximate height for visualization purposes."""
        # Area = 1/2 * base * height => height = (2 * area) / base
        area = self.compute_area()
        return round((2 * area) / self.__a, 2)
    ## This is the new method added to the Triangle class to return the perimeter points of the triangle.
    def get_perimeter_points(self, num_points=16):
        """Generate up to 16 points along the perimeter of the triangle."""
        corners = self.get_corners()
        points = list(corners.values())
        
        # Generate intermediate points along the edges
        while len(points) < num_points:
            for i in range(len(points) - 1):
                mid_point = (
                    (points[i][0] + points[i + 1][0]) / 2,
                    (points[i][1] + points[i + 1][1]) / 2
                )
                points.insert(i + 1, mid_point)
                if len(points) >= num_points:
                    break
        return points[:num_points]
    ## This is the new method added to the Triangle class to determine if a given point is inside the triangle.
    def contains_point(self, x, y):
        """Check if the point (x, y) is inside the triangle using area comparison."""
        def area(x1, y1, x2, y2, x3, y3):
            return abs((x1 * (y2 - y3) + x2 * (y3 - y1) + x3 * (y1 - y2)) / 2.0)

        corners = self.get_corners()
        x1, y1 = corners["bottom_left"]
        x2, y2 = corners["bottom_right"]
        x3, y3 = corners["top_vertex"]

        a = area(x1, y1, x2, y2, x3, y3)
        a1 = area(x, y, x2, y2, x3, y3)
        a2 = area(x1, y1, x, y, x3, y3)
        a3 = area(x1, y1, x2, y2, x, y)

        return a == a1 + a2 + a3
    ## This is the new method added to the Triangle class to determine if the triangle overlaps with another shape.
    def overlaps_with(self, other: Shape) -> bool:
        """Determine if this triangle overlaps with another shape."""
        if isinstance(other, Triangle):
            # Check if any perimeter point of either triangle is inside the other
            for point in self.get_perimeter_points():
                if other.contains_point(*point):
                    return True
            for point in other.get_perimeter_points():
                if self.contains_point(*point):
                    return True
        else:
            # Mixed shape overlap detection
            for point in self.get_perimeter_points():
                if other.contains_point(*point):
                    return True
            for point in other.get_perimeter_points():
                if self.contains_point(*point):
                    return True
        return False
    def paint(self, canvas: Canvas):
        corners = self.get_corners()
        bl = corners["bottom_left"]
        br = corners["bottom_right"]
        tv = corners["top_vertex"]

        # Use Bresenham's line algorithm for all triangle sides
        canvas.line(int(bl[0]), int(bl[1]), int(br[0]), int(br[1]), char=self.char)
        canvas.line(int(bl[0]), int(bl[1]), int(tv[0]), int(tv[1]), char=self.char)
        canvas.line(int(br[0]), int(br[1]), int(tv[0]), int(tv[1]), char=self.char)
    def __repr__(self):
        return f"Triangle({self.__a}, {self.__b}, {self.__c}, x={self.__x}, y={self.__y}, char={repr(self.char)})"

class CompoundShape(Shape):
    def __init__(self, *shapes, char='%'):
        self.shapes = shapes
        self.char = char

    def paint(self, canvas: Canvas):
        for shape in self.shapes:
            shape.paint(canvas)

    def compute_area(self):
        """Compute the total area of all contained shapes."""
        return sum(shape.compute_area() for shape in self.shapes)

    def compute_perimeter(self):
        """Compute the total perimeter of all contained shapes."""
        return sum(shape.compute_perimeter() for shape in self.shapes)

    def get_center(self):
        """Compute the geometric center of all contained shapes."""
        if not self.shapes:
            return (0, 0)
        centers = [shape.get_center() for shape in self.shapes]
        avg_x = sum(x for x, _ in centers) / len(centers)
        avg_y = sum(y for _, y in centers) / len(centers)
        return (avg_x, avg_y)

    def get_corners(self):
        """Returns all corners of the contained shapes."""
        corners = []
        for shape in self.shapes:
            shape_corners = shape.get_corners()
            if shape_corners:
                corners.extend(shape_corners.values())
        return corners

    def get_perimeter_points(self, num_points=16):
        """Aggregate perimeter points from all shapes."""
        points = []
        for shape in self.shapes:
            points.extend(shape.get_perimeter_points(num_points // len(self.shapes)))
        return points[:num_points]

    def contains_point(self, x, y):
        """Check if any shape in the compound contains the point."""
        return any(shape.contains_point(x, y) for shape in self.shapes)

    def overlaps_with(self, other: Shape) -> bool:
        """Check if any shape in the compound overlaps with the other shape."""
        return any(shape.overlaps_with(other) for shape in self.shapes)

    def __repr__(self):
        """Return a string that reconstructs the compound shape with all sub-shapes."""
        shapes_repr = ', '.join(repr(shape) for shape in self.shapes)
        return f"CompoundShape({shapes_repr}, char={repr(self.char)})"

class RasterDrawing:
    def __init__(self, width, height, bg_char=' '):
        self.canvas = Canvas(width, height)
        self.shapes = []
        self.bg_char = bg_char

    def add_shape(self, shape: Shape):
        self.shapes.append(shape)

    def remove_shape(self, shape: Shape):
        if shape in self.shapes:
            self.shapes.remove(shape)

    def clear_shapes(self):
        self.shapes = []

    def paint(self):
        """Paint all shapes onto the canvas and display the drawing."""
        self.canvas.clear_canvas()
        for shape in self.shapes:
            shape.paint(self.canvas)
        self.canvas.display()

    def save(self, filename: str):
        """Save the drawing to a file as executable Python code."""
        with open(filename, 'w') as f:
            f.write(repr(self))
    
    def __repr__(self):
        """Return a string to recreate the RasterDrawing and all its shapes."""
        shapes_repr = ', '.join(repr(shape) for shape in self.shapes)
        return f"RasterDrawing({self.canvas.width}, {self.canvas.height}, bg_char={repr(self.bg_char)}).add_shapes([{shapes_repr}])"

    def add_shapes(self, shapes: list):
        """Add multiple shapes to the drawing."""
        self.shapes.extend(shapes)
        return self  # Return self to support method chaining in __repr__