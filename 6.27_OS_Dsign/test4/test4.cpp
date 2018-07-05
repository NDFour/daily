// test4.cpp

#include <iostream>
#include <stdlib.h>

using namespace std;

const int nRow = 500;
const int nColumn = 500;

int Max[nRow][nColumn];//资源最大需求矩阵
int Allocation[nRow][nColumn];//已分配资源矩阵
int Need[nRow][nColumn];//需要资源矩阵
int BeginSource[nColumn];//最开始各种资源的数量
int Available[nColumn];//当前可用各类资源数量
int Requset[nColumn];//提出资源请求个数
int safeOrder[nRow];//安全序列
int nSource;//资源种类数
int nPortNum;//进程数量
int iTime = 0;//系统时刻

// 输出 [Allocation] 和 [Need]
void show()
{
	/*显示用户已经输入的数据*/
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

//初始化函数：输入资源种类、进程数量、需求量等
void Init()
{
    cout<< "        银行家算法 实现\n"<<endl;

	cout << "[nSource] 资源种类数" << endl;
	cin >> nSource;
	cout << "[nPortNum] 进程数量" << endl;
	cin >> nPortNum;

	// 最大需求矩阵 Max
	cout << "[MAX] 各资源最大需求数量" << nPortNum<<"*"<<nSource<<"的矩阵"<<endl;
	for (int i = 0; i < nPortNum;i++)
	{
		for (int j = 0; j < nSource;j++)
		{
			cin >> Max[i][j];
		}
	}
	// 已分配资源矩阵 Allcation
	cout << "[ALLOCATION] 已分配各个资源数量" << nPortNum << "*" << nSource << "的矩阵" << endl;
start:
	for (int i = 0; i < nPortNum; i++)
	{
		for (int j = 0; j < nSource; j++)
		{
			cin >> Allocation[i][j];
			if (Allocation[i][j]>Max[i][j])
			{
				cout << "已分配资源数量大于最大需求量，请重新分配" << endl;
				goto start;
			}
		}
	}


	// 计算 [Need] 矩阵
	for (int  i = 0; i < nPortNum; i++)
	{
		for (int j = 0; j < nSource; j++)
		{
			Need[i][j] = Max[i][j] - Allocation[i][j];
		}
	}

	// 计算当前已经分配出去的资源数量 [Available]，真正的Available的值会在后面赋值
	for (int  i = 0; i < nPortNum; i++)
	{
		for (int j = 0; j < nSource; j++)
		{
			Available[j] += Allocation[i][j];
		}
	}

    // 输入开始时刻各种资源数量
	cout << "请输入系统各种资源初始化数量" << nSource << "列" << endl;
begin:
	for (int  i = 0; i < nSource; i++)
	{
		cin >> BeginSource[i];
		if (BeginSource[i] < Available[i])
		{
			cout << "第"<<i<<"个资源初始化资源数量数量太少，请重新输入" << endl;
			goto begin;
		}
	}

    // 剩余可用的资源数量 [Available]
	for (int i = 0; i < nSource; i++)
	{
		Available[i] = BeginSource[i] - Available[i];
	}
}

//安全性算法，计算此刻状态是否安全
bool Safe()
{

	int Work[nColumn];
	bool Finish[nColumn];
	//将work工作向量初始化
	for (int i = 0; i < nSource;i++)
	{
		Work[i] = Available[i];
	}
	//初始化finish全为false
	for (int i = 0; i < nPortNum; i++)
	{
		Finish[i] = false;
	}

	int nCount = 0;
	int k = nPortNum;
	while (k--)//看工作向量是否操作了nSource次
	{
		for (int i = 0; i < nPortNum; i++)
		{
			int iCount = 0;//计数
			int iNum = 0;
			for (int j = 0; j < nSource; j++)
			{
				//所有资源Need都大于工作向量，则不安全
				if (Need[i][j] <= Work[j])
				{
					iNum++;
				}
			}
			if (iNum == nSource)//该进程满足
			{
				if (Finish[i] == true)
				{
					continue;
				}
				for (int j = 0; j < nSource; j++)
				{
					Work[j] += Allocation[i][j];
				}
				// 安全序列
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

//银行家算法
void BankSort()
{
	int n;
	show();
	a:
	cout << "哪个进程请求申请资源" << endl;
	cin >> n;
	if (n >= nPortNum)
	{
		cout << "没有这个进程号";
		goto a;
	}
	cout << "此进程每类资源的请求个数" << endl;

	for (int i = 0; i < nSource; i++)
	{
	    // 请求的资源数大于 Need 资源或大于可用资源 Available 时跳转到此重新输入
		mis:
		cin >> Requset[i];
		if (Requset[i] > Need[n][i ])
		{
			cout << "出错，申请资源大于需要资源,请重新输入！"<<endl;
			goto mis;
		}
		if (Requset[i] > Available[i])
		{
			//进程pi阻塞，返回
			cout << "出错，申请资源大于现有资源,请重新输入！" << endl;
			goto mis;
		}
	}

	// 成功分配资源后调整各个数组
	for (int i = 0; i < nSource; i++)
	{
		Available[i] -= Requset[i];
		Allocation[n][i] += Requset[i];
		Need[n][i] -= Requset[i];
	}

	//调用安全性算法,计算此刻系统状态是否安全
	if (Safe())
	{
		char c;
		// 输出安全序列
		cout << "T"<<iTime<<"时刻系统安全安全序列为" <<"  ";
		for (int i = 0; i < nPortNum;i++)
		{
			if (i == nPortNum-1)
			{
				cout << safeOrder[i] << " ";
				break;
			}
			cout <<safeOrder[i]<<"-->";//安全序列
		}
		cout << "\n输入任意字符继续" << endl;
		cin >> c;
		if (c >= 0||c <= 127)
		{
			iTime++;
			BankSort();
		}

	}
	else
	{
		//此时资源分配状态不安全，恢复数据到未分配状态
		for (int i = 0; i < nSource; i++)
		{
			Available[i] += Requset[i];
			Allocation[n][i] -= Requset[i];
			Need[n][i] += Requset[i];
		}
		char c;
		cout << "T" << iTime << "时刻系统不安全不能分配任意键继续" << endl;
		cin >> c;
		if (c >= 0 || c <= 127)
		{
			BankSort();
		}
	}

}

// 主函数
int main()
{
	// 当一进程提出资源申请时，银行家算法执行下列步骤以决定是否向其分配资源：
    // 1）检查该进程所需要的资源是否已超过它所宣布的最大值。
    // 2）检查系统当前是否有足够资源满足该进程的请求。
    // 3）系统试探着将资源分配给该进程，得到一个新状态。
    // 4）执行安全性算法，若该新状态是安全的，则分配完成；若新状态是不安全的，则恢复原状态，阻塞该进程。
	Init();
	BankSort();
	system("pause");
	return 0;
}
