*** Settings ***
Resource    ../resources/servicenow_keywords.robot
Suite Setup    Ouvrir le navigateur ServiceNow
#Suite Teardown    Fermer le navigateur

*** Test Cases ***
Création et vérifications d’un ticket sur ServiceNow
    [Documentation]    Simule la création d’un ticket LTT ServiceNow et vérifie l’ensemble des éléments requis.
    Se connecter à ServiceNow
    Sleep    time_=5
    Naviguer à la création du ticket IU
    Sleep    time_=5
    ${url_ticket}=    Remplir les champs du ticket IU
    Sleep    time_=5

DDI
    #Aller à l'URL du Ticket    ${url_ticket}
    #Aller à l'URL du Ticket    https://bouyguestelecomltt3.service-now.com/u_savftth.do?sys_id=16124af387526210e93e433d8bbb35e0&sysparm_record_target=u_savftth&sysparm_record_row=1&sysparm_record_rows=175&sysparm_record_list=active%3Dtrue%5EORDERBYDESCsys_created_on
    #Sleep    time_=5
    
    Forcer Raz et Mettre Le Ticket Actif
    Sleep    time_=5
    Affecter Ticket à l'utilisateur    Altst004 ALTST004
    Sleep    time_=5
    Lancer Demande Information
    Sleep    time_=5
    Verification envoi SMS

Date Prévisionnelle De Dégel
    Sleep    time_=5
    Aller à l'URL du Ticket    https://bouyguestelecomltt3.service-now.com/now/nav/ui/classic/params/target/%24pa_dashboard.do
    Sleep    time_=10
    Aller à la Vue des Tickets SAV
    Sleep    time_=5

    #Rechercher et Modifier le Ticket DDI1    SAV-FTTH0008669535
    #Modifier Date Degel Via Calendrier    SAV-FTTH0008669535

    Rechercher et Modifier le Ticket DDI1
    Sleep    time_=5
    Modifier Date Previsionnelle Via Calendrier
    #Attendre Et Vérifier Relance DDI1