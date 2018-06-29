# 操作系统课设  -- 实验三 设计报告

### 步骤1 - 步骤2
**实验代码：**
```c
// test3_1.cpp : Defines the entry point for the console application.
//

#include "stdafx.h"
#include <windows.h>
#include <iostream>
const unsigned short SIZE_OF_BUFFER = 2; //缓冲区长度
unsigned short ProductID = 0; //产品号
unsigned short ConsumeID = 0; //将被消耗的产品号
unsigned short in = 0; //产品进缓冲区时的缓冲区下标
unsigned short out = 0; //产品出缓冲区时的缓冲区下标
int buffer[SIZE_OF_BUFFER]; //缓冲区是个循环队列
bool p_ccontinue = true; //控制程序结束

HANDLE Mutex; //用于线程间的互斥
HANDLE FullSemaphore; //当缓冲区满时迫使生产者等待
HANDLE EmptySemaphore; //当缓冲区空时迫使消费者等待
DWORD WINAPI Producer(LPVOID); //生产者线程
DWORD WINAPI Consumer(LPVOID); //消费者线程

int main()
{
	//创建各个互斥信号
	//注意，互斥信号量和同步信号量的定义方法不同，互斥信号量调用的是 CreateMutex 函数，
	//同步信号量调用的是 CreateSemaphore 函数，函数的返回值都是句柄。
    Mutex = CreateMutex(NULL,FALSE,NULL);
    EmptySemaphore = CreateSemaphore(NULL,SIZE_OF_BUFFER,SIZE_OF_BUFFER,NULL);
	//将上句做如下修改，看看结果会怎样
	//EmptySemaphore = CreateSemaphore(NULL,0,SIZE_OF_BUFFER-1,NULL);
    FullSemaphore = CreateSemaphore(NULL,0,SIZE_OF_BUFFER,NULL);
	//调整下面的数值，可以发现，当生产者个数多于消费者个数时，
	//生产速度快，生产者经常等待消费者；反之，消费者经常等待
    const unsigned short PRODUCERS_COUNT = 3; //生产者的个数
    const unsigned short CONSUMERS_COUNT = 1; //消费者的个数
	//总的线程数
    const unsigned short THREADS_COUNT = PRODUCERS_COUNT+CONSUMERS_COUNT;
    HANDLE hThreads[THREADS_COUNT]; //各线程的 handle
    DWORD producerID[PRODUCERS_COUNT]; //生产者线程的标识符
    DWORD consumerID[CONSUMERS_COUNT]; //消费者线程的标识符
	//创建生产者线程
    for (int i=0; i<PRODUCERS_COUNT; ++i)
    {
        hThreads[i]=CreateThread(NULL,0,Producer,NULL,0,&producerID[i]);
        if (hThreads[i]==NULL) return -1;
    }
	//创建消费者线程
    for (i=0; i<CONSUMERS_COUNT; ++i)
    {
        hThreads[PRODUCERS_COUNT+i]=CreateThread(NULL,0,Consumer,NULL,0,&consumerID[i]);
        if (hThreads[i]==NULL) return -1;
    }
    while(p_ccontinue)
    {
        if(getchar())  //按回车后终止程序运行
        {
            p_ccontinue = false;
        }
    }

    return 0;
}


//生产一个产品。简单模拟了一下，仅输出新产品的 ID 号
void Produce()
{
    std::cout << std::endl<< "Producing " << ++ProductID << " ... ";
    std::cout << "Succeed" << std::endl;
}


//把新生产的产品放入缓冲区
void Append()
{
    std::cerr << "Appending a product ... ";
    buffer[in] = ProductID;
    in = (in+1)%SIZE_OF_BUFFER;
    std::cerr << "Succeed" << std::endl;
	//输出缓冲区当前的状态
    for (int i=0; i<SIZE_OF_BUFFER; ++i)
    {
        std::cout << i <<": " << buffer[i];
        if (i==in) std::cout << " <-- 生产";
        if (i==out) std::cout << " <-- 消费";
        std::cout << std::endl;
    }
}


//从缓冲区中取出一个产品
void Take()
{
    std::cerr << "Taking a product ... ";
    ConsumeID = buffer[out];
    buffer[out] = 0;
    out = (out+1)%SIZE_OF_BUFFER;
    std::cerr << "Succeed" << std::endl;
	//输出缓冲区当前的状态
    for (int i=0; i<SIZE_OF_BUFFER; ++i)
    {
        std::cout << i <<": " << buffer[i];
        if (i==in) std::cout << " <-- 生产";
        if (i==out) std::cout << " <-- 消费";
        std::cout << std::endl;
    }
}


//消耗一个产品
void Consume()
{
    std::cout << "Consuming " << ConsumeID << " ... ";
    std::cout << "Succeed" << std::endl;
}


//生产者
DWORD WINAPI Producer(LPVOID lpPara)
{
    while(p_ccontinue)
    {
        WaitForSingleObject(EmptySemaphore,INFINITE); //p(empty);
        WaitForSingleObject(Mutex,INFINITE); //p(mutex);
        Produce();
        Append();
        Sleep(1500);
        ReleaseMutex(Mutex); //V(mutex);
        ReleaseSemaphore(FullSemaphore,1,NULL); //V(full);
    }
    return 0;
}


//消费者
DWORD WINAPI Consumer(LPVOID lpPara)
{
    while(p_ccontinue)
    {
        WaitForSingleObject(FullSemaphore,INFINITE); //P(full);
        WaitForSingleObject(Mutex,INFINITE); //P(mutex);
        Take();
        Consume();
        Sleep(1500);
        ReleaseMutex(Mutex); //V(mutex);
        ReleaseSemaphore(EmptySemaphore,1,NULL); //V(empty);
    }
    return 0;
}
```
**实验截图：**
![](http://wx4.sinaimg.cn/mw690/0060lm7Tly1fsoo554qcoj30il0c2my3.jpg)

---

### 步骤3

---

### 步骤4
**修改清单 3-1 中的程序，调整生产者线程和消费者线程的个数，使得消费者数目大与生产者，看看结果有何不同。察看运行结果， 从中你可以得出什么结论？**
从结果来看，程序运行未出现明显不同，这是由于互斥和同步的结果。

---

### 步骤6
####1. CreateMutex():
*有几个参数，各代表什么含义？*

**功能：**
> 找出当前系统是否已经存在指定进程的实例。如果没有则创建一个互斥体。CreateMutex（）函数可用来创建一个有名或无名的互斥量对象。

**函数原型：**
```c
HANDLE CreateMutex( 　　
	LPSECURITY_ATTRIBUTES　lpMutexAttributes, // 指向安全属性的指针 　　
	BOOL　bInitialOwner, // 初始化互斥对象的所有者 　　
	LPCTSTR　lpName // 指向互斥对象名的指针 　　
);
```


**返回值：**
> Long，如执行成功，就返回互斥体对象的句柄；
> 0表示出错。会设置GetLastError。
> 即使返回的是一个有效句柄，但倘若指定的名字已经存在，`GetLastError`也会设为**ERROR_ALREADY_EXISTS**

 **参数及其说明：**
 >**lpMutexAttributes SECURITY_ATTRIBUTES**，指定一个SECURITY_ATTRIBUTES结构，或传递零值（将参数声明为ByVal As Long，并传递零值），表示使用不允许继承的默认描述符。


 >**bInitialOwner BOOL**，如创建进程希望立即拥有互斥体，则设为**TRUE**。一个互斥体同时只能由一个线程拥有。**FALSE**，表示刚刚创建的这个Mutex不属于任何线程。也就是没有任何线程拥有他，一个Mutex在没有任何线程拥有他的时候，他是处于**激发态**的， 所以处于**有信号状态**。


 > **lpName String**，指定互斥体对象的名字。用vbNullString创建一个未命名的互斥体对象。如已经存在拥有这个名字的一个事件，则打开现有的**已命名互斥体**。这个名字可能不与现有的事件、信号机、可等待计时器或文件映射相符,该名称可以有一个**"Global\"** 或**"Local\"**前缀，明确地建立在全局或会话命名空间的对象。剩余的名称可以包含任何字符，除反斜杠字符**（\）**。 

 **注意：
一旦不再需要，注意必须用CloseHandle函数将互斥体句柄关闭。从属于它的所有句柄都被关闭后，就会删除对象。进程中止前，一定要释放互斥体，如不慎未采取这个措施，就会将这个互斥体标记为废弃，并自动释放所有权。共享这个互斥体的其他应用程序也许仍然能够用它，但会接收到一个废弃状态信息，指出上一个所有进程未能正常关闭。这种状况是否会造成影响取决于涉及到的具体应用程序**

 ---

####2. CreateSemaphore()：
*有几个参数，各代表什么含义，信号量的初值在第几个参数中。*

**功能：**
 > 创建信号量

**原型：**

```c
HANDLE CreateSemaphore(
  LPSECURITY_ATTRIBUTES lpSemaphoreAttributes,
  LONG lInitialCount,
  LONG lMaximumCount,
  LPCTSTR lpName
);
```
**函数说明：**
>第一个参数表示安全控制，一般直接传入NULL。
>第二个参数表示初始资源数量。
>第三个参数表示最大并发数量。
>第四个参数表示信号量的名称，传入NULL表示匿名信号量。

---

####3. CreateThread():
**功能：**
> 当使用CreateProcess调用时，系统将创建一个进程和一个主线程。CreateThread将在主线程的基础上创建一个新线程。

**原型：**
```c
HANDLE CreateThread(
  LPSECURITY_ATTRIBUTES lpThreadAttributes, 
  DWORD dwStackSize,
  LPTHREAD_START_ROUTINE lpStartAddress, 
  LPVOID lpParameter,　　　　
  DWORD dwCreationFlags,　
  LPDWORD lpThreadId　
);

/*
- 第一个参数是指向SECURITY_ATTRIBUTES型态的结构的指针。在Windows 98中忽略该参数。在Windows NT中，它被设为NULL。

- 第二个参数是用于新线程的初始堆栈大小，默认值为0。在任何情况下，Windows根据需要动态延长堆栈的大小。

-第三个参数是指向线程函数的指标。函数名称没有限制，但是必须以下列形式声明：
DWORD WINAPI ThreadProc (PVOID pParam) ;

-第四个参数为传递给ThreadProc的参数。这样主线程和从属线程就可以共享数据。

- 第五个参数通常为0，但当建立的线程不马上执行时为旗标CREATE_SUSPENDED。线程将暂停直到呼叫ResumeThread来恢复线程的执行为止。

- 第六个参数是一个指标，指向接受执行线程ID值的变量。
*/
```
**注意：**
> 临界区要在线程执行前初始化，因为线程一但被建立即开始运行（除非手工挂起），但线程建立后在初始化临界区可能出现问题。
