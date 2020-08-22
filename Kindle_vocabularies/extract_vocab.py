import sqlite3
import time
import requests


def get_voca():
    conn = sqlite3.connect('vocab.db')
    print('Open db succ')

    cursor = conn.cursor()
    words_data = cursor.execute('SELECT word, stem, timestamp FROM WORDS')

    word_list = []
    i_cnt = 0
    for word in words_data:
        w = word[0]
        if word[0] == word[1]:
            s = ''
        else:
            s = word[1]
        t = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime( word[2] ))
        print(str(i_cnt) + '.   ' + w)
        '''
        print('stem: ' + s)
        print('timestamp: ' + str(t))
        print()
        '''
        word_list.append({'word': w, 'stem': w, 'timestamp': t, 'translate': ''})

        i_cnt += 1

    conn.close()
    return word_list


def trans( word ):
    data = {
        # 'from': 'en',
        # 'to': 'zh-CHS',
        'doctype': 'json',
        'type': 'AUTO',
        'i':word,
    }

    proxies = {
        'http': 'http://122.226.57.70:8888', 
        'https': 'http://122.226.57.70:8888'
    }

    '''
    'http://112.111.217.6:9999', 
    'http://171.12.115.199:9999', 
    'http://80.78.74.133:55443', 
    'http://110.243.15.92:9999', 
    'http://81.95.13.207:5836', 
    'http://180.250.85.204:8181', 
    '''

     
    url = "http://fanyi.youdao.com/translate"
    try:
        r = requests.get(url, params=data, proxies = proxies, timeout = 30)
        # r = requests.get(url, params=data, timeout = 30)
        result = r.json()

        # 打印翻译结果
        # 简单结果
        simple_rel = result['translateResult'][0][0]['tgt']
        # 完整结果
        # full_rel = result['smartResult']['entries']

        # return {'simple_rel': simple_rel, 'full_rel': full_rel}
        return {'simple_rel': simple_rel, }
    except Exception as e:
        return {}


def final_2_file(w, i_cnt):
    with open('final.txt', 'a') as f:
        # for w in word_list:
        f.write('------------------------ ' + str(i_cnt) + '\n')
        f.write('WORD: ' + w['word'])
        f.write('\n')
        if w['stem']:
            f.write('STEM: ' + w['stem'])
            f.write('\n')
        f.write('TRAN: ' + w['translate'])
        # f.write('\n')
        # f.write(w['timestamp'])
        f.write('\n')



if __name__ == '__main__':
    # 翻译出错的单词列表
    error_list = []

    # word_list = get_voca()[:5]
    word_list = get_voca()[1427:1501]

    i_cnt = 1427
    for word in word_list:
        # 翻译重试次数
        r_tran = 3
        # if i_cnt > 5:
        #     break

        print( str(i_cnt) + ' 翻译 ' + word['word'])
        time.sleep(0.5)
        rel = trans(word['word'])
        if rel:
            word['translate'] = rel['simple_rel']
            # write to file
            final_2_file(word, i_cnt)
        else:
            # 重试
            if r_tran:
                r_tran -= 1
                time.sleep(0.5)
                rel = trans(word['word'])
                if rel:
                    word['translate'] = rel['simple_rel']
                    # write to file
                    final_2_file(word, i_cnt)
            else:
                print('翻译 ' + word['word'] + '出错了')
                word['translate'] = 'null'
                error_list.append(word['word'])

        i_cnt += 1

    for e in error_list:
        print(e)

    print()
    print('失败: ' + str(len(error_list)) )
    print('共: ' + str(len(word_list))  )

    print('Writting to file...')
    print('All completed!')

