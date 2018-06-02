from xpinyin import Pinyin


def get_py(words):
result =[]
p = Pinyin()
for i in words.split('\n'):
	# 生成拼音
	a = p.get_pinyin(i,show_tone_marks=True).replace('-',' ')
	result.append(a)
	result.append(i)
	
