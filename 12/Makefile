CC=gcc
CFLAGS=-Wall -g

directions: directions.o
	$(CC) $(CFLAGS) -o $@ $^

.PHONY: clean
clean:
	$(RM) directions
	$(RM) *.o
