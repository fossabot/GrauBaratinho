from OPP import PDA
import os
import requests
from win10toast import ToastNotifier
from colorama import init, Fore, Back, Style


toaster = ToastNotifier()


def download_file(url):
    local_filename = url.split('/')[-1]
    # NOTE the stream=True parameter
    r = requests.get(url, stream=True)
    with open(local_filename, 'wb') as f:
        for chunk in r.iter_content(chunk_size=1024):
            if chunk:
                f.write(chunk)
    return local_filename


init(convert=True)

os.system("mode con cols=100 lines=35")
os.system(
    "title " + "Grau Baratinho                                                                                                                             By https://github.com/maguila93")

print(Fore.GREEN)


a = PDA()
a.set_option()
a.set_store()
a.run()
a.export_xlsx()

toaster = ToastNotifier()
toaster.show_toast("{} Products exported to Excel".format(len(a.IDs)),
                   "Excel will open automatically",
                   icon_path=download_file(
                       r"http://www.iconarchive.com/download/i91061/icons8/windows-8/Industry-Poison.ico"),
                   duration=3)


os.remove(os.path.dirname(os.path.abspath(__file__)) + r"\Industry-Poison.ico")

os.system(a.spreed_sheet_name + r".xlsx")

os.system(os.path.dirname(os.path.abspath(__file__)) + a.spreed_sheet_name)

quit()
