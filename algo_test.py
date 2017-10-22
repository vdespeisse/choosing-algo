# -*- coding: utf-8 -*-
from __future__ import print_function
import pandas as pd, numpy as np
import random
import matplotlib as mpl
import matplotlib.pyplot as plt
import seaborn as sns
from IPython.display import display, HTML, clear_output


from ipywidgets import interact, interactive, fixed, interact_manual
import ipywidgets as widgets
## Seance a 14H
# Photographe A & B: seance a 15h
# Photographe C: seance a 16h
# Photographe D & E: pas de seances dans la journée

data =   [
    {'nom':'A', 'note_ever':10, 'prox':2, 'favorite':'couple'},
    {'nom':'B', 'note_ever':5, 'prox':2, 'favorite':'solo'},
    # {'nom':'C', 'note_ever':5, 'prox':1, 'favorite':'solo'},
    # {'nom':'D', 'note_ever':10, 'prox':0, 'favorite':'solo'},
    # {'nom':'E', 'note_ever':1, 'prox':0, 'favorite':'solo'},
]
seance = {'type':'solo'}
def calcul_notes(photographes,type_seance,params):
    return {k: v.get('note_ever',0)+int(v.get('seance_adjacente',False))*params.get('seance_adjacente',0) \
                + int(v.get('seance_adjacente_2',False))*params.get('seance_adjacente_2',0) \
                + int(type_seance in v.get('types_favoris',['solo','couple']))*params.get('type_favori',0) \
                for k,v in photographes.items()}

def calcul_notes_coef(photographes,type_seance,**params):
    coef_adjacente = lambda v: max(1,int(v.get('seance_adjacente',False))*params.get('seance_adjacente',0))
    coef_adjacente2 = lambda v: max(1,int(v.get('seance_adjacente_2',False))*params.get('seance_adjacente_2',0))
    coef_favoris = lambda v: max(1,int(type_seance in v.get('types_favoris',['solo','couple']))*params.get('type_favori',0))
    return {k: int(100*v.get('note_ever',1)*coef_adjacente(v)*coef_adjacente2(v)*coef_favoris(v)) for k,v in photographes.items()}

def assign(notes_photographes):
    choice_list = []
    for photographe, note in notes_photographes.items():
        choice_list += [photographe]*note
    return random.choice(choice_list)

def simulate(notes_photographes,n=10000):
    results = {photographe: 0 for photographe in notes_photographes.keys() }
    for i in xrange(n):
        p = assign(notes_photographes)
        results[p] += 1
    return results

def autolabel(ax, labels=None, height_factor=1.05):
    total = labels.sum()
    for i, rect in enumerate(ax.patches):
        height = rect.get_height()
        if labels is not None:
            try:
                label = str(100*labels[i]/float(total)) +'%'
            except (TypeError, KeyError):
                label = ' '
        else:
            label = '%d' % int(height)
        ax.text(rect.get_x() + rect.get_width()/2., height_factor*height,
                '{}'.format(label),
                ha='center', va='bottom')

def autolabel2(ax, labels=None, height_factor=1.05):
    total = labels.sum()
    for i, rect in enumerate(ax.patches):
        height = rect.get_height()
        if labels is not None:
            try:
                label = "%.2f" % (100*labels[i]) +'%'
            except (TypeError, KeyError):
                label = ' '
        else:
            label = '%d' % int(height)
        ax.text(rect.get_x() + rect.get_width()/2., height_factor*height,
                '{}'.format(label),
                ha='center', va='bottom')


def run_compute(photographes,type_seance,seance_adjacente=1,seance_adjacente_2=1,type_favori=1):
    notes = calcul_notes_coef(photographes,type_seance,seance_adjacente=seance_adjacente,seance_adjacente_2=seance_adjacente_2,type_favori=type_favori)
    total = float(sum(notes.values()))
    results =  {photographe: note/total for photographe,note in notes.items() }
    df = pd.DataFrame(data={'photographe':list(results.keys()),"proba assignation":list(results.values())}).sort_values('photographe')

    ax=sns.barplot(y="proba assignation",x='photographe',data=df,palette=sns.color_palette('hls',len(notes.keys())))
    autolabel2(ax, labels=df["proba assignation"].values, height_factor=1.02)
    plt.show()


