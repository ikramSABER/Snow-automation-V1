*** Settings ***
Library    SeleniumLibrary
resource  ../resources/variables.robot

*** Keywords ***
Ouvrir le navigateur ServiceNow
    Open Browser    ${SERVICENOW_URL}    ${BROWSER}
    Maximize Browser Window

Se connecter à ServiceNow
    Wait Until Element Is Visible    id=user_name    timeout=15s
    Input Text    id=user_name    ${SNOW_USERNAME}
    Input Text    id=user_password    ${SNOW_PASSWORD}
    Click Button    id=sysverb_login

Naviguer Vers Lien du Ticket Creer par API
    [Documentation]    Navigue vers une URL spécifique du ticket ServiceNow pour Validation.
    Go To  https://bouyguestelecomltt3.service-now.com/u_savquality.do?sys_id=43ccdfb483fe62105985bfa6feaad3cd&sysparm_stack=u_savquality_list.do?sysparm_query=active=true
    Sleep    5s