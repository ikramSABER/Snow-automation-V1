from robot.libraries.BuiltIn import BuiltIn
from robot.api.deco import keyword
import time
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.common.exceptions import InvalidElementStateException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


def Remplir_champ_global_search(texte):
    seleniumlib = BuiltIn().get_library_instance("SeleniumLibrary")
    driver = seleniumlib.driver

    max_attempts = 30
    delay = 0.3

    for attempt in range(max_attempts):
        try:
            print(f"[{attempt+1}/{max_attempts}] Tentative d'accès au champ de recherche...")

            # Traversée du Shadow DOM imbriqué pour atteindre l'input de recherche globale
            input_element = driver.execute_script("""
                try {
                    // Niveau 1 : composant principal
                    const root1 = document.querySelector("macroponent-f51912f4c700201072b211d4d8c26010");
                    if (!root1) return null;
                    const shadow1 = root1.shadowRoot;

                    // Niveau 2 : layout global
                    const layout = shadow1.querySelector("sn-canvas-appshell-root > sn-canvas-appshell-layout > sn-polaris-layout");
                    if (!layout) return null;
                    const shadow2 = layout.shadowRoot;

                    // Niveau 3 : en-tête de page
                    const header = shadow2.querySelector("sn-polaris-header");
                    if (!header) return null;
                    const shadow3 = header.shadowRoot;

                    // Niveau 4 : wrapper du champ de recherche
                    const wrapper = shadow3.querySelector("sn-search-input-wrapper");
                    if (!wrapper) return null;
                    const shadow4 = wrapper.shadowRoot;

                    // Niveau 5 : composant de saisie typeahead
                    const typeahead = shadow4.querySelector("sn-component-workspace-global-search-typeahead");
                    if (!typeahead) return null;
                    const shadow5 = typeahead.shadowRoot;

                    // Champ de recherche
                    const input = shadow5.querySelector("#sncwsgs-typeahead-input");
                    if (!input) return null;

                    input.focus();
                    return input;
                } catch(e) {
                    return null;
                }
            """)

            if input_element:
                # On récupère la référence JS pour que Selenium puisse y envoyer du texte
                element_ref = driver.execute_script("return arguments[0];", input_element)
                element_ref.clear()
                element_ref.send_keys(texte)
                print("Texte saisi avec succès.")
                return

        except Exception as e:
            print(f"Erreur Python : {e}")

        time.sleep(delay)

    raise Exception("Impossible de trouver ou remplir le champ de recherche global après plusieurs tentatives.")

