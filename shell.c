#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#define MAX_CHAR_LINE 1024
#define MAX_NO_ARGS 10
#define PIPE "|"

struct command
{
    char *comm;
    char *args[MAX_NO_ARGS+2]; //the first item is the command itself and the last is NULL
    int no_args; //actual number of arguments excluding the first item, command name, and the last item, NULL.
    int order; //the order of the command 0, 1, ...
};

int get_commands(char* line, struct command mycommands[]);
void print_commands(struct command mycommands[], int no_commands);
char *trimwhitespace(char *str);

int main()
{
    char *prompt = "cmps405>";
    char *line = NULL;
    size_t len = MAX_CHAR_LINE;
    ssize_t read = 0;
    struct command *mycommands; // an array to store the tokenized commands.
    int no_commands;
    while (read != -1) {
        printf("%s",prompt); //display prompt
        read = getline(&line, &len, stdin); // read line
        line = trimwhitespace(line);
        if(!strcmp(line,"\0")) continue; // blank line
        if(!strcmp(line,"exit")) break; // exit command
        mycommands = (struct command*)malloc(1024*sizeof(struct command));
        no_commands = get_commands(line, mycommands);
    		print_commands(mycommands, no_commands);
    }
    return 0;
}
int get_commands(char *line, struct command *mycommands) {
  int no_commands = 0, i = 0, j = 0;
  char *token, *arg;
  int c_read = 0, arg_count = 0;
  char *command_list[1024];

    token = strtok(line, PIPE);
    while(token != NULL) {
      command_list[no_commands] = token;
      no_commands++;
      token = strtok(NULL, PIPE);
    }
    for(i = 0; i < no_commands; i++) {
      c_read = 0; arg_count = 0;
      arg = strtok(command_list[i], " ");
      while(arg != NULL) {
        if(!c_read) mycommands[i].comm = arg;
        c_read = 1;
        mycommands[i].args[arg_count] = arg;
        arg_count++;
        if(arg_count>MAX_NO_ARGS) break;
        arg = strtok(NULL, " ");
      }
      mycommands[i].order = i;
      mycommands[i].no_args = arg_count-1;
    }
    return no_commands;
}

char *trimwhitespace(char *str)
{
  char *end;
  // Trim leading space
  while(isspace((unsigned char)*str)) str++;

  if(*str == 0)  // All spaces?
    return str;
  // Trim trailing space
  end = str + strlen(str) - 1;
  while(end > str && isspace((unsigned char)*end)) end--;
  // Write new null terminator
  *(end+1) = 0;
  return str;
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
