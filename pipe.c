#include <sys/ipc.h>
#include <stdlib.h>
#include <stdio.h>
#include <unistd.h>
#include <string.h>

#define SIZE 1024

int dup2(int fildes_copy, int fildes_orig);

int main() {
  int pid;
  int pfds[2];
  char whoami[2048], grep[2048] = "";
  FILE *fp;
  pipe(pfds);

  if(fork()) {
    /* parent process */
    dup2(pfds[1], 1); // close the normal stdout and pick our own.
    close(pfds[0]);
    system("ps aux");
  } else {
    /* child process */
    dup2(pfds[0], 0); // close the normal stdin and pick our own.
    close(pfds[1]);

    // read the current logged in user
    fp = popen("whoami", "r");
    if (fp == NULL) {
      printf("Failed to run command\n" );
      exit(1);
    }
    fgets(whoami, sizeof(whoami)-1, fp);
    pclose(fp);
    // build the filter command
    strcat(grep, "grep");
    strcat(grep, " ");
    strcat(grep, whoami);
    system(grep);
  }
  return 0;
}
