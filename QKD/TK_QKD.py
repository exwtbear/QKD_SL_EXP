# 如果Alice和Bob公開比較𝑛他們發現分歧並識別出Eve存在的機率為Alice和Bob需要比較𝑛=72關鍵位。
import random
import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
from PIL import Image, ImageTk

#定義基數 ⬆ ➡ ⬈ ⬊( ⬅ ⬇ ⬉ ⬋)
basis_tuple = (('0°', '90°'), 
               ('45°', '135°'))#前為⬆ ➡後為⬈ ⬊

#隨機產生偏振片
def genRandBases(n) -> list:
    return [basis_tuple[random.randint(0,1)] for _ in range(n)]

#將偏振片角度以圖示的方式顯示出來
def basis_to_icon(basis_list):
    return ['十' if basis == ('0°', '90°') else 'X' for basis in basis_list]

#產出光子偏振方向
def genPolarizations(bit_list, basis_list) -> list:
    return [basis_list[i][bit_list[i]] for i in range(len(bit_list))]

#將光子偏振方向以箭頭表示
def pol_to_dir(pol_list) -> list:
    dir_list = []
    for deg in pol_list:
        match deg:
            case '0°':
                dir_list.append('⬆')
            case '45°':
                dir_list.append('⬈')
            case '90°':
                dir_list.append('⮕')
            case '135°':
                dir_list.append('⬊')
    return dir_list

#產出觀測的結果
def genMeasurements(A_pol_list, B_basis_list) -> list:#前放被觀察的偏振，後放觀察者的偏振片狀態
    return [A_pol_list[i] if A_pol_list[i] in B_basis_list[i] else random.choice(B_basis_list[i]) for i in range(len(A_pol_list))]

#公開討論哪些偏振片使用的一樣
def public_discussion(A_basis, B_basis) -> list:
    return [i for i in range(len(A_basis)) if A_basis[i] == B_basis[i]]

#算出Bob所獲得的金鑰
def getSecretKey(Bob_measured, same_basis_idx) -> list:
    zero_set = [basis[0] for basis in basis_tuple]
    return [0 if Bob_measured[idx] in zero_set else 1 for idx in same_basis_idx]

#找出錯誤的index值
def findIncorrect(bit_list, same_basis_idx, secret_key) -> list:
    incorrect = []
    i = 0
    for idx in same_basis_idx:
        if bit_list[idx] != secret_key[i]:
            incorrect.append(idx)
        i += 1
    return incorrect

#驗證Bob得到的金鑰是否與正確答案Alice的一樣
def verify_key(bit_list, secret_key, same_basis_idx, rp, root) -> None:
    correct_key = [bit_list[idx] for idx in same_basis_idx]
    strSecretKey = "".join(map(str, secret_key))
    if same_basis_idx:
        if secret_key == correct_key:
            ttk.Label(root, text=f"沒有人竊聽，金鑰為: {strSecretKey}", background='#ffd700', font=('標楷體',24,'bold')).grid(sticky='snw')
            if rp == 'yes':
                ttk.Label(root, text='雖然這邊驗證系統的結果為無人竊聽，但很明顯這是錯的!由於選用的bit數不夠多導致仍有機率會檢測不出來，\n但只要將bit數提升至72，檢測出竊聽者的機率就會來到0.999999999', background='#C07AB8', font=('標楷體',16,'bold')).grid(sticky='snw')
        else:
            strCorrectKey = "".join(map(str, correct_key))
            ttk.Label(root, text=f"有人竊聽! 正確金鑰為: {strCorrectKey}", background='#ffd700', font=('標楷體',24,'bold')).grid(sticky='snw')
            ttk.Label(root, text=f"被干擾後得到的金鑰為: {strSecretKey}", background='#ffd700', font=('標楷體',24,'bold')).grid(sticky='snw')
            ttk.Label(root, text=f"故須放棄此金鑰，重新產生一組", background='#C07AB8', font=('標楷體',24,'bold')).grid(sticky='snw')
    else:
        ttk.Label(root, text='所選擇的Bit數不夠多，所以也沒有同時使用相同種類的偏振片，故無法產生有效金鑰', background='#C07AB8', font=('標楷體',20,'bold')).grid(sticky='snw')

