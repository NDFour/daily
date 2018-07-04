#include "windows.h"
#include "process.h"
#include<iostream>
#include <time.h>
using namespace std;


#define P(S) WaitForSingleObject(S,INFINITE)//定义Windows下的P操作
#define V(S) ReleaseSemaphore(S,1,NULL)//定义Windows下的V操作

HANDLE Wmutex, Rmutex ,Authmutex,Amutex;
int Rcount = 0;
int waitAuthCount=0;
int authFlag=1;


HANDLE wsm,door;
int readercount = 0;

// 读者
DWORD WINAPI reader()
{
    P(door);
    readercount++;
    if(readercount == 1)
        P(wsm);
    V(door);

    cout<<"正在读数据，，，线程ID："<<GetCurrentThreadId()<<endl;
    Sleep(500);

    P(door);
    readercount--;
    if(readercount == 0)
        V(wsm);
    V(door);
    cout<<"读取完毕 ："<<GetCurrentThreadId()<<endl;
    return 1;
};

// 写者
DWORD WINAPI writer()
{
    P(wsm);

    Sleep(200);
    cout<<"正在写数据，，，线程ID："<<GetCurrentThreadId()<<endl;

    V(wsm);
    cout<<"写入完毕"<<GetCurrentThreadId()<<endl;

    return 1;
};

int main(int argc, char* argv[])
{
	// 函数原型
	//
	// HANDLE CreateSemaphoreA(
    //    LPSECURITY_ATTRIBUTES lpSemaphoreAttributes,
    //    LONG                  lInitialCount,
    //    LONG                  lMaximumCount,
    //    LPCSTR                lpName
	// );
    wsm = CreateSemaphore(NULL,1,1,NULL);
    door = CreateSemaphore(NULL,1,1,NULL);

    while(1)
    {
        Sleep(100);
        srand((unsigned)time(NULL));
        int rC=rand()%1000;
        Sleep(rC);
        if( rC % 6==0)
			// writer
            CreateThread(NULL,0,(LPTHREAD_START_ROUTINE)writer,NULL,NULL,NULL);
        else
			// reader
            CreateThread(NULL,0,(LPTHREAD_START_ROUTINE)reader,NULL,NULL,NULL);

    }

    Sleep(600000);
    return 0;
}
