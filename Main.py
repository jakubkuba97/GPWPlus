from FunctionsOnFile import SavedSites

if __name__ == '__main__':
    settings_file_name = "Settings" + ".txt"
    sites_saved = SavedSites(settings_file_name)

    print("\nWitam! Jestem zaprogramowany aby pomoc Ci w uporządkowywaniu informacji o gieldzie polskiej gpw!")
    print("Wpisz \"/help\" aby zobaczyc dostepne opcje! Wpisz \"/info\" aby dowiedziec sie wiecej o programie!")
    the_input = ""

    while the_input != sites_saved.help[0]:
        the_input = input(">>> ")
        the_input = the_input.lower().replace(" ", "")
        if len(the_input) > 0 and the_input[0] == '/':
            the_input = the_input[1:]
            if the_input != sites_saved.help[0]:
                sites_saved.do_something(the_input)
                print()
        else:
            the_input = ""
    input("XXX ")
