/*
 *    Description: ---
 *         Author: Lynn
 *          Email: lgang219@gmail.com
 *         Create: 2018-06-25 14:44:48
 *  Last Modified: 2018-06-25 16:32:45
 */
#include<stdio.h>
#include<sys/types.h>
#include<unistd.h>

int main(void)

{

       pid_t pid1;
       pid_t pid2;
       pid1=fork();    /*这里定义第一个子进程*/

       if(pid1<0)
              printf("Error.fock call fail\n");
       //else if(pid1!=0 && pid2!=0)
              //print("This is the parent process/n");
       else if(pid1 == 0)           /*当第一个子进程运行时*/
              printf("This is the NO.1 child process\n");
       else
       {
               pid2=fork();    /*这里定义第二个子进程*/
               if(pid2<0)
                       printf("Error.NO.2 fork call fail\n");
               if(pid2 == 0)           /*当第二个子进程运行时*/
                       printf("This is the NO.2 child process\n");
               else
                       printf("This is the parent process\n");
       }

       printf("Fork end.\n\n");

       exit(0);
}
