/*
 *    Description: ---
 *         Author: Lynn
 *          Email: lgang219@gmail.com
 *         Create: 2018-06-26 13:43:09
 *  Last Modified: 2018-06-26 13:59:53
 */

#include <string.h>
#include "myshell.h"
#include <sys/types.h> // fork , waitpid
#include <unistd.h> // fork
#include <sys/wait.h> // wait
#include <stdio.h>
#include <stdlib.h> // exit(0)
#define MAX_CMD 256

void eval(char *cmdstring){
    /*parse the cmdstring to argv*/
    char *argv[MAX_CMD];
    /*Holds modified command line*/
    char buf[MAX_CMD];

    strcpy(buf,cmdstring);
    /*parse the cmdstring*/
    parseline(buf,argv);
    if(argv[0]==NULL){
        return;/*ignore empty lines*/
    }
    /*is a buildin command*/
    /*direct return*/
    if(buildin_command(argv)) return;
    int pid = fork();
    if(pid == 0){
        if(execvp(argv[0],argv)<0){
            printf("%s:command not found.\n",argv[0]);
            exit(0);
        }
    }
    // wait(pid);
    wait(NULL);
}