def Cliquer_sur_bouton_all():
    from robot.libraries.BuiltIn import BuiltIn
    import time

    seleniumlib = BuiltIn().get_library_instance("SeleniumLibrary")
    driver = seleniumlib.driver

    max_attempts = 30
    delay = 0.3

    for attempt in range(max_attempts):
        try:
            print(f"[{attempt+1}/{max_attempts}] Tentative de clic sur le bouton 'All'...")

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

                    bouton.click();
                    return true;
                } catch(e) {
                    return null;
                }
            """)

            if bouton_all:
                print("Clic sur le bouton 'All' réussi.")
                return

        except Exception as e:
            print(f"Erreur lors du clic : {e}")

        time.sleep(delay)

    raise Exception("Échec du clic sur le bouton 'All' après plusieurs tentatives.")



@keyword
def Rechercher_et_selectionner_Ticket_SAV_Ouverts():
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
                js_input = driver.execute_script("return arguments[0];", input_element)
                js_input.send_keys("Ticket SAV - Tickets ouverts SAV FTTH (BO)")
                print("Texte 'Ticket SAV - Tickets ouverts SAV FTTH (BO)' saisi dans la barre contextuelle.")
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
                        if (text.includes("ticket sav - tickets ouverts sav ftth (bo)")) {
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
                print("Clic sur 'Tickets SAV Ouverts' dans les favoris réussi.")
                return

        except Exception as e:
            print(f"Erreur lors du clic sur 'Tickets SAV Ouvert' : {e}")

        time.sleep(delay)

    raise Exception("Impossible de cliquer sur 'Tickets SAV Ouvert' dans les favoris.")



def remplir_champ_assigned_to(login="Altst004 ALTST004", max_retry=5):
    selenium_lib = BuiltIn().get_library_instance("SeleniumLibrary")
    driver = selenium_lib.driver
    wait = WebDriverWait(driver, 10)

    champ_id = "sys_display.u_savftth.assigned_to"

    for attempt in range(max_retry):
        try:
            champ = wait.until(EC.element_to_be_clickable((By.ID, champ_id)))

            # Vérif si champ activé
            if not champ.is_enabled():
                raise Exception("[ERROR] Champ 'assigned_to' désactivé.")

            # Reset champ (clear ou JS fallback)
            try:
                champ.clear()
            except:
                driver.execute_script("arguments[0].value = '';", champ)

            # Écriture + validation
            champ.send_keys(login)
            time.sleep(1)
            champ.send_keys(Keys.TAB)
            time.sleep(1)

            print(f"[INFO] ✅ Champ 'assigned_to' rempli avec {login}")
            return
        except Exception as e:
            print(f"[WARN] Tentative {attempt+1}/{max_retry} échouée : {e}")
            time.sleep(2)

    raise Exception(f"[FAIL] Impossible de remplir 'assigned_to' après {max_retry} tentatives.")

def cliquer_bouton_save():
    selenium_lib = BuiltIn().get_library_instance("SeleniumLibrary")
    driver = selenium_lib.driver
    wait = WebDriverWait(driver, 15)

    wait.until(EC.presence_of_element_located((By.ID, "sysverb_update_and_stay")))

    driver.execute_script('document.getElementById("sysverb_update_and_stay").click();')



def clicker_boutton_Demande_intervention():
    selenium_lib = BuiltIn().get_library_instance("SeleniumLibrary")
    driver = selenium_lib.driver
    wait = WebDriverWait(driver, 15)

    wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "#u_savftth_demande_intervention")))

    driver.execute_script('document.querySelector("#u_savftth_demande_intervention").click();')


def remplir_champ_source_tag(valeur="Traitement N2", max_retry=5):
    selenium_lib = BuiltIn().get_library_instance("SeleniumLibrary")
    driver = selenium_lib.driver
    wait = WebDriverWait(driver, 10)

    for attempt in range(max_retry):
        try:
            champ_input = wait.until(
                lambda d: d.find_element(By.CSS_SELECTOR, "#sys_display\\.u_savftth_maintainer\\.u_source_tag")
            )

            # Vérification si le champ est activé
            if not champ_input.is_enabled():
                raise Exception("[ERROR] Champ 'u_source_tag' désactivé.")

            # Optionnel : vider proprement le champ
            try:
                champ_input.clear()
            except InvalidElementStateException:
                driver.execute_script("arguments[0].value = '';", champ_input)

            champ_input.click()
            champ_input.send_keys(valeur)
            time.sleep(1)
            champ_input.send_keys(Keys.TAB)
            time.sleep(1)

            bouton_enregistrer = wait.until(
                lambda d: d.find_element(By.CSS_SELECTOR, "#sysverb_update_and_stay")
            )
            bouton_enregistrer.click()

            print(f"[INFO] ✅ Champ 'Source Tag' rempli avec succès : {valeur}")
            return

        except Exception as e:
            print(f"[WARN] Tentative {attempt + 1}/{max_retry} échouée : {e}")
            time.sleep(2)

    raise Exception(f"[FAIL] Impossible de remplir 'Source Tag' après {max_retry} tentatives.")


def Remplir_champ_Type_Intervention():
    from selenium.webdriver.common.by import By
    from selenium.webdriver.support.ui import WebDriverWait
    from selenium.webdriver.support import expected_conditions as EC
    from robot.libraries.BuiltIn import BuiltIn

    selenium_lib = BuiltIn().get_library_instance("SeleniumLibrary")
    driver = selenium_lib.driver
    wait = WebDriverWait(driver, 15)

    # Sélecteur CSS correctement échappé pour Python
    champ_css = "#u_savftth_maintainer\\.u_inter_type"

    # Attendre que le champ soit présent et visible
    select_el = wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, champ_css)))

    # Injecter la sélection via JavaScript en utilisant l'élément passé en paramètre
    driver.execute_script("""
        const select = arguments[0];
        for (let option of select.options) {
            if (option.text.trim() === "SAV") {
                select.value = option.value;
                select.dispatchEvent(new Event('change', { bubbles: true }));
                break;
            }
        }
    """, select_el)



def clicker_bouton_Prender_RDV_Immediat():
    selenium_lib = BuiltIn().get_library_instance("SeleniumLibrary")
    driver = selenium_lib.driver
    wait = WebDriverWait(driver, 15)

    # Attendre que le bouton soit présent dans le DOM
    wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "#u_savftth_prendre_rdv_immediat")))

    # Cliquer sur le bouton via JavaScript
    driver.execute_script('document.querySelector("#u_savftth_prendre_rdv_immediat").click();')

def choisir_rdv_jplus2_apres_midi():
    from datetime import datetime, timedelta
    from selenium.webdriver.common.by import By
    from selenium.webdriver.support.ui import WebDriverWait
    from selenium.webdriver.support import expected_conditions as EC
    from robot.libraries.BuiltIn import BuiltIn

    selenium_lib = BuiltIn().get_library_instance("SeleniumLibrary")
    driver = selenium_lib.driver
    wait = WebDriverWait(driver, 20)

    # Calculer la date cible (J+2)
    date_cible = datetime.now() + timedelta(days=3)
    jour = date_cible.day
    mois = date_cible.month

    # Attendre qu'au moins un créneau "14:00 - 16:00" apparaisse
    wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "div.fc-time[data-full='14:00 - 16:00']")))

    # Exécuter le JS pour cliquer sur le bon créneau en fonction de la date
    js_code = f"""
        const allSlots = Array.from(document.querySelectorAll("div.fc-time[data-full='12:00 - 14:00']"));
        let cible = null;

        for (let el of allSlots) {{
            let cell = el.closest('td');
            if (!cell) continue;

            let colIndex = Array.from(cell.parentElement.children).indexOf(cell);
            let header = document.querySelectorAll("thead .fc-day-header")[colIndex];
            if (!header) continue;

            let text = header.innerText.trim(); // Ex: "mer. 18/6"
            let match = text.match(/(\\d+)[\\/](\\d+)/);
            if (!match) continue;

            let jour = parseInt(match[1], 10);
            let mois = parseInt(match[2], 10);

            if (jour === {jour} && mois === {mois}) {{
                cible = el;
                break;
            }}
        }}

        if (!cible) throw "Aucun créneau 14h–16h trouvé pour le jour J+2 ({jour}/{mois})";

        let clickable = cible.closest("a") || cible.closest("div.fc-content");
        if (!clickable) throw "Élément cliquable introuvable à partir du créneau";
        clickable.click();
    """
    driver.execute_script(js_code)




def cliquer_bouton_Reserver_RDV():
    selenium_lib = BuiltIn().get_library_instance("SeleniumLibrary")
    driver = selenium_lib.driver
    wait = WebDriverWait(driver, 15)

    # Attendre que le bouton du popup soit présent
    wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "#btn_reservation")))

    # Cliquer via JavaScript pour plus de fiabilité
    driver.execute_script("""
        const bouton = document.querySelector("#btn_reservation");
        if (!bouton) throw "Bouton 'Réserver le RDV' non trouvé";
        bouton.click();
    """)




def cliquer_bouton_Modifier_RDV():
    selenium_lib = BuiltIn().get_library_instance("SeleniumLibrary")
    driver = selenium_lib.driver
    wait = WebDriverWait(driver, 15)

    # Attendre la présence du bouton 
    wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "#u_savftth_modify_maintenance_appointment")))

    # Cliquer sur le bouton via JavaScript
    driver.execute_script("""
        const bouton = document.querySelector("#u_savftth_modify_maintenance_appointment");
        if (!bouton) throw "Bouton 'Modifier le RDV' non trouvé.";
        bouton.click();
    """)



def Modifier_rdv_jplus2_apres_midi():

    from datetime import datetime, timedelta
    from selenium.webdriver.common.by import By
    from selenium.webdriver.support.ui import WebDriverWait
    from selenium.webdriver.support import expected_conditions as EC
    from robot.libraries.BuiltIn import BuiltIn

    selenium_lib = BuiltIn().get_library_instance("SeleniumLibrary")
    driver = selenium_lib.driver
    wait = WebDriverWait(driver, 20)

    # Calculer la date cible (J+2)
    date_cible = datetime.now() + timedelta(days=3)
    jour = date_cible.day
    mois = date_cible.month

    # Attendre qu'au moins un créneau "14:00 - 16:00" apparaisse
    wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "div.fc-time[data-full='14:00 - 16:00']")))

    # Exécuter le JS pour cliquer sur le bon créneau en fonction de la date
    js_code = f"""
        const allSlots = Array.from(document.querySelectorAll("div.fc-time[data-full='10:00 - 12:00']"));
        let cible = null;

        for (let el of allSlots) {{
            let cell = el.closest('td');
            if (!cell) continue;

            let colIndex = Array.from(cell.parentElement.children).indexOf(cell);
            let header = document.querySelectorAll("thead .fc-day-header")[colIndex];
            if (!header) continue;

            let text = header.innerText.trim(); // Ex: "mer. 18/6"
            let match = text.match(/(\\d+)[\\/](\\d+)/);
            if (!match) continue;

            let jour = parseInt(match[1], 10);
            let mois = parseInt(match[2], 10);

            if (jour === {jour} && mois === {mois}) {{
                cible = el;
                break;
            }}
        }}

        if (!cible) throw "Aucun créneau 14h–16h trouvé pour le jour J+2 ({jour}/{mois})";

        let clickable = cible.closest("a") || cible.closest("div.fc-content");
        if (!clickable) throw "Élément cliquable introuvable à partir du créneau";
        clickable.click();
    """
    driver.execute_script(js_code)


def cliquer_bouton_Modifier_RDV2():
    from selenium.webdriver.common.by import By
    from selenium.webdriver.support.ui import WebDriverWait
    from selenium.webdriver.support import expected_conditions as EC
    from robot.libraries.BuiltIn import BuiltIn

    selenium_lib = BuiltIn().get_library_instance("SeleniumLibrary")
    driver = selenium_lib.driver
    wait = WebDriverWait(driver, 20)

    # Attendre que le bouton soit présent et visible
    wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "#btn_reservation")))

    # Exécuter le JS pour cliquer
    js_code = """
        document.querySelector("#btn_reservation").click();
    """
    driver.execute_script(js_code)
    

    


def clicker_bouton_Annuler_RDV():
    # Récupération de l'instance SeleniumLibrary
    selenium_lib = BuiltIn().get_library_instance("SeleniumLibrary")
    driver = selenium_lib.driver
    wait = WebDriverWait(driver, 15)

    # Attente de la présence du bouton "Annuler RDV"
    wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "#u_savftth_cancel_intervention")))

    # Clic sur le bouton via JavaScript
    driver.execute_script('document.querySelector("#u_savftth_cancel_intervention").click();')






def clicker_sur_popup_ok():
    from selenium.common.exceptions import NoAlertPresentException

    selenium_lib = BuiltIn().get_library_instance("SeleniumLibrary")
    driver = selenium_lib.driver

    try:
        # Attente que l'alerte apparaisse
        WebDriverWait(driver, 10).until(lambda d: d.switch_to.alert)

        # Passage à l'alerte et acceptation (équivalent au clic sur OK)
        alert = driver.switch_to.alert
        alert.accept()
    except NoAlertPresentException:
        print("Aucune alerte présente.")




@keyword
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
    
    switch_to_main_iframe(driver)
   


    #attendre_et_remplir_categorie(driver, wait)

    
   