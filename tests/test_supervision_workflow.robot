*** Settings ***
Resource    ../resources/Supervision_workflow_Keywords.robot
Library    ../libraries/Workflow/supervision_Workflow.py
Suite Setup    Ouvrir le navigateur ServiceNow
#Suite Teardown    Fermer le navigateur

*** Test Cases ***
Création et vérifications d’un ticket sur ServiceNow
    [Documentation]    Supervision workflow.
    Se connecter à ServiceNow
    Sleep    time_=10
    Naviguer Vers Lien de la liste des workflow Spécifique
    Sleep    time_=10
    Verifier Tous Les Tickets Sont Closed
    Sleep    time_=10