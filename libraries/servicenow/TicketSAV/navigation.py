from robot.libraries.BuiltIn import BuiltIn
import time

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






def rechercher_et_selectionner_creer_iu():
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
                input_element.send_keys("Créer IU")
                print("Texte 'Créer IU' saisi dans la barre contextuelle.")
                break

        except Exception as e:
            print(f"Erreur JS : {e}")

        time.sleep(delay)
    else:
        raise Exception("Impossible d’accéder à la barre contextuelle après avoir cliqué sur 'All'.")

    for attempt in range(max_attempts):
        print(f"[{attempt+1}/{max_attempts}] Tentative de clic sur le favori 'Créer IU'...")
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
                        if (text.includes("créer iu")) {
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
                print("Clic sur 'Créer IU' dans les favoris réussi.")
                return

        except Exception as e:
            print(f"Erreur lors du clic sur 'Créer IU' : {e}")

        time.sleep(delay)

    raise Exception("Impossible de cliquer sur 'Créer IU' dans les favoris.")


def switch_to_main_iframe():
    driver = get_driver()

    # verifier si on est déja dans une iframe
    if driver.execute_script("return window.frameElement !== null;"):
        print("[INFO] Déjà dans l’iframe, aucune action nécessaire.")
        return

    max_attempts = 30
    delay = 0.3

    for attempt in range(max_attempts):
        print(f"[{attempt+1}/{max_attempts}] Tentative de récupération de l’iframe principale...")

        try:
            iframe = driver.execute_script("""
                try {
                    const macro = document.querySelector("macroponent-f51912f4c700201072b211d4d8c26010");
                    if (!macro || !macro.shadowRoot) return null;

                    const shadow = macro.shadowRoot;
                    return shadow.querySelector("#gsft_main");
                } catch(e) {
                    return null;
                }
            """)

            if iframe:
                driver.switch_to.frame(iframe)
                print("[INFO] Iframe principale trouvée et activée.")
                return

        except Exception as e:
            print(f"Erreur JS : {e}")

        time.sleep(delay)

    raise Exception("Échec de récupération de l’iframe principale après plusieurs tentatives.")
