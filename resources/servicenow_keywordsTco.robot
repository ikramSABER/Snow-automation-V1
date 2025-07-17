*** Settings ***
Library    SeleniumLibrary
resource  ../resources/variables.robot
Library    ../libraries/servicenow/demandeInfoOperateur/navigation_TCO.py
Library    ../libraries/servicenow/demandeInfoOperateur/champs_TCO.py

*** Keywords ***
Ouvrir le navigateur ServiceNow
    Open Browser    ${SERVICENOW_URL}    ${BROWSER}
    Maximize Browser Window

Se connecter à ServiceNow
    Wait Until Element Is Visible    id=user_name    timeout=15s
    Input Text    id=user_name    ${SNOW_USERNAME}
    Input Text    id=user_password    ${SNOW_PASSWORD}
    Click Button    id=sysverb_login

Naviguer à la création du ticket tco
    Cliquer Sur Bouton All
    Rechercher Et Selectionner Creer Tco

Remplir les champs du ticket tco
    remplir_champs_obligatoires_Tco