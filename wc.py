# from konlpy.tag import Okt
from wordcloud import WordCloud
from collections import Counter
import matplotlib.pyplot as plt
from tkinter import *
from PIL import ImageTk, Image
import os
from kiwipiepy import *
import kiwipiepy_model

root = Tk()

root.title('WordCloudMaker - DDUALAB')
root.geometry("500x260+100+100")
root.resizable(False, False)

lbl_txt = Label(root, text="아래에 워드클라우드를 만들 문장을 넣어주세요")
lbl_txt.pack()

txt = Text(root, height=10)
txt.pack()

max_text = Label(root, text='최대 단어 개수')
max_text.place(x=80, y=160)

maxes = Entry(root, width=12)
maxes.insert(0, 70)
maxes.place(x=80, y=180)

size_text = Label(root, text='단어 크기 설정')
size_text.place(x=200, y=160)

size = Entry(root, width=12)
size.insert(0, 150)
size.place(x=200, y=180)

len_text = Label(root, text='최소 단어 길이')
len_text.place(x=320, y=160)

length = Entry(root, width=12)
length.insert(0, 1)
length.place(x=320, y=180)

# tagging = Okt()

kiwi = Kiwi()
stopwords = utils.Stopwords()

def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)


global label
label = Label(root, image = None)

def create_wordcloud():
    root.geometry("500x590+100+100")
    nouns = []
    maxx = maxes.get()
    sizes = size.get()
    lens = length.get()
    wordcloud = WordCloud(font_path="malgun",
                      max_font_size=int(sizes),
                      background_color="#FFFFFF",
                      width = 400, height = 300)
    
    txt_value = txt.get(index1 = "0.0", index2 = "end")
    # nouns = tagging.nouns(txt_value)
    # for i,v in enumerate(nouns):
    #     if len(v) < 2:
    #         nouns.pop(i)
    t = kiwi.tokenize(txt_value, stopwords=stopwords)
    for token, pos, _, _ in t:
        if pos.startswith('N') or pos.startswith('SL'):
            if len(token) >= int(lens):
                nouns.append(token)
    
    count_nouns = Counter(nouns)
    count_nouns = count_nouns.most_common(int(maxx))
    result = wordcloud.generate_from_frequencies(dict(count_nouns))
    file_name = "wordcloud.png"
    plt.tight_layout()
    plt.axis("off")
    result.to_file(resource_path(file_name))
    
    img = ImageTk.PhotoImage(Image.open(resource_path("wordcloud.png")))
    label.config(image=img)
    label.place(x=50, y=260)
    
    root.mainloop()

def clear():
    root.geometry("500x280+100+100")
    txt.delete("1.0", "end")
    label.config(image='')

btn_make = Button(root, text="생성", command = create_wordcloud)
btn_make2 = Button(root, text="초기화", command = clear)
btn_make.place(x=195, y=210)
btn_make2.place(x=245, y=210)

root.mainloop()