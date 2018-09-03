from load_functions import *

path="/.../ALL_till_31_8_2018/" # folder with .json files
assert path[-1] == '/'

sorted_keywords_list, keywords_list = all_keywords(path,demo=False)

joined_keywords = ""
for k in sorted_keywords_list:
    joined_keywords += str(k[0])+" : "+str(k[1])+"\n"

#joined_keywords = "\n".join(keywords_list)
print(joined_keywords[0:500])
save_to_txt_file(joined_keywords, "all_keywords.txt", force_cleanup=False)
