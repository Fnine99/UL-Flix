import os

from utils import HacheurDeMotDePasse, est_une_adresse_email_valide
from exception import ErreurValidationException, ErreurDeValeur, ErreurDeChamp

class Utilisateur:
    """
    Classe représentant un utilisateur membre de ULFlix.

    Un utilisateur a les attributs suivants:
        - nom (str): le nom de l'utilisateur,
        - email (str): l'adresse email de l'utilisateur,
        - age (int): l'âge de l'utilisateur,
        - pays (str): le pays de l'utilisateur,
        - abonnement (int): l'abonnement de l'utilisateur 
            * 1 pour un abonnement régional
            * et 2 pour un abonnement international
        - mot_de_passe (str): la version hachée du mot de passe de l'utilisateur.
    """
    def __init__(self, nom, email, age, pays, abonnement, mot_de_passe):
        self.nom = nom
        self.email = email
        self.mot_de_passe = mot_de_passe
        self.age = int(age)
        self.pays = pays
        self.abonnement = int(abonnement)


class AnnuaireUtilisateur:
    """
    Classe représentant l'annuaire des utilisateurs de ULFlix.
    
    Un AnnuaireUtilisateur est composé des attributs suivants:
        - chemin_base_de_donnees (str): le chemin menant au fichier dans lequel les informations des utilisateurs sont sauvegardées.
        - utilisateurs (list): la liste des utilisateurs faisant partie de l'annuaire.
    """
    def __init__(self, chemin_base_de_donnees):
        self.chemin_base_de_donnees = chemin_base_de_donnees
        
        if os.path.exists(self.chemin_base_de_donnees):
            with open(self.chemin_base_de_donnees, encoding="utf-8") as fichier:
                lignes = [ligne.strip() for ligne in fichier if ligne != '\n']
        else:
            lignes = []

        self.utilisateurs = [Utilisateur(*ligne.split(",")) for ligne in lignes]

    def inscrire(self, nom, email, age, pays, abonnement, mot_de_passe):

        if len(nom) == 0 or nom.isspace():
            raise ErreurDeChamp('Le nom ne peut être vide.')

        if not est_une_adresse_email_valide(email):
            raise ErreurValidationException("L'adresse email entrée est invalide.")

        adresses_emails_existantes = set([u.email for u in self.utilisateurs])

        if email in adresses_emails_existantes:
            raise ErreurValidationException(
                "Un utilisateur est déjà inscrit avec cette adresse email. "
                "Veuillez vous connecter si vous êtes cet utilisateur ou utilisez une autre adresse email."
            )

        try:
            assert int(age) >= 0
        except:
            raise ErreurDeValeur("L'âge doit être un entier positif.")


        if len(pays) == 0 or pays.isspace():
            raise ErreurDeChamp('Vous devez entrer un pays valide.')

        try:
            assert abonnement in [1, 2]
        except (AssertionError, ValueError, TypeError):
            raise ErreurDeChamp("Le type d'abonement doit être 1 pour régional ou 2 pour international.")

        if len(mot_de_passe) < 6 or mot_de_passe.isspace():
            raise ErreurDeChamp('Le mot de passe doit faire au minimum 6 caractères.')


        hash_mot_de_passe = HacheurDeMotDePasse.hacher(mot_de_passe)

        utilisateur = Utilisateur(
            nom=nom,
            email=email,
            age=age,
            pays=pays,
            abonnement=abonnement,
            mot_de_passe=hash_mot_de_passe,
        )

        with open(self.chemin_base_de_donnees, mode="a", encoding="utf-8") as fichier:
            fichier.write(",".join([nom, email, str(age), pays, str(abonnement), hash_mot_de_passe]) + "\n")

        return utilisateur

    def authentifier(self, email, mot_de_passe):


        if not est_une_adresse_email_valide(email):
            raise ErreurValidationException("L'adresse email entrée est invalide.")

        adresses_emails_existantes = set([u.email for u in self.utilisateurs])


        if email not in adresses_emails_existantes:
            raise ErreurValidationException("Nous n'avons trouvé aucun utilisateur avec cette adresse email au niveau de notre système.")


        utilisateur = [u for u in self.utilisateurs if u.email == email][0]



        if not HacheurDeMotDePasse.verifier(utilisateur.mot_de_passe, mot_de_passe):
            raise ErreurValidationException("Mot de passe incorrect.")


        return utilisateur
