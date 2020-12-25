FILE_PATH_ALL = "words-all-time.csv"
FILE_PATH_YRS = "words.csv"
FILE_PATH_OUT = "ranked.csv"


# Turn year in to a multiplier that rewards recency
def mult(y):
    # Most recent = 2020
    # Oldest = 1993
    if y >= 2015:
        return 50
    elif y >= 2010:
        return 20
    elif y >= 2000:
        return 5
    else:
        return 1


# Rank using recency and n appearances
def rank(a, y):
    ranked = dict()
    for w in a.keys():

        # Starting off point is "How many times has word been seen?"
        n_all = a[w]

        # Now add in a bonus
        # If this word was a Top Word for year n, we add in count * multiplier
        # Multiplier is calculated in the above funtion and prefs recency
        bonus = 0
        for yr, n_yr in y.get(w, []):
            m = mult(yr)
            bonus += (m * n_yr)

        ranked[w] = (n_all, n_all + bonus)

    return ranked


if __name__ == "__main__":

    # I know that I could use pandas but I do not want to :)

    # Parse the file of all words into a dict
    # word --> count
    all_words = dict()
    with open(FILE_PATH_ALL) as f:
        for line in f.readlines():
            if line.startswith("word"):  # Exclude header
                continue
            [word, count] = line.strip().split(",")
            all_words[word] = int(count)

    # Parse the file of yearly data into a dict
    # word --> [(yr, count), ...]
    yearly_words = dict()
    with open(FILE_PATH_YRS) as f:
        for line in f.readlines():
            if line.startswith("year"):  # Exclude header
                continue
            [year, word, count] = line.strip().split(",")
            if word in yearly_words:
                yearly_words[word].append((int(year), int(count)))
            else:
                yearly_words[word] = [(int(year), int(count))]

    # Rank the words using a multiplier
    # Final score = n_appearances + (m(yr1) * count(yr1)) + (m(yr2) * count(yr2)) + ...
    ranked = rank(all_words, yearly_words)

    # Sort the data in descending order
    l = [(k, v1, v2) for k, (v1, v2) in ranked.items()]
    l.sort(key=lambda x: x[2], reverse=True)

    # Write to output file
    with open(FILE_PATH_OUT, "w") as f:
        text_lines = ["word,old_score,new_score"]
        for a, b, c in l:
            text_lines.append("{},{},{}".format(a, b, c))
        text = "\n".join(text_lines)
        f.write(text)
    