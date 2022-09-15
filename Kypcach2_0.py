#---Imported modules----------
import sqlite3 as dbase
import tkinter as gui
import tkinter.filedialog as fdialog
import tkinter.ttk as ttk
import tkinter.messagebox as msgbox
#---Custom classes------------
class cToy(object):
    def __init__(self, Name='Toy', Amount=0, Price=0.0, RecAge=0):
        self.Name=Name
        self.Amount=Amount
        self.Price=Price
        self.RecAge=RecAge
    def get(self):
        return (self.Name, self.Amount, self.Price, self.RecAge)

class cDatabaseEntry(gui.Toplevel):
    def __init__(self, parent, Toy, *args, **kwargs):
        gui.Toplevel.__init__(self, parent, *args, **kwargs)
        self.parent=parent
        
        self.Name=gui.StringVar()
        self.Name.set(Toy.Name)
        self.Amount=gui.IntVar()
        self.Amount.set(Toy.Amount)
        self.Price=gui.DoubleVar()
        self.Price.set(Toy.Price)
        self.RecAge=gui.IntVar()
        self.RecAge.set(Toy.RecAge)
        self.ToyNameLabel=gui.Label(self, text='Name:')
        self.ToyNameEntry=gui.Entry(self, textvariable=self.Name, justify='center')
        self.ToyAmountLabel=gui.Label(self, text='Amount:')
        self.ToyAmountEntry=gui.Entry(self, textvariable=self.Amount, justify='center')
        self.ToyPriceLabel=gui.Label(self, text='Price:')
        self.ToyPriceEntry=gui.Entry(self, textvariable=self.Price, justify='center')
        self.ToyRecAgeLabel=gui.Label(self, text='Recommended Age:')
        self.ToyRecAgeEntry=gui.Entry(self, textvariable=self.RecAge, justify='center')

        self.save_entry_changes_Btn=gui.Button(self, text='Save Entry Changes')
        self.save_entry_changes_Btn.bind('<Button-1>', lambda a: self.save_entry_changes(Toy))

        self.ToyNameLabel.grid(row=0, column=0)
        self.ToyNameEntry.grid(row=0, column=1)
        self.ToyAmountLabel.grid(row=1, column=0)
        self.ToyAmountEntry.grid(row=1, column=1)
        self.ToyPriceLabel.grid(row=2, column=0)
        self.ToyPriceEntry.grid(row=2, column=1)
        self.ToyRecAgeLabel.grid(row=3, column=0)
        self.ToyRecAgeEntry.grid(row=3, column=1)
        self.save_entry_changes_Btn.grid(row=4, column=0, columnspan=2)

    def save_entry_changes(self, Toy):
        try:
            Toy.Name=self.Name.get()
            Toy.Amount=self.Amount.get()
            Toy.Price=self.Price.get()
            Toy.RecAge=self.RecAge.get()
            self.parent.dataGrid.item(Toy, value=Toy.get())
            self.parent.changes_made=True
        except gui.TclError:
            msgbox.showerror('Type-O Error', "Please, don't enter characters in fiels for digits!")



class cSQLDatabaseApp(gui.Tk):
    def __init__(self, *args, **kwargs):
        self.connection=None
        self.cursor=None
        self.current_file=''
        self.changes_made=False
        self.database=[]

#---GUI Elements--------------        
        gui.Tk.__init__(self, *args, **kwargs)
        self.main_menu=gui.Menu(self)
        self.filemenu=gui.Menu(self.main_menu, tearoff=0)
        self.tool_bar=gui.Frame(self, bg='#A1A1A1')
        self.primaryDatabaseFrame=gui.Frame(self, bg='black', bd=1)
        self.dataGrid=ttk.Treeview(self.primaryDatabaseFrame, columns=('Name', 'Amount', 'Price', 'RecAge'))
        self.avPriceBtn=gui.Button(self.tool_bar, text='Search Average Price Of Toys For 10-year-old', command=self.search_average_price)
        self.scarceToyBtn=gui.Button(self.tool_bar, text='Search Toy With Smallest Amount', command=self.search_scarce_toy)
        self.addRowBtn=gui.Button(self.tool_bar, text='Add New Entry', command=self.add_new_entry)
