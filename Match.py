import re


def get_word_count(sentence):
    return len(get_words(sentence))


def get_words(sentence):
    if len(sentence) == 0:
        return []
    string_processing = re.sub("[.?!,:()+-]", " ", sentence).lower().strip()
    string_processing = re.sub(" {2}", " ", string_processing)
    string_processing = re.split("[ ]", string_processing)
    string_processing = list(filter(None, string_processing))
    return string_processing


def get_longer(strings):
    strings.sort(key=lambda s: len(s))
    return strings


def get_location_of_word(word, sentence, after_index=0):
    words = get_words(sentence)

    for word_i in range(len(words)):
        if word_i > after_index:
            if words[word_i].lower().strip() == word.lower().strip():
                return word_i, word_i
    return -1, -1


def match_sentences(sentences):
    match_output = {}
    for sub_sentences in range(len(sentences)):
        if sub_sentences >= len(sentences):
            break
        small_sent = sentences[sub_sentences].lower().strip()
        small = get_words(small_sent)
        large = sentences[-1].lower().strip()
        normal_large = sentences[-1].lower().strip()
        max_length = get_word_count(large)
        distance_count = 1
        average_distance_off = 0
        last_index = 0
        for small_words in range(len(small)):
            dist = get_location_of_word(small[small_words], large)
            if dist != -1:
                short_term_large_sent = large
                small_sent_dist = get_location_of_word(small[small_words], small_sent, small_words - 1)[0]
                normal_large_dist = get_location_of_word(small[small_words], normal_large, last_index)
                last_index = normal_large_dist[1]
                average_distance_off += abs(normal_large_dist[0] - small_sent_dist)
                if re.search("^" + small[small_words] + ".", short_term_large_sent.strip()):
                    short_term_large_sent = re.sub("^" + small[small_words] + ".", "",
                                                   short_term_large_sent, 1).strip()
                else:
                    short_term_large_sent = re.sub("[ ,.?!]" + small[small_words] + ".", " ",
                                                   short_term_large_sent, 1).strip()
                large = short_term_large_sent
                distance_count += 1

        percent = 1 - (get_word_count(large) / max_length)
        average_distance_off_percent = 1 - ((average_distance_off * 0.25) / distance_count) / max_length
        percent = percent * average_distance_off_percent
        match_output[small_sent] = "{:0.2f}".format(percent)
    return match_output
    # return percent


temp = ["Hello", "Seann How are you today?", "HI?", "What's up, How are you?", "How was the test?", "are", "How",
        "What the ..."]
t = get_longer(temp)

output = match_sentences(sentences=t)
for i in output:
    value = output[i]
    print(value + ":" + i)

'''0.00:hi?
0.19:are
0.19:how
0.00:hello
0.00:what the ...
0.18:how was the test?
0.57:what's up, how are you?
0.99:seann how are you today?'''
