// shiyan1_2.cpp : Defines the entry point for the console application.
//

#include "stdafx.h"
#include<windows.h>
#include<iostream>
#include<stdio.h>

// �������ݹ����Ľ��̵Ŀ�¡���̲�������IDֵ
void StartClone(int nCloneID)
{
	// ��ȡ���ڵ�ǰ��ִ���ļ����ļ���
	// szFilename:[D:\testProject\Debug\testProject.exe]
	// MAX_PATH:[MAX_PATH��C��������ʱ����ͨ��#defineָ����һ���곣�����������˱�������֧�ֵ��ȫ·�����ĳ���]
	// Windows��MAX_PATH:[MAX_PATH�Ľ��ͣ� �ļ����256��ANSI���������̷���X:\��3�ֽڣ�259�ֽڣ��ټ��Ͻ�����1�ֽڣ���260]
	TCHAR szFilename[MAX_PATH];
	GetModuleFileName(NULL,szFilename,MAX_PATH);

	// ��ʽ�������ӽ��̵������в�֪ͨ��EXE�ļ����Ϳ�¡ID
	// szCmdLine:["D:\testProject\Debug\testProject.exe"5]
	TCHAR szCmdLine[MAX_PATH];
	sprintf(szCmdLine,"\"%s\"%d",szFilename,nCloneID);


	// �����ӽ��̵�STARTUPINFO�ṹ
	STARTUPINFO si;
	ZeroMemory(&si,sizeof(si));
	si.cb=sizeof(si); // �����Ǳ��ṹ�Ĵ�С

	// ���ص������ӽ��̵Ľ�����Ϣ
	PROCESS_INFORMATION pi;

	// ����ͬ���Ŀ�ִ���ļ��������д������̣����������ӽ��̵�����
	BOOL bCreateOK=::CreateProcess(
		szFilename,  // �������EXE�ļ���Ӧ�ó��������
		szCmdLine,   // ��������Ϊ��һ���ӽ��̵ı�־
		NULL,        // ȱʡ�Ľ��̰�ȫ��
		NULL,        // ȱʡ���̰߳�ȫ��
		FALSE,       // ���̳о��
		CREATE_NEW_CONSOLE, // ʹ���µĿ���̨
		NULL,        // �µĻ���
		NULL,        // ��ǰĿ¼
		&si,         // ������Ϣ
		&pi);        // ���صĽ�����Ϣ

	// ���ӽ����ͷ�����
	if(bCreateOK)
	{
		CloseHandle(pi.hProcess);
		CloseHandle(pi.hThread);
	}
}

int main(int argc, char* argv[])
{
	// ȷ���������������̣������������ڽ����б��е�λ��
	int nClone=0;
	// �޸����: int nClone;
	// ��һ���޸ģ� nClone=0;
	if(argc>1)
	{
		// �ӵڶ�����������ȡ��¡ ID
		// ֮���԰���ע���޸Ĵ���ͻ���ѭ����ԭ�����ڸ������ڴ����ӽ���ʱ���nClone���������в��������ӽ��̣�nClone=0��λ�þ��Ե���Ϊ��Ҫ!!���ο�line 20ע�ͣ������к󸽴�����[cClone]��
		::sscanf(argv[1],"%d",&nClone);
		printf("�ӽ��̶�ȡ�������в���:%d\n",nClone);
	}
	// �ڶ����޸ģ� nClone=0;
	//nClone=0;
	// ��ʾ����λ��
	std::cout<<"Process ID:"<<::GetCurrentProcessId()
		<<",Clone��ID:"<<nClone
		<<std::endl;

	// ����Ƿ��д����ӽ��̵���Ҫ
	const int c_nCloneMax=5;
	if(nClone<c_nCloneMax)
	{
		// �����½��̵������кͿ�¡��
		StartClone(++nClone);
	}
	// �ȴ���Ӧ���������������
	getchar();
	return 0;
}
