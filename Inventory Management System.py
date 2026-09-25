import tkinter as tk
import tkinter.messagebox
from tkinter import ttk

datafile='Inventorydata.txt'
inventory={}


def save_inventory():
    file=open(datafile,'w')
    for itemid in inventory:
        details=inventory[itemid]
        file.write(itemid+'\n')
        file.write(details['name']+'\n')
        file.write(str(details['qty'])+'\n')
        file.write(str(details['price'])+'\n')
        file.write(details['category']+'\n')
    file.close()

def load_inventory():
    global inventory
    file=open(datafile,'a')
    file.close()
    file=open(datafile,'r')
    inventory={}
    while True:
        itemid=file.readline()
        if itemid=='':
            break
        name=file.readline()
        qty=file.readline()
        price=file.readline()
        category=file.readline()
        itemid=itemid[:-1]
        name=name[:-1]
        qty=qty[:-1]
        price=price[:-1]
        category=category[:-1]
        inventory[itemid]={'name':name,'qty':int(qty),'price':float(price),'category':category}
    file.close()


def sort_key_id(pair):
    return pair[0]

def sort_key_name(pair):
    return pair[1]['name'].lower()

def sort_key_qty(pair):
    return pair[1]['qty']


def clear_fields():
    e1.delete(0,'end')
    e2.delete(0,'end')
    e3.delete(0,'end')
    e4.delete(0,'end')

def showitems():
    listbox.delete(0,'end')
    items_list=list(inventory.items())

    sort_choice=sort_var.get()
    if sort_choice=='name':
        items_list=sorted(items_list,key=sort_key_name)
    elif sort_choice=='qty':
        items_list=sorted(items_list,key=sort_key_qty)
    else:
        items_list=sorted(items_list,key=sort_key_id)

    for pair in items_list:
        itemid=pair[0]
        details=pair[1]
        if low_stock_var.get()==1 and details['qty']>=5:
            continue
        row=itemid+' | '+details['name']+' | '+str(details['qty'])+' | '+str(details['price'])+' | '+details['category']
        listbox.insert('end',row)


def add_item():
    itemid=e1.get()
    name=e2.get()
    qty=e3.get()
    price=e4.get()
    category=category_box.get()

    if itemid=='' or name=='' or qty=='' or price=='' or category=='':
        tkinter.messagebox.showerror('Error','Please fill in all the fields')
        return

    if itemid in inventory:
        old_qty=inventory[itemid]['qty']
        new_qty=old_qty+int(qty)
        inventory[itemid]={'name':name,'qty':new_qty,'price':float(price),'category':category}
        tkinter.messagebox.showinfo('Updated','Item already existed, quantity restocked')
    else:
        inventory[itemid]={'name':name,'qty':int(qty),'price':float(price),'category':category}

    save_inventory()
    showitems()
    clear_fields()

def dlt_items():
    itemid=e1.get()
    if itemid in inventory:
        del inventory[itemid]
        save_inventory()
        showitems()
        clear_fields()
    else:
        tkinter.messagebox.showerror('Error','Item ID not found')

def dlt_all():
    inventory.clear()
    save_inventory()
    showitems()
    clear_fields()

def search_item():
    kw=e1.get()
    listbox.delete(0,'end')
    for itemid in inventory:
        details=inventory[itemid]
        if kw==itemid or kw.lower() in details['name'].lower():
            row=itemid+' | '+details['name']+' | '+str(details['qty'])+' | '+str(details['price'])+' | '+details['category']
            listbox.insert('end',row)

def show_about():
    tkinter.messagebox.showinfo('About','Inventory Management System\nBy Caroline Giju-09')

def show_instructions():
    tkinter.messagebox.showinfo('Instructions',
        'Add: fill all fields and click Add (same ID restocks quantity)\n'
        'Delete: type an Item ID and click Delete\n'
        'Search: type an ID or part of a name, then click Search\n'
        'Delete all: clears every item\n'
        'Use the View menu to sort or filter the list')


bgcolor='whitesmoke'
hcolor='darkslategray'
labelfont=('Arial',10)
hfont=('Arial',12,'bold')
efont=('Arial',10)
bfont=('Arial',10,'bold')
listfont=('Courier',10)

top=tk.Tk()
top.title('Inventory Management System')
top.configure(bg=bgcolor)

sort_var=tk.StringVar(value='id')
low_stock_var=tk.IntVar(value=0)


menubar=tk.Menu(top)

filemenu=tk.Menu(menubar,tearoff=0)
filemenu.add_command(label='Refresh',command=showitems)
filemenu.add_command(label='Delete All',command=dlt_all)
filemenu.add_separator()
filemenu.add_command(label='Exit',command=top.destroy)
menubar.add_cascade(label='File',menu=filemenu)

editmenu=tk.Menu(menubar,tearoff=0)
editmenu.add_command(label='Clear Fields',command=clear_fields)
menubar.add_cascade(label='Edit',menu=editmenu)

