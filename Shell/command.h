#define MAX_CHAR_LINE 1024
#define MAX_NO_ARGS 10
#define MAX_COMMANDS 10
#define PIPE "|"

struct command
{
    char *comm;
    char *args[MAX_NO_ARGS+2];
    int no_args;
    int order;
};

void print_commands(struct command mycommands[], int no_commands);
