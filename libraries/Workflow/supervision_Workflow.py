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

@keyword
def Verifier_tous_les_tickets_sont_closed():
    from robot.libraries.BuiltIn import BuiltIn
    import time

    seleniumlib = BuiltIn().get_library_instance("SeleniumLibrary")
    driver = seleniumlib.driver

    max_attempts = 10
    delay = 0.5  # secondes entre chaque tentative

    for attempt in range(max_attempts):
        try:
            print(f"[{attempt + 1}/10] Vérification des états de tous les tickets...")

            tous_closed = driver.execute_script("""
                try {
                    const rows = document.querySelectorAll("table.sn-list-table tbody tr");

                    if (!rows || rows.length === 0) {
                        console.warn("⚠️ Aucune ligne trouvée dans le tableau.");
                        return null;
                    }

                    for (const row of rows) {
                        const stateCell = row.querySelector("td:nth-child(8)");
                        const ticketNumberCell = row.querySelector("td:nth-child(3) a");

                        if (!stateCell || !ticketNumberCell) {
                            console.warn("⚠️ Cellule manquante pour une ligne.");
                            continue;
                        }

                        const state = stateCell.innerText.trim();
                        const ticketNumber = ticketNumberCell.innerText.trim();
                        console.log(`Ticket ${ticketNumber} => État : ${state}`);

                        if (state !== "Closed") {
                            return false;
                        }
                    }

                    return true;
                } catch (e) {
                    console.error("Erreur JS :", e);
                    return null;
                }
            """)

            if tous_closed is True:
                print("Tous les tickets sont dans l'état 'Closed'.")
                return
            elif tous_closed is False:
                raise Exception(" Certains tickets ne sont pas dans l'état 'Closed'.")
            else:
                print("Tableau non prêt ou erreur JS. Nouvelle tentative...")

        except Exception as e:
            print(f"Erreur lors de la vérification : {e}")

        time.sleep(delay)

    raise Exception(" Impossible de confirmer que tous les tickets sont 'Closed' après plusieurs tentatives.")






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
   

    
   