from tkinter import *
import sqlite3

root = Tk()
root.title("Listas de Tareas")
root.geometry("500x500")
root.configure(bg='gray55')

conn = sqlite3.connect('todo.db')

c = conn.cursor()

c.execute("""
    CREATE TABLE IF NOT EXISTS todo (
        id INTEGER PRIMARY KEY AUTOINCREMENT, 
        created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
        descripcion TEXT NOT NULL,
        completed BOOLEAN NOT NULL
    );     
""")

conn.commit()

    
    

# currying
def complete(id):
    def _complete():
        sql="SELECT * FROM todo WHERE id=?"
        todo = c.execute(sql,(id,)).fetchone()
        
        sql = "UPDATE todo SET completed  = ? where id=?"
        c.execute(sql,(not todo[3], id))        
        conn.commit()
        render_todos()
        
    return _complete

    
def render_todos():
    sql = "SELECT * FROM todo"
    rows = c.execute(sql).fetchall()

    for widget in frame.winfo_children():
        widget.destroy()
    
    for i in range(0, len(rows)):
        id = rows[i][0]
        completed = rows[i][3]
        description = rows[i][2]
        color = "green3" if completed else 'red3'
        l = Checkbutton(frame, text=description, fg=color, width=42, anchor='w', command=complete(id))
        l.grid(row=i, column=0, sticky='w')
         
        btn = Button(frame, text='Eliminar', command=remove(id))
        btn.grid(row=i, column=1)
        
        l.select() if completed else l.deselect()
 
 
def addTodo():
    todo = e.get()
    
    if todo:
        sql = "INSERT INTO todo (descripcion, completed) VALUES (?,?)"
        c.execute(sql,(todo, False))
        conn.commit()
        e.delete(0,END)
        render_todos()
        e.focus_set()
        

def remove(id):
    def _remove():

        sql="DELETE FROM todo WHERE id=?"
        c.execute(sql,(id,))
        conn.commit()
        render_todos()
    return _remove



l = Label (root, text="Tareas")
l.grid(row=0, column=0) 

e=Entry(root, width=40)
e.grid(row=0, column=1)

btn = Button(root, text='Agregar', command=addTodo)
btn.grid(row=0, column=2)

frame = LabelFrame(root, text='Mis Tareas', padx=5, pady=5)
frame.grid(row=1, column=0, columnspan=3, sticky='snswe', padx=5)
frame.configure(bg='gray55')
e.focus()

root.bind('<Return>', lambda x: addTodo())
render_todos()
root.mainloop()