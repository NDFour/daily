/*
 *    Description: ---
 *         Author: Lynn
 *          Email: lgang219@gmail.com
 *         Create: 2018-06-26 09:45:56
 *  Last Modified: 2018-06-26 13:33:58
 */

#include<stdio.h>
#include<unistd.h>
#include<stdlib.h>
#include<fcntl.h>
#include<sys/stat.h>
#include<string.h>

#define N 256

int main(void)
{
    printf("----- HELLO __ mySH -----\n\n\n");

    // shell function()
    char buffer[N];
    int fd;

    while(1)
    {
        printf("$ ");
        bzero(buffer,N);
        fgets(buffer,N,stdin);
        buffer[strlen(buffer)-1]='\0'; // cut the '\n'

        // 退出功能
        if(strcmp(buffer,"q")==0) // function <quit>
        {
            printf("mySH will be quit...\n");
            break;
        } 
        
        // cd 功能
        else if(strcmp(buffer,"cd")==0) // function <cd>
        {
            if((fd=open(buffer+3,O_RDONLY))<0)
            {
                printf("open error!\n");
                exit(1);
            }
            if(fchdir(fd)<0) // use fchdir to change the directory
            {
                printf("cd command error!\n");
                // exit();
            }
        } 
        
        // ls 功能
        else if(strcmp(buffer,"ls")==0) // test if the <cd> function is success
        {
            if(system(buffer)<0) // use <system> to execute shell script
            {
                printf("ls command error\n");
            }
        } 
        
        // 其他功能
        else // unlisten the other instruction
        {
            printf("other command, but undefind! \n");
            printf("88%s99\n",buffer);
        }
        close(fd); // close the file object
    }

    return 0;
}
