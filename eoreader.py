import os
# import matplotlib.pyplot as plt

from eoreader.reader import Reader
# from eoreader.bands import RED, GREEN, NDVI, YELLOW, CLOUDS, to_str

path = os.path("D:/Dev/pars/014194668010_01")
reader = Reader()
prod = reader.open(path)
