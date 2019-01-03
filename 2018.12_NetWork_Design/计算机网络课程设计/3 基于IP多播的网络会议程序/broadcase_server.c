/*
 *    Description: ---
 *         Author: Lynn
 *          Email: lgang219@gmail.com
 *         Create: 2019-01-03 11:12:56
 *  Last Modified: 2019-01-03 14:44:28
 */


#include<stdio.h>
#include<string.h>
#include<unistd.h>
#include<arpa/inet.h>
#include<sys/socket.h>

#define MCAST_PORT 8888
#define MCAST_ADDR "224.0.0.100"
#define MCAST_DATA "BROADCAST TEST DATA"
#define MCAST_INTERVAL 2
#define BUFF_SIZE 256

int main()
{
    printf("I am the SERVER\n\n");

    int s;
    struct sockaddr_in mcast_addr;
    s = socket(AF_INET, SOCK_DGRAM, 0);
    if (s == -1)
    {
        perror("socket()");
        return -1;
    }
    memset(&mcast_addr, 0, sizeof(mcast_addr)); // 初始化IP多播地址为0
    mcast_addr.sin_family = AF_INET;
    mcast_addr.sin_addr.s_addr = inet_addr(MCAST_ADDR);
    mcast_addr.sin_port = htons(MCAST_PORT);

    while (1)
    {
        char buff[BUFF_SIZE];
        gets(buff);
        // int n = sendto(s, MCAST_DATA, sizeof(MCAST_DATA), 0, (struct sockaddr*)&mcast_addr, sizeof(mcast_addr));
        int n = sendto(s, buff, BUFF_SIZE, 0, (struct sockaddr*)&mcast_addr, sizeof(mcast_addr));
        if (n < 0)
        {
            perror("sendto()");
            return -2;
        }
        memset(buff, '0', BUFF_SIZE);

    }

    return 0;
}
