import io
import os

# Imports the Google Cloud client library
from google.cloud import vision
from google.cloud.vision import types

def in_bounds(vertices, limits):
  bot = (vertices[0].y + vertices[1].y) / 2
  top = (vertices[2].y + vertices[3].y) / 2
  return (bot >= (limits[0] - 10) and bot <= (limits[0] + 10)) or (top >= (limits[1] - 10) and top <= (limits[1] + 10))

def main():
  # Instantiates a client
  client = vision.ImageAnnotatorClient()

  # The name of the image file to annotate
  """
  file_name = os.path.join(
    os.path.dirname(__file__),
    'test-images/dickssportinggoods.jpg')

  """

  file_name = os.path.join(
    os.path.dirname(__file__),
    'test-images/krogers.jpg')

  # Loads the image into memory
  with io.open(file_name, 'rb') as image_file:
    content = image_file.read()

  image = types.Image(content=content)

  response = client.document_text_detection(image=image)
  document = response.text_annotations

  slope = 0
  pointA = 0
  pointB = 0
  pointC = 0
  pointD = 0
  for obj in response.text_annotations:
    if obj.description == "9700":
      pointA = obj
    elif obj.description == "CIRCLE":
      pointB = obj
    elif obj.description == "MSSN":
      pointC = obj
    elif obj.description == "CHIPS":
      pointD = obj

  slope = (pointA.bounding_poly.vertices[0].y - pointB.bounding_poly.vertices[0].y) / (pointA.bounding_poly.vertices[0].x - pointB.bounding_poly.vertices[0].x)
  print(slope)

  slope = (pointC.bounding_poly.vertices[0].y - pointD.bounding_poly.vertices[0].y) / (pointC.bounding_poly.vertices[0].x - pointD.bounding_poly.vertices[0].x)
  print(slope)

  print((obj.bounding_poly.vertices[0].y - obj.bounding_poly.vertices[1].y) / (obj.bounding_poly.vertices[0].x - obj.bounding_poly.vertices[1].x))
  print((obj.bounding_poly.vertices[2].y - obj.bounding_poly.vertices[3].y) / (obj.bounding_poly.vertices[2].x - obj.bounding_poly.vertices[3].x))

  out = []
  bounds = []
  for obj in response.text_annotations:
    if len(bounds) > 0 and in_bounds(obj.bounding_poly.vertices, bounds[-1]):
      out[-1] += " " + obj.description
    else:
      out.append(obj.description)
      bounds.append(((obj.bounding_poly.vertices[0].y+obj.bounding_poly.vertices[1].y)/2, (obj.bounding_poly.vertices[2].y+obj.bounding_poly.vertices[3].y)/2))

  for line in out:
    print("|" + line + "|")


"""
document = response.full_text_annotation


breaks = vision.enums.TextAnnotation.DetectedBreak.BreakType
paragraphs = []
lines = []

for page in document.pages:
  for block in page.blocks:
    for paragraph in block.paragraphs:
      para = ""
      line = ""
      for word in paragraph.words:
        for symbol in word.symbols:
          line += symbol.text
          if symbol.property.detected_break.type == breaks.SPACE:
            line += ' '
          if symbol.property.detected_break.type == breaks.EOL_SURE_SPACE:
            line += ' '
            lines.append(line)
            para += line
            line = ''
          if symbol.property.detected_break.type == breaks.LINE_BREAK:
            lines.append(line)
            para += line
            line = ''
      paragraphs.append(para)

for p in paragraphs:
  print(p)

print()
for l in lines:
  print(l)
"""


if __name__ == "__main__":
  main()
