import dataAnalyze
import time
import math

mRateTransition = dataAnalyze.mRateTransition
mRateLaunch = dataAnalyze.mRateLaunch
lst_Part_of_Speech = dataAnalyze.lst_Part_of_Speech  # 导入模型数据
n = len(lst_Part_of_Speech)


def analyzeSentence(lst_sentence):
    '''
    把输入句子解析加上tag
    :param lst_sentence:
    :return:
    '''
    lst_sentence_result = lst_sentence.copy()
    for i in range(len(lst_sentence)):
        print("{0:%}".format(i / len(lst_sentence)))
        if lst_sentence[i] != [[]]:
            tempword = ["", [[1, ["_"]] for i in range(n - 1)]]
            for j in range(len(lst_sentence[i])):
                tempword = viterbi(tempword, lst_sentence[i][j][1])
            result_sentence = tuple(max(tempword[1])[1])
            for j in range(len(lst_sentence[i])):
                lst_sentence_result[i][j][3] = result_sentence[j + 1]
    return lst_sentence_result


def viterbi(wordBefore, wordAfter):
    '''

    :param wordBefore: [word,
    [
    [rate, //到达该条路径的概率
    [ps1,ps2,ps3,...] //记录到达该词性最佳路径
    ],...
    ]// 所有词性都记录一条最大概率道路的路径和概率, 终点为wordBefore
    :param wordAfter: string
    :return: [wordAfter,[[rate, [ps1,ps2,ps3,...]],...] //终点为wordAfter
    '''
    tempword = [wordAfter, []]
    for i in range(n - 1):
        if wordBefore[0] == "":
            temp = [math.log10(mRateTransition[-1][i]) +
                    math.log10(mRateLaunch[i].get(wordAfter,
                                                  dataAnalyze.alpha / (mRateLaunch[i].get(
                                                      "__sum__") + dataAnalyze.alpha * dataAnalyze.sumLaunch))),
                    lst_Part_of_Speech.index("_")]
            tempword[1].append([temp[0], [i for i in wordBefore[1][i][1]]])
            tempword[1][i][1].append(lst_Part_of_Speech[i])
        else:
            temp = max([[wordBefore[1][j][0] + math.log10(mRateTransition[j][i]) + math.log10(
                mRateLaunch[i].get(wordAfter, dataAnalyze.alpha /
                                   (mRateLaunch[i].get("__sum__") + dataAnalyze.alpha * dataAnalyze.sumLaunch))), j] for
                        j in range(n - 1)])
            tempword[1].append([temp[0], [j for j in wordBefore[1][temp[1]][1]]])
            tempword[1][i][1].append(lst_Part_of_Speech[i])
    # temp = [[lst_Part_of_Speech[i], mRateTransition[lst_Part_of_Speech.index(wordBefore[1])][i]*mRateLaunch[i].get(wordAfter, dataAnalyze.alpha/mRateLaunch[i].get("__sum__"))] for i in range(len(lst_Part_of_Speech)) if lst_Part_of_Speech[i] != "_"]
    return tempword


def pingJia(result, answer):
    count = 0
    countRight = 0
    for i in range(len(result)):
        if result[i] != [[]]:
            for j in range(len(result[i])):
                if answer[i][j][3] == result[i][j][3]:
                    countRight += 1
                count += 1
    return countRight / count


if __name__ == "__main__":
    timeStart = time.time()
    answer = dataAnalyze.fileOpen("./data/dev.conll")
    result = analyzeSentence(answer)
    answer = dataAnalyze.fileOpen("./data/dev.conll")
    print("time cost: " + str(time.time() - timeStart))
    print("正确率: " + str(pingJia(result, answer)))
    with open("result.conll", "w", encoding="utf-8") as fp:
        for i in result:
            for j in i:
                fp.write("\t".join(j) + "\n")
            fp.write("\n")