#---GUI Configuration---------
        self.minsize(800, 600)
        self.configure(menu=self.main_menu)
        self.title('Toy Shop')
        self.protocol('WM_DELETE_WINDOW', self.iconify)
        self.bind_all('<Control-n>', self.create_file)
        self.bind_all('<Control-o>', self.open_file)
        self.bind_all('<Control-s>', self.save_file)
        self.bind_all('<Control-Shift-s>', self.save_file_as)
        self.primaryDatabaseFrame.grid_rowconfigure(0, weight=1)
        self.primaryDatabaseFrame.grid_columnconfigure(0, weight=1)
        self.main_menu.add_cascade(label='File', menu=self.filemenu)
        self.filemenu.add_command(label='New', command=self.create_file, accelerator='Ctrl+N')
        self.filemenu.add_command(label='Open', command=self.open_file, accelerator='Ctrl+O')
        self.filemenu.add_separator()
        self.filemenu.add_command(label='Save', command=self.save_file, accelerator='Ctrl+S')
        self.filemenu.add_command(label='Save As', command=self.save_file_as, accelerator='Ctrl+Shift+S')
        self.filemenu.add_separator()
        self.filemenu.add_command(label='Exit', command=self.exit_app)
        self.dataGrid.heading('#0', text='ID')
        self.dataGrid.column('#0', width=50, anchor='center')
        self.dataGrid.heading('Name', text='Name')
        self.dataGrid.column('Name', width=200, anchor='center')
        self.dataGrid.heading('Amount', text='Amount')
        self.dataGrid.column('Amount', width=100, anchor='center')
        self.dataGrid.heading('Price', text='Price')
        self.dataGrid.column('Price', width=150, anchor='center')
        self.dataGrid.heading('RecAge', text='Recommended Age')
        self.dataGrid.column('RecAge', width=150, anchor='center')
        self.dataGrid.bind('<Double-Button-1>', lambda a: self.call_entry())
        self.dataGrid.bind('<Delete>', lambda a: self.delete_entry())

        self.tool_bar.pack(side='top', fill='x')
        self.primaryDatabaseFrame.pack(side='bottom', fill='both', expand=True)
        self.dataGrid.pack(side='bottom', fill='both', expand=True)
        self.avPriceBtn.pack(side='left')
        self.scarceToyBtn.pack(side='left')
        self.addRowBtn.pack(side='left')
