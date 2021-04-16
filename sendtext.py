#!/usr/bin/env python

import queue
import time
import threading
import unicodedata

from grove_rgb_lcd import *

class Sendtext(threading.Thread):
    # fifo
    q = queue.Queue(maxsize=0)

    def run(self):
        # while not bool(self.q.empty()):
        while True:
            if not self.q.empty():
                setText(self.q.get())
                # temp de lecture
                time.sleep(2)
            else:
                time.sleep(1)
                setText("")
                # verification toute les x sec
                    #time.sleep(1)

    def send(self,text):
        textn = unicodedata.normalize('NFKD', text).encode('ascii', 'ignore').decode("utf-8")
        list_word = textn.split(" ")
        l1=""
        l2=""
        while len(list_word) > 0:
            l1=""
            l2=""
            l1 = self.ligne(list_word,"")
            l2 = self.ligne(l1[0],"")
            print("l1 "+ str(l1))
            print("l2 "+ str(l2))
            tab = l2[0]
            self.q.put(l1[1]+"\n"+l2[1])
            list_word = l2[0]

    def ligne(self, array, text):
        # if we don't have more word to add
        if len(array) == 0:
            print("--- ligne: plus de mots a afficher ---")
            return (array, text)
        # if word lenght are superior to 12
        elif len(array[0]) > 12:
            print("--- ligne: mot > 12 ---")
            width = 12 - 1 - len(text)
            tx = text + ' ' + str(array[0][:width])
            array[0] = "-" + str(array[0][width:])
            return (array, tx)
        # if we are unable to add
        elif len(text)+len(array[0])+1>12:
            print("--- ligne: complete pas possible d'ajouter ---")
            # Si mot de pile 12 caractere
            if len(array[0])==12:
                return ([], array[0])
            else:
                return (array, text)
        else:
            # add first word and recursive
            print("--- ligne: descend, ajout premier mot inot recursivité ---")
            return self.ligne(array[1:],text+" "+array[0])
