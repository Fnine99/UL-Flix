from tkinter import Entry, Button, Label, Tk, messagebox, IntVar, StringVar, Frame, LabelFrame
from PIL import ImageTk, Image
from tkinter import ttk
from utilisateur import AnnuaireUtilisateur
from mediatheque import Mediatheque
from exception import ErreurValidationException, ErreurDeValeur, ErreurDeChamp
from datetime import date
import random


# fenetre de base

class ULFlixBaseWindow(Tk):
    def __init__(self):
        super().__init__()
        # self.iconbitmap('C:\Utilisateurs\Franc\Images\playicon.png')

    def click_bouton_connexion(self, event=None):
        self.destroy()
        ULFlixConnexionWindow().mainloop()

    def click_bouton_inscription(self, event=None):
        self.destroy()
        ULFlixRegistrationWindow().mainloop()

    # fenetre d'accueil


class ULFlixHomeWindow(ULFlixBaseWindow):
    def __init__(self):
        super().__init__()

        self.title('Bienvenue sur ULFlix')
        self.geometry('550x350')
        self.resizable(False, False)
        # labels + buttons
        self.titre_label1 = Label(self, text='UL', font='Verdana 80 bold', fg='red', padx=50, pady=50)
        self.titre_label2 = Label(self, text='Flix', font='Verdana 80 bold')

        self.registration_button = Button(self, text='Inscription', command=self.click_bouton_inscription, bd=4,
                                          activeforeground='white', activebackground='gray', font='impact 20')
        self.connexion_button = Button(self, text='Connexion', command=self.click_bouton_connexion, bd=4,
                                       activeforeground='white', activebackground='gray', font='impact 20')
        # grid
        self.titre_label1.grid(row=2, column=0, columnspan=3)
        self.titre_label2.grid(row=2, column=4)
        self.registration_button.grid(row=4, column=2)
        self.connexion_button.grid(row=4, column=4)


# fenetre de connexion

class ULFlixConnexionWindow(ULFlixBaseWindow):
    def __init__(self):
        super().__init__()

        self.title('Connexion')
        self.geometry('500x250')
        self.resizable(False, False)
        # labels + buttons + entries
        self.titre_label = Label(self, text='Connexion', font='Verdana 20 bold', padx=30, pady=30)

        self.email_label = Label(self, text='Email: ', font='Verdana 10 bold')
        self.email_entry = Entry(self, width=30, bd=3)

        self.password_label = Label(self, text='Mot de passe: ', font='Verdana 10 bold')
        self.password_entry = Entry(self, width=30, bd=3, show='*')

        self.connexion_button = Button(self, text='Connexion', bd=4, activeforeground='white', activebackground='gray',
                                       font='impact 10', command=self.handle_login)

        self.registration_link_label = Label(self, text='Pas encore de compte? Inscrivez-vous.',
                                             font='calibri 10 underline', fg='blue', cursor='hand2')
        # bind
        self.registration_link_label.bind("<Button-1>", self.click_bouton_inscription)
        # grid
        self.titre_label.grid(row=0, column=0, columnspan=2)

        self.email_label.grid(row=1, column=1)
        self.password_label.grid(row=2, column=1)

        self.email_entry.grid(row=1, column=2, columnspan=2)
        self.password_entry.grid(row=2, column=2, columnspan=2)

        self.connexion_button.grid(row=3, column=3)

        self.registration_link_label.grid(row=4, column=3)

    def handle_login(self):
        func_utilisateur = AnnuaireUtilisateur('ulflix-utilisateurs.txt')
        try:
            utilisateur = func_utilisateur.authentifier(self.email_entry.get(), self.password_entry.get())
        except ErreurValidationException as e:
            messagebox.showerror('Erreur de validation', e, parent=self)
        else:
            self.destroy()
            ULFlixBoardWindow(utilisateur).mainloop()

    # fenetre de creation de compte