viewmenu=tk.Menu(menubar,tearoff=0)
viewmenu.add_radiobutton(label='Sort by ID',variable=sort_var,value='id',command=showitems)
viewmenu.add_radiobutton(label='Sort by Name',variable=sort_var,value='name',command=showitems)
viewmenu.add_radiobutton(label='Sort by Quantity',variable=sort_var,value='qty',command=showitems)
viewmenu.add_separator()
viewmenu.add_checkbutton(label='Show only low stock',variable=low_stock_var,command=showitems)
menubar.add_cascade(label='View',menu=viewmenu)

helpmenu=tk.Menu(menubar,tearoff=0)
helpmenu.add_command(label='Instructions',command=show_instructions)
helpmenu.add_command(label='About',command=show_about)
menubar.add_cascade(label='Help',menu=helpmenu)

top.config(menu=menubar)


header_frame=tk.Frame(top,bg=bgcolor)
header_frame.grid(row=0,column=0,pady=(10,5))

header=tk.Label(top,text='Name: Caroline Giju'+'\nRoll No:09'+'\nCourse:BCA AI-A',width=45,font=labelfont,bg=bgcolor)
header.grid(row=0,column=0)


input_frame=tk.Frame(top,bg=bgcolor)
input_frame.grid(row=1,column=0,padx=10,pady=5)

l1=tk.Label(input_frame,text='Item ID',font=labelfont,bg=bgcolor)
e1=tk.Entry(input_frame,width=15,font=efont)
l1.grid(row=0,column=0,padx=8,pady=6)
e1.grid(row=0,column=1,padx=8,pady=6)

l2=tk.Label(input_frame,text='Name',font=labelfont,bg=bgcolor)
e2=tk.Entry(input_frame,width=15,font=efont)
l2.grid(row=0,column=2,padx=8,pady=6)
e2.grid(row=0,column=3,padx=8,pady=6)

l3=tk.Label(input_frame,text='Quantity',font=labelfont,bg=bgcolor)
e3=tk.Spinbox(input_frame,from_=0,to=100000,width=13,font=efont)
l3.grid(row=1,column=0,padx=8,pady=6)
e3.grid(row=1,column=1,padx=8,pady=6)

l4=tk.Label(input_frame,text='Price',font=labelfont,bg=bgcolor)
e4=tk.Entry(input_frame,width=15,font=efont)
l4.grid(row=1,column=2,padx=8,pady=6)
e4.grid(row=1,column=3,padx=8,pady=6)

l5=tk.Label(input_frame,text='Category',font=labelfont,bg=bgcolor)
category_box=ttk.Combobox(input_frame,width=13,values=['Stationery','Electronics','Grocery','Other'],state='readonly')
l5.grid(row=2,column=0,padx=8,pady=6)
category_box.grid(row=2,column=1,padx=8,pady=6)
category_box.set('Stationery')


controls_frame=tk.Frame(top,bg=bgcolor)
controls_frame.grid(row=2,column=0,pady=5)

tk.Label(controls_frame,text='Sort by:',font=labelfont,bg=bgcolor).grid(row=0,column=0,padx=5)

tk.Radiobutton(controls_frame,text='ID',variable=sort_var,value='id',bg=bgcolor,command=showitems).grid(row=0,column=1)
tk.Radiobutton(controls_frame,text='Name',variable=sort_var,value='name',bg=bgcolor,command=showitems).grid(row=0,column=2)
tk.Radiobutton(controls_frame,text='Quantity',variable=sort_var,value='qty',bg=bgcolor,command=showitems).grid(row=0,column=3)

tk.Checkbutton(controls_frame,text='Show only low stock (qty < 5)',variable=low_stock_var,bg=bgcolor,command=showitems).grid(row=0,column=4,padx=15)


button_frame=tk.Frame(top,bg=bgcolor)
button_frame.grid(row=3,column=0,pady=10)

b1=tk.Button(button_frame,text='Add',command=add_item,font=bfont,bg='darkred',fg='white',width=10)
b1.grid(row=0,column=0,padx=8)

b2=tk.Button(button_frame,text='Delete',command=dlt_items,font=bfont,bg='darkred',fg='white',width=10)
b2.grid(row=0,column=1,padx=8)

b3=tk.Button(button_frame,text='Search',command=search_item,font=bfont,bg='darkred',fg='white',width=10)
b3.grid(row=0,column=2,padx=8)

b4=tk.Button(button_frame,text='Show all',command=showitems,font=bfont,bg='darkred',fg='white',width=10)
b4.grid(row=0,column=3,padx=8)

b5=tk.Button(button_frame,text='Delete all',command=dlt_all,font=bfont,bg='darkred',fg='white',width=10)
b5.grid(row=0,column=4,padx=8)


display_frame=tk.Frame(top,bg=bgcolor)
display_frame.grid(row=4,column=0,padx=10,pady=10)

listbox=tk.Listbox(display_frame,width=70,height=12,font=listfont,bg='white',fg='#2c3e50')
listbox.grid(row=0,column=0)

scrollbar=tk.Scrollbar(display_frame)
scrollbar.grid(row=0,column=1,sticky='ns')

listbox.config(yscrollcommand=scrollbar.set)
scrollbar.config(command=listbox.yview)

load_inventory()
showitems()
top.mainloop()
