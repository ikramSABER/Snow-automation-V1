from robot.libraries.BuiltIn import BuiltIn
from robot.api.deco import keyword
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import Select



def verifier_etat_Clos():
    selenium_lib = BuiltIn().get_library_instance("SeleniumLibrary")
    driver = selenium_lib.driver
    wait = WebDriverWait(driver, 10)

    # Attendre que le champ d'état soit présent dans le DOM
    champ = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "#sys_readonly\\.u_savquality\\.state")))

    # Extraire le texte affiché (supposé contenir l'état du ticket)
    etat_affiche = champ.text.strip()

    # Vérification si le ticket est bien 'Clos'
    if "Clos" in etat_affiche or "Closed" in etat_affiche:
        print("✅ Le ticket est bien à l'état 'Clos'.")
    else:
        # Affiche l'état actuel pour debug
        raise Exception(f"❌ Le ticket n'est pas à l'état 'Clos'. État actuel détecté : '{etat_affiche}'")


