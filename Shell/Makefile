all: shell

shell: shell.o get_commands.o exec_commands.o
	gcc -g -o shell shell.o get_commands.o exec_commands.o

shell.o: shell.c command.h get_commands.h
	gcc -g -c shell.c

exec_commands.o: exec_commands.c command.h
	gcc -g -c exec_commands.c

get_commands.o: get_commands.c command.h
	gcc -g -c get_commands.c

clean:
	rm -f shell *.o
