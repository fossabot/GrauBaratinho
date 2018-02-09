import json
import re
from os import system
from time import sleep
from openpyxl import Workbook
from requests import get
from win10toast import ToastNotifier

toaster = ToastNotifier()

# variaveis
IDs = []
Produtos = []
Quantidade = []
CustoBenef = []
Preco = []
Tipo = []
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
                    int(json.loads(pagina)["content"]["products"][x]["id"]))
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
                    int(json.loads(pagina)["content"]["products"][x]["id"]))
    except IndexError:
        None
    print("{} IDs importados com sucesso!".format(len(IDs)))
    return


def getdetails(listaids):
    global Produtos
    global Preco
    global Quantidade
    i = 0
    total = len(listaids)

    for ids in listaids:
        pagina = get("https://api.gpa.digital/pa/products/" +
                    str(ids) + "?storeId=501&isClienteMais=false").text
        Produtos.append(str(json.loads(pagina)["content"]["name"]).strip())
        if json.loads(pagina)["content"]["stock"] == True:
            Preco.append(
                round(float(json.loads(pagina)["content"]["currentPrice"]), 2))
            q = int(json.loads(pagina)["content"]["totalQuantity"])
            if q == 0:
                q = 1
                Quantidade.append(q)
            else:
                Quantidade.append(q)
        else:
            Preco.append("Indisponível")
            Quantidade.append("Indisponível")
        i = i + 1
        print("Pegando informações {} de {}".format(i, total))
        Tipo.append(
            str(json.loads(pagina)["content"]["shelfList"][0]["name"]).strip())
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
    ws.append(["Link", "Tipo", "Produtos", "Quantidade",
            "Volume", "Preco", "Custo Benefício", "Preço Unidade"])
    cont = 1
    total = len(IDs)
    for i in range(0, len(IDs)):
        try:
            ws.append([(("https://www.paodeacucar.com/produto/" + str(IDs[i]))), Tipo[i], (str(Produtos[i]).strip()), Quantidade[i], getVolume(
                Produtos[i]), Preco[i], round(float((Preco[i] / (getVolume(Produtos[i]) * Quantidade[i]))), 6), round((Preco[i] / Quantidade[i]), 2)])
        except:
            ws.append([(("https://www.paodeacucar.com/produto/" + str(IDs[i]))), Tipo[i], (str(Produtos[i]).strip()), Quantidade[i], getVolume(
                Produtos[i]), Preco[i], "Indisponível", "Indisponível"])
        print("Jogando na planilha item {} de {}".format(cont, total))
        cont += 1
    ws.auto_filter.ref = "A1:H1000"
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
    system("mode con cols=60 lines=13")
    print("")
    print("Olá, eu sou o Bot do Grau Baratinho! :)")
    print("\n")
    print("Fui desenvolvido pelo Magui Pica e estou na versão 0.5!")
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
    x = input("Press Enter to exit, Bitch!")
except:
    print("Deu pau :( ")
