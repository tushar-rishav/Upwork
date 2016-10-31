#include <stdio.h>
#include <sys/types.h>
#include <unistd.h>
#include <stdlib.h>
#include <sys/wait.h>

void  main(void)
{
     pid_t  pid;
     ssize_t read = 0;
     char *command = NULL;
     size_t len = 1024;
     int ret, status, zombie_child_pid;
     printf("Enter the command :\n");
     read = getline(&command, &len, stdin);

     pid = fork();

     if (pid == 0) { /* Child Process */
          printf("Child reports its own PID as: %d\n", getpid());
          printf("Child reports its parent's PID as: %d\n", getppid());
          printf("Executing the '/myScript.sh' file..\n");
          ret = system("sh /myScript.sh");
          if (ret == -1) {
            perror("execv");
            exit(2);
          }
          printf("*** Child process is done ***\n");
     } else { /* Parent Process */
       zombie_child_pid = wait (&status); // Zombies
       printf("Parent reports Child and Zombie Child PID as: %d %d\n", pid, zombie_child_pid);
       printf("Executing the given command: %s\n", command);
       ret = system(command);
       if (ret == -1) {
         perror("execv");
         exit(1);
       }
       printf("*** Parent process is done ***\n");
     }
}
