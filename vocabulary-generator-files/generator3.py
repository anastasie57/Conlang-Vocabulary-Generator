import random, re, codecs

# выбор согласного для слога

def con(simple, other):
    num = random.randint(1, 30)
    if num <= 5:
        return u''
    elif num >= 6 and num <=15:
        return random.choice(other)
    elif num >= 16:
        return random.choice(simple)

# выбор гласного для слога

def vow(simple, other):
    num = random.randint(1, 30)
    if num <= 10:
        return random.choice(other)
    elif num >= 11:
        return random.choice(simple)

def newword(vowels, consonants, lowerlimit, upperlimit):
    word = ''
    for num in range(random.randint(lowerlimit, upperlimit)):
        syll = con(consonants[0], consonants[1]) + vow(vowels[0], vowels[1])
        word += syll
        for sound in consonants[0]:
            m = re.search(u'(ĩ|ẽ|ũ|ã)' + sound, word, flags=0)
            if m != None:
                word = re.sub(m.group(0), random.choice(vowels[0]) + sound, word)
        for sound in consonants[1]:
            m = re.search(u'[ĩẽũã]' + sound, word, flags=0)
            if m != None:
                word = re.sub(m.group(0), random.choice(vowels[0]) + sound, word)
    m = re.search(u'(i|ĩ|e|ẽ|u|ũ|a|ã)' * 4, word, flags=0)
    if m != None:
        if m.group(0)[-1] in vowels[1]:
            word = re.sub(m.group(0), m.group(0)[:-2], word)
        else:
            word = re.sub(m.group(0), m.group(0)[:-1], word)
    if word.endswith((u'ĩ', u'ẽ', u'ũ', u'ã')):
        word = re.sub(word[-2:], random.choice(vowels[0]), word)
    return word

vows = [[u'i', u'e', u'u', u'a'], [u'ĩ', u'ẽ', u'ũ', u'ã']]

cons = [[u'pʰ', u'tʰ', u'kʰ', u't͡sʰ', u't͡ʃʰ', u'f', u'v', u's', u'z', u'ʃ', u'ʒ',
         u'x', u'ɣ', u'χ', u'ʁ', u'ħ', u'ʕ', u'h', u'm', u'n', u'ŋ', u'ɾ', u'ɫ', u'j', u'w'],
        [u'pʼ', u'tʼ', u'kʼ', u'kʷ', u't͡sʼ', u't͡ʃʼ', u'xʷ', u'ɣʷ', u'ŋʷ']]

findict = {u'ечь':u'ежение',
           u'ить':u'ение',
           u'сить':u'шение',
           u'ать':u'ание',
           u'ывать':u'ыние',
           u'еть':u'ение',
           u'сти':u'едение',
           u'ести':u'ошение'}

exceptions = {u'ечь':[u'горечь', u'печь', u'речь', u'сечь', u'течь'],
              u'ать':[u'благодать', u'гать', u'дать', u'кровать', u'мать', u'рать', u'стать', u'тать'],
              u'ывать':[],
              u'ить':[u'жить', u'нить'],
              u'сить':[],
              u'еть':[u'деть', u'плеть', u'сеть'],
              u'сти':[],
              u'ести':[]}

dict = {}
verbdict = {}

words = []

f = codecs.open('newdict_marked.txt', 'r', 'utf-8-sig')

for line in f:
    line = line.strip()
    words.append(line)
    
f.close()

# выделение глаголов и отглагольных существительных в отдельный словарь
# с их последующим удалением из общего списка слов во избежание повторений

for word in words:
    if word[-1] in ('1', '2', '3', '4'):
        if word[-1] == '1':
            dict[word] = newword(vows, cons, 1, 3) + u' ' + word[-1]
        else:
            dict[word] = newword(vows, cons, 2, 4) + u' ' + word[-1]
    else:
        dict[word] = newword(vows, cons, 1, 4)
    print word, u'-', dict[word]
    for fin in findict:
        if word not in exceptions[fin]:
            if word.endswith(fin):
                verbdict[word] = []
                noun = word
                noun = re.sub(fin, findict[fin], noun)
                for elem in words:
                    if elem.endswith(noun + u' 3'):
                        verbdict[word].append(elem)
                        words.remove(elem)
                    elif elem.endswith(noun + u' 4'):
                        verbdict[word].append(elem)
                        words.remove(elem)
                
        else:
            continue

f.close()

# за счёт добавления случайной согласной, могут образовываться разные существительные
# и может появляться омонимия

for stem in verbdict:
    dict[stem] = newword(vows, cons, 2, 4)
    for each in verbdict[stem]:
        dict[each] = u'ʃu' + random.choice(vows[0]) + dict[stem]
        print dict[each]

# выдача словаря

f = codecs.open(u'dict_conlang_rus.txt', 'w', 'utf-8-sig')

for elem in sorted(dict):
    str = ''
    str = elem + u' - ' + dict[elem] + u'\r\n'
    f.write(str)

f.close()
