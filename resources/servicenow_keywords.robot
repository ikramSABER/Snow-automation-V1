*** Settings ***
Library    SeleniumLibrary
resource  ../resources/variables.robot
Library    ../libraries/servicenow/TicketSAV/navigation.py
Library    ../libraries/servicenow/TicketSAV/champs.py
Library    ../libraries/servicenow/TicketSAV/ddi.py

*** Keywords ***
Ouvrir le navigateur ServiceNow
    Open Browser    ${SERVICENOW_URL}    ${BROWSER}
    Maximize Browser Window

Se connecter à ServiceNow
    Wait Until Element Is Visible    id=user_name    timeout=15s
    Input Text    id=user_name    ${SNOW_USERNAME}
    Input Text    id=user_password    ${SNOW_PASSWORD}
    Click Button    id=sysverb_login

Naviguer à la création du ticket IU
    Cliquer Sur Bouton All
    Rechercher Et Selectionner Creer Iu

Remplir les champs du ticket IU
    ${url}=    Remplir Champs Obligatoires IU    610000000077
    RETURN    ${url}

Aller à l'URL du Ticket
    [Arguments]    ${url}
    Aller À Lien Ticket    ${url}

Forcer Raz et Mettre Le Ticket Actif
    Forcer Raz et Mettre Ticket Actif
    
Affecter Ticket à l'utilisateur
    [Arguments]    ${login}=altst004
    Affecter Ticket    ${login}
    
Lancer Demande Information
    Cliquer Sur Demande Information
    Remplir Motif Et Worknote
    Confirmer Demande Information

Verification envoi SMS
    Verifier Etat Et Etape Technique
    Verifier Envoi Sms    ddi
    ${numero_ticket}=    Recuperer Numero Ticket
    Log To Console    Le ticket est : ${numero_ticket}


Aller à la Vue des Tickets SAV
    Cliquer Sur Bouton All
    Rechercher Et Selectionner Vue Tickets SAV

Rechercher et Modifier le Ticket DDI1
    Rechercher Ticket Par Numero

Cliquer Sur Le Numero Ticket
    Cliquer Sur Numero Ticket

Attendre Le Motif Du Gel
    [Arguments]    ${motif}
    Attendre Motif Gel    ${motif}

Rechercher et Modifier le Ticket DDI2
    Rechercher Ticket Par Numero

Vérifier Envoi SMS DDI1
    Verifier Envoi Sms    ddi1

Vérifier Envoi SMS DDI2
    Verifier Envoi Sms    ddi2

Cliquer Sur Bouton Dégeler
    Cliquer Sur Bouton Degeler

Attendre Que L'État Devienne Actif
    Attendre Etat Actif

Patienter Que Les Groupes Soient Remplis
    Patienter Groupes Chargés