#---GUI functions-------------
    def open_file(self, event):
        of=fdialog.askopenfilename(initialdir='/', title='Open File', filetypes=(('SQLite Database','*.sqlite'), ('All Files', '*.*')))
        if len(of)>0:
            if len(self.current_file)>0 and self.changes_made:
                answer=msgbox.askquestion('Confirmation', 'Unsaved changes will be lost. Are you sure?')
                if answer=='yes':
                    self.connection.rollback()
                    self.connection.close()
                    self.current_file=of
                    self.connect_database(self.current_file)
                    self.database.clear()
            else:
                self.current_file=of
                self.connect_database(self.current_file)
            table_name='ToyShop'
            self.cursor.execute('SELECT * FROM {tn}'.format(tn=table_name))
            all_rows=self.cursor.fetchall()
            for toy in all_rows:
                self.database.append(cToy(toy[1:]))
            
    def create_file(self, event):
        cf=fdialog.asksaveasfilename(initialdir='/', title='Create File', filetypes=(('SQLite Database','*.sqlite'), ('All Files', '*.*')))
        if len(cf)>0:
            if not cf[-7:]=='.sqlite':                
                cf=cf+'.sqlite'
            if len(self.current_file)>0:
                answer=msgbox.askquestion('Confirmation', 'Unsaved changes will be lost. Are you sure?')
                if answer=='yes':
                    self.connection.rollback()
                    self.connection.close()
                    self.current_file=cf
                    self.connect_database(self.current_file)
                    self.create_table()
                    self.database.clear()
            else:
                self.current_file=cf
                self.connect_database(self.current_file)
                self.create_table()

    def save_file(self, event):
        if len(self.current_file)>0:
            self.save_database()
        else:
            msgbox.showerror('Save Error', "You don't work with any databases right now")

    def save_file_as(self, event):
        if len(self.current_file)>0:
            cf=fdialog.asksaveasfilename(initialdir='/', title='Save File As', filetypes=(('SQLite Database','*.sqlite'), ('All Files', '*.*')))
            if not cf[-7:]=='.sqlite':                
                cf=cf+'.sqlite'
            self.connection.rollback()
            self.connection.close()
            self.current_file=cf
            self.connect_database(self.current_file)
            self.create_table()
            self.save_database()
        else:
            msgbox.showerror('Save Error', "You don't work with any databases right now")

    def exit_app(self):
        if self.changes_made:
            answer=msgbox.askquestion('Quit', 'Unsaved changes will be lost. Are you sure?')
            if answer=='yes':
                self.exit()
        else:
            self.exit()

    def focusCheck(self):
        entryIndex=self.dataGrid.focus()
        if entryIndex=='':
            return False
        else:
            return True

    def call_entry(self):
        if self.focusCheck():
            cDatabaseEntry(self, self.database[self.dataGrid.index(self.dataGrid.focus())])

    def delete_entry(self):
        if self.focusCheck():
            self.changes_made=True
            self.database.pop(self.dataGrid.index(self.dataGrid.focus()))
            self.delete_row(self.dataGrid.index(self.dataGrid.focus()))
            self.dataGrid.delete(self.dataGrid.focus())
            for i in range(len(self.database)):
                self.dataGrid.item(self.database[i], text=str(i+1))

    def add_new_entry(self):
        if len(self.current_file)>0:
            self.database.append(cToy())
            self.dataGrid.insert('', 'end', self.database[-1], text=str(len(self.dataGrid.get_children())+1), values=self.database[-1].get())
            self.changes_made=True
        else:
            msgbox.showerror('Save Error', "You don't work with any databases right now")

    def search_average_price(self, event):
        if len(self.current_file)>0:
            msgbox.showinfo('Average Price Of Toys For 10-year-old', 'Average Price Of Toys For 10-year-old: '+str(averPriceFor10()))
        else:
            msgbox.showerror('Action Error', "You don't work with any databases right now")

    def search_scarce_toy(self, event):
        if len(self.current_file)>0:
            output_entry(self.database[scarceToy()])
            dataGrid.focus(self.database[scarceToy()])
            dataGrid.selection_set(self.database[scarceToy()])
        else:
            msgbox.showerror('Action Error', "You don't work with any databases right now")
#---Custom functions----------
    def averPriceFor10(self):
        avPrice=0
        toy10=0
        for toy in self.database:
            if toy.RecAge<=10:
                avPrice+=toy.Price
                toy10+=1
        avPrice=avPrice/toy10
        return avPrice

    def scarceToy(self):
        minAmountInd=0
        for toyInd in range(len(self.database)):
            if ToyShop[toyInd].Amount<ToyShop[minAmountInd].Amount:
                minAmountInd=toyInd
        return minAmountInd
#---SQLite functions----------
    def connect_database(self, sqlite_file):
        self.connection=dbase.connect(sqlite_file)
        self.cursor=self.connection.cursor()

    def save_database(self):
        for i in range(len(self.database)):
            add_row(self.database[i], i)
        self.connection.commit()
        self.changes_made=False

    def create_table(self):
        try:
            table_name='ToyShop'
            self.cursor.execute('CREATE TABLE {tn} (ID INTEGER PRIMARY KEY, Name TEXT, Amount INTEGER, Price REAL, Recommended_Age INTEGER)'.format(tn=table_name))
        except dbase.OperationalError:
            pass

    def add_row(self, toy, index):
        table_name='ToyShop'
        self.cursor.execute('INSERT OR REPLACE INTO {tn} (ID, Name, Amount, Price, Recommended_Age) VALUES ({toy_id}, {toy_name}, {toy_amount}, {toy_price}, {toy_rec_age})'\
                       .format(tn=table_name, toy_id=i, toy_name=toy.Name, toy_amount=toy.Amount, toy_price=toy.Price, toy_rec_age=toy.RecAge))

    def delete_row(self, row_ID):
        table_name='ToyShop'
        self.cursor.execute('DELETE FROM {tn} WHERE ID={toy_id}'.format(tn=table_name, toy_id=row_ID))
        for i in range(row_ID, len(self.database)):
            self.cursor.execute('UPDATE {tn} SET ID={toy_id} WHERE ID={old_id}'.format(tn=table_name, toy_id=i, old_id=i+1))


if __name__=='__main__':
    root=cSQLDatabaseApp()
    root.mainloop()