class ULFlixRegistrationWindow(ULFlixBaseWindow):
    def __init__(self):
        super().__init__()

        self.title("Inscription")
        self.geometry('400x300')
        self.resizable(False, False)

        # labels + button
        self.titre_label = Label(self, text="Inscription", font='Verdana 20 bold', padx=10, pady=20)

        self.nom_label = Label(self, text="Nom: ", font='Verdana 10 bold')
        self.email_label = Label(self, text="Email: ", font='Verdana 10 bold')
        self.password_label = Label(self, text="Mot de passe: ", font='Verdana 10 bold')
        self.age_label = Label(self, text="Année de naissance: ", font='Verdana 10 bold')
        self.pays_label = Label(self, text="Pays: ", font='Verdana 10 bold')
        self.abonnement_label = Label(self, text="Abonnement: ", font='Verdana 10 bold')

        self.inscription_button = Button(self, text='Inscription', bd=4, activeforeground='white',
                                         activebackground='gray', font='impact 10', command=self.handle_signup)

        self.connexion_link_label = Label(self, text='Déjà un compte? Connectez-vous.', font='calibri 10 underline',
                                          fg='blue', cursor='hand2')
        # bind
        self.connexion_link_label.bind("<Button-1>", self.click_bouton_connexion)
        # Entries
        self.nom_entry = Entry(self, width=30, bd=3)
        self.email_entry = Entry(self, width=30, bd=3)
        self.password_entry = Entry(self, width=30, bd=3, show='*')
        # combobox pour l age
        self.current_year = date.today().year
        self.birth_dates = []
        for i in range(1900, self.current_year + 1):
            self.birth_dates.append(i)

        self.age_para = IntVar(self, value=self.current_year)
        self.age_combo = ttk.Combobox(self, width=27, textvariable=self.age_para, state='readonly',
                                      values=self.birth_dates)

        # combobex pour les pays
        with open('countries.txt') as f:
            list_of_countries = [ligne.strip() for ligne in f]

        self.pays = StringVar(self, value='Canada')
        self.pays_combo = ttk.Combobox(self, width=27, textvariable=self.pays, state='readonly',
                                       values=list_of_countries)

        # combobex pour le type d abonnement
        self.abonnement = StringVar(self, value='Régional')
        self.abonnement_combo = ttk.Combobox(self, width=27, textvariable=self.abonnement, state='readonly',
                                             values=['Régional', 'International'])

        # grid
        self.titre_label.grid(row=1, column=0, columnspan=2)
        self.nom_label.grid(row=5, column=1)
        self.email_label.grid(row=6, column=1)
        self.password_label.grid(row=7, column=1)
        self.age_label.grid(row=8, column=1)
        self.pays_label.grid(row=9, column=1)
        self.abonnement_label.grid(row=10, column=1)

        self.inscription_button.grid(row=15, column=3)

        self.connexion_link_label.grid(row=18, column=1, columnspan=3)

        self.nom_entry.grid(row=5, column=2, columnspan=2)
        self.email_entry.grid(row=6, column=2, columnspan=2)
        self.password_entry.grid(row=7, column=2, columnspan=2)
        self.age_combo.grid(row=8, column=2, columnspan=2)
        self.pays_combo.grid(row=9, column=2, columnspan=2)
        self.abonnement_combo.grid(row=10, column=2, columnspan=2)

    def handle_signup(self):
        if self.abonnement.get() == 'Régional':
            abonnement = 1

        else:
            abonnement = 2

        self.age_utilisateur = self.current_year - int(self.age_combo.get())
        func_utilisateur = AnnuaireUtilisateur('ulflix-utilisateurs.txt')

        try:
            func_utilisateur.inscrire(self.nom_entry.get(), self.email_entry.get(), self.age_utilisateur,
                                      self.pays_combo.get(), abonnement, self.password_entry.get())
        except (ErreurValidationException, ErreurDeValeur, ErreurDeChamp) as e:
            messagebox.showerror('Erreur lors de la saisie', e, parent=self)
        else:
            self.destroy()
            ULFlixConnexionWindow().mainloop()
        return self.age_utilisateur


# fenetre de tableau de bord

