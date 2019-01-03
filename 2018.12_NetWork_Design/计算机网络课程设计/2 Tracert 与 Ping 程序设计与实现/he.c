/*
 *    Description: ---
 *         Author: Lynn
 *          Email: lgang219@gmail.com
 *         Create: 2019-01-03 09:48:00
 *  Last Modified: 2019-01-03 09:56:11
 */

#include<stdio.h>
#include<stdlib.h>
#include<string.h>


int main()
{
    printf("jjj\n");
    int i=23;
    char ch[10];
    memset(ch, '\0' , sizeof(ch));
    sprintf(ch, "%d", i);
    printf("after sprintf\n");
    printf("%s\n",ch);

    return 0;
}
