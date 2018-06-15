from collections import defaultdict
from PIL import Image
import numpy as np

def tsvtodata(filename, signtoid):
    to_return = []
    lines = []
    datafile = open(filename, "r")
    for line in datafile:
        lines.append(line.split('\n')[0])
    keys = lines[0].split('\t')
    for line in lines[1:]:
        values = line.split('\t')
        entry = defaultdict()
        for i in range(0, len(keys)):
            if (i in range(1, 6)):
                entry[keys[i]] = signtoid[values[i]]
            else: 
                entry[keys[i]] = values[i]
        to_return.append(entry)
    to_return = np.array(to_return)
    return to_return
def imgstodata(directory, ydata):
    if directory[-1] != '/':
        directory = directory + '/'
    to_return = []
    for entry in ydata:
        img = Image.open(('data/' + entry['ID'] + '.png'))
        img = img.convert('L')
        img = img.resize((64, 64), Image.BILINEAR)
        img = np.array(img)
        img = img < 90
        img = np.reshape(img, (64, 64, 1))
        img = img.astype(np.float32)
        to_return.append(img)
    to_return = np.array(to_return)
    return to_return
def toromanization(predictions, idtosign):
    to_return = predictions
    for entry in to_return:
        romanization = idtosign[entry['base']]
        if entry['adjunct'] != 0:
            romanization = romanization + idtosign[entry['adjunct']]
        if idtosign[entry['base']] not in ['a', 'i', 'I', 'u', 'U', 'R', 'RR', 'lR' ,'lRR', 'e', 'ai', 
                             'o', 'au'] and entry['vowel'] != 1:
            if entry['vowel'] == 0:
                romanization = romanization + 'a'
            else:
                romanization = romanization + idtosign[entry['vowel']]
        if entry['anusvara'] == 1:
            romanization = romanization + 'M'
        if entry['visarga'] == 1:
            romanization = romanization + 'H'
        entry['result'] = romanization
    return to_return
