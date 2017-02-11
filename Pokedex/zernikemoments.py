import mahotas

class ZernikeMoments:
    def __init__(self, radius):
        self.radius = radius
    def describe(self, image):
        return mahotas.features.zernike_moments(image, self.radius)
