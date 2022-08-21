import csv
import pandas as pd

def output_trimmer(filename):
    original = pd.read_csv(filename)
    #original = original.reset_index()
    index_to_trim_list = [-1]
    prev_classification_num = 0
    for index, row in original.iterrows():
        if index != 0:
            if row['classification'] < prev_classification_num:
                index_to_trim_list.insert(0, index - 1)
        prev_classification_num = row['classification']
    index_to_trim_list.insert(0, original.shape[0] - 1)
    #print(original.head(10))

    trimmed = original.copy()
    for i in range(len(index_to_trim_list) - 1):
        trimmed.drop(index_to_trim_list[i], inplace=True)
        trim_start = index_to_trim_list[i + 1] + 1
        trim_end = index_to_trim_list[i] - 100
        #print(trim_start)
        #print(trim_end)
        trimmed.drop(range(trim_start, trim_end), inplace=True)
    #print(trimmed.shape[0])
    #print(trimmed.head(5))
    trimmed.reset_index(drop=True, inplace=True)
    trimmed.reset_index(inplace=True)
    #print(trimmed.head(5))
    trimmed["classification"] = trimmed["index"] + 1
    trimmed.drop(columns=["index"], inplace=True)
    trimmed.to_csv(filename[:-4] + "_trimmed.csv", index=False)
    print(trimmed.head(5))

if __name__ == "__main__":
    output_trimmer("RCNN_L1Coady_output.csv")