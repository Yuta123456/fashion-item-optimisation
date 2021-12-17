from os import times_result
import PySimpleGUI as sg
import glob
import io
from PIL import Image, ImageTk
sg.theme('DarkAmber')   # デザインテーマの設定
def get_img_data(f, maxsize=(600, 450), first=False):
    """Generate image data using PIL
    """
    print("open file:", f)
    img = Image.open(f)
    img.thumbnail(maxsize)
    if first:  # tkinter is inactive the first time
        bio = io.BytesIO()
        img.save(bio, format="PNG")
        del img
        return bio.getvalue()
    return ImageTk.PhotoImage(img)

dir_pathes = glob.glob('../images/RichWearImageSprited/**/**/')[2000:4000]
with open("anotation/finish.txt", mode="r") as f:
    finish = set([s.strip() for s in f.readlines()])
# イベントループ
image_elem = sg.Image(key="-IMAGE-")
layout = [  [sg.Text("a")],
            [image_elem],
            [sg.Button('OK'), sg.Button('NG')] ]
window = sg.Window('アノテーション', layout, finalize=True)
flg = times_result
for p in dir_pathes:
    # ウィンドウに配置するコンポーネント
    if p in finish:
        continue
    image_path = p[:-1].replace("RichWearImageSprited", "RichWear/photos") + ".jpg"
    image_elem.update(data=get_img_data(image_path, first=flg))
    flg = False
    # ウィンドウの生成
    while True:
        event, values = window.read()
        if event == sg.WIN_CLOSED:
            break
        elif event == 'OK':
            with open("anotation/path.txt", mode="a") as f:
                f.write(p + "\n")
            break
        elif event == 'NG':
            break
    with open("anotation/finish.txt", mode="a") as f:
        f.write(p + "\n")
window.close()