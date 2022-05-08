# -*- coding: utf-8 -*-
"""
Created on Sat Dec 15 23:38:40 2018

@author: worlapim
"""

"""
TODO:
    VÍC
    vícenásobná podmínka
"""

import random
from tkinter import filedialog
from tkinter import *
from datetime import *
from tkinter import messagebox

speed=3
dictionary = []
paterns = []
next_sentence = [""]
rest_sentence = ""
pamet = []
smer_paterns = "paterns.txt"
smer_dictionary = "words.txt"
smer_additions = "additions.txt"
first_sentence = False
dictionary_extras = []
end_soon = False
v_uvozovkach = False

def otevrit_w():
    global dictionary
    global smer_dictionary
    smer_dictionary = filedialog.askopenfilename(title=u"Otevřít soubor",filetypes=(('texts', '*.txt'),('anything', '*')))
    update_w()

def otevrit_p():
    global paterns
    global smer_paterns
    smer_paterns = filedialog.askopenfilename(title=u"Otevřít soubor",filetypes=(('texts', '*.txt'),('anything', '*')))
    update_p()
    
def otevrit_a():
    global additions
    global smer_additions
    smer_additions = filedialog.askopenfilename(title=u"Otevřít soubor",filetypes=(('texts', '*.txt'),('anything', '*')))
    additions=[]
    update_a()

"""
funkce načte slova a fráze.
"""
def update_w():
    global smer_dictionary  
    global dictionary
    global dictionary_extras
    dictionary=[]
    soubor=open(smer_dictionary,'r')
    hruby=soubor.readlines()
    soubor.close()
    
    for i in hruby:
        ok=0
        for y in i:
            if y=='/' and ok == 0:
                ok = 1
            elif y == '=' and ok == 1:
                ok = 2
                break
        if ok == 1:
            splitted = i.split('/')
            kategorie = splitted[0]
            fraze = splitted[1]
            if fraze[-1:]=='\n':
                fraze = remove_last_char(fraze)
            new=1
            spot=0
            for y in dictionary:
                if y[0]==kategorie:
                    new=0
                    break
                spot=spot+1
            if new==1:
                dictionary.append([kategorie,[fraze]])
            else:
                dictionary[spot][1].append(fraze)
        if ok == 2:
            splitted = i.split('/')
            kategorie = splitted[0]
            splitted = splitted[1].split('=')
            fraze=splitted[0]
            extra=splitted[1]
            if extra[-1:]=='\n':
                extra = remove_last_char(extra)
            new=1
            spot=0
            for y in dictionary:
                if y[0]==kategorie:
                    new=0
                    break
                spot=spot+1
            if new==1:
                dictionary.append([kategorie,[fraze]])
            else:
                dictionary[spot][1].append(fraze)
            fraze_splited = fraze.split()
            dictionary_extras.append([fraze_splited[0],extra])
    #print(dictionary)
    #print(dictionary_extras)
    
    
                
                
def update_a():
    global smer_additions
    global additions
    additions = []
    soubor = open(smer_additions,'r')
    hruby = soubor.readlines()
    soubor.close()
    lines = hruby
    for line in lines:
        if line[-1] == '\n': #odstranění '\n' na konci řádku
            line = line[:-1]
        if line == "":
            continue
        split_line = line.split('/')
        additions.append([split_line[0]])
        words = split_line[1].split(' ')
        for word in words:
            percentage = 100
            dictonary_spot = ''
            variable = ''
            if '%' in word:
                word_info = word.split('%')
                percentage = int(word_info[0])
                if '=' in word_info[1]:
                    #print(word_info)
                    word_info2 = word_info[1].split('=')
                    dictonary_spot = word_info2[0]
                    variable = word_info2[1]
                else:
                    dictonary_spot = word_info[1]
            else:
                if '=' in word:
                    word_info = word.split('=')
                    dictonary_spot = word_info[0]
                    variable = word_info[1]
                else:
                    dictonary_spot = word
            additions[-1].append([percentage,dictonary_spot,variable])
    #print(additions)      
    
    

