#!/usr/bin/env python3
"""
Given a file of image tiles, find an arrangement that results in a single
composite image. Each tile may be rotated or flipped as needed so that its edge
can match all neighbors.

https://adventofcode.com/2020/day/20/input
"""

import argparse, math

class Tile:
  def __init__(self, tile_id, lines):
    self.id = tile_id
    self.pixels = [list(line) for line in lines]
    self.calc_edges()
    self.width = len(self.pixels)

  def calc_edges(self):
    self.top_edge = self.pixels[0][:]
    self.bottom_edge = self.pixels[-1][:]
    self.left_edge = [line[0] for line in self.pixels]
    self.right_edge = [line[-1] for line in self.pixels]

  def get_edges_list(self):
    """List of edges in order top, right, bottom, left"""
    return [self.top_edge, self.right_edge, self.bottom_edge, self.left_edge]

  def rotate_right(self):
    new_pixels = [[None for x in range(self.width)] for y in range(self.width)]
    for y in range(self.width):
      for x in range(self.width):
        new_pixels[x][self.width - 1 - y] = self.pixels[y][x]
    self.pixels = new_pixels
    self.calc_edges()

  def flip_horizontal(self):
    self.pixels = [line[::-1] for line in self.pixels]
    self.calc_edges()

  def flip_vertical(self):
    self.pixels = self.pixels[::-1]
    self.calc_edges()

  def duplicate(self):
    return Tile(self.id, self.pixels)

  def __str__(self):
    return 'Tile %d:\n%s' % (self.id, '\n'.join([''.join(line) for line in self.pixels]))

class Edge:
  def __init__(self, tile, edge):
    self.tile = tile
    self.edge = edge
    self.match = None

class TilesMap:
  def __init__(self, tiles):
    self.tiles = tiles
    self.width = int(math.sqrt(len(self.tiles)))
    self.map = [[None for x in range(self.width)] for y in range(self.width)]

  def do_match(self, tile_a, tile_b):
    for edge_a in tile_a.get_edges_list():
      for edge_b in tile_b.get_edges_list():
        if edge_a == edge_b:
          return True
    return False

  def get_neighbor_candidates(self, tile):
    return [candidate for candidate in self.tiles if self.do_match(candidate, tile)]

  def arrange(self):
    edges = []
    for tile in self.tiles:
      edges += [Edge(tile, edge) for edge in tile.get_edges_list()]

    for i in range(len(edges)):
      edge = edges[i]
      if edge.match is not None:
        continue
      for j in range(i + 1, len(edges)):
        other_edge = edges[j]
        if edge.edge == other_edge.edge:
          edge.match = other_edge
          other_edge.match = edge
          break
        elif edge.edge == other_edge.edge[::-1]:
          edge.match = other_edge
          other_edge.match = edge
          break

    match_counts = {}
    for edge in edges:
      if edge.match is not None:
        if not edge.tile.id in match_counts:
          match_counts[edge.tile.id] = 1
        else:
          match_counts[edge.tile.id] += 1

    corner_ids = [tile_id for (tile_id, count) in match_counts.items() if count == 2]
    product = 1
    for tile_id in corner_ids:
      product *= tile_id

    print('Product of corner tile IDs:', product)

def read_tiles(filename):
  tiles = []
  with open(filename, 'r') as f:
    lines = []
    for line in f:
      line = line.replace('\n', '')
      if 'Tile' in line:
        tile_id = int(line.replace('Tile ', '').replace(':', ''))
      elif line != '':
        lines.append(line)
      else:
        tiles.append(Tile(tile_id, lines))
        lines = []
    if len(lines) > 0:
      tiles.append(Tile(tile_id, lines))
  return tiles

if __name__ == '__main__':
  parser = argparse.ArgumentParser(description=__doc__)
  parser.add_argument('filename', help='Path to the file with image tiles')
  args = parser.parse_args()

  tiles = read_tiles(args.filename)

  tm = TilesMap(tiles)
  tm.arrange()