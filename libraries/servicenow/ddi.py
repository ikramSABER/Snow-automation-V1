from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from utils import get_driver, get_wait
from navigation import switch_to_main_iframe
from selenium.webdriver.support.ui import Select
import time
from selenium.webdriver.common.action_chains import ActionChains
from datetime import datetime, timedelta

def aller_à_lien_ticket(url):
    driver = get_driver()
    driver.get(url)

def forcer_raz_et_mettre_ticket_actif():
    driver = get_driver()
    wait = get_wait()

    switch_to_main_iframe()

    # Forcer RAZ
    label_raz = wait.until(
        lambda d: d.find_element(By.CSS_SELECTOR, "#label\\.ni\\.u_savftth\\.u_force_raz")
    )
    driver.execute_script("arguments[0].scrollIntoView(true);", label_raz)
    time.sleep(0.5)
    label_raz.click()

    # statut "Active"
    select_statut = wait.until(
        lambda d: d.find_element(By.CSS_SELECTOR, "#u_savftth\\.state")
    )
    Select(select_statut).select_by_visible_text("Active")

    # étape technique "Trt Usine"
    select_techstage = wait.until(
        lambda d: d.find_element(By.CSS_SELECTOR, "#u_savftth\\.u_techstage")
    )
    Select(select_techstage).select_by_visible_text("Trt Usine")

    # "Enregistrer"
    bouton_enregistrer = wait.until(
        lambda d: d.find_element(By.CSS_SELECTOR, "#sysverb_update_and_stay")
    )
    bouton_enregistrer.click()


def affecter_ticket(login="Altst004 ALTST004"):
    driver = get_driver()
    wait = get_wait()

    assigned_to_input = wait.until(
        lambda d: d.find_element(By.CSS_SELECTOR, "#sys_display\\.u_savftth\\.assigned_to")
    )
    assigned_to_input.clear()
    assigned_to_input.send_keys(login)
    time.sleep(1)
    assigned_to_input.send_keys(Keys.TAB)

    time.sleep(1)

    bouton_enregistrer = driver.find_element(By.CSS_SELECTOR, "#sysverb_update_and_stay")
    bouton_enregistrer.click()

def cliquer_sur_demande_information():
    driver = get_driver()
    wait = get_wait()
    #switch_to_main_iframe()
    bouton_demande = wait.until(
        lambda d: d.find_element(By.CSS_SELECTOR, "#u_ticketsav_infoRequest")
    )
    driver.execute_script("arguments[0].scrollIntoView(true);", bouton_demande)
    time.sleep(0.5)
    bouton_demande.click()

def remplir_motif_et_worknote():
    driver = get_driver()
    wait = get_wait()

    select_elem = wait.until(lambda d: d.find_element(By.ID, "ddi_reason"))

    # motif "Refaire les tests du N1"
    Select(select_elem).select_by_value("refaire_les_tests_du_n1")

    # Work Note : "TEST DDI"
    textarea = wait.until(lambda d: d.find_element(By.ID, "dialog_comments"))
    textarea.clear()
    textarea.send_keys("TEST DDI")


def confirmer_demande_information():
    driver = get_driver()
    wait = get_wait()

    wait.until(lambda d: d.find_element(By.ID, "dialog_buttons"))

    bouton_ok = wait.until(lambda d: d.find_element(By.ID, "ok_button"))

    driver.execute_script("arguments[0].scrollIntoView(true);", bouton_ok)
    time.sleep(0.5)
    bouton_ok.click()

def verifier_etat_et_etape_technique():
    driver = get_driver()
    wait = get_wait()

    #switch_to_main_iframe()

    # recuperer l'état et étape technique
    etat_select_elem = wait.until(lambda d: d.find_element(By.ID, "u_savftth.state"))
    etape_elem = wait.until(lambda d: d.find_element(By.ID, "u_savftth.u_techstage"))

    etat_select = Select(etat_select_elem)
    etat_label = etat_select.first_selected_option.text.strip().lower()

    etape_value = etape_elem.get_attribute("value").strip().lower()

    print(f"[DEBUG] État visible (label) : {etat_label}")
    print(f"[DEBUG] Étape technique : {etape_value}")

    # anglais ou français
    assert any(x in etat_label for x in ["freezed", "gelé"]), "L'état n'est pas 'gelé/Freezed'"
    assert "attente_client_ddi" in etape_value, "Étape technique incorrecte"



