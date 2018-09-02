#coding:utf8
from django import template
register = template.Library()

def for_json(value):
    '''过滤对json不友好的字符'''
    value = value.replace("\n", "");
    value = value.replace("\r", "");
    value = value.replace("\t", "");
    return value

register.filter('for_json', for_json)
