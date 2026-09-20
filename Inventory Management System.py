import tkinter as tk
import tkinter.messagebox
datafile='Inventory data.txt'

inventory={}
def save_inventory():
    file=open(datafile,'w')
    for itemid in inventory:
        details=inventory[itemid]
        file.write(itemid+'\n')
        file.write(details['name']+'\n')
        file.write(str(details['qty'])+'\n')
        file.write(str(details['price'])+'\n')
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
        itemid=itemid[:-1]
        name=name[:-1]
        qty=qty[:-1]
        price=price[:-1]
        inventory[itemid]={'name':name,'qty':int(qty),'price':float(price)}
    file.close()
def clear_fields():
    e1.delete(0,'end')
    e2.delete(0,'end')
    e3.delete(0,'end')
    e4.delete(0,'end')
def showitems():
    listbox.delete(0,'end')
    for itemid in inventory:
        details=inventory[itemid]
        row=itemid+'  |  '+details['name']+'  |  '+str(details['qty'])+'  |  '+str(details['price'])
        listbox.insert('end',row)
def add_item():
    itemid=e1.get()
    name=e2.get()
    qty=e3.get()
    price=e4.get()
    if itemid=='' or name=='' or qty=='' or price=='':
        tkinter.messagebox.showerror('Empty Field','Please fill in all the fields')
        return
    if itemid in inventory:
        old_qty=inventory[itemid]['qty']
        new_qty=old_qty+int(qty)
        inventory[itemid]={'name':name,'qty':new_qty,'price':float(price)}
        tkinter.messagebox.showinfo('Updated','Item already existed, quantity restocked')
    else:
        inventory[itemid]={'name':name,'qty':int(qty),'price':float(price)}
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
            row=itemid+'  |  '+details['name']+'  |  '+str(details['qty'])+'  |  '+str(details['price'])
            listbox.insert('end',row)
top=tk.Tk()
top.title('Inventory Management System')
l1=tk.Label(top,text='Item ID')
e1=tk.Entry(top,width=15)
l1.grid(row=0,column=0)
e1.grid(row=0,column=1)
l2=tk.Label(top,text='Name')
e2=tk.Entry(top,width=15)
l2.grid(row=0,column=2)
e2.grid(row=0,column=3)
l3=tk.Label(top,text='Quantity')
e3=tk.Entry(top,width=15)
l3.grid(row=1,column=0)
e3.grid(row=1,column=1)
l4=tk.Label(top,text='Price')
e4=tk.Entry(top,width=15)
l4.grid(row=1,column=2)
e4.grid(row=1,column=3)
b1=tk.Button(top,text='Add',command=add_item)
b1.grid(row=2,column=0)                                                      
b2=tk.Button(top,text='Delete',command=dlt_items)
b2.grid(row=2,column=1)                                                     
b3=tk.Button(top,text='Search(type ID or name)',command=search_item)
b3.grid(row=2,column=2)
b4=tk.Button(top,text='Show all',command=showitems)
b4.grid(row=2,column=3)
b5=tk.Button(top,text='Delete all',command=dlt_all,width=15)
b5.grid(row=2,column=4)
listbox=tk.Listbox(top,width=50,height=12)
listbox.grid(row=3,column=2)         
load_inventory()
showitems()                                                      


top.mainloop()
    
