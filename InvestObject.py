import requests
from bs4 import BeautifulSoup
from termcolor import colored


class Spolka:
    def __init__(self, web_adress, colorized):
        self.web_adress = web_adress
        self.name_of_invest = "---"
        self.short_name = "---"

        self.wartosc = "00,00"
        self.wartosc_minimalna = "00,00"
        self.wartosc_maksymalna = "00,00"
        self.zmiana_proc = "0,00%"

        self.wol_obrotu = "0 000"
        self.wart_obrotu = "00 000,00"
        self.oferta_kupna = "00.0000"
        self.oferta_sprzedazy = "00.0000"
        try:
            req = requests.get(self.web_adress)
            if "gpw.pl/spolka?isin=" not in self.web_adress:
                if colorized:
                    print(colored("Strona: " + self.web_adress + " nie jest poprawna strona gpw!", 'red'))
                else:
                    print("Strona: " + self.web_adress + " nie jest poprawna strona gpw!")
            else:
                soup = BeautifulSoup(req.text, "html.parser")
                soup = soup.find('body')
                check1 = False
                for header in soup.find_all(class_="col-sm-6"):
                    for small_id in header.find_all(id="getH1"):
                        self.name_of_invest = small_id.contents[0].strip("\n").replace(" ", "").strip("\t")
                        self.name_of_invest = self.name_of_invest[:self.name_of_invest.index("(")]
                        check1 = True
                        break
                    if check1:
                        break
                if self.name_of_invest != "---":
                    print("  1/2  ", end="")
                for header in soup.find_all(class_="PaL header text-right text-left-xs"):
                    check1 = False
                    for small_id in header.find_all(class_="loss"):
                        self.zmiana_proc = str(small_id)[16:-4]
                        check1 = True
                        break
                    if not check1:
                        for small_id in header.find_all(class_="profit"):
                            if "0,00%" not in str(small_id):
                                self.zmiana_proc = str(small_id)[18:-4]
                            else:
                                self.zmiana_proc = str(small_id)[38:-4]
                            break
                    for small_id in header.find_all(class_="summary"):
                        self.wartosc = small_id.contents[0]
                        break
                    for small_id in header.find_all(class_="max_min"):
                        self.wartosc_minimalna = (str(small_id.contents[0]).strip()[4:])
                        self.wartosc_maksymalna = (str(small_id.contents[2]).strip()[4:])
                        break
                    break
                for header in soup.find_all(class_="table table-borderLess table-sm"):
                    for small_id in header.find_all(align="right"):
                        try:
                            self.wol_obrotu = small_id.contents[0]
                        except IndexError:
                            self.wol_obrotu = small_id.contents
                        break
                    break
                for header in soup.find_all(class_="table table-borderLess table-sm font18 margin-bottom-0"):
                    count = 0
                    for small_id in header.find_all(align="right"):
                        if count == 0:
                            self.oferta_kupna = small_id.contents[0]
                            count += 1
                        elif count == 1:
                            self.oferta_sprzedazy = small_id.contents[0]
                            count += 1
                        elif count == 2:
                            self.wart_obrotu = small_id.contents[0]
                            break
                    break
                if self.name_of_invest != "---":
                    print("  2/2    ", end="")
                req = requests.get(self.web_adress + "#infoTab")
                soup = BeautifulSoup(req.text, "html.parser")
                soup = soup.find('body')
                for header in soup.find_all(id="glsSkrot"):
                    self.short_name = str(header)[42:-3]
                    break
                self.wart_obrotu = self.wart_obrotu.replace(",", " ") + "0"
                if self.name_of_invest != "---":
                    if colorized:
                        print(colored("Zaladowano strone!", 'yellow'))
                    else:
                        print("Zaladowano strone!")
        except requests.exceptions.MissingSchema:
            if colorized:
                print(colored("Strona: " + self.web_adress + " nie istnieje!", 'red'))
            else:
                print("Strona: " + self.web_adress + " nie istnieje!")
        except (requests.exceptions.ConnectionError, AttributeError):
            if colorized:
                print(colored("Brak polaczenia z internetem lub blad strony gpw!", 'red'))
            else:
                print("Brak polaczenia z internetem lub blad strony gpw!")
