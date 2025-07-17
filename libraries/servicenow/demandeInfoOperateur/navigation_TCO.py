from robot.libraries.BuiltIn import BuiltIn
import time
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from robot.libraries.BuiltIn import BuiltIn
from datetime import datetime, timedelta
import time
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import Select

def get_driver():
    return BuiltIn().get_library_instance("SeleniumLibrary").driver

def cliquer_sur_bouton_all():
    from robot.libraries.BuiltIn import BuiltIn
    import time

    driver = BuiltIn().get_library_instance("SeleniumLibrary").driver
    max_attempts = 30
    delay = 0.3

    for attempt in range(max_attempts):
        print(f"[{attempt+1}/{max_attempts}] Tentative de clic sur le bouton 'All'...")
        try:
            bouton_all = driver.execute_script("""
                try {
                    const root1 = document.querySelector("macroponent-f51912f4c700201072b211d4d8c26010");
                    if (!root1) return null;
                    const shadow1 = root1.shadowRoot;

                    const layout = shadow1.querySelector("sn-canvas-appshell-root > sn-canvas-appshell-layout > sn-polaris-layout");
                    if (!layout) return null;
                    const shadow2 = layout.shadowRoot;

                    const header = shadow2.querySelector("sn-polaris-header");
                    if (!header) return null;
                    const shadow3 = header.shadowRoot;

                    const bouton = shadow3.querySelector("#d6e462a5c3533010cbd77096e940dd8c");
                    if (!bouton) return null;

                    return bouton;
                } catch(e) {
                    return null;
                }
            """)

            if bouton_all:
                driver.execute_script("arguments[0].click();", bouton_all)
                print("Clic sur le bouton 'All' réussi.")
                return

        except Exception as e:
            print(f"Erreur lors du clic : {e}")

        time.sleep(delay)

    raise Exception("Échec du clic sur le bouton 'All' après plusieurs tentatives.")



def remplir_champ_global_search(texte):
    driver = get_driver()
    max_attempts = 30
    delay = 0.3

    for attempt in range(max_attempts):
        print(f"[{attempt+1}/{max_attempts}] Tentative d'accès au champ de recherche globale...")
        try:
            input_element = driver.execute_script("""
                try {
                    return document
                        .querySelector("now-nav-layout")
                        .shadowRoot
                        .querySelector("sn-polaris-layout")
                        .shadowRoot
                        .querySelector("now-header")
                        .shadowRoot
                        .querySelector("sn-polaris-search input");
                } catch(e) {
                    return null;
                }
            """)
            if input_element:
                input_element.clear()
                input_element.send_keys(texte)
                print("Texte saisi avec succès.")
                return
        except Exception as e:
            print(f"Erreur JS : {e}")
        time.sleep(delay)
    raise Exception("Impossible de remplir le champ de recherche global.")


