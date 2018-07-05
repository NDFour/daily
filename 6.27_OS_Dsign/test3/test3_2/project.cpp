#include "windows.h"
#include "process.h"
#include<iostream>
#include <time.h>
using namespace std;


#define P(S) WaitForSingleObject(S,INFINITE)//定义Windows下的P操作

// A handle to the semaphore object.
// The amount by which the semaphore object's current count is to be increased. 
// A pointer to a variable to receive the previous count for the semaphore.
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
	// door 确保 readercount 被正确更新
    P(door);
    readercount++;
    if(readercount == 1)
        P(wsm);
    V(door);

    cout<<"Readding... [ID]："<<GetCurrentThreadId()<<endl;
    Sleep(500);

    P(door);
    readercount--;
    if(readercount == 0)
        V(wsm);
    V(door);
    cout<<"Read complete"<<GetCurrentThreadId()<<endl;
    return 1;
};

// 写者
DWORD WINAPI writer()
{
    P(wsm);

    Sleep(200);
    cout<<"Writting... [ID]："<<GetCurrentThreadId()<<endl;

    V(wsm);
    cout<<"Wrote complete"<<GetCurrentThreadId()<<endl;

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
        if( (rC % 6)==0)
			// writer
            CreateThread(NULL,0,(LPTHREAD_START_ROUTINE)writer,NULL,NULL,NULL);
        else
			// reader
            CreateThread(NULL,0,(LPTHREAD_START_ROUTINE)reader,NULL,NULL,NULL);

    }

    // Sleep(600000);
	cout<<"Program finished"<<endl;
    return 0;
}
