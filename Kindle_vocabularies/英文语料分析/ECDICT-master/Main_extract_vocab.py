import sqlite3
import time
import os
# stardict.py
import stardict

import nltk
from nltk.corpus import stopwords

# write_2_excel.py
import write_2_excel

# generate wordcloud
# gen_word_cloud.py
import gen_word_cloud



'''
输出单词内容到文件
'''
class Words_2_File(object):
    file_name = 'output/'
    word_list = []

    def __init__(self, file_name, word_list):
        self.file_name += file_name
        self.word_list = word_list


    '''
    w: 单词的翻译结果
    '''
    def export_2_txt(self):
        with open(self.file_name, 'a') as f:
            i_cnt = 0
            for w in self.word_list:
                i_cnt += 1

                # 开始写入
                f.write('-------------------------------------- ' + str(i_cnt) + '\n')
                f.write(w['word'])

                if w['phonetic']:
                    f.write('  [' + w['phonetic'] + ']')
                f.write('\n')

                if w['collins']:
                    f.write('collins Rank: ' + str(w['collins']) )
                    f.write('   ')
                    if w['oxford']:
                        f.write('oxford 3000: ' + str(w['oxford']) )
                        f.write('\n')
                    else:
                        f.write('\n')

                if int(w['bnc']):
                    f.write('BNC Rank: ' + str(w['bnc']) + '  ' )
                    f.write('\n')
                if int(w['frq']):
                    f.write('FRQ Rank: ' + str(w['frq']) )
                    f.write('\n')

                if w['tag']:
                    f.write('标签: ' + w['tag'])
                    f.write('\n')

                f.write('\n')

                f.write(w['translation'])
                f.write('\n')

                if w['exchange']:
                    f.write('\n')
                    f.write('变形: ' + w['exchange'])
                    f.write('\n')


'''
读取 Txt 英文语料的文本
'''
def load_txt_data(file_name):
    text = ''
    with open('sources/' + file_name, 'r') as f:
        text = f.read()

    return text


'''
获得字符串的分词列表
'''
def get_words(text):
    stopWords = set(stopwords.words('english'))

    # sent_tokenize 文本分句处理，text是一个英文句子或文章
    value = nltk.sent_tokenize(text)

    word_list = []
    # 先分句，再逐个句子分词
    # word_tokenize 分词处理,分词不支持中文
    '''
    for i in value:
        words = nltk.word_tokenize(text=i)

        for w in words:
            word_list.append(w)
    '''

    # 直接对整篇文章 分词
    words = nltk.word_tokenize(text=text)
    for w in words:
        if w not in stopWords:
            word_list.append(w)
            
    return len(value), len(word_list), word_list



'''
获得 单词 word 的翻译结果
'''
def get_tran(sd, word):
    # print('翻译 ' + w)

    rel = sd.query(word)

    return rel




if __name__ == '__main__':
    input_name = input('需要导入的 txt 文件名（带后缀名）：')

    output_name = input('请输入要保存的文件名（不带后缀名）：')
    # output_name = output_name + '/' + output_name
    print('output_name: ' + output_name)

    # 调用 ECDICT
    sd = stardict.StarDict('full_dic.db', False)
    # 查询词干 用 
    # lemma = stardict.LemmaDB()
    # lemma.load('lemma.en.txt')

    # text = load_txt_data('animal_farm.txt')
    text = load_txt_data(input_name)
    len_sentence, len_words, word_list = get_words(text)

    print('len_sentence')
    print(len_sentence)
    print('len_words')
    print(len_words)

    # 开始翻译
    err_list = []
    succ_list = []
    # 避免重复翻译同一个词
    tmp_list = []
    repeat_cnt = 0
    for w in word_list:
        # 避免重复翻译同一个词
        if w in tmp_list:
            repeat_cnt += 1
            continue

        rel = get_tran(sd, w)
        if not rel:
            err_list.append(w)
        else:
            succ_list.append(rel)

        tmp_list.append(w)
    print('repeat_cnt: ' + str(repeat_cnt) )

    # 开始写入 Txt 文件
    word_2_file = Words_2_File( output_name + '.txt', succ_list)
    word_2_file.export_2_txt()

    # 开始写入 excel 文件
    w_2_excel = write_2_excel.Write_2_Excel(output_name + '.xls', succ_list)
    w_2_excel.write_excel()

    # 生成词云
    g_word_cloud = gen_word_cloud.Gen_Word_Cloud(input_name)
    g_word_cloud.gen_pic()

    # 输出 最终结果
    print('\n\n#########################')
    print('len err_list:' + str(len(err_list)) )
    for err in err_list:
        # print(err)
        with open('output/' + output_name + 'err_list.txt', 'a') as f:
            f.write(err)
            f.write('\n')


