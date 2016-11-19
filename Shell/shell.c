#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#include "command.h"
#include "get_commands.h"
#include "exec_commands.h"

int main()
{
    char *prompt = "cmps405> ";
    char *line = NULL;
    size_t len = MAX_CHAR_LINE;
    ssize_t read = 0;
    struct command *mycommands;
    int no_co = 0;

    while (read != -1) {
	     printf("%s", prompt);
	      read = getline(&line, &len, stdin);
	      line = trimwhitespace(line);
	      if (strcmp(line, "exit") == 0) {
	         break;
	      }
	      // Check if the user entered a blank line
      	if (strcmp(line, "") == 0) {
      	    continue;
      	}
      	mycommands = (struct command*)malloc(MAX_CHAR_LINE*sizeof(struct command));
      	no_co = get_commands(line, mycommands);
      	execute_commands(mycommands, no_co);
        // print_commands(mycommands, no_co);
    }
    return 0;
}
void print_commands(struct command mycommands[], int no_commands)
{
    int i;
    for(i=0; i < no_commands; i++)
    {
        int j;
        printf("command order: %d\n", mycommands[i].order);
        printf("command : %s\n", mycommands[i].comm);
        printf("no of args: %d\n", mycommands[i].no_args);
        printf("args: ");
        for(j=1; j <= mycommands[i].no_args; j++)
        {
            printf("%s ", mycommands[i].args[j]);
        }
        printf("\n");
    }
}
