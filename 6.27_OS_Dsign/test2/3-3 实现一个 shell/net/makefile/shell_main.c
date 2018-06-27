/*
 *    Description: ---
 *         Author: Lynn
 *          Email: lgang219@gmail.com
 *         Create: 2018-06-26 13:40:09
 *  Last Modified: 2018-06-26 14:34:33
 */

#include <stdio.h>
#include <stdlib.h>
#include <unistd.h> // io: read | write
#include "myshell.h"

#define MAX_CMD 256

int main(int argc,char *argv[]){
// int main(void){

    char cmdstring[MAX_CMD];
    int n;
    while(1){
        printf("*myshell*>");
        fflush(stdout);

        /*read*/
        if((n=read(0,cmdstring,MAX_CMD))<0){
            printf("read error");
        }

        eval(cmdstring);
    }
    return 0;
}
