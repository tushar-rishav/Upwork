#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <sys/wait.h>

#include "command.h"

void execute_commands(struct command mycommands[], int no_commands)
{
	int i, fdin, ret, fdout;
	int tmpin = dup(0);
	int tmpout = dup(1); // to restore stdin, stdout before returning.

	fdin = dup(tmpin);
	for(i=0; i < no_commands; i++) {
		dup2(fdin, 0); // redirect stdin from fdin
		close(fdin);
		if(i == no_commands-1) {
			fdout = dup(tmpout);
		} else {
				int fdpipe[2];
				pipe(fdpipe);
				fdout = fdpipe[1];
				fdin = fdpipe[0];
		}
		dup2(fdout, 1); // redirect stdout to fdout
		close(fdout);
		ret = fork();
		if(!ret) {
			execvp(mycommands[i].comm, mycommands[i].args);
			perror(NULL);
			exit(1);
		}
	}

	dup2(tmpin, 0);
	dup2(tmpout, 1);
	close(tmpin);
	close(tmpout);
	wait(&ret);
	//waitpid(-1, &ret, NULL);
	return;
}