"""
funkce načte vzorce vět.
"""
def update_p(): 
    global paterns
    paterns=[]
    global smer_paterns
    global next_sentence
    soubor=open(smer_paterns,'r')
    hruby=soubor.readlines()
    soubor.close()
    next_sentence=[""]
    y=-2
    for i in range(len(hruby[0])):
        if hruby[0][i]==" ":
            for y in range(2+y,i):
                next_sentence[len(next_sentence)-1]=next_sentence[len(next_sentence)-1]+hruby[0][y]
            next_sentence.append("")
    for y in range(2+y,i):
        next_sentence[len(next_sentence)-1]=next_sentence[len(next_sentence)-1]+hruby[0][y]
    pocet_modelu=0
    for veta in hruby:
        if veta=="\n":
            continue
        if veta==hruby[0]:
            continue
        paterns.append([])
        for i in range(len(veta)-1):
            if veta[i]=='/':
                break
        paterns[pocet_modelu].append("")
        for y in range(i):
            paterns[pocet_modelu][0]=paterns[pocet_modelu][0]+veta[y]
        for i in range(i,len(veta)-1):
            if veta[i]==" " or veta[i]==".":
                kus=""
                for y in range(y+2,(i)):
                    kus=kus+veta[y]
                procenta=0
                promenna=0
                for q in kus:
                    if q=="%":
                        procenta=1
                    elif q=="=":
                        promenna=1
                paterns[pocet_modelu].append([])
                if procenta==1:
                    for q in range(len(kus)):
                        if kus[q]=='%':
                            break
                    cislo=""
                    for q in range(q):
                        cislo=cislo+kus[q]
                    paterns[pocet_modelu][len(paterns[pocet_modelu])-1].append(int(cislo))
                else:
                    paterns[pocet_modelu][len(paterns[pocet_modelu])-1].append(100)
                fraze=""
                uloz=""
                if promenna==0:
                    if procenta==1:
                        for q in range(len(kus)):
                            if kus[q]=='%':
                                break
                        for q in range(q+1,len(kus)):
                            fraze=fraze+kus[q]
                    else:
                        for q in range(len(kus)):
                            fraze=fraze+kus[q]
                else:
                    od=0
                    do=0
                    if procenta==1:
                        for od in range(len(kus)):
                            if kus[od]=='%':
                                break
                        od=od+1
                    for do in range(len(kus)):
                        if kus[do]=='=':
                            break
                    for q in range(od,do):
                        fraze=fraze+kus[q]
                    for q in range(do+1,len(kus)):
                        uloz=uloz+kus[q]
                paterns[pocet_modelu][len(paterns[pocet_modelu])-1].append(fraze)
                paterns[pocet_modelu][len(paterns[pocet_modelu])-1].append(uloz)
            if veta[i]==".":
                break
        paterns[pocet_modelu].append([])
        konec=""
        for i in range(i+1,len(veta)-1):
            if veta[i]==" ":
               paterns[pocet_modelu][len(paterns[pocet_modelu])-1].append(konec)
               konec=""
            else:
                konec=konec+veta[i]
        paterns[pocet_modelu][len(paterns[pocet_modelu])-1].append(konec)
        pocet_modelu=pocet_modelu+1
    for patern in paterns:
        paths = patern[-1]
        for i in range(len(paths)):
            paths[i] = paths[i].replace('_', ' ')
    #print(paterns)
    
def is_next_sentence_parameter_true(parametr):
    od_zavorky = 0
    konec_zavorky = 1
    while parametr[od_zavorky] == '(':
        while parametr[konec_zavorky] != ')':
            konec_zavorky += 1
        podminka = parametr[od_zavorky + 1:konec_zavorky]
        #print(podminka)
        if is_single_sentence_parameter_true(podminka) == False:
            return False
        else:
            od_zavorky = konec_zavorky + 1
            konec_zavorky = konec_zavorky + 2
    return True
    
def is_single_sentence_parameter_true(podminka):
    global pamet
    if podminka.find('=') != -1:
        splitted = podminka.split('=')
        #print(splitted)
        value = splitted[0]
        variable = splitted[1]
        for poznamka in pamet:
            if (poznamka[0]==variable) & (poznamka[1]==value):
                return True
        return False
    if podminka.find('!') != -1:
        splitted = podminka.split('!')
        #print(splitted)
        value = splitted[0]
        variable = splitted[1]
        for poznamka in pamet:
            if (poznamka[0]==variable):
                if (poznamka[1]==value):
                    return False
                else:
                    return True
        return True
    
    
def vyber_z_next_sentence(next_sentence):
    if len(next_sentence) > 0:
        if next_sentence[0]==".":
            return vyber_z_next_sentence_iter(next_sentence,1)
        return vyber_z_next_sentence_iter(next_sentence,0)
def vyber_z_next_sentence_iter(next_sentence,od):
    while True:
        chosen = next_sentence[random.randint(od,len(next_sentence)-1)]
        if chosen == "":
            return None
        if chosen[0] != '(':
            return chosen
        if is_next_sentence_parameter_true(chosen):
            konec_zavorek=-1
            for i in range(len(chosen)):
                if chosen[i] == ')':
                    konec_zavorek = i
            return chosen[konec_zavorek+1 : None]
                    

