#!/bin/python3

import io, os

# Imports the Google Cloud client library
from google.cloud import vision
from google.cloud.vision import types

def calc_slope(objA, objB):
  # calculate slope (y1 - y2) / (x1 - x2)
  # TODO: how to handle divs by zero, absolute value

  s = 0
  if (objA.bounding_poly.vertices[0].x - objB.bounding_poly.vertices[0].x) != 0:
    s = (objA.bounding_poly.vertices[0].y - objB.bounding_poly.vertices[0].y) / \
        (objA.bounding_poly.vertices[0].x - objB.bounding_poly.vertices[0].x)
  return s

def in_bounds(new_slope, old_slope, residual=0.20):
    new_slope = abs(new_slope)
    old_slope = abs(old_slope)
    return new_slope >= (old_slope - residual) \
      and new_slope <= (old_slope + residual)

def calc_slope_of_reciept(text_annotations):
  # use * to calculate the slope of the text in a reciept
  # we want to use the slope to find which text is on the same line

  line = []
  # grab a line of *'s
  for obj in text_annotations:
    if obj.description != "*" and len(line) != 0:
      break
    elif obj.description == "*":
      line.append(obj)

  return calc_slope(line[0], line[-1])


def assemble_lines(text_annotations, slope):
  out = [[text_annotations[0]]]

  for obj in text_annotations[1:]:
    if obj.description != "*":
      for i in range(len(out)-1, -1, -1):
        s = calc_slope(obj, out[i][0])
        if in_bounds(s, slope):
          out[i].append(obj)
        else:
          out.append([obj])

  return out

def print_lines(objs):
  for line_list in objs:
    for line in line_list:
      print(line.description, end='')

def main():
  # Instantiates a client
  client = vision.ImageAnnotatorClient()

  # The name of the image file to annotate


  file_name = os.path.join(
    os.path.dirname(__file__),
    # 'test-images/krogers.jpg'
    # 'test-images/dickssportinggoods.jpg'
    'test-images/gianteagle.jpg'
    # 'test-images/target.jpg'
    # 'test-images/homedepot.jpg'
    )

  # Loads the image into memory
  with io.open(file_name, 'rb') as image_file:
    content = image_file.read()

  image = types.Image(content=content)

  response = client.document_text_detection(image=image)
  document = response.text_annotations
  
  # slope = calc_slope_of_reciept(response.text_annotations)
  # print(slope)
  slope = 0
  lines = assemble_lines(response.text_annotations, slope)
  print_lines(lines)


if __name__ == "__main__":
  main()
