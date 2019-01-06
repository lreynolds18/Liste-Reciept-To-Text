import io
import os

# Imports the Google Cloud client library
from google.cloud import vision
from google.cloud.vision import types

def in_bounds(vertices, prev_x, prev_y, slope, residual):
  if (vertices[0].x - prev_x) != 0:
    s = abs((vertices[0].y - prev_y) / (vertices[0].x - prev_x))
    slope = abs(slope)

    return s >= (slope - residual) and s <= (slope + residual)
  else:
    return True

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
  prev_x = 0
  prev_y = 0
  for obj in response.text_annotations:
    if len(out) > 0 and in_bounds(obj.bounding_poly.vertices, prev_x, prev_y, slope, 0.2):
      out[-1] += " " + obj.description
    else:
      out.append(obj.description)
      prev_x = obj.bounding_poly.vertices[0].x
      prev_y = obj.bounding_poly.vertices[0].y 
    print(prev_x, prev_y)


  for line in out:
    print("|" + line + "|")


if __name__ == "__main__":
  main()
