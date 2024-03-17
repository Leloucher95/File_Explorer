import tkinter as tk
import tkinter.ttk as ttk
import os
import subprocess

root = tk.Tk()
root.geometry('600x590')
root.title('File Explorer')

"""Style de la fenêtre"""
#style=ttk.Style(root) 
#style.configure('Treeview', font=('Bold'))


#Liste des lecteurs disponibles 
drives=['A://', 'B://', 'C://', 'D://', 'E://', 'F://', 'G://', 'H://', 'I://', 'J://', 'K://', 'L://', 'M://', 'N://', 'O://', 'P://', 'Q://', 'R://', 'S://', 'T://', 'U://', 'V://', 'W://', 'X://', 'Y://', 'Z://']

#Liste des lecteurs valides ; cette liste ser remplie avec find_valid_drives()
valid_drives= []

browse_dir=[]


#fonction insérant les lecteurs disponibles dans la colonne du tableau side_table (Treeview)
def insert_drives():
    for i  in side_table.get_children() :
        side_table.delete(i)

    for r in range(len(valid_drives)):
        side_table.insert(parent='', iid=r,text='',values=[valid_drives[r]], index='end')


#fonction chargée de trouver les lecteurs présents sur l'O.S
def find_valid_drives () :
    for drive in drives:
        if os.path.exists(drive): #retourne True si le lecteur existe
            valid_drives.append(drive)
    
    insert_drives()




#Fonction permettant d'afficher la liste des fichiers et dossiers dans main_table|Treeview (zone d'affichage des dossiers)
def insert_folders(path):
    global browse_dir
    for i in main_table.get_children() :
        main_table.delete(i) #On nettoie la zone à chaque appel de la fonction

    folders=os.listdir(path) #listdir retourne la liste des fichiers et des sous répertoire en prenant en entrée le chemin vers un répertoire(path)

    browse_dir=[]

    for r in range(len(folders)) :
        main_table.insert(parent='', iid=r, text='', values=[folders[r]], index='end')
        browse_dir.append(str(path) + '/'+ folders[r]) 

      




#fonction déclenchée à chaque sélection sur le treeview
#Elle se charge de récupérer l'index de l'élément sélectionné sur le widget et de le retourner à insert_folders()

def open_drive():
    selected=side_table.selection() #side_table.selection() retourne un tuple contenant les items sélectionnés
    if selected : # Vérifie si le tuple n'est pas vide
        index=int(selected[0])
        path=valid_drives[index] #on accède au lecteur correspondant à l'index
        insert_folders(path)
    
    root.title(path)


#
def insert_files(path):
    global browse_dir
    for i in main_table.get_children() :
        main_table.delete(i) #On nettoie la zone à chaque appel de la fonction


    files = os.listdir(path)   
    browse_dir=[]

    for r in range(len(files)):
        main_table.insert(parent='', iid=r, text='',index='end', values=[files[r]] )
        browse_dir.append(str(path) + '/' + files[r])
    


def open_folder():
    selected = main_table.selection()
    if selected:  # Vérifie si le tuple n'est pas vide
        index = int(selected[0])
        path = browse_dir[index]
        if os.path.isdir(path) :
            insert_files(path)
        else :
            os.startfile(path)  
        root.title(path)





side_table=ttk.Treeview(root) #Widget Treeview pour la liste des lecteurs et dossiers

side_table['column']=['Drives']
side_table.column('#0' ,anchor=tk.W,width=0, stretch=tk.NO) #Permet de cacher la première colonne inutile ici
side_table.column('Drives' ,anchor=tk.W, width=120, stretch=tk.NO) #Colonne affichant les lecteurs présents ainsi que certains dossiers
side_table.heading('Drives', text='Drives', anchor=tk.W,) #Définit l'en-tête de la colonne

side_table.pack(side=tk.LEFT, anchor =tk.W, fill=tk.Y)
side_table.bind('<<TreeviewSelect>>', lambda e: open_drive() )

main_table=ttk.Treeview(root) #Widget Treeview pour la zone d'affichage des dossiers

main_table['column']=['Files']
main_table.column('#0', anchor=tk.W, width=0, stretch=tk.NO)
main_table.column('Files', anchor=tk.W, width=500,)
main_table.heading('Files', text='Files', anchor=tk.W)

scrollbar = ttk.Scrollbar(root, orient="vertical", command=main_table.yview)
# Configurez le Treeview pour utiliser la Scrollbar
main_table.configure(yscrollcommand=scrollbar.set)

# Emballez la Scrollbar et le Treeview dans la fenêtre
scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
main_table.pack(side=tk.LEFT, fill=tk.BOTH)


main_table.pack(side=tk.LEFT, anchor =tk.W, fill=tk.Y)
main_table.bind('<<TreeviewSelect>>', lambda e : open_folder())
find_valid_drives()



root.mainloop()
