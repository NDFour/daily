/*
 *    Description: ---
 *         Author: Lynn
 *          Email: lgang219@gmail.com
 *         Create: 2018-06-26 13:40:09
 *  Last Modified: 2018-06-29 14:37:36
 */

/* char* getcwn(char *buf, size_t size);
 *
 * 头文件：include <unistd.h>
 * 函数说明：getcwd()会将当前的工作目录绝对路径复制到参数buf所指的内存空间，参数size为buf的空间大小
 */

#include <stdio.h>
#include <stdlib.h>
#include <unistd.h> // io: read | write
#include <string.h>

#define MAX_CMD 256
#define MAX_DIR_NAME 256

void shell_eval(char *);
int shell_parseline(char *,char **);
int shell_buildin_command(char *);

//int main(int argc,char *argv[]){
 int main(void){

    char cmdstring[MAX_CMD];
    int n;
    while(1){
        // 修改提示符颜色
        printf("\033[37;43m *myshell*>\033[0m");
        // 清空缓冲流，使stdout清空，就会立刻输出所有在缓冲区的内容
        fflush(stdout);

        /* read */
        // ssize_t read(int fd, void * buf, size_t count)
        if((n=read(0,cmdstring,MAX_CMD))<0){
            printf("read error");
        }

        eval(cmdstring);
    }
    return 0;
}


void eval(char *cmdstring){
    // command
    char *argv[MAX_CMD];
    // 暂存command
    char buf[MAX_CMD];

    strcpy(buf,cmdstring);
    // 解析cmdstring中的command和params
    parseline(buf,argv);
    // printf("arter parseline():%s\n",argv[0]);
    if(argv[0]==NULL){
        return;
    }
    // 判断是否为mySHELL内置command
    if(buildin_command(argv)) 
        return;

    // 不是内置命令的话直接fork创建子进程利用execvp函数执行command
    int pid = fork();
    if(pid == 0){
        if(execvp(argv[0],argv)<0){
            printf("%s:command not found.\n",argv[0]);
            exit(0);
        }
    }
    // 等待子进程执行结束
    // wait(pid);
    wait(NULL);
}


// 判断是否为内置命令
int buildin_command(char **argv){   
    if(strcmp(argv[0],"exit")==0){
        exit(0);
    }
    if(strcmp(argv[0],"quit")==0){
        exit(0);
    }
    if(strcmp(argv[0],"bye")==0){
        exit(0);
    }

    if(strcmp(argv[0],"cd")==0){
        // 返回-1，代表执行失败，否则返回0
        if(chdir(argv[1])){
            printf("mySHELL:cd:%s:no such directory\n",argv[1]);
        }
        return 1;
    }
    if(strcmp(argv[0],"pwd")==0){
        char buf[MAX_DIR_NAME];
        printf("%s\n",getcwd(buf,sizeof(buf)));
        return 1;
    }
    if(strcmp(argv[0],"help")==0){
        printf("\n        mySHELL\n\n");
        printf("    - environ 列出所有环境变量字符串的设置\n");
        printf("    - echo <内容> 显示 echo 后的内容且换行\n");
        printf("    - help 简短概要的输出你的 shell 的使用方法和基本功能\n");
        printf("    - jobs 输出 shell 当前的一系列子进程\n");
        printf("    - quit,exit,bye 退出 shell\n\n");
    }
    if(strcmp(argv[0],"environ")==0){
        argv[0][3]='\0';
        argv[0][4]='\0';
        argv[0][5]='\0';
    }
    return 0;//not a buildin_command
}


int parseline(char *buf,char**argv){ 
    while(*buf==' '){
        buf++;
    }
    int delim = 0;

    int argc = 0;
    while(*buf!='\n'){

        while(buf[delim]!='\n'&&buf[delim]!=' '){
            delim++;
        }

        if(buf[delim] == '\n'){
            buf[delim] = '\0';
            argv[argc++] = buf;
            break;
        }
        buf[delim] = '\0';
        argv[argc++] = buf; 

        buf+=delim+1;
        /*指示器indicator=0*/
        delim = 0;
        while(*buf==' '){
            buf++;
        }
    }
    /*the last element is NULL*/
    argv[argc] = NULL;
    return 0;
}
