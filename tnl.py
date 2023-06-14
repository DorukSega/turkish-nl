import re
from typing import Any

#from typing import Literal, NewType

###########################################################
# These are all the possible types that Natural Language Parser can parse

# V    -> Verb
# N    -> Noun
# AD   -> Adjective
# AV   -> Adverbs
# CJ   -> Conjunctions
# DT   -> Determiners
# PT   -> Particles

# N2NF -> Noun to Noun Forming (İsimden İsim Yapan)
# N2VF -> Noun to Verb Forming
# V2VF -> Verb to Verb Forming
# V2NF -> Verb to Noun Forming

# PL   -> Plural Suffix

# NP
# PS   -> Possessive Suffix (İyelik)
# BL   -> Belongingness Suffix (Aitlik)
# EL   -> Elative Suffix (Ayrılma Hali)
# RL   -> Relative Suffix (İlgi Hali)
# IN   -> Innesive Suffix (Bulunma Hali)
# AC   -> Accusative Suffix (Belirtme Hali)

# VP
# PP   -> Perfect Past Tense (Görülen Geçmiş Zaman)
# LT   -> Learned Past Tense (Öğrenilen Geçmiş Zaman)
# PR   -> Present Tense
# FT   -> Future Tense
# AOR  -> Aorist Tense (Geniş Zaman)

# CO   -> Conditional Mood (Şart Kipi)

# PER  -> Personal Suffix (Kişi Eki)
# EF   -> Extra Verb (Ek Fiil)
# The type decleration, because of Pylance issues disabled
# CFG = NewType("CFG", Literal['V',
#                              'N',
#                              'N2NF',
#                              'N2VF',
#                              'V2VF',
#                              'V2NF',
#                              'PL',
#                              'PS',
#                              'BL',
#                              'EL',
#                              'RL',
#                              'IN',
#                              'AD',
#                              'AV',
#                              'CJ',
#                              'DT',
#                              'PT',
#                              'PP',
#                              'LT',
#                              'PR',
#                              'FT',
#                              'AOR',
#                              'NP',
#                              'VP',
#                              'CO',
#                              'PER',
#                              'AC',
#                              'EF', ])


class Match:
    raw: str
    type: Any
    start_index: int

    def __init__(self, raw: str, type, start_index: int):
        self.raw = raw
        self.type = type
        self.start_index = start_index

    def __str__(self) -> str:
        return f"{self.raw} - {self.type}"

    def __repr__(self):
        return f"'{self.raw}' - {self.type}"

###########################################################
# Generates lists for turkish langauge


def fileList(fname: str) -> list[str]:
    return open("data/" + fname + ".txt", "r", encoding="utf-8").read().splitlines()


#nouns = fileList("nouns")
nouns = fileList("adlar")  # more nouns from turkish wikipedia instead english
verbs = fileList("verbs")
adjectives = fileList("adjectives")
adverbs = fileList("adverbs")
conjunctions = fileList("conjunctions")
determiners = fileList("determiners")
particles = fileList("particles")
pronouns = fileList("pronouns")
iiye = fileList("iiye")  # isimden isim yapan ekler - noun to noun forming suffixes
ifye = fileList("ifye")  # isimden fiil yapan ekler - noun to verb forming suffixes
ffye = fileList("ffye")  # fiilden fiil yapan ekler - verb to verb forming suffixes
fiye = fileList("fiye")  # fiilden isim yapan ekler - verb to noun forming suffixes
possessive = fileList("possessive")
present = fileList("present")
personal = fileList("personal")

###########################################################


def parse_lexeme(raw: str, matches: list[Match] | None = None, i: int = 0, word: str = "", c_type: str = '') -> tuple[list[Match], Any] | None:
    if matches is None:
        matches = []
    word = word + raw[i]
    old_match = matches[:]
    old_ctype = c_type
    if (n_type := match_it(matches, i, word, c_type)) != "":
        c_type = n_type
    else:
        if len(raw)-1 == i:
            return None
        else:
            return parse_lexeme(raw, matches, i+1, word, c_type)

    if len(raw)-1 == i:
        return matches, c_type
    else:
        if travel := parse_lexeme(raw, old_match, i+1, word, old_ctype):
            return travel
        else:
            return parse_lexeme(raw, matches, i+1, "", c_type)


