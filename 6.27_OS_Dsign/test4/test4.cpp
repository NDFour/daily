// test4.cpp

#include <iostream>
#include <stdlib.h>

using namespace std;

const int nRow = 500;
const int nColumn = 500;

int Max[nRow][nColumn];//��Դ����������
int Allocation[nRow][nColumn];//�ѷ�����Դ����
int Need[nRow][nColumn];//��Ҫ��Դ����
int BeginSource[nColumn];//�ʼ������Դ������
int Available[nColumn];//��ǰ���ø�����Դ����
int Requset[nColumn];//�����Դ�������
int safeOrder[nRow];//��ȫ����
int nSource;//��Դ������
int nPortNum;//��������
int iTime = 0;//ϵͳʱ��

// ��� [Allocation] �� [Need]
void show()
{
	/*��ʾ�û��Ѿ����������*/
	cout << "------------Allocation-----------------" << endl;
	for (int i = 0; i < nPortNum; i++)
	{
		cout << "port" << i << "\t";
		for (int j = 0; j < nSource; j++)
		{
			cout << Allocation[i][j] << "\t";
		}
		cout << endl;
	}
	cout << "------------Need-----------------------" << endl;
	for (int i=0; i < nPortNum; i++)
	{
		cout << "port" << i << "\t";
		for (int j = 0; j < nSource; j++)
		{
			cout << Need[i][j] << "\t";
		}
		cout << endl;
	}
	cout << endl;
	cout << "---------------------------------------" << endl;
}

//��ʼ��������������Դ���ࡢ������������������
void Init()
{
    cout<< "        ���м��㷨 ʵ��\n"<<endl;

	cout << "[nSource] ��Դ������" << endl;
	cin >> nSource;
	cout << "[nPortNum] ��������" << endl;
	cin >> nPortNum;

	// ���������� Max
	cout << "[MAX] ����Դ�����������" << nPortNum<<"*"<<nSource<<"�ľ���"<<endl;
	for (int i = 0; i < nPortNum;i++)
	{
		for (int j = 0; j < nSource;j++)
		{
			cin >> Max[i][j];
		}
	}
	// �ѷ�����Դ���� Allcation
	cout << "[ALLOCATION] �ѷ��������Դ����" << nPortNum << "*" << nSource << "�ľ���" << endl;
start:
	for (int i = 0; i < nPortNum; i++)
	{
		for (int j = 0; j < nSource; j++)
		{
			cin >> Allocation[i][j];
			if (Allocation[i][j]>Max[i][j])
			{
				cout << "�ѷ�����Դ������������������������·���" << endl;
				goto start;
			}
		}
	}


	// ���� [Need] ����
	for (int  i = 0; i < nPortNum; i++)
	{
		for (int j = 0; j < nSource; j++)
		{
			Need[i][j] = Max[i][j] - Allocation[i][j];
		}
	}

	// ���㵱ǰ�Ѿ������ȥ����Դ���� [Available]��������Available��ֵ���ں��渳ֵ
	for (int  i = 0; i < nPortNum; i++)
	{
		for (int j = 0; j < nSource; j++)
		{
			Available[j] += Allocation[i][j];
		}
	}

    // ���뿪ʼʱ�̸�����Դ����
	cout << "������ϵͳ������Դ��ʼ������" << nSource << "��" << endl;
begin:
	for (int  i = 0; i < nSource; i++)
	{
		cin >> BeginSource[i];
		if (BeginSource[i] < Available[i])
		{
			cout << "��"<<i<<"����Դ��ʼ����Դ��������̫�٣�����������" << endl;
			goto begin;
		}
	}

    // ʣ����õ���Դ���� [Available]
	for (int i = 0; i < nSource; i++)
	{
		Available[i] = BeginSource[i] - Available[i];
	}
}