def verifier_envoi_sms():
    driver = get_driver()
    wait = get_wait()

    #switch_to_main_iframe()

    wait.until(lambda d: d.find_element(By.ID, "sn_form_inline_stream_entries"))
    ul = driver.find_element(By.CSS_SELECTOR, "#sn_form_inline_stream_entries > ul.activities-form")
    elements_li = ul.find_elements(By.CSS_SELECTOR, "li.h-card")

    contenu_global = ""
    for li in elements_li:
        try:
            # acitivtés (work notes)
            metadata = li.find_element(By.CSS_SELECTOR, ".sn-card-component-time").text.lower()
            if "work notes" in metadata:
                # Extraire le texte du bloc de contenu
                bloc = li.find_element(By.CSS_SELECTOR, ".sn-card-component_summary")
                contenu = bloc.text.strip().lower()
                contenu_global += contenu + "\n"
        except Exception as e:
            continue  # Ignore les cartes non conformes

    print("[DEBUG] Contenu global des notes de travail :")
    print(contenu_global)

    if "l'envoi du sms a été effectué avec succès" in contenu_global:
        print("[INFO] ✅ SMS envoyé avec succès")
    elif "le sms ftth - ddi - demande d'information n'a pas été envoyé" in contenu_global:
        print("[AVERTISSEMENT] ⚠️ SMS non envoyé")
    else:
        print("[AVERTISSEMENT] ⚠️ Aucun message relatif au SMS trouvé")



def recuperer_numero_ticket():
    driver = get_driver()
    wait = get_wait()

    numero_elem = wait.until(lambda d: d.find_element(By.ID, "u_savftth.number"))
    numero = numero_elem.get_attribute("value")

    BuiltIn().set_suite_variable("${numero_ticket}", numero)  # stocker le numero du  ticket
    print(f"[INFO] Numéro du ticket récupéré et stocké : {numero}")
    return numero


def rechercher_et_selectionner_vue_tickets_sav():
    driver = get_driver()
    max_attempts = 30
    delay = 0.3

    # saisir la recherche BO ouverts
    for attempt in range(max_attempts):
        print(f"[{attempt+1}/{max_attempts}] Accès à la barre de recherche contextuelle...")
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
                input_element.send_keys("ticket SAV - tickets ouverts SAV FTTH (BO)")
                print("[OK] Saisie dans la barre contextuelle réussie.")
                break
        except Exception as e:
            print(f"[ERREUR] JS : {e}")

        time.sleep(delay)
    else:
        raise Exception("Impossible d’accéder à la barre contextuelle après clic sur 'All'.")

    # selectionner l'element recherché
    for attempt in range(max_attempts):
        print(f"[{attempt+1}/{max_attempts}] Clic sur l'élément 'ticket SAV - tickets ouverts SAV FTTH (BO)'...")
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
                print("[OK] Clic sur la vue 'ticket SAV...' réussi.")
                return
        except Exception as e:
            print(f"[ERREUR] JS : {e}")

        time.sleep(delay)

    raise Exception("Impossible de cliquer sur la vue 'ticket SAV - tickets ouverts SAV FTTH (BO)'.")


def get_numero_ticket_suite():
    return BuiltIn().get_variable_value("${numero_ticket}")

