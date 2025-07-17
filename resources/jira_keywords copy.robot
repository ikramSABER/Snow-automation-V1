*** Settings ***
Library    RequestsLibrary
Library    ../libraries/jira/JiraUpload.py
Library    Collections
Library    JSONLibrary

Resource   variables.robot

*** Keywords ***
Créer un ticket Jira
    [Documentation]    Création d'un ticket Jira et retour de sa clé (ex: AL-79).
    ${project}=    Create Dictionary    key=AL
    ${issuetype}=    Create Dictionary    name=Tâche
    ${fields}=    Create Dictionary
    ...    project=${project}
    ...    summary=Incident de test depuis Robot Framework
    ...    description=Ticket généré automatiquement pour test d'automatisation
    ...    issuetype=${issuetype}
    ${data}=    Create Dictionary    fields=${fields}
    ${headers}=    Create Dictionary    Content-Type=application/json
    ${auth}=    Create List    ${JIRA_USER}    ${JIRA_TOKEN}
    Create Session    jira    ${JIRA_URL}    auth=${auth}    headers=${headers}    verify=False
    ${response}=    POST On Session    jira    /rest/api/2/issue    json=${data}
    Should Be Equal As Numbers    ${response.status_code}    201
    ${ticket_key}=    Set Variable    ${response.json()["key"]}
    RETURN   ${ticket_key}

Lister les transitions disponibles
    [Arguments]    ${ticket_key}
    ${available_transitions}=    GET On Session    jira    /rest/api/2/issue/${ticket_key}/transitions
    RETURN    ${available_transitions.json()["transitions"]}

Ajouter un commentaire
    [Arguments]    ${ticket_key}    ${commentaire}
    ${data}=    Create Dictionary    body=${commentaire}
    ${response}=    POST On Session    jira    /rest/api/2/issue/${ticket_key}/comment    json=${data}
    Should Be Equal As Numbers    ${response.status_code}    201

Mettre à jour le statut du ticket
    [Arguments]    ${ticket_key}    ${transition_name}
    ${transitions}=    Lister les transitions disponibles    ${ticket_key}
    ${transition_id}=    Set Variable    None
    FOR    ${transition}    IN    @{transitions}
        IF    '${transition["name"]}' == '${transition_name}'
            ${transition_id}=    Set Variable    ${transition["id"]}
            BREAK
        END
    END
    Run Keyword If    '${transition_id}' == 'None'    Fail    "Transition '${transition_name}' non trouvée."
    ${transition_data}=    Create Dictionary    id=${transition_id}
    ${data}=    Create Dictionary    transition=${transition_data}
    ${response}=    POST On Session    jira    /rest/api/2/issue/${ticket_key}/transitions    json=${data}
    Should Be Equal As Numbers    ${response.status_code}    204

Ajouter une pièce jointe
    [Arguments]    ${ticket_key}    ${file_path}
    ${result}=    Upload File    ${ticket_key}    ${file_path}    ${JIRA_USER}    ${JIRA_TOKEN}
