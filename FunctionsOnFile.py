from os import system, name
from sys import exit
from InvestObject import Spolka
from termcolor import colored
from platform import release


class SavedSites:
    def __init__(self, sett_file_name):
        try:
            with open(sett_file_name, 'r') as read_it:
                self.sett_name = sett_file_name
                self.text = read_it.read().split("\n")
                self.file_name = self.text[0]
        except FileNotFoundError:
            print("Brakuje pliku z ustawieniami!")
            input("XXX ")
            exit()
        self.color_it = False
        if release() == '10':
            self.color_it = True
            self.make_space()               # for colors
        self.color_info = "blue"
        self.color_bad = "red"
        self.spolki_objects = []
        self.actualize_invest()
        self.help = {
            "\tOpcje: ": self.color_info,
            "Dowiedz sie wiecej o programie: ": "/info",
            "Pokaz mozliwe opcje: ": "/help",
            "Zmien plik z zapisanymi stronami: ": "/name",
            "Sortuj strony w pliku alfabetycznie / po zysku procentowym: ": "/sort-a | /sort-p",

            "\tStrony: ": self.color_info,
            "Pokaz zapisane strony: ": "/sites",
            "Dodaj nowa strone: ": "/add",
            "Usun jedna strone / spolke: ": "/remove-*czesc nazwy lub strony internetowej*",
            "Wyczysc wszystkie zapisane strony: ": "/clear",

            "\tSpolki: ": self.color_info,
            "Pokaz zapisane spolki: ": "/invest",
            "Pokaz detalowe informacje o spolce: ": "/look-*czesc nazwy lub strony internetowej*",
            "Analiza wszystkich zapisanych spolek: ": "/look",
            "Pokaz najwieksze zyski: ": "/best",

            "\tKonsola: ": self.color_info,
            "Zrob miejsce na konsoli: ": "/space",
            "Powrot: ": "/back",
            "Wyjscie: ": "/exit",
            0: "exit"
        }

    @staticmethod
    def make_space():
        print()
        if name == 'nt':
            _ = system('cls')
        else:
            _ = system('clear')
        print()

    @staticmethod
    def more_info():
        print("\nJestem programem ktory przetrzyma strony z polskiej gieldy dla Ciebie i ulatwi ich przegladanie.")
        print("Po jednorazowym wskazaniu stron dla Ciebie interesujacych, bede w stanie wyszukiwac najwazniejsze informacje o danych spolkach.")
        print("Dzieki temu wszystkie Twoje (potencjalne) inwestycje z gieldy zawsze beda w jednym miejscu!")
        print("\nPlik z zapisanymi stronami moze byc aktualizowany manualnie, lecz nie w trakcie dzialania programu.")
        print("Zapisane manualnie strony powinny byc oddzielone pojedynczym klawiszem \"enter\".")
        print("Plik z opcjami nie powinien byc w zaden sposob modyfikowany.")
        print("\nProgram dziala w pelni poprawnie jedynie na systemie Windows 10.")

    def show_detail(self, obj):
        try:
            max_chars_2 = 34
            max_chars_3 = 68
            max_chars_4 = 88
            print("Strona: " + obj.web_adress + " " * (max_chars_3 - (len(obj.web_adress) + 8)), end="")
            if self.color_it:
                print("Nazwa: " + colored(obj.name_of_invest, 'blue') + " " * (max_chars_4 - (len(obj.name_of_invest) + 7 + max_chars_3)), end="")
                print("Skrot Nazwy: " + colored(obj.short_name, 'blue'))
            else:
                print("Nazwa: " + obj.name_of_invest + " " * (max_chars_4 - (len(obj.name_of_invest) + 7 + max_chars_3)), end="")
                print("Skrot Nazwy: " + obj.short_name)
            print("Wartosc teraz: " + obj.wartosc + " " * (max_chars_2 - (len(obj.wartosc) + 15)), end="")
            print("Wartosc minimalna: " + obj.wartosc_minimalna + " " * (max_chars_3 - (len(obj.wartosc_minimalna) + 19 + max_chars_2)), end="")
            print("Wartosc maksymalna: " + obj.wartosc_maksymalna)
            print("Zmiana procentowa: ", end="")
            if obj.zmiana_proc[0] == '+' and self.color_it:
                print(colored(obj.zmiana_proc, 'green'))
            elif self.color_it:
                print(colored(obj.zmiana_proc, 'red'))
            else:
                print(obj.zmiana_proc)
            print("Wolumin obrotu: " + obj.wol_obrotu + " " * (max_chars_2 - (len(obj.wol_obrotu) + 16)), end="")
            print("Wartosc obrotu: " + obj.wart_obrotu)
            print("Oferta kupna: " + obj.oferta_kupna + " " * (max_chars_2 - (len(obj.oferta_kupna) + 14)), end="")
            print("Oferta sprzedazy: " + obj.oferta_sprzedazy)
        except TypeError:                   # tymczasowy blad na stronie gpw
            if self.color_it:
                print(colored("Brak danych na stronie spolki! Manualna inspekcja wymagana!", self.color_bad))
            else:
                print("Brak danych na stronie spolki! Manualna inspekcja wymagana!")

    def look_for_name_or_site(self, the_value):
        the_value = the_value.replace(" ", "")
        for site in self.spolki_objects:            # look for exact
            if the_value == site.web_adress:
                return site
            elif the_value.upper() == site.name_of_invest:
                return site
            elif the_value == site.short_name:
                return site
        found_1 = False
        found_2 = False
        the_site = 0
        for site in self.spolki_objects:            # look for a bigger part
            if the_value.upper() in site.name_of_invest and not found_2:
                if not found_1:
                    the_site = site
                    found_1 = True
                else:
                    found_2 = True
            elif "gpw.pl/spolka?isin=" in site.web_adress and not found_2:
                if the_value in site.web_adress.replace("gpw.pl/spolka?isin=", ""):
                    if not found_1:
                        the_site = site
                        found_1 = True
                    else:
                        found_2 = True
        if the_site != 0 and not found_2:
            return the_site
        return 0

    def actualize_invest(self):
        try:
            with open(self.file_name, 'r') as sites_read:
                print("\nProsze zaczekac! Odczytywanie danych!")
                sites_list = sites_read.read().split("\n")
                self.spolki_objects = []
                for a_site in sites_list:
                    if a_site != "" and a_site not in "   ":
                        self.spolki_objects.append(Spolka(a_site, self.color_it))
        except FileNotFoundError:
            if self.color_it:
                print(colored("Nie znaleziono pliku ze stronami!", self.color_bad))
            else:
                print("Nie znaleziono pliku ze stronami!")
            self.change_sites_file_name()
            self.actualize_invest()

    def actualize_single_invest(self, individual_web_site, plus_minus):
        try:
            with open(self.file_name, 'r') as sites_read:
                individual_web_site = individual_web_site.replace(" ", "")
                sites_list = sites_read.read().split("\n")
                if plus_minus == 'plus':
                    if individual_web_site != "" and individual_web_site not in "   " and individual_web_site not in sites_list:
                        print("Wczytywanie!")
                        self.spolki_objects.append(Spolka(individual_web_site, self.color_it))
                elif plus_minus == 'minus':
                    if individual_web_site != "" and individual_web_site not in "   ":
                        for count in range(len(self.spolki_objects)):
                            if self.spolki_objects[count - 1].web_adress == individual_web_site:
                                self.spolki_objects.remove(self.spolki_objects[count - 1])
                    elif individual_web_site not in sites_list:
                        if self.color_it:
                            print(colored("Blad znalezienia podanej strony!", self.color_bad))
                        else:
                            print("Blad znalezienia podanej strony!")
        except FileNotFoundError:
            if self.color_it:
                print(colored("Nie znaleziono pliku ze stronami!", self.color_bad))
            else:
                print("Nie znaleziono pliku ze stronami!")
            self.change_sites_file_name()
            self.actualize_single_invest(individual_web_site, plus_minus)

    def show_invest(self):
        if len(self.spolki_objects) > 0:
            for spolka in self.spolki_objects:
                print(spolka.name_of_invest, end="")
                if spolka != self.spolki_objects[len(self.spolki_objects) - 1]:
                    print(" | ", end="")
            print()
        else:
            if self.color_it:
                print(colored("Brak zapisanych spolek!", self.color_bad))
            else:
                print("Brak zapisanych spolek!")

    def change_sites_file_name(self):
        old_text = self.text[1:]
        old_text = "\n".join(old_text)
        entered = " "
        first = True
        while " " in entered or "." in entered or "," in entered or entered == self.sett_name or len(entered) < 1:
            if not first:
                if self.color_it:
                    print(colored("Zla nazwa!", self.color_bad))
                else:
                    print("Zla nazwa!")
            entered = input("Wpisz nowa nazwe pliku ze stronami: ")
            first = False
        entered = entered + ".txt"
        new_text = entered + "\n" + old_text
        with open(self.sett_name, 'w') as write_here:
            write_here.write(new_text)
        self.text = new_text.split("\n")
        self.file_name = self.text[0]
        try:
            with open(self.file_name, 'r') as read:
                if self.color_it:
                    print(colored("Uzywanie istniejacego pliku!", self.color_info))
                else:
                    print("Uzywanie istniejacego pliku!")
        except FileNotFoundError:
            with open(self.file_name, 'w') as write:
                write.write("")
            if self.color_it:
                print(colored("Stworzono nowy plik!", self.color_info))
            else:
                print("Stworzono nowy plik!")
        self.actualize_invest()

    def show_options(self):
        print()
        for an_option in self.help:
            if an_option != 0:
                if an_option[0] != '\t':
                    print(an_option, end="")
                    print(self.help[an_option])
                else:
                    if self.color_it:
                        print(colored(an_option, self.help[an_option]))
                    else:
                        print(an_option)

    def add_new_site(self):
        with open(self.file_name, 'a') as file_to_append:
            exit_code = False
            strona_spolki = ""
            with open(self.file_name, 'r') as file_to_read:
                file_text = str(file_to_read.read())
                while len(strona_spolki) <= 2:
                    print("\nWpisz \"/back\" aby wrocic!")
                    print("Liste spolek gpw mozna znalezc na: https://www.gpw.pl/spolki")
                    print("Przyklad: \"https://www.gpw.pl/spolka?isin=PL11BTS00015\"")
                    strona_spolki = input("Wklej adres url strony internetowej spolki na gpw.pl: ")
                    if strona_spolki == "/back":
                        exit_code = True
                        break
                    if strona_spolki[0] == '/':
                        if self.color_it:
                            print(colored("Wpisano niepoprawna opcje!", self.color_bad))
                        else:
                            print("Wpisano niepoprawna opcje!")
                        strona_spolki = ""
                    else:
                        if (strona_spolki[:-2] in file_text and strona_spolki != "") or " " in strona_spolki[:-2]:
                            if self.color_it:
                                print(colored("Podana strona juz istnieje w bazie danych albo nie podano poprawnej strony!", self.color_bad))
                            else:
                                print("Podana strona juz istnieje w bazie danych albo nie podano poprawnej strony!")
                            strona_spolki = ""
                        elif " " in strona_spolki[-3:]:
                            strona_spolki = strona_spolki.strip(" ")
            if not exit_code:
                self.actualize_single_invest(strona_spolki, 'plus')
                file_to_append.write(str(strona_spolki) + "\n")
                if self.color_it:
                    print(colored("Dodano do bazy stron!", self.color_info))
                else:
                    print("Dodano do bazy stron!")
            else:
                if self.color_it:
                    print(colored("Powrot!", self.color_info))
                else:
                    print("Powrot!")

    def clear_saved_sites(self):
        answer = input("Wpisz \"y\" aby potwierdzic usuniecie wszystkich stron z bazy danych: ")
        if answer.lower() == "y":
            with open(self.file_name, 'w') as file_to_write:
                file_to_write.write("")
            self.actualize_invest()
            if self.color_it:
                print(colored("Wyczyszczono baze stron!", self.color_info))
            else:
                print("Wyczyszczono baze stron!")
        else:
            if self.color_it:
                print(colored("Anulowano!", self.color_info))
            else:
                print("Anulowano!")

    def show_saved_sites(self):
        try:
            with open(self.file_name, 'r') as file_to_read:
                print("Nazwa pliku ze stronami: " + self.file_name)
                text = file_to_read.read()

                while "\n\n" in text:
                    text = text.replace("\n\n", "\n")
                for x in range(int(len(text) / 4)):
                    text = text.replace("\n", " | ", 3)
                    text = text.replace("\n", "AXDS09", 1)
                text = text.replace("AXDS09", "\n")
                if len(text) > 0 and text[0] in "\t \n|":
                    while text[0] in "\t \n|":
                        text = text[1:]
                if len(text) >= 3:
                    text = text[:-2]
                if text in "    \n  " or len(text) < 4:
                    print("Brak stron w bazie stron! ")
                else:
                    print(text)
        except FileNotFoundError:
            if self.color_it:
                print(colored("Nie znaleziono pliku ze stronami!", self.color_bad))
            else:
                print("Nie znaleziono pliku ze stronami!")
            self.change_sites_file_name()
            print()
            self.show_saved_sites()

    def sort_sites(self, how, potential_list):
        if potential_list != 0:
            new_list = []
            value_list = []
            for spolka in potential_list:
                value_list.append(float(spolka.zmiana_proc[:-1].replace(",", ".")))
            value_list = sorted(value_list, reverse=True)
            for value in value_list:
                for spolka in potential_list:
                    if spolka.zmiana_proc[1:-1] == str(str(value).replace(".", ",")):
                        new_list.append(spolka)
                        break
            return new_list
        elif how == 'a':
            names_list = []
            for spolka in self.spolki_objects:
                names_list.append(spolka.name_of_invest)
            names_list = sorted(names_list)
            with open(self.file_name, 'w') as file_to_write:
                new_objects_list = []
                for name in names_list:
                    for spolka in self.spolki_objects:
                        if spolka.name_of_invest == name:
                            new_objects_list.append(spolka)
                            file_to_write.write(spolka.web_adress + "\n")
                            break
                self.spolki_objects = new_objects_list
        elif how == 'p':
            value_list = []
            for spolka in self.spolki_objects:
                value_list.append(float(spolka.zmiana_proc[:-1].replace(",", ".")))
            value_list = sorted(value_list, reverse=True)
            with open(self.file_name, 'w') as file_to_write:
                new_objects_list = []
                for value in value_list:
                    for spolka in self.spolki_objects:              # twice for duplicates with different +/-
                        if spolka.zmiana_proc[:-1] == str(value).replace(".", ",") + "0" or (
                                spolka.zmiana_proc[:-1] == str(value).replace(".", ",")):
                            # zero, plus
                            new_objects_list.append(spolka)
                            file_to_write.write(spolka.web_adress + "\n")
                            break
                    for spolka in self.spolki_objects:
                        if spolka.zmiana_proc[1:-1] == str(value).replace(".", ",") or (
                                spolka.zmiana_proc[1:-1] == str(value).replace(".", ",") + "0"):
                            # minus, minus with 0 at end
                            new_objects_list.append(spolka)
                            file_to_write.write(spolka.web_adress + "\n")
                            break
                self.spolki_objects = new_objects_list
        else:                           # safety
            if self.color_it:
                print(colored("Blad kodu!", self.color_bad))
            else:
                print("Blad kodu!")

    def show_best(self, lista_spolek):
        naj_spolki = []
        for spolka in lista_spolek:
            if spolka.zmiana_proc[0] == '+':
                naj_spolki.append(spolka)
        if len(naj_spolki) > 0:
            naj_spolki = self.sort_sites('this', naj_spolki)
            self.analyze(naj_spolki)
        else:
            if self.color_it:
                print(colored("Brak zyskow w spolkach!", self.color_info))
            else:
                print("Brak zyskow w spolkach!")

    def analyze(self, lista_spolek):
        if len(lista_spolek) > 0:
            longest_nazwa = 1
            longest_war_teraz = 1
            longest_war_minmax = 1
            longest_zmiana = 1
            for spolka in lista_spolek:
                if len(spolka.name_of_invest) > longest_nazwa:
                    longest_nazwa = len(spolka.name_of_invest)
                if len(spolka.wartosc) > longest_war_teraz:
                    longest_war_teraz = len(spolka.wartosc)
                if len(spolka.wartosc_minimalna + " - " + spolka.wartosc_maksymalna) > longest_war_minmax:
                    longest_war_minmax = len(spolka.wartosc_minimalna + " - " + spolka.wartosc_maksymalna)
                if len(spolka.zmiana_proc) > longest_zmiana:
                    longest_zmiana = len(spolka.zmiana_proc)
            default_space = "      "
            for spolka in lista_spolek:
                if self.color_it:
                    print("Nazwa: " + colored(spolka.name_of_invest, 'blue') + default_space, end="")
                else:
                    print("Nazwa: " + spolka.name_of_invest + default_space, end="")
                if len(spolka.name_of_invest) < longest_nazwa:
                    print(" " * (longest_nazwa - len(spolka.name_of_invest)), end="")
                print("Wartosc teraz: " + spolka.wartosc + default_space, end="")
                if len(spolka.wartosc) < longest_war_teraz:
                    print(" " * (longest_war_teraz - len(spolka.wartosc)), end="")
                print("Wartosc min-max: " + spolka.wartosc_minimalna + " - " + spolka.wartosc_maksymalna + default_space, end="")
                if len(spolka.wartosc_minimalna + " - " + spolka.wartosc_maksymalna) < longest_war_minmax:
                    print(" " * (longest_war_minmax - len(spolka.wartosc_minimalna + " - " + spolka.wartosc_maksymalna)), end="")
                print("Zmiana: ", end="")
                if spolka.zmiana_proc[0] == '-':
                    if self.color_it:
                        print(colored(spolka.zmiana_proc, 'red'))
                    else:
                        print(spolka.zmiana_proc)
                elif spolka.zmiana_proc[0] == '+':
                    if self.color_it:
                        print(colored(spolka.zmiana_proc, 'green'))
                    else:
                        print(spolka.zmiana_proc)
                else:
                    print(" " + spolka.zmiana_proc)
        else:
            print("Nie podano zadnych spolek!")

    def remove_one_site(self, the_web_site):
        try:
            with open(self.file_name, 'r') as file_to_read:
                text = file_to_read.read().split("\n")
                with open(self.file_name, 'w') as file_to_write:
                    for site in text:
                        if site == the_web_site:
                            text[text.index(site)] = ""
                            break
                    file_to_write.write("\n".join(text))
            self.actualize_single_invest(the_web_site, 'minus')
        except FileNotFoundError:
            if self.color_it:
                print(colored("Nie znaleziono pliku ze stronami!", self.color_bad))
            else:
                print("Nie znaleziono pliku ze stronami!")
            self.change_sites_file_name()
            print()
            self.remove_one_site(the_web_site)

    def do_something(self, value):
        if value == "help":
            self.show_options()
        elif value == "info":
            self.more_info()
        elif value == "back":
            if self.color_it:
                print(colored("Nie mozna powrocic ze strony glownej!", self.color_info))
            else:
                print("Nie mozna powrocic ze strony glownej!")
        elif value == "clear":
            self.clear_saved_sites()
        elif value == "sites":
            self.show_saved_sites()
        elif value == "add":
            self.add_new_site()
        elif value == "space":
            self.make_space()
        elif value == "invest":
            self.show_invest()
        elif value == "look":
            self.analyze(self.spolki_objects)
        elif value == "sort-a" or value == "sort-p":
            if len(self.spolki_objects) > 0:
                if value == "sort-a":
                    self.sort_sites('a', 0)
                    if self.color_it:
                        print(colored("Wysortowano spolki w kolejnosci alfabetycznej!", self.color_info))
                    else:
                        print("Wysortowano spolki w kolejnosci alfabetycznej!")
                else:
                    self.sort_sites('p', 0)
                    if self.color_it:
                        print(colored("Wysortowano spolki wedlug zysku procentowego!", self.color_info))
                    else:
                        print("Wysortowano spolki wedlug zysku procentowego!")
            else:
                if self.color_it:
                    print(colored("Brak spolek w bazie danych!", self.color_info))
                else:
                    print("Brak spolek w bazie danych!")
        elif "remove-" in value[:7]:
            if len(self.spolki_objects) < 1:
                if self.color_it:
                    print(colored("Brak spolek w bazie danych!", self.color_info))
                else:
                    print("Brak spolek w bazie danych!")
            else:
                local_value = value[7:]
                if len(local_value) < 1:
                    if self.color_it:
                        print(colored("Nie podano poprawnej nazwy spolki / strony spolki do usuniecia!", self.color_info))
                    else:
                        print("Nie podano poprawnej nazwy spolki / strony spolki do usuniecia!")
                else:
                    try:
                        local_obj = self.look_for_name_or_site(local_value)
                        print("Usunieto strone: " + local_obj.web_adress + " - spolka: " + local_obj.name_of_invest)
                        self.remove_one_site(local_obj.web_adress)
                    except AttributeError:
                        if self.color_it:
                            print(colored("Nie podano poprawnej, unikatowej nazwy spolki / strony spolki do usuniecia!", self.color_info))
                        else:
                            print("Nie podano poprawnej, unikatowej nazwy spolki / strony spolki do usuniecia!")
        elif "look-" in value[:6]:
            if len(self.spolki_objects) < 1:
                if self.color_it:
                    print(colored("W bazie danych nie ma zadnych spolek!", self.color_info))
                else:
                    print("W bazie danych nie ma zadnych spolek!")
            else:
                local_value = value[6:]
                if len(local_value) < 1:
                    if self.color_it:
                        print(colored("Nie podano poprawnej nazwy spolki / strony spolki!", self.color_info))
                    else:
                        print("Nie podano poprawnej nazwy spolki / strony spolki!")
                else:
                    try:
                        local_obj = self.look_for_name_or_site(local_value)
                        if local_obj.web_adress:            # trigger exception here
                            self.show_detail(local_obj)
                    except AttributeError:
                        if self.color_it:
                            print(colored("Nie podano poprawnej, unikatowej nazwy spolki / strony spolki!", self.color_info))
                        else:
                            print("Nie podano poprawnej, unikatowej nazwy spolki / strony spolki!")
        elif value == "best":
            self.show_best(self.spolki_objects)
        elif value == "name":
            self.change_sites_file_name()
        else:
            if self.color_it:
                print(colored("Wpisano niepoprawna opcje!", self.color_bad))
            else:
                print("Wpisano niepoprawna opcje!")