def run(photographes,type_seance,seance_adjacente=1,seance_adjacente_2=1,type_favori=1,n=10000):
    notes = calcul_notes_coef(photographes,type_seance,seance_adjacente=seance_adjacente,seance_adjacente_2=seance_adjacente_2,type_favori=type_favori)
    print(notes)
    results= simulate(notes,n)
    df = pd.DataFrame(data={'photographe':results.keys(),'assignations':results.values()}).sort_values('photographe')

    ax=sns.barplot(y='assignations',x='photographe',data=df,palette=sns.color_palette('hls',len(notes.keys())))
    autolabel(ax, labels=df.assignations.values, height_factor=1.02)
    plt.show()

def assign_variable(var_name):
    def fn(x):
        globals()[var_name] = x
    return fn
def create_slider(var_name,desc='',default=0):
    globals()[var_name] = globals().get(var_name,default)
    return interact(assign_variable(var_name),x=widgets.FloatSlider(min=1,max=6,step=0.1,value=globals()[var_name],description=desc))
def run_compute(photographes,type_seance,seance_adjacente=1,seance_adjacente_2=1,type_favori=1):
    notes = calcul_notes_coef(photographes,type_seance,seance_adjacente=seance_adjacente,seance_adjacente_2=seance_adjacente_2,type_favori=type_favori)
    total = float(sum(notes.values()))
    results =  {photographe: note/total for photographe,note in notes.items() }
    df = pd.DataFrame(data={'photographe':list(results.keys()),"proba assignation":list(results.values())}).sort_values('photographe')

    ax=sns.barplot(y="proba assignation",x='photographe',data=df,palette=sns.color_palette('hls',len(notes.keys())))
    autolabel2(ax, labels=df["proba assignation"].values, height_factor=1.02)
    plt.show()
def on_button_clicked(b,photographes,type_seance):
    clear_output()
     display(HTML('''<style>
    .widget-label { min-width: 20ex !important; }
    .slide-container { min-width: 30ex !important; }
    div.p-Widget { min-width: 50ex !important; }
</style>'''))
    print('Photographes')
    display(pd.DataFrame(photographes).fillna(False))
    #generate_display_compute(photographes,type_seance)
    print('Paramètres 1')
    run_compute(photographes,type_seance,seance_adjacenteA,seance_adjacente_2A,type_favoriA)
    print('Paramètres 2')
    run_compute(photographes,type_seance,seance_adjacenteB,seance_adjacente_2B,type_favoriB)
def generate_display_compute(photographes,type_seance):
    display(HTML('''<style>
    .widget-label { min-width: 20ex !important; }
    .slide-container { min-width: 30ex !important; }
    div.p-Widget { min-width: 50ex !important; }
</style>'''))
    print('Photographes')
    display(pd.DataFrame(photographes).fillna(False))
    interact(lambda x: None,x=widgets.BoundedIntText(value=1,description='Parametres:', disabled=True))
    create_slider('seance_adjacenteA','seance_adjacente',1)
    create_slider('seance_adjacente_2A','seance_adjacente_2',1)
    create_slider('type_favoriA','type_favori',1)
    interact(lambda x: None,x=widgets.BoundedIntText(value=2,description='Parametres:', disabled=True))
    create_slider('seance_adjacenteB','seance_adjacente',1)
    create_slider('seance_adjacente_2B','seance_adjacente_2',1)
    create_slider('type_favoriB','type_favori',1)
    button = widgets.Button(description="Run")
    display(button)
    button.on_click(lambda b: on_button_clicked(b,photographes,type_seance))


# results = simulate(data,seance)
# df = pd.DataFrame(data={'photographe':results.keys(),'assignations':results.values()}).sort_values('photographe')
# ax=sns.barplot(y='assignations',x='photographe',data=df)
# autolabel(ax, labels=df.assignations.values, height_factor=1.02)
# plt.show()
