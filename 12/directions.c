#include <stdio.h>
#include <string.h>
#include <stdlib.h>

#define MODE_DIRECT 0
#define MODE_HEADING 1

typedef struct VECTOR2_STRUCT {
  int x;
  int y;
} Vector2;

// Fetch the next direction from `file`. Read until a newline is encountered.
// The first character is written to `out_action`. The rest is parsed as an
// integer and written to `out_magnitude`. Return 0 on success, nonzero on
// failure (eg, invalid characters).
int next_direction(FILE *file, char *out_action, int *out_magnitude) {
  int i = 0;
  char c = fgetc(file);
  int magnitude = 0;
  while (c != '\n') {
    if (c == EOF) {
      if (i == 0) {
        return -1;
      } else {
        *out_magnitude = magnitude;
        return 0;
      }
    }
    if (i == 0) {
      if (c != 'N' && c != 'S' && c != 'E' && c != 'W' && c != 'L' && c != 'R' && c != 'F') {
        return -1;
      }
      *out_action = c;
    } else {
      if (c < 0x30 || c > 0x39) {
        return -1;
      }
      magnitude = magnitude * 10 + c - 0x30;
    }
    c = fgetc(file);
    i++;
  }
  *out_magnitude = magnitude;
  return 0;
}

// Add vector b to vector a. Results left in vector a.
void vector_add(Vector2 *a, Vector2 *b) {
  a->x += b->x;
  a->y += b->y;
}

// Ditto, but multiply
void vector_mul(Vector2 *a, Vector2 *b) {
  a->x *= b->x;
  a->y *= b->y;
}

void update_heading(Vector2 *heading, int angle) {
  int steps = (angle / 90) % 4;
  int direction = 1;
  int tmp;
  if (steps < 0) {
    steps = -steps;
    direction = -1;
  }
  while (steps--) {
    tmp = heading->y;
    heading->y = heading->x * direction;
    heading->x = tmp * (-direction);
  }
}

int calc_distance(FILE *file, int mode) {
  Vector2 position = { 0, 0 };
  Vector2 heading = { 1, 0 };
  Vector2 delta;
  char action;
  int magnitude;

  if (mode == MODE_HEADING) {
    heading.x = 10;
    heading.y = -1;
  }

  while (next_direction(file, &action, &magnitude) == 0) {
    delta.x = delta.y = 0;
    switch(action) {
      case 'N':
        if (mode == MODE_DIRECT) {
          delta.y = -magnitude;
        } else if (mode == MODE_HEADING) {
          heading.y -= magnitude;
        }
        break;
      case 'S':
        if (mode == MODE_DIRECT) {
          delta.y = magnitude;
        } else if (mode == MODE_HEADING) {
          heading.y += magnitude;
        }
        break;
      case 'E':
        if (mode == MODE_DIRECT) {
          delta.x = magnitude;
        } else if (mode == MODE_HEADING) {
          heading.x += magnitude;
        }
        break;
      case 'W':
        if (mode == MODE_DIRECT) {
          delta.x = -magnitude;
        } else if (mode == MODE_HEADING) {
          heading.x -= magnitude;
        }
        break;
      case 'F':
        delta.x = magnitude;
        delta.y = magnitude;
        vector_mul(&delta, &heading);
        break;
      case 'L':
        update_heading(&heading, -magnitude);
        break;
      case 'R':
        update_heading(&heading, magnitude);
        break;
    }
    vector_add(&position, &delta);
  }
  return abs(position.x) + abs(position.y);
}

void print_usage(FILE *stream, char *program_name) {
  fprintf(stream,
    "Usage: %s <FILE> <MODE>\n"
    "  where <FILE> is the path to a file containing directions\n"
    "  and <MODE> is either \"direct\" or \"heading\"\n\n",
    program_name);
}

void print_help() {
  printf(
    "Given a file of directions to follow, follow the directions and\n"
    "calculate the Manhattan distance from the starting point\n\n"
    "Each line of the directions file is a direction to follow. The first\n"
    "character denotes an action or direction. The rest of the line\n"
    "is an operand specifying the number of units to travel, or degrees to\n"
    "turn.\n\n"
    "IN DIRECT MODE:\n"
    "N, S, E, or W result in travel by the specified number of units\n"
    "in that direction, without turning. L or R turns by a specified angle.\n"
    "F travels forward in the current direction.\n\n"
    "IN HEADING MODE:\n"
    "N, S, E, or W adjust the heading by the specified number of units.\n"
    "L or R still rotate the heading. F travels towards the current heading\n"
    "by the specified number of steps\n\n"
    "https://adventofcode.com/2020/day/12\n\n"
  );
}

int main(int argc, char **argv) {
  if (argc != 3) {
    if (argc == 2 && strncmp(argv[1], "-h", 2) == 0) {
      print_usage(stdout, argv[0]);
      print_help();
      return 0;
    }
    print_usage(stderr, argv[0]);
    fprintf(stderr, "For more help, run %s -h\n\n", argv[0]);
    return 1;
  }

  char *file_name = argv[1];
  FILE *file = fopen(file_name, "r");

  int mode;
  if (strcmp(argv[2], "direct") == 0) {
    mode = MODE_DIRECT;
  } else if (strcmp(argv[2], "heading") == 0) {
    mode = MODE_HEADING;
  } else {
    print_usage(stderr, argv[0]);
    fprintf(stderr, "Invalid mode argument. For help, run %s -h\n\n", argv[0]);
    return 1;
  }

  int distance = calc_distance(file, mode);
  printf("Manhattan distance: %d\n", distance);

  fclose(file);

  return 0;
}