import genanki


def gen_apgk(word_list, file_name):
    print('-> 进入 gen_apgk()')

    '''
    Once again, you need a unique deck_id that you should generate 
    once and then hardcode into your .py file.
    '''
    my_deck = genanki.Deck(
        2057400113,
        'Kindle生词本')

    my_model = genanki.Model(
        1607394563,
        'Simple Model',
        fields=[
          {'name': 'Question'},
          {'name': 'Answer'},
        ],
        templates=[
          {
            'name': 'Card 1',
            'qfmt': '{{Question}}',
            'afmt': '{{FrontSide}}<hr id="answer">{{Answer}}',
          },
        ])

    for word in word_list:
        # print(word)
        # print()

        question_str = ''
        question_str += "<b>" + word['word'] + "</b>"
        question_str += " <i>[" 
        question_str += word['phonetic']
        question_str += "]</i>"

        question_str += '<br ><br >'

        if word['simple_phrase']:
            # print(word + ' 有例句')

            question_str += '<b>例句：</b>'
            for phrase in word['simple_phrase']:
                question_str += '<br ><p style="text-align: left;">' + phrase + '</p><br >'
        else:
            pass

        answer_str = ''
        # answer_str += word['phonetic'] + '<br >'
        # answer_str += '\n' + word['collins'] + '<br />' + word['oxford']
        answer_str += '<b>Bnc:</b>' + str(word['bnc']) + '   <b>Frq:</b>' + str(word['frq']) + '<br ><br >'
        answer_str += word['translation'] + '<br ><br >'
        answer_str += '<b>Tag:</b> ' + word['tag']

        '''
        print(word['word'])
        print('@@@@')
        print(answer_str)
        print('#####################')
        '''
        my_note = genanki.Note(
            model = my_model,
            fields = [
                question_str,
                '<p style="text-align: left;">' + answer_str + '</p>'
                ]
            )

        my_deck.add_note(my_note)

    genanki.Package(my_deck).write_to_file(file_name + '.apkg')
    print('-> gen_apgk 结束，共 ' + str(len(word_list)) )



if __name__ == '__main__':
    word_list = []

    word_list.append({
        'word': 'word_1',
        'phonetic': 'phonetic_1',
        'bnc': 'bnc_1',
        'frq': 'frq_1',
        'translation': 'translation_1',
        'tag': 'tag_1',
        'simple_phrase': ['phrase_1111']
        })

    word_list.append({
        'word': 'word_2',
        'phonetic': 'phonetic_2',
        'bnc': 'bnc_2',
        'frq': 'frq_2',
        'translation': 'translation_2',
        'tag': 'tag_2',
        'simple_phrase': ['phrase_222']
        })

    gen_apgk(word_list, 'output/output')