//��ȫ���㷨������˿�״̬�Ƿ�ȫ
bool Safe()
{

	int Work[nColumn];
	bool Finish[nColumn];
	//��work����������ʼ��
	for (int i = 0; i < nSource;i++)
	{
		Work[i] = Available[i];
	}
	//��ʼ��finishȫΪfalse
	for (int i = 0; i < nPortNum; i++)
	{
		Finish[i] = false;
	}

	int nCount = 0;
	int k = nPortNum;
	while (k--)//�����������Ƿ������nSource��
	{
		for (int i = 0; i < nPortNum; i++)
		{
			int iCount = 0;//����
			int iNum = 0;
			for (int j = 0; j < nSource; j++)
			{
				//������ԴNeed�����ڹ����������򲻰�ȫ
				if (Need[i][j] <= Work[j])
				{
					iNum++;
				}
			}
			if (iNum == nSource)//�ý�������
			{
				if (Finish[i] == true)
				{
					continue;
				}
				for (int j = 0; j < nSource; j++)
				{
					Work[j] += Allocation[i][j];
				}
				// ��ȫ����
				safeOrder[nCount] = i;
				Finish[i] = true;
				if (nPortNum == ++nCount)
				{
					return true;
				}
			}
		}

	}
	return false;
}

//���м��㷨
void BankSort()
{
	int n;
	show();
	a:
	cout << "�ĸ���������������Դ" << endl;
	cin >> n;
	if (n >= nPortNum)
	{
		cout << "û��������̺�";
		goto a;
	}
	cout << "�˽���ÿ����Դ���������" << endl;

	for (int i = 0; i < nSource; i++)
	{
	    // �������Դ������ Need ��Դ����ڿ�����Դ Available ʱ��ת������������
		mis:
		cin >> Requset[i];
		if (Requset[i] > Need[n][i ])
		{
			cout << "����������Դ������Ҫ��Դ,���������룡"<<endl;
			goto mis;
		}
		if (Requset[i] > Available[i])
		{
			//����pi����������
			cout << "����������Դ����������Դ,���������룡" << endl;
			goto mis;
		}
	}

	// �ɹ�������Դ�������������
	for (int i = 0; i < nSource; i++)
	{
		Available[i] -= Requset[i];
		Allocation[n][i] += Requset[i];
		Need[n][i] -= Requset[i];
	}

	//���ð�ȫ���㷨,����˿�ϵͳ״̬�Ƿ�ȫ
	if (Safe())
	{
		char c;
		// �����ȫ����
		cout << "T"<<iTime<<"ʱ��ϵͳ��ȫ��ȫ����Ϊ" <<"  ";
		for (int i = 0; i < nPortNum;i++)
		{
			if (i == nPortNum-1)
			{
				cout << safeOrder[i] << " ";
				break;
			}
			cout <<safeOrder[i]<<"-->";//��ȫ����
		}
		cout << "\n���������ַ�����" << endl;
		cin >> c;
		if (c >= 0||c <= 127)
		{
			iTime++;
			BankSort();
		}

	}
	else
	{
		//��ʱ��Դ����״̬����ȫ���ָ����ݵ�δ����״̬
		for (int i = 0; i < nSource; i++)
		{
			Available[i] += Requset[i];
			Allocation[n][i] -= Requset[i];
			Need[n][i] += Requset[i];
		}
		char c;
		cout << "T" << iTime << "ʱ��ϵͳ����ȫ���ܷ������������" << endl;
		cin >> c;
		if (c >= 0 || c <= 127)
		{
			BankSort();
		}
	}

}

// ������
int main()
{
	// ��һ���������Դ����ʱ�����м��㷨ִ�����в����Ծ����Ƿ����������Դ��
    // 1�����ý�������Ҫ����Դ�Ƿ��ѳ����������������ֵ��
    // 2�����ϵͳ��ǰ�Ƿ����㹻��Դ����ý��̵�����
    // 3��ϵͳ��̽�Ž���Դ������ý��̣��õ�һ����״̬��
    // 4��ִ�а�ȫ���㷨��������״̬�ǰ�ȫ�ģ��������ɣ�����״̬�ǲ���ȫ�ģ���ָ�ԭ״̬�������ý��̡�
	Init();
	BankSort();
	system("pause");
	return 0;
}
