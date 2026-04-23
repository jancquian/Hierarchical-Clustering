import pandas as pd
import matplotlib
import ast
from scipy.cluster.hierarchy import dendrogram

matplotlib.use("TkAgg")
import matplotlib.pyplot as plt

def uploaddoc():
    doc_o = pd.read_csv("./iris.csv")
    #doc_o.drop(columns=["sepal.length", "sepal.width", "variety"], inplace=True)
    return doc_o

def compute_distances(o_dots):
    matrix = dict()
    claves = list()
    # 0 length, 1 width
    for a in range(0, len(o_dots)):
        if a not in claves:
            claves.append(a)
        for b in range(a, len(o_dots)):
            if a != b:
                dif_pl = o_dots.iloc[b, 2] - o_dots.iloc[a, 2]
                dif_pw = o_dots.iloc[b, 3] - o_dots.iloc[a, 3]
                dif_sl = o_dots.iloc[b, 0] - o_dots.iloc[a, 0]
                dif_sw = o_dots.iloc[b, 1] - o_dots.iloc[a, 1]
                distance = (dif_pl ** 2 + dif_pw ** 2 + dif_sl ** 2 + dif_sw ** 2 ) ** 0.5
                distance = round(float(distance), 3)
                matrix[frozenset((str(a), str(b)))] = distance
    return matrix, claves

def find_min(mat, patt):
    # a = -, b = |
    aux_d = (0,0)
    aux_l = float('inf') # Para minimo
    #aux_l = -1 # Para maximo
    for dup in mat:
        if mat[dup] < aux_l: # Para minimo
        #if mat[dup] > aux_l: # Para maximo
            aux_l = mat[dup]
            aux_d = dup
    s_a, s_b = tuple(aux_d)
    patt['('+str(s_a)+','+str(s_b)+')'] = aux_l
    return aux_d, aux_l, patt

def merge_dots(mat, clv, dup):
    # Se fusionan los puntos "a" y "b"
    dota, dotb = tuple(dup)
    for key in clv:
        fdota = frozenset((dota, str(key)))
        fdotb = frozenset((dotb, str(key)))
        if fdota in mat and fdotb in mat:
            max_dst = min(mat[fdota], mat[fdotb]) #A
            mat[frozenset(('('+str(dota)+","+str(dotb)+')',str(key)))] = max_dst
        elif fdota in mat and fdotb not in mat:
            mat[frozenset(('('+str(dota)+","+str(dotb)+')',str(key)))] = mat[fdota]
        elif fdotb in mat and fdota not in mat:
            mat[frozenset(('('+str(dota)+","+str(dotb)+')',str(key)))] = mat[fdotb]
    clv.append('('+str(dota) + "," + str(dotb)+')')

    # Se purgan las distancias relacionadas a "a" y "b"
    for key in clv:
        fdota = frozenset((dota, str(key)))
        fdotb = frozenset((dotb, str(key)))
        if fdota in mat:
            mat.pop(fdota)
        if fdotb in mat:
            mat.pop(fdotb)
    return mat, clv

def plot_dendrogram_from_dict_colors(data, labels_df, figsize=(6, 4)):
    parsed = {ast.literal_eval(k): v for k, v in data.items()}
    leaves = set()
    def collect(x):
        if isinstance(x, int):
            leaves.add(x)
        else:
            l, r = x
            collect(l)
            collect(r)

    for k in parsed.keys():
        collect(k)

    leaves = sorted(leaves)

    clusters = {}
    size = {i: 1 for i in leaves}
    Z = []
    next_id = max(leaves) + 1
    cache = {}

    def build(node):
        nonlocal next_id

        if isinstance(node, int):
            return node

        if node in cache:
            return cache[node]

        left, right = node
        left_id = build(left)
        right_id = build(right)

        key = tuple(sorted((left_id, right_id)))

        if key not in clusters:
            clusters[key] = next_id
            size[next_id] = size.get(left_id, 1) + size.get(right_id, 1)

            if node not in parsed:
                raise KeyError(f"Falta nodo en data: {node}")

            Z.append([
                left_id,
                right_id,
                float(parsed[node]),
                size[next_id]
            ])

            next_id += 1

        cache[node] = clusters[key]
        return clusters[key]

    root = max(parsed.keys(), key=lambda x: len(str(x)))
    build(root)

    # -----------------------------
    # plot
    # -----------------------------
    plt.figure(figsize=figsize)
    ddata = dendrogram(Z)

    # -----------------------------
    # colorear labels
    # -----------------------------
    ax = plt.gca()
    labels = ax.get_xmajorticklabels()

    # mapa clase -> color
    color_map = {
        "Setosa": "red",
        "Versicolor": "green",
        "Virginica": "blue"
    }

    # labels_df: DataFrame con índice = número (0..149) y columna "species"
    for lbl in labels:
        idx = int(lbl.get_text())
        species = labels_df.loc[idx, "variety"]
        lbl.set_color(color_map.get(species, "black"))

    plt.title("Dendrograma automático")
    plt.xlabel("Puntos")
    plt.ylabel("Distancia")
    plt.show()

if __name__ == '__main__':
    doc = uploaddoc()
    doc_c = doc.copy(deep=True)
    doc_c.drop(columns=["sepal.length", "sepal.width", "petal.length", "petal.width"], inplace=True)
    patron = dict()
    matrix, keys = compute_distances(doc)
    while True:
        dupla, distance, patron = find_min(matrix, patron)
        merge_dots(matrix, keys, dupla)
        if len(matrix) == 0:
            break
    plot_dendrogram_from_dict_colors(patron,doc_c, figsize=(15, 10))
