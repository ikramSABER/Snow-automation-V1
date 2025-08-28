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


Naviguer Vers Lien Ticket Spécifique
    [Documentation]    Navigue vers une URL spécifique du ticket ServiceNow pour consultation ou modification.
    Go To    https://bouyguestelecomltt3.service-now.com/u_savftth.do?sys_id=5fdae4e8c3206e104c5b2dd9d001312a&sysparm_record_target=u_savftth&sysparm_record_row=63&sysparm_record_rows=185&sysparm_record_list=active%3Dtrue%5EORDERBYDESCsys_created_on
    Sleep    5s