import matplotlib.pyplot as plt
import csv
import os


def get_all_csv():
    dossier = '../data/csv/'
    files = []
    
    for file in os.listdir(dossier):
        if file.endswith('.csv'):
            files.append(f"../data/csv/{file}")
    return files

def is_dec(elem: str):
    for e in elem:
        if e.isnumeric() or e == ".":
            continue
        else:
            return False
    return True

def generate_camembert(array: dict):
    titles = []
    values = []
    
    nb = 0
    for key, value in array.items():
        titles.append(key.replace("_", " "))
        values.append(value)
        nb += 1
        if(nb == 20):
            break
    
    plt.pie(values, labels=titles, autopct="%1.1f%%")
    
    plt.title("Pourcentage de livre dans chaque catégorie")
    print(sum(values))
    plt.show()

def generate_histo(array : dict):
    values = []
    genre = []
    n = 1
    for key, value in array.items():
        values.append(value)
        if(len(key.split("_")) != 1):
            genre.append(str(key.split("_")[0][0]) + str(key.split("_")[1][0])+ "_"+str(n))
        else:
            genre.append(key[0] + "_"+str(n))
        n += 1
    print(len(genre))
    plt.bar(genre, values)
    plt.ylabel("Prix Moyen")
    plt.xlabel("Genre Livres")
    plt.legend()
    plt.show()

total_book =  0
folder_files = get_all_csv()
camembert = {}
histo = {}


for file in folder_files:
    with open(file, newline='') as csv_file:
        reader = csv.reader(csv_file, delimiter=',', quotechar='|')
        
        total_price = 0
        total_book_genre = -1
        
        for row in reader:
            total_book += 1
            total_book_genre += 1
            
            if(is_dec(row[3])):
                total_price += float(row[3])
                #print(row[3])
            elif(is_dec(row[4])):
                total_price += float(row[4])
                #print(row[4])
            else: continue
        genre = file.replace("../data/csv/", "").replace(".csv", "")
        camembert[genre] = total_book_genre
        histo[genre] = total_price / total_book_genre


camembert = dict(sorted(camembert.items(), key=lambda item: item[1], reverse=True))
histo = dict(sorted(histo.items(), key=lambda item: item[1], reverse=True))

for key,value in camembert.items():
    camembert[key] = (value / total_book) * 100

print(camembert)
generate_camembert(camembert)
generate_histo(histo)