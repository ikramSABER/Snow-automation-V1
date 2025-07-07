from robot.libraries.BuiltIn import BuiltIn
from robot.api.deco import keyword
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import Select



from robot.libraries.BuiltIn import BuiltIn
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.common.exceptions import TimeoutException



def verifier_etat_actif():
    selenium_lib = BuiltIn().get_library_instance("SeleniumLibrary")
    driver = selenium_lib.driver
    builtin = BuiltIn()

    try:
        # Attente que le champ State soit présent
        WebDriverWait(driver, 10).until(
            lambda d: d.execute_script('return document.querySelector("#u_savquality\\\\.state") !== null')
        )

        # Récupération de l’élément via JS
        state_element = driver.execute_script('return document.querySelector("#u_savquality\\\\.state")')

        # Lire l’option sélectionnée avec Select
        select = Select(state_element)
        selected_text = select.first_selected_option.text.strip()

        # Vérification stricte de l’état
        if selected_text.lower() == "active":
            builtin.log_to_console("Le ticket est en état ACTIF.")
        else:
            msg = f"Le ticket n'est pas actif. État actuel : '{selected_text}'."
            builtin.log_to_console(msg)
            builtin.fail(msg)

    except TimeoutException:
        msg = "Le champ 'State' n'a pas été trouvé dans les 10 secondes."
        builtin.log_to_console(msg)
        builtin.fail(msg)





def verifier_etape_technique_attente_docs():
    selenium_lib = BuiltIn().get_library_instance("SeleniumLibrary")
    driver = selenium_lib.driver
    builtin = BuiltIn()

    try:
        # Attente de l'élément <select>
        WebDriverWait(driver, 10).until(
            lambda d: d.execute_script('return document.querySelector("#u_savquality\\\\.u_techstage") !== null')
        )

        # Récupérer l'élément
        tech_stage_element = driver.execute_script('return document.querySelector("#u_savquality\\\\.u_techstage")')

        # Lire l’option sélectionnée
        select = Select(tech_stage_element)
        selected_text = select.first_selected_option.text.strip()

        if selected_text.lower() == "attente documents client":
            builtin.log_to_console("L'étape technique est bien 'Attente Documents Client'.")
        else:
            # Affiche et échoue le test
            message = f"L'étape technique attendue est 'Attente Documents Client', mais trouvée : '{selected_text}'."
            builtin.log_to_console(message)
            builtin.fail(message)

    except TimeoutException:
        message = "Le champ 'Étape technique' n'a pas été trouvé dans les 10 secondes."
        builtin.log_to_console(message)
        builtin.fail(message)


def verifier_groupe_affectation_attente_photo_client():
    selenium_lib = BuiltIn().get_library_instance("SeleniumLibrary")
    driver = selenium_lib.driver
    builtin = BuiltIn()

    try:
        # Attendre que l'élément soit présent dans le DOM
        WebDriverWait(driver, 10).until(
            lambda d: d.execute_script('return document.querySelector("#sys_display\\\\.u_savquality\\\\.assignment_group") !== null')
        )

        # Récupérer l'élément via JS
        element = driver.execute_script('return document.querySelector("#sys_display\\\\.u_savquality\\\\.assignment_group")')

        # Récupérer la valeur (pour input, c'est l'attribut 'value')
        selected_value = driver.execute_script('return document.querySelector("#sys_display\\\\.u_savquality\\\\.assignment_group").value').strip()

        builtin.log_to_console(f"Groupe d'affectation sélectionné : '{selected_value}'")

        # Vérifier la valeur
        if selected_value.lower() == "attente photo client":
            builtin.log_to_console("Le groupe d'affectation est bien 'Attente Photo Client'.")
        else:
            message = f"Le groupe d'affectation attendu est 'Attente Photo Client', mais trouvé : '{selected_value}'."
            builtin.log_to_console(message)
            builtin.fail(message)

    except TimeoutException:
        message = "Le champ 'Groupe d'affectation' n'a pas été trouvé dans les 10 secondes."
        builtin.log_to_console(message)
        builtin.fail(message)
    except Exception as e:
        message = f"Erreur inattendue : {str(e)}"
        builtin.log_to_console(message)
        builtin.fail(message)