/*
 *    Description: ---
 *         Author: Lynn
 *          Email: lgang219@gmail.com
 *         Create: 2018-12-05 16:34:10
 *  Last Modified: 2018-12-09 17:00:22
 */

#include<stdio.h>
#include<stdlib.h>
#include<string.h>
#include<unistd.h>
#include<sys/socket.h>
#include<string.h>
#include<arpa/inet.h>
#include<sys/types.h>
#include<linux/if_ether.h>
#include<linux/in.h>

// snifer frame  0:succ  -1:parameters not equall  -2:incomplete header
int snifer(int sock, int pPort, char *pprototype, char* pipaddr);
// -h show help msg
void showhelp();
// translate char to int
int char2int(char ch);
// array to string
char* arr2str(char ch[4]);
// calc how many nums a number
int calcmany(int a);

#define BUFFER_MAX 2048

int main(int argc, char* argv[])
{
    int sock;
    int pPort = -1;
    int n_packages = 0;
    char *pprototype = NULL;
    char *pipaddr = NULL;

    char2int('1');
    char2int('9');
    char2int('0');
    char2int('d');

    // parse paramters
    int ch;
    // opterr = 0;
    while ((ch = getopt(argc, argv, "a:P:p:n:h")) != -1)
        switch (ch)
        {
        case 'a': // ip
            printf("Filter IP:%s\n", optarg);
            pipaddr = optarg;
            break;
        case 'P': // Port
            // atoi: translate str to int
            printf("Filter Port:%d\n", atoi(optarg));
            pPort = atoi(optarg);
            break;
        case 'p': // protocol
            printf("Filter Protocol:%s\n", optarg);
            pprototype = optarg;
            break;
        case 'n': // n packages
            printf("N packages:%s\n", optarg);
            n_packages = atoi(optarg);
            break;
        case 'h': // help
            showhelp();
            return 0;
        default:
            printf("Unknown Filter:%c\n", optopt);
        }
    printf("\n");

    sock = socket(PF_PACKET, SOCK_RAW, htons(ETH_P_IP));
    if (sock < 0)
    {
        printf( "create socket error\n");
        exit(0);
    }

    // always sniff
    while (1)
    {
        int snifer_rel = 0;
        int n_tmp = n_packages;
        while (n_tmp != 0)
        {
            // int snifer(int sock, int pPort, char *pprototype, char* pipaddr, char *pmacaddr);
            snifer_rel = snifer(sock, pPort, pprototype, pipaddr);
            if (snifer_rel == 0)
            {
                printf("\n");
                n_tmp--;
            }
        }
        break;
    }

    printf("\n\nAll Down !\n%d packages\n", n_packages);

    return 0;
}


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

// -h show help msg
void showhelp()
{
    printf("\tSnifer Everything\n\n");
    printf("  -a  Filte by IP address\n");
    printf("  -m  Filte by MAC address\n");
    printf("  -P  Filte by PORT\n");
    printf("  -p  Filte by Protocol\n");
    printf("  -h  Show this message\n");
    printf("\n");
    printf(" sudo ./snifer -a 10.1.8.1 -m ff:ff:ff:ff -P 1080 -p TCP\n\n");
}


// translate char to int
int char2int(char ch)
{
    if (ch < 48 || ch > 59)
    {
        printf("\033[47;41munknow Port\033[0m\n");
        return -1;
    }
    int poi = (int)ch;
    printf("char2int:%d\n", poi - 48);
    return poi;
}

// array to string
char* arr2str(char ch[4])
{
    printf("INTO arr2str\n");
    char * b = "";
    for (int i = 0; i < 4; i++)
    {
        //b[i] = ch[i];
        printf("%d", ch[i]);
    }
    return b;
}

// calc how many nums a number
int calcmany(int a)
{
    int b = 0;
    if (a < 10)
        b = 1;
    else if (a < 100)
        b = 2;
    else if (a < 1000)
        b = 3;
    return b;
}
