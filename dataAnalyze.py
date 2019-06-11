import json
import os.path

lst_Part_of_Speech = set()  # 词性列表
mRateTransition = []  # 转移概率矩阵[before][after]
# mRateTransition2 = []
mRateLaunch = []  # 发射概率词典列表套字典 [ps][word]
dictWord = set()  # 词典集合
alpha = 1e-9  # 加 α 平滑参数


def fileOpen(path):
    '''
     :param path: path of train data
    :return: lst_sentence: [sentence:[word:[number, word, ???, part of speech, ???, ???, ???, ???, ???, ???],],]
    '''
    try:
        with open(path, "r", encoding="utf-8") as fp:
            lst_sentence = fp.read().split("\n\n")
    except Exception:
        print("wrong path!")
        exit()
    for i in range(len(lst_sentence)):
        lst_sentence[i] = lst_sentence[i].split("\n")
        for j in range(len(lst_sentence[i])):
            lst_sentence[i][j] = lst_sentence[i][j].split()
    return lst_sentence


def anylyze():
    for sentence in lst_sentence:
        if sentence == [[]]:
            continue
        tempWord = "_"
        # tempWord2 = ["_", "_"]
        for word in sentence:
            dictWord.add(word[3])
            if word[3] not in lst_Part_of_Speech:
                lst_Part_of_Speech.append(word[3])
            mRateTransition[lst_Part_of_Speech.index(tempWord)][lst_Part_of_Speech.index(word[3])] += 1
            # mRateTransition[lst_Part_of_Speech.index(tempWord2[0])][lst_Part_of_Speech.index(tempWord2[1])][lst_Part_of_Speech.index(word[3])] += 1
            mRateLaunch[lst_Part_of_Speech.index(word[3])][word[1]] = mRateLaunch[
                                                                          lst_Part_of_Speech.index(word[3])].get(
                word[1], 0) + 1
            tempWord = word[3]
            # tempWord2.pop()
            # tempWord2.append(word[3])


def rateLaunch(alpha):
    '''
    计算发射概率
    :param alpha: 加α平滑参数
    :return:
    '''
    sumLaunch = len(dictWord)
    for i in mRateLaunch:
        sum0 = sum(i.values())
        i["__sum__"] = sum0
        for word in i.keys():
            if word != "__sum__":
                i[word] = (i[word] + alpha) / (sumLaunch * alpha + sum0)


def rateTransition():
    for i in range(len(mRateTransition)):
        sumTransition = sum(mRateTransition[i])
        for j in range(len(mRateTransition[i])):
            mRateTransition[i][j] = (mRateTransition[i][j] + alpha) / (sumTransition + alpha * sumLaunch)


if __name__ == "dataAnalyze":
    lst_sentence = fileOpen("./data/train.conll")
    if not os.path.exists("./lst_part_of_speech.json"):
        for sentence in lst_sentence:
            if not sentence == [[]]:
                for word in sentence:
                    lst_Part_of_Speech.add(word[3])
        lst_Part_of_Speech = tuple(list(lst_Part_of_Speech) + ["_"])
        with open("lst_part_of_speech.json", "w", encoding="utf-8") as fp:
            json.dump(lst_Part_of_Speech, fp=fp, ensure_ascii=False, indent=4)
    else:
        with open("lst_part_of_speech.json", "r", encoding="utf-8") as fp:
            lst_Part_of_Speech = json.load(fp)
    mRateTransition = [[0 for i in range(len(lst_Part_of_Speech) - 1)] for i in range(len(lst_Part_of_Speech))]
    mRateLaunch = [{} for i in range(len(lst_Part_of_Speech))]
    anylyze()
    sumLaunch = len(dictWord)
    rateLaunch(alpha)
    rateTransition()

if __name__ == "__main__":
    lst_sentence = fileOpen("./data/train.conll")
    if not os.path.exists("./lst_part_of_speech.json"):
        for sentence in lst_sentence:
            if sentence == [[]]:
                continue
            for word in sentence:
                lst_Part_of_Speech.add(word[3])
        lst_Part_of_Speech = list(lst_Part_of_Speech) + ["_"]
        with open("lst_part_of_speech.json", "w", encoding="utf-8") as fp:
            json.dump(lst_Part_of_Speech, fp=fp, ensure_ascii=False, indent=4)
    else:
        with open("lst_part_of_speech.json", "r", encoding="utf-8") as fp:
            lst_Part_of_Speech = json.load(fp)
    mRateTransition = [[0 for i in range(len(lst_Part_of_Speech))] for i in range(len(lst_Part_of_Speech) - 1)]
    # mRateTransition2 = [[[0 for i in range(len(lst_Part_of_Speech))] for i in range(len(lst_Part_of_Speech))] for i in
    #                    range(len(lst_Part_of_Speech))]
    mRateLaunch = [{} for i in range(len(lst_Part_of_Speech))]
    anylyze()
    rateLaunch(alpha)
    rateTransition()

    with open("./data/Lrate.json", "w", encoding="utf-8") as fp:
        json.dump(mRateLaunch, fp=fp, ensure_ascii=False, indent=4)
    with open("./data/Trate.json", "w", encoding="utf-8") as fp:
        json.dump(mRateTransition, fp=fp, ensure_ascii=False, indent=4)