def match_it(matches: list[Match] = [], i: int = 0, word: str = "", c_type: str = ''):
    state = ""
    if len(matches) == 0:
        if word in verbs:
            matches.append(
                Match(word, 'V', i-len(word)))
            state = 'V'
        elif word in nouns or word in pronouns:
            matches.append(
                Match(word, 'N', i-len(word)))
            state = 'N'
        elif word in adjectives:
            matches.append(
                Match(word, 'AD', i-len(word)))
            state = 'AD'
        elif word in adverbs:
            matches.append(
                Match(word, 'AV', i-len(word)))
            state = 'AV'
        elif word in conjunctions:
            matches.append(
                Match(word, 'CJ', i-len(word)))
            state = 'CJ'
        elif word in determiners:
            matches.append(
                Match(word, 'DT', i-len(word)))
            state = 'DT'
        elif word in particles:
            matches.append(
                Match(word, 'PT', i-len(word)))
            state = 'PT'

    elif c_type == "N" or c_type == "NP":
        if re.search(r"^l[ae]r$", word) and not len([x for x in matches if x.type == 'PL']):
            matches.append(
                Match(word, 'PL', i-len(word)))
            state = c_type
        elif len([x for x in possessive if re.search(r"^" + x + r"$", word)]) > 0 and not len([x for x in matches
                                                                                               if x.type == 'PS']):
            matches.append(
                Match(word, 'PS', i-len(word)))
            state = 'NP'
        elif re.search(r"^ki$", word) and not len([x for x in matches if x.type == 'BL']):
            matches.append(
                Match(word, 'BL', i-len(word)))
            state = 'NP'
        elif re.search(r"^[dt][ae]n$", word) and not len([x for x in matches if x.type == 'EL']):
            matches.append(
                Match(word, 'EL', i-len(word)))
            state = 'NP'
        elif re.search(r"^[ıiuü]n$", word) and not len([x for x in matches if x.type == 'RL']):
            matches.append(
                Match(word, 'RL', i-len(word)))
            state = 'NP'
        elif re.search(r"^[dt][ae]$", word) and not len([x for x in matches if x.type == 'IN']):
            matches.append(
                Match(word, 'IN', i-len(word)))
            state = 'NP'
        elif (re.search(r"^[ıiuü]$", word) or re.search(r"^y[ıiuü]$", word)) and not len([x for x in matches if x.type == 'AC']):
            matches.append(
                Match(word, 'AC', i-len(word)))
            state = 'NP'
        if re.search(r"^[dt][ıiuü]$", word) and not len([x for x in matches if x.type == 'PP']):
            matches.append(
                Match(word, 'PP', i-len(word)))
            state = 'EF'
        elif re.search(r"^m[ıiuü]ş$", word) and not len([x for x in matches if x.type == 'LT']):
            matches.append(
                Match(word, 'LT', i-len(word)))
            state = 'EF'
        elif len([x for x in iiye if re.search(r"^" + x + r"$", word)]) > 0:
            matches.append(
                Match(word, 'N2NF', i-len(word)))
            state = 'N'
        elif len([x for x in ifye if re.search(r"^" + x + r"$", word)]) > 0:
            matches.append(
                Match(word, 'N2VF', i-len(word)))
            state = 'V'

    elif c_type == "V" or c_type == "VP":
        if re.search(r"^[dt][ıiuü]$", word) and not len([x for x in matches if x.type == 'PP']):
            matches.append(
                Match(word, 'PP', i-len(word)))
            state = c_type
        elif re.search(r"^m[ıiuü]ş$", word) and not len([x for x in matches if x.type == 'LT']):
            matches.append(
                Match(word, 'LT', i-len(word)))
            state = c_type
        elif len([x for x in present if re.search(r"^" + x + r"$", word)]) > 0 and not len([x for x in matches
                                                                                            if x.type == 'PR']):
            matches.append(
                Match(word, 'PR', i-len(word)))
            state = c_type
        elif (re.search(r"^aca[kğ]$", word) or re.search(r"^ece[kğ]$", word)) and not len([x for x in matches
                                                                                           if x.type == 'FT']):
            matches.append(
                Match(word, 'FT', i-len(word)))
            state = c_type
        elif (word == "r" or re.search(r"^[aeıi]r$", word)) and not len([x for x in matches
                                                                         if x.type == 'AOR']):
            matches.append(
                Match(word, 'AOR', i-len(word)))
            state = c_type
        elif re.search(r"^s[ae]$", word) and not len([x for x in matches if x.type == 'CO']):
            matches.append(
                Match(word, 'CO', i-len(word)))
            state = c_type
        elif matches[-1].type != 'V' and len([x for x in personal
                                              if re.search(r"^" + x + r"$", word)]) > 0 and not len([x for x in matches
                                                                                                     if x.type == 'PER']):
            matches.append(
                Match(word, 'PER', i-len(word)))
            state = c_type
        elif len([x for x in ffye if re.search(r"^" + x + r"$", word)]) > 0:
            matches.append(
                Match(word, 'V2VF', i-len(word)))
            state = 'V'
        elif len([x for x in fiye if re.search(r"^" + x + r"$", word)]) > 0:
            matches.append(
                Match(word, 'V2NF', i-len(word)))
            state = 'N'

    return state


def parse_sentence(sentence):
    sentence = sentence.split()
    results = []
    for lex in sentence:
        if parsed := parse_lexeme(lex):
            results.extend(parsed[0])
    print(results)
    results = [x.raw for x in results]

    return results
