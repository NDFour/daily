// shiyan1_2.cpp : Defines the entry point for the console application.
//

#include "stdafx.h"
#include<windows.h>
#include<iostream>
#include<stdio.h>

// 创建传递过来的进程的克隆过程并赋予其ID值
void StartClone(int nCloneID)
{
	// 提取用于当前可执行文件的文件名
	// szFilename:[D:\testProject\Debug\testProject.exe]
	// MAX_PATH:[MAX_PATH是C语言运行时库中通过#define指令定义的一个宏常量，它定义了编译器所支持的最长全路径名的长度]
	// Windows的MAX_PATH:[MAX_PATH的解释： 文件名最长256（ANSI），加上盘符（X:\）3字节，259字节，再加上结束符1字节，共260]
	TCHAR szFilename[MAX_PATH];
	GetModuleFileName(NULL,szFilename,MAX_PATH);

	// 格式化用于子进程的命令行并通知其EXE文件名和克隆ID
	// szCmdLine:["D:\testProject\Debug\testProject.exe"5]
	TCHAR szCmdLine[MAX_PATH];
	sprintf(szCmdLine,"\"%s\"%d",szFilename,nCloneID);


	// 用于子进程的STARTUPINFO结构
	STARTUPINFO si;
	ZeroMemory(&si,sizeof(si));
	si.cb=sizeof(si); // 必须是本结构的大小

	// 返回的用于子进程的进程信息
	PROCESS_INFORMATION pi;

	// 利用同样的可执行文件和命令行创建进程，并赋予其子进程的性质
	BOOL bCreateOK=::CreateProcess(
		szFilename,  // 产生这个EXE文件的应用程序的名称
		szCmdLine,   // 告诉其行为像一个子进程的标志
		NULL,        // 缺省的进程安全性
		NULL,        // 缺省的线程安全性
		FALSE,       // 不继承句柄
		CREATE_NEW_CONSOLE, // 使用新的控制台
		NULL,        // 新的环境
		NULL,        // 当前目录
		&si,         // 启动信息
		&pi);        // 返回的进程信息

	// 对子进程释放引用
	if(bCreateOK)
	{
		CloseHandle(pi.hProcess);
		CloseHandle(pi.hThread);
	}
}

int main(int argc, char* argv[])
{
	// 确定派生出几个进程，及派生进程在进程列表中的位置
	int nClone=0;
	// 修改语句: int nClone;
	// 第一次修改： nClone=0;
	if(argc>1)
	{
		// 从第二个参数中提取克隆 ID
		// 之所以按照注释修改代码就会死循环，原因在于父进程在创建子进程时会把nClone当作命令行参数传入子进程，nClone=0的位置就显得尤为重要!!（参考line 20注释，命令行后附带参数[cClone]）
		::sscanf(argv[1],"%d",&nClone);
		printf("子进程读取到命令行参数:%d\n",nClone);
	}
	// 第二次修改： nClone=0;
	//nClone=0;
	// 显示进程位置
	std::cout<<"Process ID:"<<::GetCurrentProcessId()
		<<",Clone　ID:"<<nClone
		<<std::endl;

	// 检查是否有创建子进程的需要
	const int c_nCloneMax=5;
	if(nClone<c_nCloneMax)
	{
		// 发送新进程的命令行和克隆号
		StartClone(++nClone);
	}
	// 等待响应键盘输入结束进程
	getchar();
	return 0;
}
