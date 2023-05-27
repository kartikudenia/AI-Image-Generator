from tkinter import *
from tkinter import messagebox
import openai
import requests
from io import BytesIO
from PIL import Image,ImageTk
def generate():
    if ( user_prompt.get() == ' '):
        messagebox.showerror(title='ERROR',message='Please insert Prompt')
        return
    
    if (selected_option.get() == 'Select Style Type'):
        temp_var = ''
    else:
        temp_var = ' in style: ' + selected_option.get()
    new_prompt = user_prompt.get() + temp_var
    
    openai.api_key = open('key.txt').read()
    response = openai.Image.create(prompt=new_prompt,n=int(mySlider1.get()),size='512x512')
    
    image_urls=[]
    for i in range(len(response['data'])):
        image_urls.append(response['data'][i]['url'])
    
    images=[]
    for url in image_urls:
        response = requests.get(url)
        img = Image.open(BytesIO(response.content))
        tk_image = ImageTk.PhotoImage(img)
        images.append(tk_image)
    my_canvas.update()
    my_canvas.delete('all')
    def update_img(index=0):
        my_canvas.delete('all')
        my_canvas.create_image(0,0,anchor='nw',image=images[index])
        index = (index + 1) % len(images)
        my_canvas.after(2000,update_img,index)
    update_img()
    
root = Tk()
root.geometry('+400+200')
root.config(background='black')
root.title('AI Image Generator')
root.resizable(0,0)
root.overrideredirect(True)
titleframe = Frame(root)
titleframe.place(x=40,y=50)
titlelabel = Label(titleframe, text="AI Image Generator",font='algerian 20 bold', fg='white',background='black')
titlelabel.pack()

button_frame = Frame(root,background='#1f1e1e')
button_frame.pack(side='left',pady=50,padx=50)

user_prompt = StringVar()
user_prompt.set(' ')
prompt_label = Label(button_frame,text='Prompt *',background=button_frame['background'],fg='white',font=7)
prompt_label.grid(pady=10,padx=10,sticky=W)
prompt_entry = Entry(button_frame,width=30,textvariable=user_prompt,fg='white',background='#141310',
                     insertbackground='white',relief=GROOVE)
prompt_entry.grid(row=0,column=1,pady=10,padx=10,sticky=W)

style_label = Label(button_frame,text='Style',background=button_frame['background'],fg='white',font=7)
style_label.grid(row=1,column=0,pady=10,padx=10,sticky=W)

selected_option = StringVar()
selected_option.set('Select Style Type')
l = ['Realistic','Cartoon','3D Illustration','Flat Art']

style_menu = OptionMenu(button_frame,selected_option,*l)
style_menu.config(background='#141310',fg='white',highlightbackground='#141310')
style_menu.grid(row=1,column=1,pady=10,padx=10)

number_label = Label(button_frame,text='Number',background=button_frame['background'],fg='white',font=7)
number_label.grid(row=2,column=0,pady=10,padx=10,sticky=W)

mySlider1 = Scale(button_frame,from_=1,to=10,orient='horizontal',background=button_frame['background'],fg='white')
mySlider1.grid(row=2,column=1,pady=10,padx=10)

my_canvas = Canvas(root,width=512,height=512)
my_canvas.pack(side=RIGHT)
my_canvas.create_text(190,250,text='Image will Appear here',anchor='nw',font=20)

inner_frame = Frame(root,background='black')
inner_frame.place(x=100,y=400)

generate_img = PhotoImage(file='generate.png')
generate_button = Button(inner_frame,image=generate_img,borderwidth=0,command=generate,relief=GROOVE)
generate_button.pack(pady=10)

exit_img = PhotoImage(file='exit.png')
exit_button = Button(inner_frame,image=exit_img,borderwidth=0,background=button_frame['background'],command=root.destroy)
exit_button.pack(pady=10)

root.mainloop()
