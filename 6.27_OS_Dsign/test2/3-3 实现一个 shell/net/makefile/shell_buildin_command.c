/*
 *    Description: ---
 *         Author: Lynn
 *          Email: lgang219@gmail.com
 *         Create: 2018-06-26 13:44:48
 *  Last Modified: 2018-06-26 14:03:24
 */

#include <string.h>
#include <stdio.h>
#include <stdlib.h> // exit
#include "myshell.h"
#include <string.h>
#include <sys/types.h>
#include <unistd.h> // chdir

#define MAX_DIR_NAME 256

int buildin_command(char **argv){   
    if(strcmp(argv[0],"exit")==0){
        exit(0);
    }
    if(strcmp(argv[0],"cd")==0){
        if(chdir(argv[1])){
            printf("myselous:cd:%s:no such directory\n",argv[1]);
        }
        return 1;
    }
    if(strcmp(argv[0],"pwd")==0){
        char buf[MAX_DIR_NAME];
        printf("%s\n",getcwd(buf,sizeof(buf)));
        return 1;
    }
    return 0;//not a buildin_command
}
