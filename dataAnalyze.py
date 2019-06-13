import json
import os.path


class DataAnalyze(object):
    lst_Part_of_Speech = set()  # 词性列表
    mRateTransition = []  # 转移概率矩阵[before][after]
    # mRateTransition2 = []
    mRateLaunch = []  # 发射概率词典列表套字典 [ps][word]
    dictWord = set()  # 词典集合
    alpha = 1e-9  # 加 α 平滑参数
    sumLaunch = 0

    def fileOpen(self, path):
        """
         :param path: path of train data
        :return: lst_sentence: [sentence:[word:[number, word, ???, part of speech, ???, ???, ???, ???, ???, ???],],]
        """
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

    def anylyze(self, lst_sentence):
        for sentence in lst_sentence:
            if sentence == [[]]:
                continue
            tempWord = "_"
            # tempWord2 = ["_", "_"]
            for word in sentence:
                self.dictWord.add(word[3])
                if word[3] not in self.lst_Part_of_Speech:
                    self.lst_Part_of_Speech.append(word[3])
                self.mRateTransition[self.lst_Part_of_Speech.index(tempWord)][
                    self.lst_Part_of_Speech.index(word[3])] += 1
                # mRateTransition[lst_Part_of_Speech.index(tempWord2[0])][lst_Part_of_Speech.index(tempWord2[1])][lst_Part_of_Speech.index(word[3])] += 1
                self.mRateLaunch[self.lst_Part_of_Speech.index(word[3])][word[1]] = self.mRateLaunch[
                                                                                        self.lst_Part_of_Speech.index(
                                                                                            word[3])].get(
                    word[1], 0) + 1
                tempWord = word[3]
                # tempWord2.pop()
                # tempWord2.append(word[3])

    def rateLaunch(self, alpha):
        """
        计算发射概率
        :param alpha: 加α平滑参数
        :return:
        """
        self.sumLaunch = len(self.dictWord)
        for i in self.mRateLaunch:
            sum0 = sum(i.values())
            i["__sum__"] = sum0
            for word in i.keys():
                if word != "__sum__":
                    i[word] = (i[word] + alpha) / (self.sumLaunch * alpha + sum0)

    def rateTransition(self):
        for i in range(len(self.mRateTransition)):
            sumTransition = sum(self.mRateTransition[i])
            for j in range(len(self.mRateTransition[i])):
                self.mRateTransition[i][j] = (self.mRateTransition[i][j] + self.alpha) / (
                            sumTransition + self.alpha * self.sumLaunch)

    def saveData(self, path):
        with open(os.path.join(path, "lst_part_of_speech.json"), "w", encoding="utf-8") as fp:
            json.dump(self.lst_Part_of_Speech, fp=fp, ensure_ascii=False, indent=4)
        with open(os.path.join(path, "Trate.json"), "w", encoding="utf-8") as fp:
            json.dump(self.mRateTransition, fp=fp, ensure_ascii=False, indent=4)
        with open(os.path.join(path, "Lrate.json"), "w", encoding="utf-8") as fp:
            json.dump(self.mRateLaunch, fp=fp, ensure_ascii=False, indent=4)

    def __init__(self, path="./data/train.conll", alpha=1e-6):
        """
        :param path: 训练数据集路径
        :param alpha: 平滑参数
        """
        self.alpha = alpha
        lst_sentence = self.fileOpen(path)
        try:
            with open("lst_part_of_speech.json", "r", encoding="utf-8") as fp:
                self.lst_Part_of_Speech = json.load(fp)
        except FileNotFoundError:
            for sentence in lst_sentence:
                if not sentence == [[]]:
                    for word in sentence:
                        self.lst_Part_of_Speech.add(word[3])
            self.lst_Part_of_Speech = tuple(list(self.lst_Part_of_Speech) + ["_"])
        self.mRateTransition = [[0 for i in range(len(self.lst_Part_of_Speech) - 1)] for i in
                                range(len(self.lst_Part_of_Speech))]
        self.mRateLaunch = [{} for i in range(len(self.lst_Part_of_Speech))]
        self.anylyze(lst_sentence)
        self.sumLaunch = len(self.dictWord)
        self.rateLaunch(self.alpha)
        self.rateTransition()

if __name__ == "__main__":
    if os.path.exists("./lst_part_of_speech"):
        os.remove("./lst_part_of_speech.json")
        os.remove("./data/Lrate.json")
        os.remove("./data/Trate.json")
    module = DataAnalyze()
    module.saveData(".")
