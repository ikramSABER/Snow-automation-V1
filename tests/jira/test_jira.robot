*** Settings ***
Resource    ..\resources\jira\jira_keywords.robot

*** Test Cases ***
Créer un ticket Jira et effectuer des actions post-création
    [Documentation]    Créer un ticket et ajouter un commentaire, mettre à jour le statut, et ajouter une pièce jointe.
    
    ${ticket_key}=    Créer un ticket Jira
    Log    "🔹 Ticket clé récupérée : ${ticket_key}"
    ${transitions}=    Lister les transitions disponibles    ${ticket_key}
    Ajouter un commentaire    ${ticket_key}    "Ce ticket a été créé automatiquement via Robot Framework."
    Mettre à jour le statut du ticket    ${ticket_key}    Done
    Ajouter une pièce jointe    ${ticket_key}    ${ATTACHMENT_PATH}
