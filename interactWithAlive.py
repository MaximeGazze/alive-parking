# Samuel Lajoie, Maxime Gazzé, Miguel Boka et Edgar Pereda Puig
# Lancer le code avec python3 -i iteration1.py
# Les différentes commandes sont:
# command.createUpdate()
# command.stationnement()
# command.visite()
# command.nbVisites(cible) e.g command.nbVisites("employe") | command.nbVisites("day") | command.nbVisites("week") | command.nbVisites("month")
from bson.objectid import ObjectId
from datetime import datetime, timedelta
import re

class interactiveAlive:
    def __init__(self, iotObject):
        self.my_iot = iotObject
        
    #fonction pour créé ou mettre à jour un utilisateur
    def createUpdate(self):
        action = input('Create or Update? insert C or U: ')

        prenom = input('Entrez le prenom: ')
        nom = input('Entrez le nom: ')

        employees = self.my_iot.get_doc('/document/employees')
        existant = False
        currentEmploye = {}
        for i in employees:
            if i['nom'] == nom and i['prenom'] == prenom:
                existant = True
                currentEmploye = i
                break

        #Message erreur
        if ((action == 'U' or action == 'u') and not existant):
            print('employé inexistant')
        elif ((action == 'C' or action =='c') and existant):
            print('employé existant')

        if ((action == 'C' or action =='c') and not existant):
            #create employe(e)
            dept = input('Entrez le departement: ')
            poste = input('Entrez le poste: ')
            stationnement = bool(input('Stationnement  true/false: '))
            immatriculation = input('Entrez l\'immatriculation du vehicule : ')
            employees.append(
                {"nom": nom,
                "prenom": prenom,
                "departement": dept,
                "poste": poste,
                "stationnement": stationnement,
                "immatriculation": immatriculation})

            self.my_iot.update_doc({'/document/employees': employees})
            print('employé(e) créé avec succès !')

        elif ((action == 'U' or action == 'u') and existant):
            #update employe(e) aux options répondues par "y"
            changeNom = input('Changez le nom? y/n: ')
            if changeNom == 'y' or changeNom == 'Y':
                nom = input('Entrez le nom: ')
                currentEmploye['nom'] = nom

            changePrenom = input('Changez le prenom? y/n: ')
            if changePrenom == 'y' or changePrenom == 'Y':
                prenom = input('Entrez le nom: ')
                currentEmploye['prenom'] = prenom

            changeDept = input('Changez le departement? y/n: ')
            if changeDept == 'y' or changeDept == 'Y':
                dept = input('Entrez le departement: ')
                currentEmploye['departement'] = dept

            changePoste = input('Changez le poste? y/n: ')
            if changePoste == 'y' or changePoste == 'Y':
                poste = input('Entrez le poste: ')
                currentEmploye['poste'] = poste

            changeStationnement = input('Changez le status du stationnement? y/n: ')
            if changeStationnement == 'y' or changeStationnement == 'Y':
                stationnement = str(input('Stationnement  true/false: ')).lower()
                if(stationnement == 'false'):
                    stationnement = False
                else:
                    stationnement = True
                currentEmploye['stationnement'] = stationnement

            changeImmatri = input('Changez l\'immatriculation? y/n: ')
            if changeImmatri == 'y' or changeImmatri == 'Y':
                immatriculation = input('Entrez l\'immatriculation du vehicule : ')
                currentEmploye['immatriculation'] = immatriculation

            for i in employees:
                if i['nom'] == nom and i['prenom'] == prenom:
                    employees.remove(i)
            employees.append(currentEmploye)

            self.my_iot.update_doc({'/document/employees': employees})
            print('employé(e) mis à jour avec succès !')

    #Fonction qui retourne les informations conçernant le stationnement d'un véhicule selon son immatriculation
    def stationnement(self, matricule):
        #matricule = input('Immatriculation: ')

        user = None
        employees = self.my_iot.get_doc('/document/employees')

        for i in employees:
            if i['immatriculation'] == matricule:
                user = i

        if user:
            prenom = user["prenom"]
            nom = user["nom"]
            stationnement = user["stationnement"]

            print('employe: %s %s \naccess: %r' %(prenom, nom, stationnement))
            return {
                    "prenom": prenom,
                    "nom": nom,
                    "access": stationnement
                    }
        else:
            print('employe inexistant')

    #Fonction qui cummul les visites
    def visite(self, immatricule):
        #immatricule = input('Immatriculation de la personne visitante: ').upper()
        immatricule = immatricule.upper()
        reg = '[A-Z][0-9]{3}[A-Z]{2}'
        match = re.search(reg, immatricule)
        if match is None: return "matricule non conforme"
        now = datetime.now().strftime("%Y-%m-%d")
        myQuery1 = {"immatriculation": immatricule}
        myQuery2 = {"immatriculation": immatricule, "date": now}

        employees = self.my_iot.get_doc('/document/employees')
        visites = self.my_iot.get_doc('/document/visites')
        actuallyPresent = self.my_iot.get_doc('/document/actuellementPresent')
        
        employee_exist = None
        visite_exist = None
        for visite in visites:
            if visite['immatriculation'] == immatricule and visite['date'][0:10] == now:
                visite_exist = visite
                break
            elif visite['immatriculation'] == immatricule:
                visite_exist = visite

        for employe in employees:
            if employe['immatriculation'] == immatricule:
                employee_exist = employe
                break

        condition1 = employee_exist != None and visite_exist == None
        condition2 = employee_exist != None and visite_exist != None
        #TODO à compléter
        if(condition1):
            #créer une première visite si un(e) employé(e) existe et que c'est ça première visite
            visites.append({ "date": now, "visites": 1, "immatriculation": immatricule})
            self.my_iot.update_doc({'/document/visites': visites})
        elif(condition2):
            #Si un(e) employé(e) existe et qu'il a déjà visité
            visite = visite_exist
            #TODO à vérifier parce que wt% is that
            #for i in range(collection_visites.count_documents(myQuery2)):
            #    date1 = datetime.strptime(visites_exist[i]["date"], "%Y-%m-%d")
            #    date2 = datetime.strptime(visite["date"], "%Y-%m-%d")
            #    if( date1 > date2):
            #        visite = visites_exist[i]

            if(visite["date"][0:10] == now):
                #si l'employé(e) visite le stationnement à nouveau dans une même journée, effectue la mise à jour
                visites.remove(visite)
                visite['visites'] = visite['visites'] + 1
                visites.append(visite)
                self.my_iot.update_doc({'/document/visites': visites})
            elif(visite["date"] != now):
                #Si l'employé(e) visite le stationnement pour la première fois une nouvelle journée, crée une nouvelle entrez
                visites.append({ "date": now, "visites": 1, "immatriculation": immatricule})
                self.my_iot.update_doc({'/document/visites': visites})
        return "l'employé(e) n'existe probablement pas"

    #Fonction qui retourne le nombre de visites selon le critère ciblé
    def nbVisites(self):
        #msg = "Entrez la date de la journée désiré (ex:2001-01-01)(yyyy-mm-dd): "
        #Code si l'option choisie est "day"
        #myQuery = {"date": cibleDate}
        #listDay = collection_visites.find(myQuery)
        nbVisites = 0
        #TODO rendre ce qui suit potable
        # Soit que le nombre de visites soit reelement present et non pour la journee complete
        now = datetime.now().strftime("%Y-%m-%d")
        dates = self.my_iot.get_doc('/document/visites')
        nbVisites = 0
        
        for day in dates:
            if day['date'][0:10] == now:
                nbVisites += day['visites']


        self.my_iot.update_doc({'/document/nbActuellementPresent': nbVisites})
        print("Le nombre total de visite: ", nbVisites)
        return nbVisites
