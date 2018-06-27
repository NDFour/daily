/*
 *    Description: ---
 *         Author: Lynn
 *          Email: lgang219@gmail.com
 *         Create: 2018-06-26 13:44:24
 *  Last Modified: 2018-06-26 14:39:32
 */

#include <stdio.h>
#include <stdlib.h>
#include "myshell.h"

int parseline(char *buf,char**argv){ 
    while(*buf==' '){
        buf++;
    }
    int delim = 0;

    int argc = 0;
    while(*buf!='\n'){

        while(buf[delim]!='\n'&&buf[delim]!=' '){
            delim++;
        }

        if(buf[delim] == '\n'){
            buf[delim] = '\0';
            argv[argc++] = buf;
            break;
        }
        buf[delim] = '\0';
        argv[argc++] = buf; 

        buf+=delim+1;
        /*指示器indicator=0*/
        delim = 0;
        while(*buf==' '){
            buf++;
        }
    }
    /*the last element is NULL*/
    argv[argc] = NULL;
    return 0;
}
