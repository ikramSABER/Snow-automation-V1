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
    Go To   https://bouyguestelecomltt3.service-now.com/u_savftth.do?sys_id=02115817839ce6105985bfa6feaad397&sysparm_view=&sysparm_domain=null&sysparm_domain_scope=null&sysparm_record_row=1&sysparm_record_rows=100&sysparm_record_list=active%3dtrue%5estate%3d2%5eORDERBYDESCstate
    Sleep    5s