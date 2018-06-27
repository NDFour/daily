/*
 *    Description: ---
 *         Author: Lynn
 *          Email: lgang219@gmail.com
 *         Create: 2018-06-25 16:38:37
 *  Last Modified: 2018-06-25 17:40:56
 */

#include <sys/types.h>
#include <stdio.h>
#include <unistd.h>
int main()
{
        pid_t pid;
        pid = fork();
        if (pid < 0)
        {
                fprintf(stderr, "Fork Failed");
                return 1;
        }
        else if (pid == 0)
        { 
                // int execlp( const char *file, const char *arg, ...);
                // 作为约定,第一个 arg 参数应该指向执行程序名自身,参数列表必须用 NULL 指针结束
                execlp("/bin/ls","ls",NULL);
                exit();
        }
        else { 
                /* 父进程将一直等待,直到子进程运行完毕*/

                //wait(NULL);
                wait();
                printf("Child Complete");
        }
        return 0;
}