def rechercher_ticket_par_numero():
    numero_ticket = get_numero_ticket_suite()
    if not numero_ticket:
        raise Exception("La variable ${numero_ticket} est vide ou non définie.")

    driver = get_driver()
    wait = get_wait()
    switch_to_main_iframe()

    champ_numero = wait.until(lambda d: d.find_element(By.ID, "u_savftth_table_header_search_control"))
    champ_numero.clear()
    champ_numero.send_keys(numero_ticket)

    # declenchement de recherche
    driver.execute_script("""
        const input = arguments[0];
        input.dispatchEvent(new Event('change', { bubbles: true }));
        input.dispatchEvent(new KeyboardEvent('keydown', { key: 'Enter', keyCode: 13, which: 13, bubbles: true }));
        input.dispatchEvent(new KeyboardEvent('keyup', { key: 'Enter', keyCode: 13, which: 13, bubbles: true }));
        input.form?.dispatchEvent(new Event('submit', { bubbles: true, cancelable: true }));
    """, champ_numero)
    print(f"[INFO] Recherche du ticket {numero_ticket} effectuée.")


from robot.libraries.BuiltIn import BuiltIn

def modifier_date_previsionnelle_via_calendrier():
    driver = get_driver()
    wait = get_wait()
    numero_ticket = get_numero_ticket_suite()

    # la ligne du ticket
    row_selector = f"tr[id^='row_u_savftth_'] td:nth-child(3)"
    rows = driver.find_elements(By.CSS_SELECTOR, row_selector)
    row = None
    for cell in rows:
        if cell.text.strip() == numero_ticket:
            row = cell.find_element(By.XPATH, "../..")
            break
    if not row:
        raise Exception(f"Ligne du ticket {numero_ticket} introuvable")
    time.sleep(15)
    # prendre la date de création
    date_creation_str = row.find_element(By.CSS_SELECTOR, "td:nth-child(5) div.datex.date-calendar").text.strip()
    print(f"[DEBUG] Date de création lue : {date_creation_str}")
    try:
        date_creation = datetime.strptime(date_creation_str, "%d-%m-%Y %H:%M:%S")
    except ValueError:
        date_creation = datetime.strptime(date_creation_str, "%d-%m-%Y %H:%M")

    date_target = (date_creation + timedelta(minutes=2)).replace(microsecond=0)
    print(f"[INFO] Nouvelle date prévisionnelle = {date_target.strftime('%d/%m/%Y %H:%M:%S')}")
    time.sleep(15)
    # calendrier
    champ_calendrier = row.find_element(By.CSS_SELECTOR, "td:nth-child(6) div.datex.date-calendar")
    ActionChains(driver).double_click(champ_calendrier).perform()
    print("[INFO] Double clic effectué sur le calendrier.")
    time.sleep(1)

    # sélection du jour
    day_id = f"GwtDateTimePicker_day{date_target.day}"
    driver.execute_script("""
        const el = document.getElementById(arguments[0]);
        if (el) {
            el.dispatchEvent(new MouseEvent('mousedown', { bubbles: true }));
            el.dispatchEvent(new MouseEvent('mouseup', { bubbles: true }));
            el.dispatchEvent(new MouseEvent('click', { bubbles: true }));
        }
    """, day_id)

    # sélection de l'heure
    try:
        heure, minute, seconde = date_target.strftime("%H:%M:%S").split(":")
        champ_hh = driver.find_element(By.ID, "GwtDateTimePicker_hh")
        champ_mm = driver.find_element(By.ID, "GwtDateTimePicker_mm")
        champ_ss = driver.find_element(By.ID, "GwtDateTimePicker_ss")
        champ_hh.clear(); champ_hh.send_keys(heure.zfill(2))
        champ_mm.clear(); champ_mm.send_keys(minute.zfill(2))
        champ_ss.clear(); champ_ss.send_keys(seconde.zfill(2))
        print(f"[INFO] Heure {heure}:{minute}:{seconde} saisie avec succès.")
    except Exception as e:
        print(f"[ERROR] Échec de la saisie de l’heure : {e}")

    # clic de validation hors calendrier
    try:
        cellule_numero = row.find_element(By.CSS_SELECTOR, "td:nth-child(3)")
        cellule_numero.click()
        print("[INFO] Validation de la date via clic hors calendrier.")
    except Exception:
        champ_calendrier.send_keys(Keys.TAB)
        print("[INFO] Validation via touche TAB.")

    print(f"[INFO] Date prévisionnelle fixée à : {date_target.strftime('%d/%m/%Y %H:%M:%S')}")
