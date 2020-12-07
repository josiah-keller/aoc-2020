#include <stdio.h>
#include <string.h>

#define NUM_QUESTIONS 26

int count_group_yeses(FILE *input_file, int all) {
  /*
    Explanation:
    for "any" mode, yeses is initialized to all 0's for each group. for each
    line, we iterate the characters and mark the corresponding spots in yeses
    as nonzero, then count them up at the end of the group.

    for "all" mode, yeses is initialized to all 1's for each group. for each
    line, each character is marked 1 and the previous value is shifted up into
    the 2's bit. then, an extra loop passes through all positions in yeses and
    shifts the value back down by one bit. this way, as long as you do find a
    given character, its nonzero value gets preserved - but as soon as you miss
    a character, the only set bit gets shifted out and it gets stuck at zero.
  */
  char line[NUM_QUESTIONS + 2]; // # of questions to answer + \n + NUL
  char yeses[NUM_QUESTIONS]; // each group's aggregate yeses
  int total_yeses = 0; // accumulator for entire file

  memset(yeses, all, NUM_QUESTIONS);

  while(fgets(line, NUM_QUESTIONS + 2, input_file)) {
    int line_len = strlen(line);
    if (line_len == 0 || line[0] == '\n') {
      for (int i=0; i<NUM_QUESTIONS; i++) {
        if (yeses[i]) {
          total_yeses += 1;
        }
      }
      memset(yeses, all, NUM_QUESTIONS);
      continue;
    }
    for(int i=0; i<line_len; i++) {
      char c = line[i];
      if (c < 'a' || c > 'z') continue;

      int idx = c - 'a';
      yeses[idx] = 1 | (yeses[idx] << 1);
    }
    if (all) {
      for (int i=0; i<NUM_QUESTIONS; i++) {
        yeses[i] >>= 1;
      }
    }
  }
  // handle last group in file
  for (int i=0; i<NUM_QUESTIONS; i++) {
    if (yeses[i]) {
      total_yeses += 1;
    }
  }
  return total_yeses;
}

void print_usage(FILE *stream, char *program_name) {
  fprintf(stream, "Usage: %s <FILE> <CRITERION>\n", program_name);
  fprintf(stream, "  where <FILE> is the path to the input file to process\n");
  fprintf(stream, "  and <CRITERION> is either 'any' or 'all'\n\n");
}

void print_help() {
  printf("Given an input FILE of customs questionnaire responses, count the\n"
         "\"yes\" responses for each customs group according to CRITERION\n"
         "and output the sum of those counts for the entire file.\n\n"

         "A group is a cluster of nonblank lines. Each line represents a\n"
         "single member of the group. Groups are separated by blank lines.\n"
         "Each character in a line represents a single \"yes\" answer to\n"
         "the question denoted by that character (a-z).\n\n"

         "CRITERION can be 'any' or 'all'. A value of 'any' counts only the\n"
         "*unique* yeses from *any* member of the group. A value of 'all'\n"
         "counts only the yeses marked by *all* members of the group.\n\n"

         "https://adventofcode.com/2020/day/6\n\n");
}

int main(int argc, char **argv) {
  if (argc != 3) {
    if (argc == 2 && strncmp(argv[1], "-h", 2) == 0) {
      print_usage(stdout, argv[0]);
      print_help();
      return 0;
    }
    print_usage(stderr, argv[0]);
    fprintf(stderr, "For more help, run with -h\n\n");
    return 1;
  }

  char *file_name = argv[1];
  FILE *input_file = fopen(file_name, "r");
  if (input_file == NULL) {
    perror("Could not open input file");
    return 1;
  }

  int all; // 0 for any mode, 1 for all mode
  if (strncmp(argv[2], "any", 3) == 0) {
    all = 0;
  } else if (strncmp(argv[2], "all", 3) == 0) {
    all = 1;
  } else {
    print_usage(stderr, argv[0]);
    return 1;
  }

  int yeses = count_group_yeses(input_file, all);
  printf("%d yes answers\n\n", yeses);

  fclose(input_file);
  return 0;
}