from robot.libraries.BuiltIn import BuiltIn
from robot.api.deco import keyword
import time
from selenium.webdriver.common.by import By
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
                print("Clic sur 'Créer Tco' dans les favoris réussi.")
                return

        except Exception as e:
            print(f"Erreur lors du clic sur 'Créer Tco' : {e}")

        time.sleep(delay)

    raise Exception("Impossible de cliquer sur 'Créer Tco' dans les favoris.")



def remplir_champ_assigned_to():
    selenium_lib = BuiltIn().get_library_instance("SeleniumLibrary")
    driver = selenium_lib.driver
    wait = WebDriverWait(driver, 10)

    champ_id = "sys_display.u_savftth.assigned_to"
    champ = wait.until(EC.presence_of_element_located((By.ID, champ_id)))
    
    # Clic sur le champ
    champ.click()
    time.sleep(0.5)

    # Taper pour déclencher les suggestions
    champ.send_keys("Alt")
    time.sleep(2)  # Attente suggestions

    # JS : tenter de cliquer sur la suggestion
    js_script = """
        try {
            const items = Array.from(document.querySelectorAll("div.ac_item"))
                .filter(i => i.offsetParent !== null);

            const target = items.find(i => i.innerText.includes("Altst004 ALTST004"));
            if (target) {
                ['mouseover', 'mousedown', 'mouseup', 'click'].forEach(evt => {
                    target.dispatchEvent(new MouseEvent(evt, { bubbles: true }));
                });
            } else {
                console.warn("Suggestion 'Altst004 ALTST004' non trouvée.");
            }
        } catch (e) {
            console.warn("Erreur JS ignorée : " + e);
        }
    """
    driver.execute_script(js_script)
    time.sleep(3)

def cliquer_bouton_save():
    selenium_lib = BuiltIn().get_library_instance("SeleniumLibrary")
    driver = selenium_lib.driver
    wait = WebDriverWait(driver, 15)

    wait.until(EC.presence_of_element_located((By.ID, "sysverb_update_and_stay")))

    driver.execute_script('document.getElementById("sysverb_update_and_stay").click();')



def cliquer_bouton_request_for_information():
    selenium_lib = BuiltIn().get_library_instance("SeleniumLibrary")
    driver = selenium_lib.driver
    wait = WebDriverWait(driver, 15)

    wait.until(EC.presence_of_element_located((By.ID, "u_ticketsav_infoRequest")))

    driver.execute_script('document.getElementById("u_ticketsav_infoRequest").click();')



def traiter_popup_information():
    selenium_lib = BuiltIn().get_library_instance("SeleniumLibrary")
    driver = selenium_lib.driver
    wait = WebDriverWait(driver, 15)

    # Attendre que la liste déroulante soit présente
    wait.until(EC.presence_of_element_located((By.ID, "ddi_reason")))

    # Sélectionner l'option "Refaire les tests du N1"
    driver.execute_script("""
        const select = document.getElementById("ddi_reason");
        if (!select) throw "Liste déroulante 'ddi_reason' introuvable";

        for (let option of select.options) {
            if (option.text.trim() === "Refaire les tests du N1") {
                select.value = option.value;
                select.dispatchEvent(new Event('change', { bubbles: true }));
                break;
            }
        }
    """)

    # Remplir le champ "Description"
    driver.execute_script("""
        const description = document.getElementById("dialog_comments");
        if (!description) throw "Champ 'dialog_comments' introuvable";

        description.value = "Veuillez effectuer de nouveaux tests selon les remarques N1.";
        description.dispatchEvent(new Event('input', { bubbles: true }));
    """)

    # Cliquer sur le bouton OK
    driver.execute_script("""
        const boutonOK = document.getElementById("ok_button");
        if (!boutonOK) throw "Bouton OK introuvable";

        boutonOK.click();
    """)


def verifier_etat_et_etape_technique():
    selenium_lib = BuiltIn().get_library_instance("SeleniumLibrary")
    driver = selenium_lib.driver

    result = driver.execute_script("""
        const etatElem = document.getElementById("u_savftth.state");
        const etapeElem = document.getElementById("u_savftth.u_techstage");

        if (!etatElem || !etapeElem) {
            return { success: false, message: "Champs non trouvés" };
        }

        const etatText = etatElem.options[etatElem.selectedIndex].text.trim();
        const etapeText = etapeElem.options[etapeElem.selectedIndex].text.trim();

        const etatOk = etatText === "Freezed";
        const etapeOk = etapeText === "Attente Client DDI";

        return {
            success: etatOk && etapeOk,
            etatText,
            etapeText,
            message: etatOk && etapeOk 
                     ? "Vérification réussie" 
                     : `État: ${etatText}, Étape technique: ${etapeText}`
        };
    """)

    if not result["success"]:
        raise AssertionError(f"Vérification échouée : {result['message']}")


def verifier_sms():
    selenium_lib = BuiltIn().get_library_instance("SeleniumLibrary")
    driver = selenium_lib.driver

    expected_text = """Liste des communications : 
SMS - Le SMS FTTH - DDI - demande d'information n'a pas été envoyé
Serveur vocal interactif - La communication IVR n'a pas été effectuée : 26"""

    try:
        result = driver.execute_script("""
            try {
                const el = document.querySelector("#activity_bd40ad4c874eaa10e93e433d8bbb3597 > div > span");
                if (!el) return "__ELEMENT_NON_TROUVE__";
                return el.innerText.trim();
            } catch(e) {
                return "__ERREUR_JS__";
            }
        """)
        
        if result == "__ELEMENT_NON_TROUVE__":
            print("⚠️ Élément introuvable avec le sélecteur CSS.")
        elif result == "__ERREUR_JS__":
            print("⚠️ Une erreur s’est produite en exécutant le JavaScript.")
        elif expected_text.strip() in result:
            print("✅ Texte trouvé et correspondance réussie.")
        else:
            print("❌ Texte trouvé, mais différent du texte attendu.")
            print("Texte obtenu :")
            print(result)
    
    except Exception as e:
        print("❌ Exception Python capturée :")
        print(str(e))


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

    
   