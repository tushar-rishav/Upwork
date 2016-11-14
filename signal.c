 #include <stdio.h>
 #include <sys/types.h>
 #include <sys/stat.h>
 #include <fcntl.h>
 #include <signal.h>
 #include <string.h>

 void my_handler(){
   exit(1);
 }

 int main() {
   char string[100];
   char buff[100];
   int pdes[2], n;
   pid_t pid;
   int fdl;
   pipe(pdes);
   pid = fork();
   if(pid==0){
     signal(SIGINT, my_handler);
     while(1){
       printf("Enter inputs\n");
       scanf("%s", string);
       close(pdes[0]);
       write(pdes[1], string, strlen(string)+1);

     }
   } else {
     while(1){
     close(pdes[1]);
     n = read(pdes[0], buff, sizeof(buff));
     if(!strcmp(buff, "Done")){
       printf("DONE\n");
       kill(pid, SIGINT);
       break;
     }
     printf("Characters count %s: %d\n", buff, strlen(buff));
    }
    wait(NULL);
    }
 }
