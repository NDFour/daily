/*
 *    Description: ---
 *         Author: Lynn
 *          Email: lgang219@gmail.com
 *         Create: 2018-11-25 12:50:32
 *  Last Modified: 2018-12-26 10:09:23
 */

#include<iostream>
#include <string.h>
#include <stdlib.h>
#include <unistd.h>
#include <arpa/inet.h>
#include <sys/socket.h>
using namespace std;

int main()
{
    // request to serv (ip & port)
    struct sockaddr_in serv_addr;
    // fill with 0 each byte
    memset(&serv_addr, 0, sizeof(serv_addr));

    serv_addr.sin_family = AF_INET;
    serv_addr.sin_addr.s_addr = inet_addr("127.0.0.1");
    serv_addr.sin_port = htons(1234);

    /*
    char usr_name[10];
    cout << "Please input your name:" << endl;
    cin >> usr_name;
    cout << "User_Name:" << usr_name << endl;
    */

    char str_smthing[100] = {0};
    char buffer[100] = {0};

    while (1)
    {
        // create socket
        int sock = socket(AF_INET, SOCK_STREAM, 0);
        connect(sock, (struct sockaddr*)&serv_addr, sizeof(serv_addr));

        // input smthing to send to serv
        cout << "To Server:";
        // cin >> str_smthing;
        string data;
        getline(cin, data);
        strcpy(str_smthing, data.c_str());
        // write to serv
        // int w_state = write(sock, msg, sizeof(msg));
        int w_state = write(sock, str_smthing, sizeof(str_smthing));
        cout << "Send succ :" << w_state << endl;

        // read msg from serv
        read(sock, buffer, sizeof(buffer) - 1);
        cout << "Message from server:" << buffer << endl << endl;

        // clean buffer
        memset(str_smthing, 0, sizeof(str_smthing));
        memset(buffer, 0, sizeof(buffer));
        // close sock
        close(sock);
    }

    return 0;
}
