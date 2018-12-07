/*
 *    Description: ---
 *         Author: Lynn
 *          Email: lgang219@gmail.com
 *         Create: 2018-12-07 19:40:21
 *  Last Modified: 2018-12-07 20:54:07
 */

#include<stdio.h>
#include<pcap.h>

int main(int argc, char *argv[])
{
    pcap_t *handle;
    char *dev, errbuf[PCAP_ERRBUF_SIZE];
    struct bpf_program fp; // The compiled filter expression
    char filter_exp[] = "port 80"; // The filter expression
    bpf_u_int32 mask; // The netmask of our sniffing device
    bpf_u_int32 net; // The IP of our sniffing device
    struct pcap_pkthdr header; // The header that pcap gives us
    const u_char *packet; // The actual packet

    dev = pcap_lookupdev(errbuf);
    if (dev == NULL)
    {
        fprintf(stderr, "Couldn't find default device:%s\n", errbuf);
        return (2);
    }
    printf("Device:%s\n", dev);

    // Find the properties for the device
    if (pcap_lookupnet(dev, &net, &mask, errbuf) == -1)
    {
        fprintf(stderr, "Couldn't get netmask for devices %s:%s\n", dev, errbuf);
        net = 0;
        mask = 0;
    }

    // Open the session in promiscuous mode
    // sniff
    handle = pcap_open_live(dev, BUFSIZ, 1, 1000, errbuf);
    if (handle == NULL)
    {
        fprintf(stderr, "Couldn't open device %s:%s\n", dev, errbuf);
        return (2);
    }

    // Compile and apply the filter
    // filter expression
    if (pcap_compile(handle, &fp, filter_exp, 0, net) == -1)
    {
        fprintf(stderr, "Couldn't parse filter %s:%s\n", filter_exp, pcap_geterr(handle));
        return (2);
    }
    // set filter expression
    if (pcap_setfilter(handle, &fp) == -1)
    {
        fprintf(stderr, "Couldn't install filter %s:%s\n", filter_exp, pcap_geterr(handle));
        return (2);
    }

    // Grab a packet
    packet = pcap_next(handle, &header);
    // Print its length
    printf("Jacked a packet with length of [%d]\n", header.len);
    // And close the session
    pcap_close(handle);

    return (0);
}
