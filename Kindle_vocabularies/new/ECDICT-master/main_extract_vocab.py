import sqlite3
import time
import os
# stardict.py
import stardict
# convert_to_anki.py
import convert_to_anki


'''
1. 读取 生词本 数据库
2. 与旧版本数据库对比，筛选出本次需要翻译的 “新”单词
3. 将 “新”单词 写入 “旧”版本数据库
4. 返回 “新”单词 列表

param:
    do_check: 是否检测 该词 已存在之前的单词数据库
'''
def get_voca(do_check):
    conn = sqlite3.connect('kindle_db/vocab_2020_08_21.db')
    print('Open db succ')

    # 已存储过的单词列表
    repeted_list = []

    cursor = conn.cursor()
    words_data = cursor.execute('SELECT word FROM WORDS')

    word_list = []
    i_cnt = 0
    for word in words_data:
        w = word[0].replace('"', '').replace("'", '').strip()

        # 判断该词是否已存在于之前的生词本数据库中
        if do_check:
            if is_stored(w):
                repeted_list.append(w)
                continue
            else:
                insert_to_base(w)

        # print(str(i_cnt) + '.   ' + w)

        word_list.append(w)

        i_cnt += 1

    conn.close()

    print('共有 ' + str(len(repeted_list)) + ' 个重复的单词')

    return word_list

'''
判断该词是否已存在于之前的生词本数据库中
'''
def is_stored(word):
    conn = sqlite3.connect('kindle_db/vocab_2020_08_21.db')
    cursor = conn.cursor()

    # 匹配数据库已有记录时 不区分大小写
    rel = cursor.execute("SELECT word from WORDS where word = '" + str(word) + "' COLLATE NOCASE").fetchall()

    # print(rel)

    status = len(rel)

    conn.close()

    return status


'''
将该词插入基数据库中
'''
def insert_to_base(word):
    conn = sqlite3.connect('kindle_db/vocab_2020_08_21.db')
    cursor = conn.cursor()

    id_next = len( cursor.execute('SELECT ID FROM WORDS').fetchall() ) + 1

    cursor.execute("INSERT INTO WORDS (id, word) VALUES (" + str(id_next) + ", '" + str(word) + "')")

    conn.commit()

    # print('插入单词' + str(word) + '到 基数据库 成功.')

    conn.close()

    return


'''
w: 单词的翻译结果
w_stem: 单词的词干 lemma
'''
def final_2_file(w, w_stem, i_cnt):
    with open('output/final.txt', 'a') as f:
        f.write('-------------------------------------- ' + str(i_cnt) + '\n')
        f.write(w['word'])
        if w['phonetic']:
            f.write('  [' + w['phonetic'] + ']')
        f.write('\n')
        if w_stem:
            f.write('lemma: ' + str(w_stem))
            f.write('\n')
        '''
        if w['collins']:
            f.write('collins: ' + str(w['collins']) )
            f.write('   ')
            if w['oxford']:
                f.write('oxford: ' + str(w['oxford']) )
                f.write('\n')
            else:
                f.write('\n')
        '''

        '''
        bnc_frq_cnt = 0
        if int(w['bnc']):
            f.write('BNC: ' + str(w['bnc']) + '  ' )
            bnc_frq_cnt += 1
        if int(w['frq']):
            f.write('FRQ: ' + str(w['frq']) )
            bnc_frq_cnt += 1
        if bnc_frq_cnt:
            f.write('\n')
        '''

        if w['tag']:
            f.write('TAG: ' + w['tag'])
            f.write('\n')
        f.write(w['translation'])
        f.write('\n')
        '''
        if w['exchange']:
            f.write('EXC: ' + w['exchange'])
            f.write('\n')
        '''



if __name__ == '__main__':
    do_check = int(input('需要检测单词是否存在基础词库？ (0/1) : '))
    if do_check:
        print('检查')
    else:
        print('不 检查')

    if_gen_txt = int(input('是否需要生成 Txt 文件？（0/1）：'))
    if if_gen_txt:
        print('输出 Txt')
    else:
        print('不 输出 Txt')

    if_gen_anki = int(input('是否需要生成 Anki 文件？（0/1）：'))
    if if_gen_anki:
        print('输出 Anki')
    else:
        print('不 输出 Anki')

    '''
    while 1:
        w_word = input('word:')
        rel = is_stored(w_word)
        if rel:
            print('存在')
        else:
            print('不存在')
            insert_to_base(w_word)
        print()
    '''

    # 调用 ECDICT
    sd = stardict.StarDict('full_dic.db', False)
    # 查询词干 用 
    lemma = stardict.LemmaDB()
    lemma.load('lemma.en.txt')

    # 翻译出错的单词列表
    error_list = []

    # word_list = get_voca()[:5]
    word_list = get_voca(do_check)
    print('len (word_list) = ' + str(len(word_list)))

    # 存储翻译后的结果的单词列表
    translated_word_list = []

    i_cnt = 0
    for word in word_list:
        # if i_cnt > 10:
        #     break
        # print( str(i_cnt) + ' 翻译 ' + word)

        rel = sd.query(word)
        if rel:
            # 查询词干 lemma
            '''
            w_stem = lemma.word_stem(word)
            if w_stem:
                if w_stem[2:-2] == word:
                    w_stem = None
            '''
            # write to file
            # final_2_file(rel, w_stem, i_cnt)
            if if_gen_txt:
                final_2_file(rel, '', i_cnt)
            if if_gen_anki:
                translated_word_list.append(rel)
            else:
                pass
        else:
            print('查询 ' + word + ' 失败')
            error_list.append(word)
        i_cnt += 1

    # for e in error_list:
    #     print(e)

    '''
    print('translated_word_list:')
    print(translated_word_list)
    print()
    '''

    # 开始生成 Anki 文件
    if if_gen_anki:
        c_anki = convert_to_anki.gen_apgk(translated_word_list, 'output/output')

    print()
    print('失败: ' + str(len(error_list)) )
    print('共: ' + str(len(word_list))  )

    print('Writting to file...')
    print('All completed!')

    '''
    if len(error_list):
        for w in error_list:
            print(w)
    '''