shotdown = False#控制有沒有突然關閉程式
def main():
    root = tk.Tk()
    root.title('QKD模擬實驗')
    root.geometry('600x450')
    root.resizable(False, False) 

    tk_str = tk.StringVar()
    #按鈕的獲取輸入及跳轉視窗的指令
    def get_and_clear():
        global n
        #Random bit有幾位
        try:
            n = int(tk_str.get())
        except:
            messagebox.showerror('Error', '請輸入正整數!')
        else:
            entry.delete(0, 'end')
            root.destroy()
    #按下Enter鍵也能觸發
    def enter_event(event):
        global n
        #Random bit有幾位
        try:
            n = int(tk_str.get())
        except:
            messagebox.showerror('Error', '請輸入正整數!')
        else:
            entry.delete(0, 'end')
            root.destroy()
    #偵測使用者有沒有想提前結束程式關閉視窗
    def on_closing():
        if messagebox.askokcancel('Quit', '確定要關閉嗎?'):
            global shotdown
            shotdown = True
            root.destroy()
    
    #導入圖片
    photo = tk.PhotoImage(file="wd_bg.png")
    
    canvas = tk.Canvas(root, width=600, height=450, highlightthickness=0)   # 放入標籤
    canvas.create_image(300, 225, image=photo, )
    canvas.pack()
    
    label = tk.Label(root, text='請輸入要幾個Random bit?', font=('標楷體',24,'bold'))   # 放入標籤
    
    label.pack()
    canvas.create_window(300, 160, window=label)

    entry = tk.Entry(root, textvariable=tk_str, font=('標楷體',20,'bold'))   # 放入輸入欄位 ( 變數為 tk_str )
    entry.pack()
    canvas.create_window(300, 210, width=150, height=25, window=entry)
    entry.delete(0, 'end')
    btn1 = tk.Button(root, text='確認', command=get_and_clear, font=('標楷體',16,'bold'))   # 放入顯示按鈕
    btn1.pack()
    canvas.create_window(300, 260, width=50, height=25, window=btn1)
    entry.bind('<Return>', enter_event)#偵測輸入Return事件
    root.protocol('WM_DELETE_WINDOW', on_closing)
    root.mainloop()

    #如果中途結束程式，後面就不需要執行
    if not shotdown:
        #訊問要不要有人從中監聽
        response = messagebox.askquestion('訊問要不要有人從中攔截監聽並重新發送', '建立金鑰的過程中是否要有人從中監聽?')

        # 創建n個由1, 0所組成的Random bit list
        Alice_bit_list = [random.randint(0,1) for _ in range(n)]

        #生成n個Alice的偏振片模板
        Alice_basis_list = genRandBases(n)

        #生成偏振方向
        Alice_pol_list = genPolarizations(Alice_bit_list, Alice_basis_list)

        #生成n個Bob的偏振片模板
        Bob_basis_list = genRandBases(n)
        
        if response == 'no':
            #只有兩人產出金鑰的過程
            #Bob去測量Alice的結果
            Bob_measured_list = genMeasurements(Alice_pol_list, Bob_basis_list)
            data_names = ["Bit List: ", "Alice的偏振片模板: ", "Alice的偏振方向: ", "Bob的偏振片模板: ", "Bob測量出來的結果: "]
            datas = [Alice_bit_list, basis_to_icon(Alice_basis_list), pol_to_dir(Alice_pol_list), basis_to_icon(Bob_basis_list), pol_to_dir(Bob_measured_list)]
        else:
            #有第三者偷偷攔截監聽並重新發送
            #生成Eve的偏振片模板
            Eve_basis_list = genRandBases(n)
            
            #第三者Eve進行觀測
            Eve_measured_list = genMeasurements(Alice_pol_list, Eve_basis_list)

            #Eve將自己觀測後的結果丟給Bob觀測
            Bob_measured_list = genMeasurements(Eve_measured_list, Bob_basis_list)
            data_names = ["Bit List: ", "Alice的偏振片模板: ", "Alice的偏振方向: ", "Eve的偏振片模板: ", "Eve測量出來的結果: ",  "Bob的偏振片模板: ", "Bob測量出來的結果: "]
            datas = [Alice_bit_list, basis_to_icon(Alice_basis_list), pol_to_dir(Alice_pol_list), basis_to_icon(Eve_basis_list), pol_to_dir(Eve_measured_list), basis_to_icon(Bob_basis_list), pol_to_dir(Bob_measured_list)]
            
        #得出使用一樣的偏振片是哪些
        same_basis_index = public_discussion(Alice_basis_list, Bob_basis_list)

        #算出Bob測量出來的金鑰
        secret_key = getSecretKey(Bob_measured_list, same_basis_index)

        incorrect_list = findIncorrect(Alice_bit_list, same_basis_index, secret_key)

        #顯示結果視窗
        root2 = tk.Tk()
        root2.title('結果輸出')
        root2.geometry('1440x600')
        root2.maxsize(1440, 720)
        root2.minsize(0, 480)

        frame = ttk.Frame(root2)
        frame.grid(row=0, column=0, sticky="nsew")

        canvas = tk.Canvas(frame)
        #水平的滾動軸
        scrollbar = ttk.Scrollbar(frame, orient='horizontal', command=canvas.xview)
        canvas.configure(xscrollcommand=scrollbar.set)
        content_frame = ttk.Frame(canvas)
        content_frame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))

        text_size = 20
        ttk.Label(content_frame, text=' ', font=('標楷體',text_size)).grid(column=0, row=0)
        txt_count = 0
        #依據不同角色分顏色
        for txt in data_names:
            if 'Alice' in txt:
                ttk.Label(content_frame, text=txt, font=('標楷體',18,'bold'), background='#FFC0CB').grid(column=0, row=txt_count+1)
            elif 'Eve' in txt:
                ttk.Label(content_frame, text=txt, font=('標楷體',18,'bold'), background='#99FF4D').grid(column=0, row=txt_count+1)
            elif 'Bob' in txt:
                ttk.Label(content_frame, text=txt, font=('標楷體',18,'bold'), background='#FFCC00').grid(column=0, row=txt_count+1)
            else:
                ttk.Label(content_frame, text=txt, font=('標楷體',18,'bold'), background='#AAAAFF').grid(column=0, row=txt_count+1)
            txt_count += 1

        #顯示index編號
        for i in range(n):
            if i not in same_basis_index:
                ttk.Label(content_frame, text='  $'+str(i)+'  ', font=('標楷體',text_size,'bold')).grid(column=i+2, row=0)
            else:
                ttk.Label(content_frame, text='  $'+str(i)+'  ', background='#00ffff', font=('標楷體',text_size,'bold')).grid(column=i+2, row=0)

        #顯示資料
        data_count = 0
        for data in datas:
            for i in range(n):
                #EXPO M字體能夠更好的呈現符號
                if data[i] == '十' or data[i] == 'X':
                    ttk.Label(content_frame, text=data[i], font=('EXPO M',text_size,'bold')).grid(column=i+2, row=data_count+1)
                #標記有錯誤的結果
                elif i in incorrect_list and data[i] in ['⬆','⬈','⮕','⬊']:
                    ttk.Label(content_frame, text=data[i], font=('Arial',text_size,'bold'), background='red').grid(column=i+2, row=data_count+1)
                else:
                    ttk.Label(content_frame, text=data[i], font=('Arial',text_size,'bold')).grid(column=i+2, row=data_count+1)    
            data_count += 1
        
        #印出公開討論後的index編號有哪些
        ttk.Label(content_frame, text='公開討論後得出使用相同\n的偏振片的index編號是: ', background='#1AFD9C', font=('標楷體',text_size-4,'bold')).grid(column=0, row=txt_count+1)
        i = 0
        for idx_str in map(str, same_basis_index):
            ttk.Label(content_frame, text='{'+idx_str+'}', font=('Arial',text_size,'bold'), background='#1AFD9C').grid(column=i+2, row=txt_count+1)
            i += 1

        root2.columnconfigure(0, weight=1)
        root2.rowconfigure(0, weight=1)
        frame.columnconfigure(0, weight=1)
        frame.rowconfigure(0, weight=1)

        canvas.create_window((0, 0), window=content_frame, anchor="nw")
        canvas.grid(row=0, column=0, sticky="nsew")
        scrollbar.grid(row=1, column=0, sticky="ew")

        #滑鼠滾輪事件
        def _on_mousewheel(event):
            canvas.xview_scroll(int(-1 * (event.delta / 120)), "units")

        canvas.bind_all("<MouseWheel>", _on_mousewheel)

        img = Image.open('basis_sample.png')        # 開啟圖片
        tk_img = ImageTk.PhotoImage(img)    # 轉換為 tk 圖片物件
        ttk.Label(root2, image=tk_img).grid(sticky='snw')  # 在 Lable 中放入圖片

        #驗證Bob所得出的金鑰是否與答案一樣以說明是否有被第三者監聽
        verify_key(Alice_bit_list, secret_key, same_basis_index, response, root2)

        root2.mainloop()

if __name__ == '__main__' :
    main()

# Basis | 0 | 1 |
# ------+---+-----
#   十  | ⬆ | ➡ |
# ------+---+-----
#   X   | ⬈ | ⬊ |