# 五、网络代理服务器的设计与实现

实现一个简易的proxy程序。proxy程序的功能：能够做“二传手”的工作。它自身处在能同时连通外界目标服务器和我的机器的位置上。我的机器把请求发送给它，它接受请求，把请求原封不动的抄下来发送给外界目标服务器；外界目标服务器响应了请求，把回答发送给它，它再接受回答，把回答原封不动的发送给我的机器。这样，我的机器实际上是把它当作了目标服务器（由于是原封不动的转抄，请求和回答没有被修改）。而它则是外界目标服务器的客户端。

## 课程设计内容

程序工作原理示意图如下所示：

 <pre>   
   +----------+        +-----------+       +----------+      +----------+
   |          |        |           |       |          |      |          |
   |          |        |           |       |          |      |          |
   |  APP     +------->| mproxy    |+------> mproxy   +------> Web      |
   |          |        |           |       |          |      |          |
   |          |        | client    |       | server   |      |          |
   +----------+        +-----------+       +----------+      +----------+
</pre>

## 课程设计结果及结果分析 心得体会

工作模式和普通的http代理一样，目前只做简单的http转发，不做任何页面的缓存。

## 程序源文件主要代码展示

**程序运行截图**

![2019-01-08 18-51-00 的屏幕截图](/home/lynn/Pictures/2019-01-08 18-51-00 的屏幕截图.png)

**程序主要代码展示**

