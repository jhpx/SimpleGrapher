# -*- coding: utf-8 -*-
import tkFileDialog
import pygraphviz as pgv
if __name__ == "__main__":
    csv_filename = tkFileDialog.askopenfilename()
    tree_data = [line.rstrip('\n').split(',')
                 for line in open(csv_filename, 'r')]

    # 抛弃头部
#   if tree_data[0][0].isdigit() is not True:
#       tree_data = tree_data[1:]

    # 指定id,label与pid对应的列号
#   COL_ID = 0
    COL_LABEL = 0
#   COL_PID = 3
    COL_NEXT = 1
    COL_TYPE = 2

    G = pgv.AGraph(rankdir='LR')
    G.node_attr['fontname'] = 'Simsun'
    G.edge_attr['fontname'] = 'Simsun'

    # 生成Label
    for line in tree_data:
        if(line[COL_TYPE] == '输入'):
            G.add_node(line[COL_LABEL].decode('utf8'), shape='box')
            G.add_node(line[COL_NEXT].decode('utf8'), shape='record')
            G.add_edge(
                line[COL_LABEL].decode('utf8'),
                line[COL_NEXT].decode('utf8')
            )
        elif(line[COL_TYPE] == '输出'):
            G.add_node(line[COL_LABEL].decode('utf8'), shape='record')
            G.add_node(line[COL_NEXT].decode('utf8'), shape='box')
            G.add_edge(
                line[COL_LABEL].decode('utf8'),
                line[COL_NEXT].decode('utf8')
            )
        elif(line[COL_TYPE] == '内容'):
            n = G.get_node(line[COL_LABEL].decode('utf8'))
            if (n==None):
                G.add_node(line[COL_LABEL].decode('utf8'),shape='record')
            content = line[COL_NEXT].decode('utf8')
            if(n.attr['label'] and n.attr['label']!='\N'):
                n.attr['label'] = n.attr['label'].rstrip('}') + '| ' + content + '}}'
            else:
                n.attr['label'] = '{ ' + n.name + '|{ ' + content + '}}'

    G.layout('dot')
    G.draw(csv_filename[:-4] + '.png')
