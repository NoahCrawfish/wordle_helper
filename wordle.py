import string
import enchant
from wordfreq import word_frequency

d = enchant.Dict("en_US")
LETTER_FREQ = {
    "e": 56.88,
    "a": 43.31,
    "r": 38.64,
    "i": 38.45,
    "o": 36.51,
    "t": 35.43,
    "n": 33.92,
    "s": 29.23,
    "l": 27.98,
    "c": 23.13,
    "u": 18.51,
    "d": 17.25,
    "p": 16.14,
    "m": 15.36,
    "h": 15.31,
    "g": 12.59,
    "b": 10.56,
    "f": 9.24,
    "y": 9.06,
    "w": 6.57,
    "k": 5.61,
    "v": 5.13,
    "x": 1.48,
    "z": 1.39,
    "j": 1.00,
    "q": 1.00,
}
CHARS = set(LETTER_FREQ)

# for words of the form _____, brute force each "_" with every possible letter and return the valid words found
# for example __ill becomes "skill", "spill", "trill", etc.
def letter_combiner(known_chars, omit_chars="", cutoff_frequency=10**-6, words_dict=None):
    known_chars = known_chars.lower()
    
    if "_" not in known_chars:
        if d.check(known_chars):
            freq = word_frequency(known_chars, "en")
            return {known_chars: {"freq": freq}}
        else:
            return dict()
    
    omit_chars = omit_chars.lower()
    remaining_chars = CHARS - set(omit_chars)
    
    if words_dict is None:
        words_dict = dict()
    
    for char in remaining_chars:
        new_string = known_chars.replace("_", char, 1)
        if "_" in new_string:
            letter_combiner(new_string, omit_chars, cutoff_frequency, words_dict)
        elif d.check(new_string):
            freq = word_frequency(new_string, "en")
            words_dict[new_string] = {"freq": freq}
    
    return words_dict

def score_word_info(word: str, info_chars: set) -> float:
    score = 0
    for char in word:
        # info_chars are chars that would give more info about the word (i.e. haven't been confirmed or ruled out yet)
        if char in info_chars:
            score += LETTER_FREQ[char]
    return round(score, 2)

def word_generator(known_chars, forced_chars="", omit_chars="", sortby="info", cutoff_frequency=10**-6, partial_words=None, top_level=True):
    if partial_words is None:
        partial_words = []
    
    if forced_chars != "":
    # append every possible combination of forced chars to partial_words
        for i, known_char in enumerate(known_chars):
            if known_char == "_":
                for forced_char in forced_chars:
                    new_word = known_chars[:i] + forced_char + known_chars[i+1:]

                    if "_" in new_word:
                        word_generator(new_word, forced_chars, omit_chars, sortby, cutoff_frequency, partial_words, top_level=False)

                    all_forced_chars_in = set(forced_chars).issubset(set(new_word))
                    if all_forced_chars_in:
                        partial_words.append(new_word)
    else:
        partial_words.append(known_chars)
    
    if top_level:
        # fill in each partial word using the "letter_combiner" func
        full_words = dict()
        for partial_word in partial_words:
            new_words = letter_combiner(partial_word, omit_chars=omit_chars+forced_chars, cutoff_frequency=cutoff_frequency)
            if new_words:
                full_words |= new_words
        
        if full_words:
            # remove uncommon words according to cutoff frequency
            full_words = {word: full_words[word] for word in full_words if full_words[word]["freq"] > cutoff_frequency}
            
            # calculate which characters would provide new information
            only_known_chars = set(known_chars.replace("_", ""))
            no_info_chars = set.union(only_known_chars, set(forced_chars), set(omit_chars))
            info_chars = CHARS - no_info_chars
            # add an "info" attribute to each word that scores how likely it is that a new letter will be found
            full_words = {word: full_words[word] | {"info": score_word_info(word, info_chars)} for word in full_words}
            
            # flatten to list of dicts
            full_words = [{"word": word} | full_words[word] for word in full_words]
            # sort list by sortby attribute
            full_words = sorted(full_words, key=lambda x: x[sortby], reverse=True)
        
        return full_words
