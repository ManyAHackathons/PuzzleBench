from google import genai
from .bomb import Module
import base64
import random

class Dec(Module):
    #We can use a function called base64.decodebytes() to decode our base 64 string.
    super().__init__()
    self.file = "base64encoded.txt"
    self.open = open(self.file, "rt")
    self.word = file.readline(random.randint(1, 20))
    self.decoded = base64.decodebytes(self.word.encode())
    #for the more than 4 letters off thinggy we are going to need to make an array of the decoded
    #word with different respective lenghts that are 75% in the range of the length of the word. 
    self.length = len(self.decoded)
    #I'm not sure how to do the part where I can make an array with lenghts that are 4 letters off or less. 