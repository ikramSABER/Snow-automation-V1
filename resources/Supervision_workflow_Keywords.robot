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


Naviguer Vers Lien de la liste des workflow Spécifique
    [Documentation]    Navigue vers une URL spécifique du ticket ServiceNow pour consultation ou modification.
    Go To   https://bouyguestelecomltt3.service-now.com/u_replay_workflow_list.do?sysparm_query=u_business_process.u_activity_nameLIKEBP_RET&sysparm_first_row=1&sysparm_view=&sysparm_choice_query_raw=&sysparm_list_header_search=true
    Sleep    5s

