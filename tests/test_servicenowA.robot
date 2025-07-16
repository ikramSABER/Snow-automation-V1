*** Settings ***
Resource    ../resources/servicenow_keywordsA.robot
Suite Setup    Ouvrir le navigateur ServiceNow
Library    ../libraries/servicenow/navigation_TCO.py
#Suite Teardown    Fermer le navigateur

*** Test Cases ***
*** Test Cases ***
Création et vérifications d’un ticket sur ServiceNow
    [Documentation]    Simule la création d’un ticket LTT ServiceNow et vérifie l’ensemble des éléments requis.
    Se connecter à ServiceNow
    
    
    
    Sleep    time_=5
    Naviguer à la création du ticket IU
    Sleep    time_=5
    Remplir les champs du ticket IU
    Sleep    time_=5
   