def vyber_slovo(slovo):
    if (slovo[0] == "name-man") | (slovo[0] == "name-woman"):
        return vyber_a_odstran(slovo[1])
    else:
        return vyber(slovo[1])
def vyber(moznosti):
    return(moznosti[random.randint(0,len(moznosti)-1)])
def vyber_a_odstran(moznosti):
    return(moznosti.pop(random.randint(0,len(moznosti)-1)))
    
def chance(proc):
    a=random.randint(1,100)
    if a<=proc:
        return (1)
    else:
        return (0)

def remove_last_char(before):
    after = ""
    for i in range(len(before)-1):
        after += before[i]
    return after


"""
funkce připíše další znak, slovo nebo, větu
pokud nemá nic v zásobníku, nejdříve ho doplní
"""
def pis():
    global text
    global next_sentence
    global rest_sentence
    global paterns
    global dictionary    
    global pamet
    global first_sentence
    global dictionary_extras
    global v_uvozovkach
    #print(next_sentence)
    if rest_sentence=="":
        """
        doplnění zásobníku o další větu
        """
        plan=""        
        model=vyber_z_next_sentence(next_sentence)
        #print(model)
        if model==None:
            end_of_story()
            return 
        else:
            for i in paterns:
                if i[0]==model:
                    plan=i
                    break
            #print(plan)
            next_sentence=plan[len(plan)-1]
            for i in range(1,len(plan)-1):
                """ '+' značí větu vedlejší """
                if plan[i][2] != '+':
                    if plan[i][2]=="":
                        for y in dictionary:
                            if plan[i][1]==y[0]:
                                if chance(plan[i][0])==1:
                                    rest_sentence=rest_sentence+" "+vyber_slovo(y)
                                break
                        else:
                            rest_sentence=rest_sentence+" "+plan[i][1]
                    else:
                        nalezeno=0                    
                        for y in pamet:
                            if plan[i][2]==y[0]:
                                nalezeno=1
                                if chance(plan[i][0])==1:
                                    rest_sentence=rest_sentence+" "+y[1]
                                    break
                        if nalezeno==0:
                            for y in dictionary:
                                if plan[i][1]==y[0]:
                                    to=vyber_slovo(y)
                                    if chance(plan[i][0])==1:
                                        rest_sentence=rest_sentence+" "+to
                                    pamet.append([plan[i][2],to])
                elif chance(plan[i][0]) == 1:
                    pis_addition(plan[i])  
            #print(rest_sentence)
            """
            finální úpravy věty.
            """
            """
            "a" na "an"
            """
            splitted = rest_sentence.split()
            for i in range(len(splitted)):
                if splitted[i] == 'a':
                    for extra in dictionary_extras:
                        #print(splitted[i + 1],extra[0])
                        if extra[0]==splitted[i + 1]:
                            splitted[i] = "an"
                            break
            rest_sentence=""
            for i in range(len(splitted)):
                rest_sentence+= " " + splitted[i]
            """
            tečka, mezery
            """
            rest_sentence = rest_sentence+"."
            rest_sentence = capitalize_first_letter( rest_sentence )
            if first_sentence:
                """
                odstraněni mezery před větou
                """
                first_sentence = False
                rest_sentence=rest_sentence[1:]
            rest_sentence = no_space_before_dots_etc( rest_sentence )  
            """
            nový odstavec
            """
            if len(plan[-1])>0:
                if plan[-1][0]== ".":
                    rest_sentence = rest_sentence + "\n"
            """
            mezery kolem uvozovek
            """
            i = 0
            while i < len(rest_sentence):
                if rest_sentence[i] == '"':
                    #print(rest_sentence)
                    if v_uvozovkach:
                        v_uvozovkach = False
                        if i != 0:
                            if rest_sentence[i-1] == ' ':
                                rest_sentence = pop( rest_sentence,  i-1 )
                                i -= 1
                        if (rest_sentence[i+1] != ' ') & (rest_sentence[i+1] != '.'):
                            rest_sentence = insert( rest_sentence, ' ', i+1 )
                    else:
                        v_uvozovkach = True
                        if i != 0:
                            if rest_sentence[i-1] != ' ':
                                rest_sentence = insert( rest_sentence, ' ', i-1 )
                        if rest_sentence[i+1] == ' ':
                            rest_sentence = pop( rest_sentence, i+1 )
                i += 1
    """
    výpis
    """
    if speed==1:
        text.insert(END, rest_sentence[0])
        rest_sentence=rest_sentence[1:]
    elif speed==2:
        while True:
            text.insert(END, rest_sentence[0])
            rest_sentence=rest_sentence[1:]
            if (rest_sentence == "" or rest_sentence[0] == " "):
                break
    elif speed==3:
        text.insert(END, rest_sentence)
        rest_sentence=""
        #print(next_sentence)
    #print(dictionary)
        
