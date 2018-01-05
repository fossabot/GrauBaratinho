from json import loads
import re
from time import sleep
from os import system
from win10toast import ToastNotifier
from openpyxl import Workbook
from requests import get
from sys import exit

toaster = ToastNotifier()

# variaveis
IDs = []
Produtos = []
Quantidade = []
CustoBenef = []
Preco = []
# Pegar os IDs - Retorna a lista IDs:


def getlistaids():
    print("Pegando os IDs....")
    print("\n")
    global IDs
    try:
        for i in range(0, 100):
            url = r"https://api.gpa.digital/pa/products/list/secoes/C4215/cervejas?storeId=501&qt=12&s=&ftr=facetSubShelf_ss%3A4215_Cervejas&p=" + \
                str(i)
            pagina = get(url).text
            for x in range(0, 12):
                IDs.append(
                    int(loads(pagina)["content"]["products"][x]["id"]))
    except IndexError:
        None

    # Cervejas Especiais

    try:
        for i in range(0, 100):
            url = r"https://api.gpa.digital/pa/products/list/secoes/C4215/cervejas-especiais?storeId=501&qt=12&s=&ftr=facetSubShelf_ss%3A4215_Cervejas__facetSubShelf_ss%3A4215_Cervejas%20Especiais&p=" + \
                str(i)
            pagina = get(url).text
            for x in range(0, 12):
                IDs.append(
                    int(loads(pagina)["content"]["products"][x]["id"]))
    except IndexError:
        None
    print("{} IDs importados com sucesso!".format(len(IDs)))
    return


def getdetails(listaids):
    global Produtos
    global Preco
    global Quantidade
    p = 0
    i = 0
    total = len(listaids)
    for ids in listaids:
        url = r"https://api.gpa.digital/pa/products/" + \
            str(ids) + r"?storeId=501&isClienteMais=false"
        Produtos.append(str(loads(get(url).text)
                            ["content"]["name"]).strip())
        q = loads(get(url).text)["content"]["totalQuantity"]
        if q == 0:
            Quantidade.append(1)
        else:
            Quantidade.append(int(loads(get(url).text)[
                              "content"]["totalQuantity"]))
        p = round(float(loads(get(url).text)
                        ["content"]["currentPrice"]), 2)
        if p == 0:
            p = "Indisponível"
        Preco.append(p)
        i = i + 1
        print("Pegando informações {} de {}".format(i, total))
    return


def getVolume(Produto):
    volumeRegex = re.compile("(\d+)([ ]*)(ml|litro|litros)+", re.IGNORECASE)
    result = volumeRegex.findall(Produto)
    if len(result) > 0:
        volume = result[0][0]
        volume = int(volume)
        if "litro" in (item.lower() for item in result[0]):
            volume *= 1000
    else:
        volume = "Indisponível"
    return volume


def joganaplan():
    wb = Workbook()
    ws = wb.active
    ws.append(["Link", "Produtos", "Quantidade",
               "Volume", "Preco", "Custo Benefício", "Preço Unidade"])
    cont = 1
    total = len(IDs)
    for i in range(0, len(IDs)):
        try:
            ws.append([(("https://www.paodeacucar.com/produto/" + str(IDs[i]))), (str(Produtos[i]).strip()), Quantidade[i], getVolume(
                Produtos[i]), Preco[i], round(float((Preco[i] / (getVolume(Produtos[i]) * Quantidade[i]))), 6),(Preco[i]/Quantidade[i])])
        except:
            ws.append([(("https://www.paodeacucar.com/produto/" + str(IDs[i]))), (str(Produtos[i]).strip()), Quantidade[i], getVolume(
                Produtos[i]), Preco[i],"Indisponível", "Indisponível"])
        print("Jogando na planilha item {} de {}".format(cont, total))
        cont += 1
    ws.auto_filter.ref = "A1:G1000"
    for col in ws.columns:
        max_length = 0
        column = col[0].column  # Get the column name
        for cell in col:
            try:  # Necessary to avoid error on empty cells
                if len(str(cell.value)) > max_length:
                    max_length = len(cell.value)
            except:
                pass
        adjusted_width = (max_length + 2) * 1.2
        ws.column_dimensions[column].width = adjusted_width
    wb.save("Brejinhas.xlsx")
    print("Salvo em Excel!")
    return


try:
    print("Olá, eu sou o Bot do Grau Baratinho! :)")
    print("\n")
    print("Fui desenvolvido pelo Magui Pica e estou na versão 0.3!")
    print("\n")
    print("Borá Chapar?")
    print("\n")
    input("Manda um enter para chamar as brejinhas!")
    system('CLS')

    getlistaids()
    sleep(1)
    print("\n")
    getdetails(IDs)
    print("\n")
    joganaplan()
    print("\n")
    print("Agora é só curtir :)")
    try:
        toaster.show_toast("Finalizado com sucesso Parça!",
                        "{} Brejinhas foram adicionadas na sua planilha de Excel :)".format(len(IDs)))
    except:
        print("Notificação falhou :(")
    print("\n")
    input("Press Enter to exit, Bitch!")
    exit()
except:
    print("Deu pau :( ")
