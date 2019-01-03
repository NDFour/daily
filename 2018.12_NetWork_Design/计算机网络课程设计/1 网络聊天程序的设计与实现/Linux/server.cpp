/*
 *    Description: ---
 *         Author: Lynn
 *          Email: lgang219@gmail.com
 *         Create: 2018-11-25 11:43:12
 *  Last Modified: 2018-12-26 09:33:29
 */

#include<iostream>
#include<string.h>
#include<stdlib.h>
#include<unistd.h>
#include<arpa/inet.h>
#include<sys/socket.h>
#include<netinet/in.h>
using namespace std;

int main()
{
    // create socket
    int serv_sock = socket(AF_INET, SOCK_STREAM, IPPROTO_TCP);

    // bind socket with ip & port
    struct sockaddr_in serv_addr;
    // fill with 0 each byte
    memset(&serv_addr, 0, sizeof(serv_addr));
    // use IPV4
    serv_addr.sin_family = AF_INET;
    serv_addr.sin_addr.s_addr = inet_addr("127.0.0.1");
    serv_addr.sin_port = htons(1234);
    bind(serv_sock, (struct sockaddr*)&serv_addr, sizeof(serv_addr));

    cout << "Create socket suss!" << endl;

    // listen
    listen(serv_sock, 20);

    cout << "Listening..." << endl << endl;

    // accept client's requests
    struct sockaddr_in clnt_addr;
    socklen_t clnt_addr_size = sizeof(clnt_addr);

    while (1)
    {
        // accept can pause code to run, until receive a request
        cout << "Wait client to accept..." << endl;
        int clnt_sock = accept(serv_sock, (struct sockaddr * )&clnt_addr, &clnt_addr_size);
        cout << "Accept one request" << endl;

        // send msg to client
        char buffer[100] = {0};
        int strLen = read(clnt_sock, buffer, sizeof(buffer) - 1);
        // int w_l = write(clnt_sock, buffer, sizeof(buffer));
        // cout << "Write " << w_l << " bytes" << endl << endl;
        cout << "From Client:" << buffer << endl << endl;
        cout << "To Client:";
        cin >> buffer;
        write(clnt_sock, buffer, sizeof(buffer));
        cout << "Write to client succ" << endl << endl;

        // close client socket
        close(clnt_sock);
        // clean buffer
        memset(buffer, 0, sizeof(buffer));

    }
    // close serv sock
    close(serv_sock);

    return 0;
}
