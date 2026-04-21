# merge sort puro sem funções de terceiros, sem bibliotecas.


def merge_sort(lista):
    if len(lista) > 1:
        # Encontra o meio do vetor
        metade = len(lista) // 2
        esquerda = lista[:metade]  # Subvetor da esquerda
        direita = lista[metade:]  # Subvetor da direita

        # Chamada recursiva para cada metade
        print(f"Dividindo: {lista} -> Esquerda: {esquerda}, Direita: {direita}")
        merge_sort(esquerda)
        merge_sort(direita)
        print(f"Conquistando: Esquerda: {esquerda}, Direita: {direita}")

        i = j = k = 0

        # Combina os subvetores ordenados (Merge)
        while i < len(esquerda) and j < len(direita):
            if esquerda[i] < direita[j]:
                lista[k] = esquerda[i]
                i += 1
                print(f"Mesclando: {lista[:k+1]}")
            else:
                lista[k] = direita[j]
                j += 1
                print(f"Mesclando: {lista[:k+1]}")

            k += 1

        # Verifica se restou algum elemento
        while i < len(esquerda):
            lista[k] = esquerda[i]
            i += 1
            k += 1
            print(f"Mesclando: {lista[:k+1]}")

        while j < len(direita):
            lista[k] = direita[j]
            j += 1
            k += 1
            print(f"Mesclando: {lista[:k+1]}")

    return lista

print("---- Merge Sort ---")
print(merge_sort([38, 27, 43, 3, 9, 82, 10]))