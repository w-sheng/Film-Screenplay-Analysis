import csv
import math
import os
import re
import tarfile
import sys

import matplotlib.pyplot as plt
import networkx as nx
import numpy as np
import pandas as pd

class ScreenplayModel(object):
    ''' A model representing a movie screenplay, its characters, 
    and its social networks. '''
    
    def __init__(self, film, format):
        self.title = film.replace('.tar.gz','')
        self.script_format = format
        
        # script, characters, lines
        self.text = ''
        self.lines = []
        self.characters = {}
        self.sorted_char = {}
        self.main_chars = {} # dict of main characters to number of lines
        self.char_lines = {}
        self.num_char_lines = 0

        # social network
        self.interactions = {} # keyed by character-pairs
        self.char_interactions = {} # keyed by characters
        self.sorted_interactions = {} 
        self.main_to_main = {} # main chac to main char interactions
        self.main_to_all = {} # main char to everyone interactions
        self.char_network = {}
        self.G = nx.Graph()
        self.graph_chars = []
        self.graph_chars_size = []

        self.load_init(film)
        self.load_script()
        self.update_main_chars()
        self.update_interactions()
        self.construct_graph()


    # =====================================================
    # INITIALIZING
    # =====================================================
    def load_init(self, film):
        sb_path = '/data/scriptbase/scriptbase_alpha/'
        tf = tarfile.open(os.getcwd() + sb_path + film, mode='r')
        
        try: 
            f_script = tf.extractfile('./' + self.title + '/script.txt')
        except:
            f_script = tf.extractfile(self.title + '/script.txt')
        self.text = f_script.read().decode('utf-8')

        
    def load_script(self):
        for line in self.text.split('\n'):
            if line.strip() != '':
                self.lines.append(line)

        self.parse_script()

    def parse_script(self):
        if (self.script_format == 1):
            self.parse_script1()
        elif (self.script_format == 2):
            self.parse_script2()
        elif (self.script_format == 3):
            self.parse_script3()
        elif (self.script_format == 4):
            self.parse_script4()
        elif (self.script_format == 5):
            self.parse_script5()
        elif (self.script_format == 6):
            self.parse_script6()

    def update_main_chars(self):
        self.sorted_char = {k: v for k,v in sorted(self.characters.items(), 
            key=lambda item: item[1], reverse=True)}
        
        top_char = ''
        for k,v in self.sorted_char.items():
            top = v
            break
        for k,v in self.sorted_char.items():
            if v >= (top * 0.3):
                self.main_chars[k] = v
            else:
                break
            prev = v

    def update_interactions(self):
        self.interactions = {k: v for k,v in sorted(self.interactions.items(), 
            key=lambda item: item[1], reverse=True)}
        
        self.update_main_to_all()
        self.update_main_to_main()
    
      



    # =====================================================
    # GRAPH METHODS
    # =====================================================       
    def construct_graph(self):
        ''' Constructs film's social network graph. '''

        # add nodes
        graph_dict = {k: self.characters[k] for k in self.characters.keys() 
            if self.characters[k] > 1}

        self.graph_chars = graph_dict.keys()
        self.graph_chars_size = list(graph_dict.values())
        self.G.add_nodes_from(self.graph_chars)
        
        # add edges
        edges = []
        for i in self.interactions.items():
            chars = list(i[0])
            weight = i[1]
            if (chars[0] in self.graph_chars and chars[1] in self.graph_chars):
                e = (chars[0], chars[1], weight)
                edges.append(e)
        self.G.add_weighted_edges_from(edges)

    def draw_graph(self, df):
        plt.figure(figsize=(15,12))
        pos = nx.nx_agraph.graphviz_layout(self.G)
        sizes_scaled = [60 * s for s in self.graph_chars_size]
        edge_weights = [d['weight'] / 4 for (_,_,d) in self.G.edges(data=True)]

        main_list = self.main_chars.keys()
        node_colors = []
        for c in self.graph_chars:
            if c in main_list:
                g = self.get_gender(df, c)
                if (g == 1.0):
                    node_colors.append('pink')
                elif (g == 0.0):
                    node_colors.append('skyblue')
                else:
                    node_colors.append('purple')
            else:
                node_colors.append('gray')

        nx.draw(self.G, pos=pos, with_labels=True, nodelist=self.graph_chars, 
            node_color=node_colors, node_size=sizes_scaled) 
        nx.draw_networkx_edges(self.G, pos=pos, width=edge_weights)

        plt.title('Social Network of ' + self.title, fontsize=36)
        plt.savefig(self.title + '.png')
        plt.show() 

    def construct_char_graph(self, c):
        char_G = nx.Graph()
        
        # add nodes
        graph_dict = {k: self.characters[k] for k in self.main_to_all[c].keys() 
            if self.characters[k] > 1}
        graph_dict[c] = self.characters[c]

        graph_chars = graph_dict.keys()
        graph_chars_size = list(graph_dict.values())
        char_G.add_nodes_from(graph_chars)
        
        # add edges
        edges = []
        for i in self.main_to_all[c].items():
            char = i[0]
            weight = i[1]
            if (char in graph_chars):
                e = (c, char, weight)
                edges.append(e)
        char_G.add_weighted_edges_from(edges)
        
        return char_G, graph_chars, graph_chars_size

    def draw_char_graph(self, c, df):
        plt.figure(figsize=(20,18))
        char_G, graph_chars, graph_chars_size = self.construct_char_graph(c)
        pos = nx.nx_agraph.graphviz_layout(char_G)
        sizes_scaled = [60 * s for s in graph_chars_size]
        edge_weights = [d['weight'] / 4 for (_,_,d) in char_G.edges(data=True)]

        main_list = list(self.main_to_main[c].keys())
        main_list.append(c)
        node_colors = []
        for c in graph_chars:
            if c in main_list:
                g = self.get_gender(df, c)
                if (g == 1.0):
                    node_colors.append('pink')
                elif (g == 0.0):
                    node_colors.append('skyblue')
                else:
                    node_colors.append('purple')
            else:
                node_colors.append('gray')

        nx.draw(char_G, pos=pos, with_labels=False, nodelist=graph_chars, 
            node_color=node_colors, node_size=sizes_scaled) 
        nx.draw_networkx_labels(char_G, pos=pos, font_size=24)
        nx.draw_networkx_edges(char_G, pos=pos, width=edge_weights)
        
        female = mpatches.Patch(color='pink', label='female')
        male = mpatches.Patch(color='skyblue', label='male')
        minor = mpatches.Patch(color='gray', label='minor')
        plt.legend(handles=[female, male, minor], prop={'size': 24})
        
        plt.title('Social Network of ' + c + ' in ' + self.title, fontsize=36)
        plt.savefig(self.title + ' - ' + c + '.png')
        plt.show() 




    # =====================================================
    # CHARACTER METHODS
    # =====================================================
    def get_protag(self):
        ''' Returns a the name of the protagonist name. '''

        (protag,_) = list(self.main_chars.items())[0]
        return protag

    def plot_char_lines(self):
        plt.figure(figsize=((6,4)))
        plt.bar(range(len(self.sorted_char)), list(self.sorted_char.values()), align='center', color='skyblue')
        plt.tick_params(axis='x', which='both', bottom=False, top=False, labelbottom=False)
        plt.title('Distribution of Character Lines in ' + self.title)
        plt.xlabel('Characters')
        plt.ylabel('Number of Lines')
        plt.show()
    
    # def get_gender(self, df, c):
    #     g = df[(df['film'] == self.title) & (df['main_char'] == c)]['gender']
    #     if (len(g.tolist()) > 0):
    #         return g.tolist()[0]
    #     else:
    #         return -1

    def get_char_lines_ratio(self, c):
        ''' Given a main character c, returns the ratio of lines c has
            over the total number of lines in the film. '''

        num_lines = self.main_chars[c]
        num_all_lines = sum(self.characters.values())
        lines_ratio = num_lines / num_all_lines
        
        return lines_ratio
        
    def get_char_intxns(self, c):
        ''' Gets the interactions of a main character.

            c: a main character
            returns: a tuple of dictionaries; 
                     the first is keyed on other main characters, mapped to
                     number of interactions;
                     the second is keyed on all other characters, mapped to
                     number of interactions. '''

        main_intxns = self.main_to_main[c]
        all_intxns = self.main_to_all[c]
        
        return main_intxns, all_intxns
 
    def remove_char_names(self, upper_names, text_to_clean):
        ''' Removes all character names from text_to_clean.

            upper_names: list of entire cast's names in upper case.
            text_to_clean: a list of strings (e.g., lines, directions).

            returns: a single string of text_to_clean with names removed. '''

        result = []
        for l in text_to_clean:
            new_line = re.sub(r'[.,?!]', '', l)
            lines = new_line.split()
            for token in lines:
                if token.upper() in upper_names:
                    new_line = new_line.replace(token, '')
            result.append(new_line)

        return " ".join(str(s).strip() for s in result)




    # =====================================================
    # INITIALIZING HELPER METHODS
    # =====================================================

    def add_character(self, c):
        ''' Updates given character name c in model's list of characters,
            and increments count of number of lines. '''

        if c in self.characters:
            self.characters[c] += 1
        else:
            self.characters[c] = 1

    def add_interaction(self, curr_char, c):
        ''' Updates interaction of given character names curr_char and c 
            in model's list of character interactions, and increments 
            count of number of interactions. '''

        if (curr_char != '') and (c != curr_char):
            intxn = frozenset([curr_char,c])
            if intxn in self.interactions:
                self.interactions[intxn] += 1
            else:
                self.interactions[intxn] = 1

    def confirm_not_char(self, c):
        ''' Checks if given name c contains direction words. '''

        dir_strs = ['INTERIOR','EXTERIOR','INT.','EXT.','INT','EXT','DISSOLVE','CLOSEUP','CUT TO','CUT BACK TO','FADE OUT','FADE IN','FADE TO','VIEW ON','CLOSE ON','ANGLE ON','CLOSER ANGLE','HIGH ANGLE','WIDE ANGLE','WIDER ANGLE','WIDE SHOT','FULL SHOT','CLOSE SHOT','MED. SHOT','CONTINUED','(CONTINUED)','(MORE)','IN THE']
        non_char_upper = False
        for d in dir_strs:
            if d in c:
                non_char_upper = True

        return (non_char_upper or c == '')

    def parse_script1(self):
        curr_char = ''
        for l in self.lines:
            if l.isupper(): # potentially a character
                # parse char name
                c = ''
                c = re.sub('\s*\(.+\)', '', l)
                c = re.sub(']', '', c)
                c = re.sub(':', '', c)
                c = c.strip()

                if (self.confirm_not_char(c)):
                    continue

                # this is a character!
                self.add_character(c)
                self.add_interaction(curr_char, c)

                curr_char = c # update char as new previous speaking character
            
            else: # not a character -- parse as dialogue or direction
                if curr_char != '':
                    self.num_char_lines += 1
                    if re.match(r'\s', l):
                        if curr_char in self.char_lines:
                            self.char_lines[curr_char].append(l.strip())
                        else:
                            self.char_lines[curr_char] = [l.strip()]
                    else:
                        char_dir = 'DIRECTIONS - ' + curr_char
                        if char_dir in self.char_lines:
                            self.char_lines[char_dir].append(l.strip())
                        else:
                            self.char_lines[char_dir] = [l.strip()]

    def parse_script2(self):
        curr_char = ''
        for l in self.lines:
            match = re.match('([A-Z].*):(.*)', l.strip())
            if (match != None): # potentially a character
                # parse char name
                c = match.group(1)
                no_actions = re.match('(.*)( \[.*\])', c)
                if no_actions:
                    c = no_actions.group(1)
                
                if (self.confirm_not_char(c)):
                    continue

                # this is a character!
                self.add_character(c)
                self.add_interaction(curr_char, c)

                # include this character's dialogue
                dialogue = match.group(2)
                if c in self.char_lines:
                    self.char_lines[c].append(dialogue.strip())
                else:
                    self.char_lines[c] = [dialogue.strip()]
                self.num_char_lines += 1

                curr_char = c # update char as new previous speaking character

            else: # not a character -- parse as dialogue
                if curr_char != '':
                    self.num_char_lines += 1
                    if curr_char in self.char_lines:
                        self.char_lines[curr_char].append(l.strip())
                    else:
                        self.char_lines[curr_char] = [l.strip()]

    def parse_script3(self):
        curr_char = ''
        for l in self.lines:
            match = re.match('([A-Z]*) (.*)', l)
            if (match != None): # potentially a character
                # parse char name
                c = match.group(1)
                no_actions = re.match('(.*)( \[.*\])', c)
                if no_actions:
                    c = no_actions.group(1)
                
                if (self.confirm_not_char(c)):
                    continue

                # this is a character!
                self.add_character(c)
                self.add_interaction(curr_char, c)

                # include this character's dialogue
                dialogue = match.group(2)
                if c in self.char_lines:
                    self.char_lines[c].append(dialogue.strip())
                else:
                    self.char_lines[c] = [dialogue.strip()]
                self.num_char_lines += 1

                curr_char = c # update char as new previous speaking character

            else: # not a character -- parse as dialogue
                if curr_char != '':
                    self.num_char_lines += 1
                    if curr_char in self.char_lines:
                        self.char_lines[curr_char].append(l.strip())
                    else:
                        self.char_lines[curr_char] = [l.strip()]

    def parse_script4(self):
        curr_char = ''
        for l in self.lines:
            match = re.match('([A-Za-z]*) -', l.strip())
            if (match != None): # potentially a character
                # parse char name
                c = match.group(1)
                no_actions = re.match('(.*)( \[.*\])', c)
                if no_actions:
                    c = no_actions.group(1)
                
                if (self.confirm_not_char(c)):
                    continue

                # this is a character!
                self.add_character(c)
                self.add_interaction(curr_char, c)

                curr_char = c # update char as new previous speaking character

            else: # not a character -- parse as dialogue
                if curr_char != '':
                    self.num_char_lines += 1
                    if curr_char in self.char_lines:
                        self.char_lines[curr_char].append(l.strip())
                    else:
                        self.char_lines[curr_char] = [l.strip()]

    def parse_script5(self):
        curr_char = ''
        for l in self.lines:
            if (' ' not in l.strip()): # potentially a character
                # parse char name
                c = l.strip()
                
                if (self.confirm_not_char(c)):
                    continue

                # this is a character!
                self.add_character(c)
                self.add_interaction(curr_char, c)

                curr_char = c # update char as new previous speaking character

            else: # not a character -- parse as dialogue
                if curr_char != '':
                    self.num_char_lines += 1
                    if curr_char in self.char_lines:
                        self.char_lines[curr_char].append(l.strip())
                    else:
                        self.char_lines[curr_char] = [l.strip()]

    def parse_script6(self):
        curr_char = ''
        for l in self.lines:
            match = re.match('\[ ([A-Za-z]+) \]', l.strip())
            if (match != None): # potentially a character
                # parse char name
                c = match.group(1)
                
                if (self.confirm_not_char(c)):
                    continue

                # this is a character!
                self.add_character(c)
                self.add_interaction(curr_char, c)

                curr_char = c # update char as new previous speaking character

            else: # not a character -- parse as dialogue
                if curr_char != '':
                    self.num_char_lines += 1
                    if curr_char in self.char_lines:
                        self.char_lines[curr_char].append(l.strip())
                    else:
                        self.char_lines[curr_char] = [l.strip()]

    def update_main_to_all(self):
        ''' Updates all main characters interactions to all other
            characters in the film. '''

        main_list = list(self.main_chars.keys())
        main_to_all = {}
        
        for m in main_list:
            other_mains = list.copy(main_list)
            other_mains.remove(m)
            m_int = {}
            for o in other_mains:
                m_int[o] = 0
            main_to_all[m] = m_int
        
        for (cs,n) in self.interactions.items():
            cs_list = list(cs)
            if len(cs_list) > 1:
                c1 = cs_list[0]
                c2 = cs_list[1]

                if c1 in main_list: 
                    c1_int = main_to_all[c1]
                    c1_int[c2] = n
                if c2 in main_list: 
                    c2_int = main_to_all[c2]
                    c2_int[c1] = n
        
        self.main_to_all = main_to_all

    def update_main_to_main(self):
        ''' Updates all main characters interactions to all other
            main characters in the film. '''

        main_list = list(self.main_chars.keys())
        main_to_main = {}

        for (m,ints) in self.main_to_all.items():
            m_int = {}
            m_int['Other'] = 0

            for (c,f) in ints.items():
                if c in main_list:
                    m_int[c] = f
                else:
                    m_int['Other'] += f

            main_to_main[m] = m_int

        self.main_to_main = main_to_main

        