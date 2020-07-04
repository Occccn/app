import tkinter as tk
import tkinter.ttk as ttk
import datetime
import sqlite3
import pandas as pd
import japanize_matplotlib
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from matplotlib.backends.backend_tkagg  import FigureCanvasTkAgg
from tkinter import font

class Application(tk.Frame):
    def __init__(self, master=None):
        ##frameクラスを継承、frameクラスの初期化,引数に持ってきたmaster(メインウインドウ)に配置
        super().__init__(master,height = 500,width = 500,bg='mint cream' , relief='sunken')
        self.master = master
        self.master.geometry("500x500")
        self.grid(column=0, row=0, sticky=tk.NSEW, padx=5, pady=5)
        self.title_font = font.Font(family='メイリオ', size = 20 , weight='bold')
        self.create_widgets()

    def register_sql(self):
        date = '"' + self.day_entry.get() + '"'
        weight = self.weight_entry.get()
        abura = self.abura_entry.get()
        try:
            if len(weight) != 0:
                weight = float(weight)
            else:
                weight = 'NULL'

            if len(abura) != 0:
                abura = float(abura)
            
            else:
                abura = 'NULL'

            try:
                c.execute('INSERT INTO kenco VALUES({} , {} , {})'.format(date , weight ,abura))
                conn.commit()
                print('登録完了')
            except:
                print("登録できませんでした。")

        except:
            print('体重または体脂肪率の入力が数値ではありません。')


    def plot(self , day1 , day2 , target):
        dbname = 'kenco.db'
        conn = sqlite3.connect(dbname)
        df = pd.read_sql('SELECT * FROM kenco WHERE date BETWEEN "{0}" AND "{1}" ;'.format(day1 , day2), conn)
        df = df.dropna()
        df['date'] = pd.to_datetime(df['date'])
        df = df.sort_values(by='date')
        fig = plt.figure(figsize=(10,10))
        ax = fig.add_subplot(111)
        print(df['weight'])
        if target == '体重':
            ax.plot(df['date'] , df['weight'] , label = '生データ')
            if len(df) >= 7:
                df['rolling_mean'] = df['weight'].rolling(7).mean()
                ax.plot(df['date'] , df['rolling_mean'] , label = '一週間レベルでみた変化')
            if len(df) >= 30:
                df['rolling_mean'] = df['weight'].rolling(7).mean()
                ax.plot(df['date'] , df['rolling_mean'] , label = '一月でみた変化')     
            ax.set_ylabel('{0} kg'.format(target))
        else:
            ax.plot(df['date'] , df['abura'] , label = '生データ')
            if len(df) >= 7:
                df['rolling_mean'] = df['abura'].rolling(7).mean()
                ax.plot(df['date'] , df['rolling_mean'] , label = '一週間レベルでみた変化')
            if len(df) >= 30:
                df['rolling_mean'] = df['abura'].rolling(7).mean()
                ax.plot(df['date'] , df['rolling_mean'] , label = '一月でみた変化')            
            ax.set_ylabel('{0} %'.format(target))
        ax.legend()
        ax.set_title('line plot')

        ax.xaxis.set_major_formatter(mdates.DateFormatter('%m/%d'))
        return fig

    def get_date_list(self):
        dbname = 'kenco.db'
        conn = sqlite3.connect(dbname)
        c = conn.cursor()
        result = c.execute('SELECT date FROM kenco ;')
        combo_list = []
        for i in result:
            combo_list.append(i)
        return combo_list


    def create_plot_win(self):
        self.plot_win = tk.Toplevel(self.master , height = 1000,width = 500,bg='mint cream')
        self.plot_win.title("推移結果")
        self.plot_win.geometry("1000x500")
        self.create_plot_widgets()

    def create_plot_widgets(self):
        day1 = self.init_combo.get()
        day2 = self.fin_combo.get()
        target = self.combo.get()
        fig = self.plot(day1 , day2 , target)
        self.plot_win.plot_canvas = FigureCanvasTkAgg(fig,self.plot_win)
        self.plot_win.plot_canvas.draw()
        self.plot_win.plot_canvas.get_tk_widget().pack()


    def create_widgets(self):
        #各ウィジェットはself(frameクラスを継承したもの)に配置
        self.day = datetime.datetime.now()
        self.day = self.day.strftime("%Y-%m-%d")

        self.day_label = tk.Label(self)
        self.day_label['text'] = "日付"
        self.day_label['font']= 20
        self.day_label['background']='gray91'
        self.day_label.place(x = 125 ,y = 20)

        self.weight_label = tk.Label(self)
        self.weight_label['text'] = "体重"
        self.weight_label['font']= 20
        self.weight_label['background']='gray91'
        self.weight_label.place(x = 125 ,y = 50)   

        self.abura_label = tk.Label(self)
        self.abura_label['text'] = "体脂肪率"
        self.abura_label['font']= 20
        self.abura_label['background']='gray91'
        self.abura_label.place(x = 105 ,y = 80)

        #データ登録ボタン設定
        self.input_button = tk.Button(self)
        self.input_button["text"] = "データ登録"
        self.input_button["command"] =  self.register_sql
        self.input_button.place(x = 190 ,y = 130, relwidth=0.3 )

        #Entry設定(日付)
        self.day_entry = tk.Entry(self,font=("",12),justify="center",width=20)
        self.day_entry.insert(0,self.day)
        self.day_entry.place(x = 175 ,y = 20)

        #Entry設定(体重)
        self.weight_entry = tk.Entry(self,font=("",12),justify="center",width=20)
        self.weight_entry.place(x = 175 ,y = 50)


        #Entry設定(体脂肪率)
        self.abura_entry = tk.Entry(self,font=("",12),justify="center",width=20)
        self.abura_entry.place(x = 175 ,y = 80)

        #閉じるボタン設定
        self.quit = tk.Button(self, text="閉じる", fg="red",command=self.master.destroy)
        self.quit.pack(side="bottom")

        #体重、体脂肪率選択
        self.combo = ttk.Combobox(self, state='readonly')
        self.combo["values"] =["体重","体脂肪率"]
        self.combo.current(0)
        self.combo.place(x = 190 ,y = 370, relwidth=0.3 )

        self.range_label = tk.Label(self)
        self.range_label['text'] = '期間'
        self.range_label['background']='gray91'
        self.range_label.place(x = 50 , y = 340)

        self.init_combo = ttk.Combobox(self, state='readonly')
        self.init_combo["values"] = self.get_date_list()
        self.init_combo.place(x = 100 , y = 338 ,relwidth=0.3 )

        self.s_label = tk.Label(self , font = self.title_font , bg='mint cream')
        self.s_label['text'] = '〜'
        self.s_label.place(x = 250 , y = 338)

        self.fin_combo = ttk.Combobox(self, state='readonly')
        self.fin_combo["values"] = self.get_date_list()
        self.fin_combo.place(x = 300 , y = 338 ,relwidth=0.3 )
    

        #出力ボタン設定
        self.input_button = tk.Button(self)
        self.input_button["text"] = "推移を表示"
        self.input_button["command"] = self.create_plot_win
        self.input_button.place(x = 190 ,y = 400, relwidth=0.3 )

dbname = 'kenco.db'
conn = sqlite3.connect(dbname)
c = conn.cursor()
ddl = 'CREATE TABLE if not exists kenco(date NOT NULL, weight REAL , abura REAL);'
#sqlの発行
c.execute(ddl)

root = tk.Tk()
root.rowconfigure(0, weight=1)
root.columnconfigure(0, weight=1)

app = Application(master=root)
app.mainloop()