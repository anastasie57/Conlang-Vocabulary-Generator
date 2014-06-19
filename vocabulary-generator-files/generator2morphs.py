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

# порождение морфем

#u'POSS1', u'POSS2', u'POSS3', u'POSS4',
          #u'PL (pref)', u'PL verbs',
          #u'INDEF', u'NMNLZ',
          #u'1SG)', u'1PL)', u'INCL)', u'2SGINF)', u'2SGF)', u'2PL)',
          #u'CLF1', u'CLF2', u'CLF3', u'CLF4',
morphs = [u'3SG.NFUT (pref)', u'3SG.FUT (pref)', u'MOD']
          #u'INCL.NFUT (pref)',
          #u'2SGINF.NFUT (pref)', u'2SGF.NFUT (pref)', u'2PL.NFUT (pref)',
          #u'1SG.FUT (pref)', u'1PL.FUT (pref)', u'INCL.FUT (pref)',
          #u'2SGINF.FUT (pref)', u'2SGF.FUT (pref)', u'2PL.FUT (pref)',
          #u'PERF', u'SUBJ', u'OPT', u'SENS', 'NEG',
          #u'ERG (prep)', u'GEN (prep)', u'DAT (prep)', u'LOC/PREP (prep)',
          #u'PL', u'COM (prep)', u'LAT (prep)', u'DISTR', u'QUOT', u'NEG',
          #u'кто-то', u'что-то', u'Dem', u'Dems', u'Deml', u'Demr', u'сам']

dict = {}

f = codecs.open(u'morphemes_add.txt', 'w', 'utf-8-sig')

for elem in morphs:
    num = random.randint(1, 30)
    if num < 11:
        if elem.endswith(u')'):
            dict[elem] = newword(vows, cons, 2, 2) + u'\r\n'
        else:
            rand = random.randint(1, 30)
            if num < 15:
                dict[elem + u' (suf)'] = newword(vows, cons, 2, 2) + u'\r\n'
            if num >= 15:
                dict[elem + u' (pref)'] = newword(vows, cons, 2, 2) + u'\r\n'
    elif num >= 11:
        if elem.endswith(u')'):
            dict[elem] = newword(vows, cons, 1, 1) + u'\r\n'
        else:
            rand = random.randint(1, 30)
            if num < 15:
                dict[elem + u' (suf)'] = newword(vows, cons, 1, 1) + u'\r\n'
            if num >= 15:
                dict[elem + u' (pref)'] = newword(vows, cons, 1, 1) + u'\r\n'

for elem in dict:
    f.write(elem + u' - ' + dict[elem])

f.close()
