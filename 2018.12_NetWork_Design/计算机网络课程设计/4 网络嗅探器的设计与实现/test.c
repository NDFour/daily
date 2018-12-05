/*
 *    Description: ---
 *         Author: Lynn
 *          Email: lgang219@gmail.com
 *         Create: 2018-12-05 18:24:12
 *  Last Modified: 2018-12-05 18:29:24
 */

#include<stdio.h>
#include<unistd.h>

int main(int argc, char **argv)
{
    int ch;
    // opterr=0;
    while ((ch = getopt(argc, argv, "a:b:cde")) != -1)
        switch (ch)
        {
        case 'a':
            printf("Operation a:%s\n", optarg);
            break;
        case 'b':
            printf("Operation b:\n");
            break;
        default:
            printf("Other option:%c\n", optopt);
        }
}
