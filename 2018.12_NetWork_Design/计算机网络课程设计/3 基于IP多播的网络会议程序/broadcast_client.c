/*
 *    Description: ---
 *         Author: Lynn
 *          Email: lgang219@gmail.com
 *         Create: 2019-01-03 11:20:38
 *  Last Modified: 2019-01-03 14:45:41
 *
 *
 *  1>建立一个socket;
 *  2>设置多播的参数，例如超时时间TTL，本地回环许可LOOP等
 *  3>加入多播组
 *  4>发送和接收数据
 *  5>从多播组离开
 */

#include<stdio.h>
#include<string.h>
#include<unistd.h>
#include<arpa/inet.h>
#include<sys/socket.h>

#define MCAST_PORT 8888
#define MCAST_ADDR "224.0.0.100"
#define MCAST_INTERVAL 5
#define BUFF_SIZE 256

int main()
{
    printf("I am the CLIENT\n\n");

    int s;
    struct sockaddr_in local_addr;
    int err = -1;

    // create socket
    s = socket(AF_INET, SOCK_DGRAM, 0);
    if (s == -1)
    {
        perror("socket()");
        return -1;
    }

    // fill with 0
    memset(&local_addr, 0, sizeof(local_addr));
    local_addr.sin_family = AF_INET;
    local_addr.sin_addr.s_addr = htonl(INADDR_ANY); // INADDR_ANY:回送到默认接口
    local_addr.sin_port = htons(MCAST_PORT);

    err = bind(s, (struct sockaddr*)&local_addr, sizeof(local_addr));
    if (err < 0)
    {
        perror("bind()");
        return -2;
    }

    // 设置回环许可
    int loop = 1; // 1: 允许数据回送到本地的回环接口
    err = setsockopt(s, IPPROTO_IP, IP_MULTICAST_LOOP, &loop, sizeof(loop));
    if (err < 0)
    {
        perror("setsockopt():IP_MULTICAST_LOOP");
        return -3;
    }

    // 加入多播祖
    struct ip_mreq mreq;
    mreq.imr_multiaddr.s_addr = inet_addr(MCAST_ADDR);
    mreq.imr_interface.s_addr = htonl(INADDR_ANY); // 网络接口为默认

    err = setsockopt(s, IPPROTO_IP, IP_ADD_MEMBERSHIP, &mreq, sizeof(mreq));
    if (err < 0)
    {
        perror("setsockopt():IP_ADD_MEMBErSHIP");
        return -4;
    }

    int times = 0;
    int addr_len = 0;
    char buff[BUFF_SIZE];
    int n = 0;
    for (times = 0; times < 5; times++)
    {
        addr_len = sizeof(local_addr);
        memset(buff, 0, BUFF_SIZE); // 清空接收缓冲区
        n = recvfrom(s, buff, BUFF_SIZE, 0, (struct sockaddr*)&local_addr, &addr_len);
        if (n == -1)
        {
            perror("recvfrom()");
        }

        printf("Recv %dst message from server:%s\n", times, buff);
        // sleep(MCAST_INTERVAL);
    }

    err = setsockopt(s, IPPROTO_IP, IP_DROP_MEMBERSHIP, &mreq, sizeof(mreq));

    close(s);
    return 0;
}