class ULFlixBoardWindow(ULFlixBaseWindow):
    def __init__(self, utilisateur=None):
        super().__init__()

        self.title('Board')
        self.geometry('800x600')
        self.resizable(True, True)

        self.titre_label = Label(self, text=f"Bienvenue {utilisateur.nom}! Que souhaitez-vous visionner?",
                                 font='Verdana 20 bold', pady=10)

        self.titre_label.grid(row=0, column=0)

        # frame de la watch list
        # self.watchlist = Frame(self)

        # SHOW QUI RESPECTENT LA LIMITE D AGE
        self.fucn_show = Mediatheque('ulflix.txt')
        self.show_permis_pour_utilisateur = self.fucn_show.filtrer_ids_sur_age(utilisateur.age)

        # SHOW FAISANT PARTIE D UNE CATEGORIE
        categories = ['Thrillers', 'Anime Series', 'Comedies', 'International Movies', 'Horror Movies', 'Sports Movies',
                      'Action & Adventure', 'International TV Shows', 'TV Shows']




        ligne = 5
        index = 0
        col = 0
        # fait un tri croise des shows permis pour l age de l utilisateur et des shows dans une categorie choisie au
        # au hasard, affiche ensuite cette liste dans un frame.
        for i in range(10):
            self.choix_categories = random.choice(categories)

            self.show_categorie = self.fucn_show.filtrer_ids_sur_attribut_par_inclusion_de_liste_de_string(attribut='categories',
                                                                                                 valeur=self.choix_categories)

            self.movie_frame = LabelFrame(self, text=self.choix_categories, font='Verdana 10', fg='white', bd=5, padx=15, pady=15,
                                          bg='blue', height=170, width=10000)
            for self.element in self.show_categorie[:50]:
                if self.element in self.show_permis_pour_utilisateur:
                    try:
                        image = ImageTk.PhotoImage(Image.open(f"C:\\Users\\Franc\\Desktop\\data\\images\\{self.element}.JPG"))
                        self.image_label = Label(self.movie_frame, image=image)
                        self.image_label.bind("<Button-1>", self.handle_click_show)
                        self.image_label.grid(row=0, column=col)
                        col += 2
                    except:
                        pass

            self.movie_frame.grid(row=ligne, column=0, pady=10)
            ligne += 1
            index += 1

    def handle_click_show(self, show=None):
        self.fucn_show = Mediatheque('ulflix.txt')
        self.shows = self.fucn_show.charger_shows_depuis_fichier('ulflix.txt')
        self.h = self.shows.get(self.element)




# fenetre de detail de show

class ULFlixShowDetail(Tk):
    def __init__(self):
        super().__init__()

        self.title(f'')
        self.geometry('800x250')
        self.resizable(False, False)

        self.titre_label = Label(self, text=self.h, font='arial 10')
        # self.annee_label = Label(self, text= f'Année: ', font='arial 10')
        # self.duree_label = Label(self, text= f'Durée: ', font='arial 10')
        # self.synopsis_label = Label(self, text= f'Synopsis: ', font='arial 10')
        # self.acteurs_label = Label(self, text= f'Acteurs: ', font='arial 10')

        self.bouton_lire = Button(self, text='Lire', bd=4, activeforeground='white',
                                         activebackground='gray', font='impact 10', command=self.play_thrailler)
        self.bouton_ok = Button(self, text='Ok', bd=4, activeforeground='white',
                                         activebackground='gray', font='impact 10', command=self.ok_button)

        self.titre_label.grid(row=0, column=0)
        # self.annee_label.grid(row=2, column=0)
        # self.duree_label.grid(row=4, column=0)
        # self.synopsis_label.grid(row=6, column=0)
        # self.acteurs_label.grid(row=8, column=0)

    def play_thrailler_button(self):
        pass

    def ok_button(self):
        self.destroy()







# fenetre de bande annoce

class ULFlixThraillerWindow(Tk):
    pass


# fenetre pas de video associee au show

class ULFlixNovideoWindow(Tk):
    pass


if __name__ == '__main__':
    ULFlixHomeWindow().mainloop()
    # ULFlixShowDetail().mainloop()