def insert (source_str, insert_str, pos):
    return source_str[:pos] + insert_str+source_str[pos:]
def pop (source_str, pos):
    return source_str[:pos] + source_str[1+pos:]
        

def pis_addition(parametr):
    #print(parametr)
    global rest_sentence
    usable_additions = []
    for addition in additions:
        if addition[0] == parametr[1]:
            usable_additions.append(addition[1:])
    if usable_additions == []:
        rest_sentence += " ERROR"
    #print(usable_additions)
    addition = vyber(usable_additions)
    for addition_i in range(len(addition)):
        #print(addition[addition_i])
        if addition[addition_i][2]=="":
            for y in dictionary:
                if addition[addition_i][1]==y[0]:
                    if chance(addition[addition_i][0])==1:
                        rest_sentence=rest_sentence+" "+vyber_slovo(y)
        elif addition[addition_i][2]=="+":
            pis_addition(addition[addition_i])
        else:
            nalezeno=0                    
            for y in pamet:
                if addition[addition_i][2]==y[0]:
                    nalezeno=1
                    if chance(addition[addition_i][0])==1:
                        rest_sentence=rest_sentence+" "+y[1]
                        break
            if nalezeno==0:
                for y in dictionary:
                    if addition[addition_i][1]==y[0]:
                        to=vyber_slovo(y)
                        if chance(addition[addition_i][0])==1:
                            rest_sentence=rest_sentence+" "+to
                        pamet.append([addition[addition_i][2],to])
        

def capitalize_first_letter(in_sentence):
    out_sentence = ""
    got_capitalized = False
    for letter in in_sentence:
        if not got_capitalized and letter.isalpha():
            out_sentence += letter.capitalize()
            got_capitalized = True
        else:
            out_sentence += letter
    return out_sentence

    
"""
odstranění mezery před tečkou, otazníkem atd.
"""
def no_space_before_dots_etc(in_sentence):
    out_sentence = ""
    space = False
    for char in in_sentence:
        if space:
            if char == "." or char == "!" or char == "?" or char == ",":
                pass
            else:
                out_sentence += " "
            space = False
        if char == " ":
            space = True
        else:
            out_sentence += char
    return out_sentence

def wrap_up():
    global end_soon
    end_soon = True
    b_end['state'] = 'disabled'
    
def text_restart():
    global text
    global next_sentence
    global rest_sentence
    global pamet
    global first_sentence
    global end_soon
    global v_uvozovkach
    next_sentence = [""]
    rest_sentence = ""
    pamet = []
    #first_sentence = True
    end_soon = False
    text.delete(1.0, END)
    update_p()
    update_w()
    update_a()
    b_generate['state'] = 'normal'
    v_uvozovkach = False
    
def end_of_story():
    b_generate['state'] = 'disabled'
    
def speed1():
    global speed
    speed=1

def speed2():
    global speed
    speed=2

def speed3():
    global speed
    speed=3


update_p()
update_w()
update_a()
    
"""
vzhled
"""
       
    
hlavni=Tk()


speedMenu=Menu(hlavni,tearoff=0)
speedMenu.add_command(label="1",command=speed1)
speedMenu.add_command(label="2",command=speed2)
speedMenu.add_command(label="3",command=speed3)

sourceMenu=Menu(hlavni,tearoff=0)
sourceMenu.add_command(label="words",command=otevrit_w)
sourceMenu.add_command(label="sentence paterns",command=otevrit_p)
sourceMenu.add_command(label="sentence additions",command=otevrit_a)

HorniMenu=Menu(hlavni,tearoff=0)
HorniMenu.add_cascade(label="source",menu=sourceMenu)
HorniMenu.add_cascade(label="speed",menu=speedMenu)
HorniMenu.add_cascade(label="restart",command=text_restart)
hlavni.config(menu=HorniMenu)


b_generate = Button(hlavni, text="GENERATE!", width=28, font="Arial 16 bold", command=pis)
b_generate.grid(row=1,column=0)
#b_end = Button(hlavni, text="FINISH IT", width=14, font="Arial 16 bold", command=wrap_up)
#b_end.grid(row=1,column=1)

text=Text(wrap=WORD)
text.grid(row=0,column=0,columnspan=1)


mainloop()  