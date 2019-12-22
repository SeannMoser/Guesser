import re


def get_word_count(t):
    return len(get_words(t))


def get_words(t):
    if len(t) == 0:
        return []
    temp = re.sub("[\.\?\!\,\:\(\)\+\-]", " ", t).lower().strip()
    temp = re.sub("  ", " ", temp)
    temp = re.split("[ ]", temp)
    temp = list(filter(None, temp))
    return temp


def get_longer(strings):
    strings.sort(key=lambda s: len(s))
    return strings


def get_location_of_word(word, sentence, after_index=0):
    words = get_words(sentence)

    for i in range(len(words)):
        if i > after_index:
            if words[i].lower().strip() == word.lower().strip():
                return i, i
    return -1, -1;


def match_sentences(sentences):
    output = {}
    for i in range(len(sentences)):
        if i >= len(sentences):
            break
        small_sent = sentences[i].lower().strip()
        small = get_words(small_sent)
        large = sentences[-1].lower().strip()
        normal_large = sentences[-1].lower().strip()
        maxLength = get_word_count(large)
        distanceCount = 1
        average_distance_off = 0
        last_index = 0
        for i in range(len(small)):
            dist = get_location_of_word(small[i], large)
            if dist != -1:
                templarge = large
                small_sent_dist = get_location_of_word(small[i], small_sent, i - 1)[0]
                normal_large_dist = get_location_of_word(small[i], normal_large, last_index)
                last_index = normal_large_dist[1]
                average_distance_off += abs(normal_large_dist[0] - small_sent_dist)
                if re.search("^" + small[i] + ".", templarge.strip()):
                    templarge = re.sub("^" + small[i] + ".", "", templarge, 1).strip()
                else:
                    templarge = re.sub("([ \,\.\?\!])" + small[i] + ".", " ", templarge, 1).strip()
                large = templarge
                distanceCount += 1

        percent = 1 - (get_word_count(large) / maxLength)
        temp = 1 - ((average_distance_off * 0.25) / distanceCount) / maxLength
        percent = percent * (temp)
        # print("{:0.2f}".format((percent)) + ":" + small_sent)
        output[small_sent] = "{:0.2f}".format((percent))
    return output
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