def rechercher_et_selectionner_creer_Tco():
    from robot.libraries.BuiltIn import BuiltIn
    import time

    seleniumlib = BuiltIn().get_library_instance("SeleniumLibrary")
    driver = seleniumlib.driver

    max_attempts = 30
    delay = 0.3

    for attempt in range(max_attempts):
        print(f"[{attempt+1}/{max_attempts}] Tentative d’accès à la barre de recherche contextuelle...")

        try:
            input_element = driver.execute_script("""
                try {
                    const root1 = document.querySelector("macroponent-f51912f4c700201072b211d4d8c26010");
                    if (!root1) return null;
                    const shadow1 = root1.shadowRoot;

                    const layout = shadow1.querySelector("sn-canvas-appshell-root > sn-canvas-appshell-layout > sn-polaris-layout");
                    if (!layout) return null;
                    const shadow2 = layout.shadowRoot;

                    const header = shadow2.querySelector("sn-polaris-header");
                    if (!header) return null;
                    const shadow3 = header.shadowRoot;

                    const menu = shadow3.querySelector("nav > div > div.starting-header-zone > sn-polaris-menu:nth-child(2)");
                    if (!menu) return null;
                    const shadow4 = menu.shadowRoot;

                    const input = shadow4.querySelector("#filter");
                    if (!input) return null;

                    input.focus();
                    input.value = "";
                    input.dispatchEvent(new Event('input', { bubbles: true }));
                    return input;
                } catch(e) {
                    return null;
                }
            """)

            if input_element:
                input_element.send_keys("Créer Tco")
                print("Texte 'Créer IU' saisi dans la barre contextuelle.")
                break

        except Exception as e:
            print(f"Erreur JS : {e}")

        time.sleep(delay)
    else:
        raise Exception("Impossible d’accéder à la barre contextuelle après avoir cliqué sur 'All'.")

    for attempt in range(max_attempts):
        print(f"[{attempt+1}/{max_attempts}] Tentative de clic sur le favori 'Créer Tco'...")
        try:
            result = driver.execute_script("""
                try {
                    const root1 = document.querySelector("macroponent-f51912f4c700201072b211d4d8c26010");
                    if (!root1) return false;
                    const shadow1 = root1.shadowRoot;

                    const layout = shadow1.querySelector("sn-canvas-appshell-root > sn-canvas-appshell-layout > sn-polaris-layout");
                    if (!layout) return false;
                    const shadow2 = layout.shadowRoot;

                    const header = shadow2.querySelector("sn-polaris-header");
                    if (!header) return false;
                    const shadow3 = header.shadowRoot;

                    const menu = shadow3.querySelector("nav > div > div.starting-header-zone > sn-polaris-menu:nth-child(2)");
                    if (!menu) return false;
                    const shadow4 = menu.shadowRoot;

                    const resultsContainer = shadow4.querySelector("#favoriteResults > div > div.sn-polaris-tab-content.-left.is-visible.can-animate > div > sn-collapsible-list");
                    if (!resultsContainer) return false;
                    const shadow5 = resultsContainer.shadowRoot;

                    const items = shadow5.querySelectorAll("span > span");

                    for (const item of items) {
                        const text = item.innerText.trim().toLowerCase();
                        if (text.includes("créer tco")) {
                            item.click();
                            return true;
                        }
                    }

                    return false;
                } catch(e) {
                    return false;
                }
            """)
            if result:
                print("Clic sur 'Créer tco' dans les favoris réussi.")
                return

        except Exception as e:
            print(f"Erreur lors du clic sur 'Créer tco' : {e}")

        time.sleep(delay)

    raise Exception("Impossible de cliquer sur 'Créer tco' dans les favoris.")

def remplir_champ_assigned_to():
    selenium_lib = BuiltIn().get_library_instance("SeleniumLibrary")
    driver = selenium_lib.driver
    wait = WebDriverWait(driver, 10)
 
    # Trouver et basculer dans le bon iframe dynamiquement
    iframes = driver.find_elements(By.TAG_NAME, "iframe")
    for iframe in iframes:
        driver.switch_to.default_content()
        try:
            driver.switch_to.frame(iframe)
            champ_test = driver.find_elements(By.CSS_SELECTOR, "#sys_display\\.u_savorder\\.assigned_to")
            if champ_test:
                print("Champ trouvé dans cet iframe:", iframe.get_attribute("id"))
                break
        except Exception:
            continue
 
    # Champ visible et remplissage simple
    champ = wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, "#sys_display\\.u_savorder\\.assigned_to")))
    champ.clear()
    champ.send_keys("Altst004 ALTST004")
    time.sleep(1)
def forcer_raz():
    driver = get_driver()
    max_attempts = 30
    delay = 0.3
 
    for attempt in range(max_attempts):
        print(f"[{attempt+1}/{max_attempts}] Tentative de clic sur le champ 'Forcer RAZ'...")
        try:
            label_raz = driver.find_element(By.CSS_SELECTOR, "#label\\.ni\\.u_savorder\\.u_force_raz")
            driver.execute_script("arguments[0].scrollIntoView(true);", label_raz)
            time.sleep(0.5)
            label_raz.click()
            print("Clic sur 'Forcer RAZ' réussi.")
            return
        except Exception as e:
            print(f"Erreur lors du clic sur RAZ : {e}")
        time.sleep(delay)
    raise Exception("Impossible de cliquer sur 'Forcer RAZ'.")
