#include <string.h>  
#include "String.h"  
#include <stdio.h>  
//默认构造函数,用于创建空字符串  
String::String()  
{  
    cout<<"---String constructor---"<<endl;  
    len = 0;  
    str = new char[1];  
    str[0] = '\0';  
}  
//析构函数  
String::~String()  
{  
      //cout<<"---String destructor---"<<endl;  
    delete []str;  
    len=0;  
}  
//构造函数,带一个参数用来初始化字符串  
String::String(const char*const cstr)  
{  
    /*len = strlen(cstr);  
    str = new char[len+1];  
    for (unsigned int i =0; i < len; i++) {  
      str[i] = cstr[i];  
    }  
    str[len]='\0';*/  
    cout<<"---String constructor:char*---"<<endl;  
    if (cstr == NULL) {  
        len = 0;  
    str = new char[1];  
    memset(str, 0, len+1);  
    if (str == NULL) return;  
  }  
  else {  
     len = strlen(cstr);  
     str = new char[len + 1];  
     memset(str, 0, len+1);  
     if (str == NULL) return;  
     strncpy(str, cstr, len);  
   }  
}  
//复制构造函数,默认是浅层复制,需重载  
String::String(const String &rs)  
{  
    cout<<"---String copy constructor---"<<endl;  
    len = rs.getlen();  
  str = new char[len + 1];  
  for(unsigned int i = 0 ;i < len; i++) {  
    str[i] = rs.str[i];  
  }  
  str[len] = '\0';  
  /*len = rs.getlen();  
  str = new char[len+1];  
  if (str == NULL) return;  
  strcpy(str, rs.str);*/  
}  
//重载下标运算符[]  
char&String::operator[](unsigned int length)  
{  
  if(length>len) return str[len-1];  
  else return str[length];  
}  
//重载下标运算符[](const版本)  
char String::operator[](unsigned int length)const  
{  
    //cout<<"String::operator[] const"<<endl;  
  if(length>len) return str[len-1];  
  else return str[length];  
}  
//重载复制运算符=，用于两个字符串之间的赋值  
String &String::operator=(const String &rs)  
{  
    cout<<"String::operator="<<endl;  
    if (this == &rs) return *this;  
  delete []str;  
  len = rs.getlen();  
  str = new char[len + 1];  
  for(int i = 0; i < len; i++) {  
    str[i] = rs[i];     //重载下标运算符[]才可使用  
    //str[i] = rs.str[i];  
  }  
  str[len] = '\0';  
  return *this;  
}  
//重载加法运算符+  
String String::operator+(const String &rs)  
{  
    /*char *st= new char[len + rs.getlen() + 1];  
  memset(st, 0, len + rs.getlen() + 1);  
  strcat(st, str);  
  strcat(st, rs.str);  
  return String(st);*/  
  cout<<"String::operator+"<<endl;   
  unsigned int total = len + rs.getlen();  
  char *tmpstr = new char[total + 1];  
  unsigned int i, j;  
  for (i = 0; i < len; i++) {  
    tmpstr[i] = str[i];  
  }  
  for( j = 0; j < rs.getlen(); j++, i++) {  
    tmpstr[i] = rs[j];  
  }  
  tmpstr[total] ='\0';  
  String st(tmpstr);  
  delete tmpstr;  
  tmpstr = NULL;  
  return st;   
}  
//重载组合运算符+=  
String String::operator+=(const String &rs)  
{  
  cout<<"String::operator+="<<endl;   
    int total = len + rs.getlen();  
  //delete []str;  
  char *tmpstr = new char[total + 1];     
  unsigned int i,j;  
  for(i = 0; i < len; i++) {  
    tmpstr[i] = str[i];  
  }  
  for(j = 0; j < rs.getlen(); j++,i++) {  
    tmpstr[i] = rs[j];  
  }  
  tmpstr[total]='\0';  
  delete []str;  
  str = new char[total + 1];  
  strncpy(str, tmpstr, total + 1);  
  return *this;  
  /*  
  char *temp = str;    
  len = len + rs.getlen();   
  str = new char[len + 1];    
  strcpy(str, temp);    
  strcat(_str, rs.getstr());    
  delete[] temp;    
  return *this;*/  
}  
//重载输出流运算符<<  
ostream &operator<<(ostream &output, const String &str)  
{  
    output<<str.str;  
  return output;  
}  
//重载输入流运算符>>  
istream &operator>>(istream &input, String &str)  
{  
    input>>str.str;  
  return input;  
}  
//重载小于运算符<  
bool operator<(const String&str1,const String &str2)  
{  
    if(strcmp(str1.str, str2.str) < 0) return 1;  
  else return 0;  
}  
//重载大于运算符>  
bool operator>(const String&str1,const String &str2)  
{  
    if(strcmp(str1.str, str2.str) > 0) return 1;  
  else return 0;  
}  
//重载等于运算符==  
bool operator==(const String&str1,const String &str2)  
{  
    if(strcmp(str1.str, str2.str) == 0) return 1;  
  else return 0;  
}  
//获取字符串长度  
unsigned int String::getlen()const  
{  
    return len;  
}  
//获取字符串  
const char*String::getstr()const  
{  
    return str;
}
