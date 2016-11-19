#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <ctype.h>

#include "command.h"


char *trimwhitespace(char *str)
{
  char *end;
  while(isspace((unsigned char)*str)) {
    str++;
  }
  if(*str == 0) return str;
  end = str + strlen(str) - 1;
  while(end > str && isspace((unsigned char)*end)) {
    end--;
  }
  *(end+1) = 0;
  return str;
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
      arg = strtok(command_list[i], " \t");
      while(arg != NULL) {
        if(!c_read) {
          mycommands[i].comm = arg;
        }
        c_read = 1;
        mycommands[i].args[arg_count] = arg;
        arg_count++;
        if(arg_count > MAX_NO_ARGS)
          break;
        arg = strtok(NULL, " \t");
      }
      mycommands[i].order = i;
      mycommands[i].no_args = arg_count-1;
    }
    return no_commands;
}
