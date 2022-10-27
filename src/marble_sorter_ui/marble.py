class Marble:
    """
    A Marble object modeling a marble with a phenotypic color defined by its RGB color components.
    """


    def __init__(self, color="BLACK", r=0, g=0, b=0):
        """
        Construct self such that it has the given color and the red (r),
        green (g), and blue (b) components.
        """
        self._color = color
        self._r = r  # Red component
        self._g = g  # Green component
        self._b = b  # Blue component


    def get_color(self):
        """
        Returns the color of self.
        """
        return self._color


    def get_red(self):
        """
        Return the red component of self.
        """
        return self._r


    def get_green(self):
        """
        Return the green component of self.
        """
        return self._g


    def get_blue(self):
        """
        Return the blue component of self.
        """
        return self._b


    def __str__(self):
        """
        Return the string equivalent of self, that is, a
        string of the form 'color(r, g, b)'.
        """
        return str(self._color) + '(' + str(self._r) + ', ' + str(self._g) + ', ' + \
            str(self._b) + ')'