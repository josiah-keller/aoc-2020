CC=gcc
CFLAGS=-Wall -g

customs: customs.o
	$(CC) $(CFLAGS) -o $@ $^

.PHONY: clean
clean:
	$(RM) customs
	$(RM) *.o
