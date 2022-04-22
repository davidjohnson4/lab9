from logging import root
from tkinter import *
from tkinter import ttk
from pokeapii import get_pokemon_list, get_pokemon_image_url
import os
import sys
import ctypes
import requests

def main():

    script_dir = sys.path[0]
    images_dir = os.path.join(script_dir, 'images')
    if not os.path.isdir(images_dir):
        os.makedirs(images_dir)

    #creates the icon and deskspot for the part of the lab
    root = Tk()
    root.title('Pokemon Image Viewer')
    app_id = 'comp593.pokemonimage'
    ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(app_id)
    root.iconbitmap('Master-Ball.ico')
    root.columnconfigure(0, weight=1)
    root.rowconfigure(0, weight=1)

    #code that will allow the page to expand to certain images or photos brought
    frm = ttk.Frame(root)
    frm.grid(sticky=(N,S,E,W))
    frm.columnconfigure(0, weight=1)
    frm.rowconfigure(0, weight=1)
    
    #sets the image into a certain spot on the page
    img_pokemon = PhotoImage(file='pokeball.png')
    lbl_image = Label(frm, image=img_pokemon)
    lbl_image.grid(row=0, column=0, padx=10, pady=10)

    pokemon_list = get_pokemon_list(limit=1000)
    pokemon_list.sort()
    cbo_pokemon_sel = ttk.Combobox(frm, values=pokemon_list, state='readonly')
    cbo_pokemon_sel.set('select a pokemon')
    cbo_pokemon_sel.grid(row=1, column=0)


    def handle_cbo_pokemon_sel(event):
        pokemon_name = cbo_pokemon_sel.get()
        image_url = get_pokemon_image_url(pokemon_name)
        image_path = os.path.join(images_dir, pokemon_name + '.png')
        if download_image_url(image_url, image_path):
            img_pokemon['file'] = image_path
            btn_set_desktop.state(['!disabled'])

    cbo_pokemon_sel.bind('<<ComboboxSelected>>', handle_cbo_pokemon_sel)
    #code that can set the selected image to be the background of the computer
    def btn_set_desktop_click():
        pokemon_name = cbo_pokemon_sel.get()
        image_path = os.path.join(images_dir, pokemon_name + '.png')
        set_desktop_background_image(image_path)
        
    #code to show the button to cause the set code
    btn_set_desktop = ttk.Button(frm, text="set as desktop image", command=btn_set_desktop_click)
    btn_set_desktop.state(['disabled'])
    btn_set_desktop.grid(row=2, column=0, padx=10, pady=10)

    root.mainloop()
def set_desktop_background_image(path):
    ctypes.windll.user32.SystemParametersInfoW(20, 0, path, 0)
#definiton code will get the code from the url
def download_image_url(url, path):

    if os.path.isfile(path):
        return path
    resp_msg = requests.get(url)
    if resp_msg.status_code == 200:
        #try:
            img_data = resp_msg.content
            with open(path, 'wb') as fp:
                fp.write(img_data)
            return path
        #except:
            #return
    else:
        print('failed to download')
        print('respons code:', resp_msg.status_code)
        print(resp_msg.text)

main()