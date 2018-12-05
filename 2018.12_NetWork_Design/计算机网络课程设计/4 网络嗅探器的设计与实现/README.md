# 课程设计题目

## 网络嗅探器的设计与实现
参照附录4 raw socket编程例子，设计一个可以监视网络的状态，数据流动情况以及网络上传输的信息的网络嗅探器。

## 课程设计内容
C语言getop()函数:分析命令行参数

> 头文件 #include <unistd.h>
>
> 定义函数：int getopt(int argc, char * const argv[], const char * optstring);
>
> 函数说明：getopt()用来分析命令行参数。
> 1、参数argc 和argv 是由main()传递的参数个数和内容。
> 2、参数optstring 则代表欲处理的选项字符串。
>
> 此函数会返回在argv 中下一个的选项字母，此字母会对应参数optstring 中的字母。
>
> 如果选项字符串里的字母后接着冒号":"，则表示还有相关的参数，全域变量optarg 即会指向此额外参数。
> 如果getopt()找不到符合的参数则会印出错信息，并将全域变量optopt 设为"?"字符, 如果不希望getopt()印出错信息，则只要将全域变量opterr 设为0 即可。
>
> 返回值：如果找到符合的参数则返回此参数字母, 如果参数不包含在参数optstring 的选项字母则返回"?"字符,分析结束则返回-1.
>
> 范例
> \#include <stdio.h>
> \#include <unistd.h>
> int main(int argc, char **argv)
> {
>    int ch;
>    opterr = 0;
>    while((ch = getopt(argc, argv, "a:bcde")) != -1)
>    switch(ch)
>    {
> ​      case 'a':
> ​         printf("option a:'%s'\n", optarg);  break;
> ​      case 'b':
> ​         printf("option b :b\n");  break;
> ​      default:
> ​         printf("other option :%c\n", ch);
>    }
>    printf("optopt +%c\n", optopt);
> }
>
> 执行：
> $. /getopt -b
> option b:b
> $. /getopt -c
> other option:c
> $. /getopt -a
> other option :?
> $. /getopt -a12345
> option a:'12345'

## 课程设计步骤

## 调试过程

## 课程设计结果及结果分析 心得体会
#### 需要注意的地方:
> 原始套接字**SOCKET_RAW**的获取必须获得**root**权限，否则返回-1

## 程序源文件

## 可执行文件
