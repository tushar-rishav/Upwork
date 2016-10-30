#include  <stdio.h>
#include  <sys/types.h>

float avg(int arr[], int n)
{
   int i, s = 0;
   for (int i=0; i < n; i++)
       s += arr[i];
   return (float)s/n;
}
int prod(int arr[], int n)
{
  int p = 1;
  for (int i=0; i < n; i++) {
      if(arr[i] < 0)
        p *= arr[i];
  }
  return p;
}

void  main(void)
{
     pid_t  pid;
     int e, arr_size=10;

     printf("Enter 10 array elements\n");
     int* arr = (int*)malloc(arr_size*sizeof(int));
     for (int i = 0; i < arr_size; i++) {
       scanf("%d", &e);
       arr[i] = e;
     }
     pid = fork();
     if (pid == 0) { /* Child Process */
          printf("Product of negative numbers is %d\n", prod(arr, 10));
          printf("*** Child process is done ***\n");
     } else { /* Parent Process */
       printf("Average of numbers is %f\n", avg(arr, 10));
       printf("*** Parent process is done ***\n");
     }
}