def statut_active():
    driver = get_driver()
    max_attempts = 30
    delay = 0.3
 
    for attempt in range(max_attempts):
        print(f"[{attempt+1}/{max_attempts}] Tentative de sélection du statut 'Active'...")
        try:
            # Scroller jusqu'au champ statut
            statut_element = driver.find_element(By.ID, "u_savorder.state")
            driver.execute_script("arguments[0].scrollIntoView(true);", statut_element)
            time.sleep(0.5)
 
            # Cliquer sur le champ pour afficher les options
            statut_element.click()
            time.sleep(0.5)
 
            # Chercher et cliquer sur l'option "Active"
            option_active = driver.find_element(By.XPATH, "//option[text()='Active']")
            option_active.click()
 
            print("Statut 'Active' sélectionné avec succès.")
            return
        except Exception as e:
            print(f"Erreur lors de la sélection du statut : {e}")
            time.sleep(delay)
 
    raise Exception("Impossible de sélectionner le statut 'Active'.")

def remplir_date_relance():
    print("[INFO] Remplissage de la date de relance...")
 
    # Récupérer le driver via SeleniumLibrary (Robot Framework)
    selenium_lib = BuiltIn().get_library_instance("SeleniumLibrary")
    driver = selenium_lib.driver
 
    wait = WebDriverWait(driver, 10)
 
    # Calculer la date de relance à +4 jours
    date_relance = datetime.now() + timedelta(days=4)
    date_formatee = date_relance.strftime("%d-%m-%Y %H:%M:%S")
    print(f"[INFO] Date calculée = {date_formatee}")
 
    # Rechercher le champ et remplir la date
    champ = wait.until(EC.presence_of_element_located((By.ID, "u_savorder.u_reminder_date")))
    champ.clear()
    champ.send_keys(date_formatee)
    print(f"[INFO] Champ rempli avec : {date_formatee}")
    


from robot.libraries.BuiltIn import BuiltIn
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.common.exceptions import TimeoutException

def selectionner_trt_usine():
    selenium_lib = BuiltIn().get_library_instance("SeleniumLibrary")
    driver = selenium_lib.driver
    builtin = BuiltIn()

    try:
        # Attente de l'élément
        WebDriverWait(driver, 10).until(
            lambda d: d.execute_script(
                'return document.querySelector("#u_savorder\\\\.u_techstage") !== null'
            )
        )

        # Récupération de l'élément
        tech_stage_element = driver.execute_script(
            'return document.querySelector("#u_savorder\\\\.u_techstage")'
        )

        # Utiliser Select pour changer la valeur
        select = Select(tech_stage_element)

        for option in select.options:
            if option.text.strip().lower() == "trt usine":
                select.select_by_visible_text(option.text.strip())
                builtin.log_to_console("✅ 'Trt usine' sélectionné dans Étape technique.")
                return

        # Si l'option n'existe pas
        message = "❌ L'option 'Trt usine' n'est pas disponible dans le champ 'Étape technique'."
        builtin.log_to_console(message)
        builtin.fail(message)

    except TimeoutException:
        message = "❌ Le champ 'Étape technique' n'a pas été trouvé dans les 10 secondes."
        builtin.log_to_console(message)
        builtin.fail(message)

def enregistrer_ticket():
    driver = get_driver()
    max_attempts = 30
    delay = 0.3
 
    for attempt in range(max_attempts):
        print(f"[{attempt+1}/{max_attempts}] Tentative de clic sur 'Enregistrer'...")
        try:
            bouton_save = driver.find_element(By.CSS_SELECTOR, "#sysverb_update_and_stay")
            bouton_save.click()
            print("Ticket mis à jour avec succès.")
            return
        except Exception as e:
            print(f"Erreur lors du clic sur Enregistrer : {e}")
        time.sleep(delay)
    raise Exception("Impossible de cliquer sur le bouton 'Enregistrer'.")
 

def enregistrer_apres_affectation():
    enregistrer_ticket()  # On peut réutiliser la fonction précédente

def switch_to_main_iframe(driver):
    iframe = driver.execute_script("""
        return document
            .querySelector("body > macroponent-f51912f4c700201072b211d4d8c26010")
            .shadowRoot
            .querySelector("#gsft_main");
    """)
    if not iframe:
        raise Exception("Iframe introuvable dans le Shadow DOM.")
    driver.switch_to.frame(iframe)