```c
int snifer(int sock, int pPort,  char *pprototype, char *pipaddr)
{
    if (pPort > 0)
        printf("pPort:%d\n", pPort);
    if (pprototype != NULL)
        printf("pprototype:%s\n", pprototype);
//    if (pipaddr != NULL)
//        printf("pipaddr:%s\n", pipaddr);

    int n_read, proto;
    char buffer[BUFFER_MAX];
    char *ethhead, *iphead, *tcphead, *udphead, *icmphead, *p;
    unsigned int sport = 0; // source port
    unsigned int dport = 0; // destination prot

    n_read = recvfrom(sock, buffer, 2048, 0, NULL, NULL);
    /*
    14  6(dest)+6(source)+2(type or length) // MAC dst(6) + src(6) + type(2)  (p96)
    +
    20  ip header                           // IP static(20)
    +
    8  icmp, tcp or udp header              // UDP static(8)
    = 42
    */
    if (n_read < 42)
    {
        fprintf(stdout, "Incomplete header, packet corrupt\n");
        return -2;
    }

    ethhead = buffer;
    p = ethhead;
    int n = 0XFF; // 255

    // MAC address
    // printf("MAC:%.2X:%.02X:%02X:%02X:%02X:%02X=>"
    //        "%.2X:%.2X:%.2X:%.2X:%.2X:%.2X\n",
    //        p[6]&n, p[7]&n, p[8]&n, p[9]&n, p[10]&n, p[11]&n, p[0]&n, p[1]&n, p[2]&n, p[3]&n, p[4]&n, p[5]&n);
    int mac_src_addr[6];
    int mac_dst_addr[6];
    mac_src_addr[0] = p[6] & n;
    mac_src_addr[1] = p[7] & n;
    mac_src_addr[2] = p[8] & n;
    mac_src_addr[3] = p[9] & n;
    mac_src_addr[4] = p[10] & n;
    mac_src_addr[5] = p[11] & n;

    mac_dst_addr[0] = p[0] & n;
    mac_dst_addr[1] = p[1] & n;
    mac_dst_addr[2] = p[2] & n;
    mac_dst_addr[3] = p[3] & n;
    mac_dst_addr[4] = p[4] & n;
    mac_dst_addr[5] = p[5] & n;

    iphead = ethhead + 14; // position IP frame
    p = iphead + 12; // position src & dst

    // IP address
    // printf("IP:%d.%d.%d.%d => %d.%d.%d.%d\n",
    //        p[0] & 0XFF, p[1] & 0XFF, p[2] & 0XFF, p[3] & 0XFF, p[4] & 0XFF, p[5] & 0XFF, p[6] & 0Xff, p[7] & 0XFF);
    int ip_src_addr[4];
    int ip_dst_addr[4];
    ip_src_addr[0] = p[0] & n;
    ip_src_addr[1] = p[1] & n;
    ip_src_addr[2] = p[2] & n;
    ip_src_addr[3] = p[3] & n;
    ip_dst_addr[0] = p[4] & n;
    ip_dst_addr[1] = p[5] & n;
    ip_dst_addr[2] = p[6] & n;
    ip_dst_addr[3] = p[7] & n;

    // diff with pipaddr
    if (pipaddr != NULL)
    {
        char str_src[15] = {'\0'};
        char str_dst[15] = {'\0'};
        int i, L_src, L_dst;
        for (i = 0; i < 4; i++)
        {
            L_src = strlen(str_src);
            L_dst = strlen(str_dst);
            if (i < 3)
            {
                sprintf(str_src + L_src, "%d.", ip_src_addr[i]);
                sprintf(str_dst + L_dst, "%d.", ip_dst_addr[i]);
            }
            else
            {
                sprintf(str_src + L_src, "%d", ip_src_addr[i]);
                sprintf(str_dst + L_dst, "%d", ip_dst_addr[i]);
            }
        };
        // if str_src equal pipaddr or str_dst equal pipaddr
        if (strcmp(str_src, pipaddr) != 0 && strcmp(str_dst, pipaddr) != 0)
        {
            return -1;
        }
    }

    proto = (iphead + 9)[0]; // position Protocol (p130)
    p = iphead + 20; // position TCP/UDP frame

    // Protocol
    // get Port
    if (proto == IPPROTO_TCP)
    {
        sport = (p[0] << 8) & 0XFF00 | p[1] & 0XFF;
        dport = p[2] << 8 & 0XFF00 | p[3] & 0XFF;
    }
    else if (proto == IPPROTO_UDP)
    {
        sport = (p[0] << 8) & 0XFF00 | p[1] & 0XFF;
        dport = p[2] << 8 & 0XFF00 | p[3] & 0XFF;
    }

    printf("Protocol:");
    switch (proto) // int
    {
    case IPPROTO_ICMP:
        printf("\033[47;35mICMP\033[0m\n");
        break;
    case IPPROTO_IGMP:
        printf("\033[47;35mIGMP\033[0m\n");
        break;
    case IPPROTO_IPIP:
        printf("\033[47;35mIPIP\033[0m\n");
        break;
    case IPPROTO_TCP:
    case IPPROTO_UDP:
        if (pPort > 0)
        {
            if (pPort != sport)
                if (pPort != dport)
                    return -1;
        }
        printf("\033[47;35m%s\033[0m,", proto == IPPROTO_TCP ? "TCP" : "UDP");
        printf("source port:\033[;33m%u\033[0m,", sport);
        printf("dest port:\033[;33m%u\033[0m\n", dport);
        break;
    case IPPROTO_RAW:
        printf("\033[47;35mRAW\033[0m\n");
        break;
    default:
        printf("\033[47;41mUnkown\033[0m, please query in include/linux/in.h\n");
    }

    // Output
    // MAC adrress
    printf("MAC:%.2X:%.02X:%02X:%02X:%02X:%02X => "
           "%.2X:%.2X:%.2X:%.2X:%.2X:%.2X\n",
           mac_src_addr[0], mac_src_addr[1], mac_src_addr[2], mac_src_addr[3], mac_src_addr[4], mac_src_addr[5], mac_dst_addr[0], mac_dst_addr[1], mac_dst_addr[2], mac_dst_addr[3], mac_dst_addr[4], mac_dst_addr[5]);

    // IP address
    printf("IP:%d.%d.%d.%d => %d.%d.%d.%d\n",
           ip_src_addr[0], ip_src_addr[1], ip_src_addr[2], ip_src_addr[3], ip_dst_addr[0], ip_dst_addr[1], ip_dst_addr[2], ip_dst_addr[3]);


    return 0;
}

```

