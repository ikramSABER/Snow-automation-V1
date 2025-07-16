from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from utils import get_driver, get_wait
from navigation import switch_to_main_iframe
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import InvalidElementStateException
import time
from selenium.webdriver.common.action_chains import ActionChains
from datetime import datetime, timedelta
from robot.libraries.BuiltIn import BuiltIn
from datetime import datetime, timedelta
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
import time
import locale

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


def affecter_ticket(login="Altst004 ALTST004", max_retry=5):
    driver = get_driver()
    wait = get_wait()

    for attempt in range(max_retry):
        try:
            assigned_to_input = wait.until(
                lambda d: d.find_element(By.CSS_SELECTOR, "#sys_display\\.u_savftth\\.assigned_to")
            )

            # Vérification si le champ est activé
            if not assigned_to_input.is_enabled():
                raise Exception("[ERROR] Champ 'assigned_to' désactivé.")

            # Optionnel : clean JS en cas d’échec de clear classique
            try:
                assigned_to_input.clear()
            except InvalidElementStateException:
                driver.execute_script("arguments[0].value = '';", assigned_to_input)

            assigned_to_input.send_keys(login)
            time.sleep(1)
            assigned_to_input.send_keys(Keys.TAB)

            time.sleep(1)

            bouton_enregistrer = wait.until(
                lambda d: d.find_element(By.CSS_SELECTOR, "#sysverb_update_and_stay")
            )
            bouton_enregistrer.click()
            print(f"[INFO] ✅ Affectation du ticket à {login} réussie.")
            return

        except InvalidElementStateException as e:
            print(f"[WARN] Tentative {attempt + 1}/{max_retry} échouée (champ non interactif). Retry...")
            time.sleep(2)
        except Exception as e:
            print(f"[ERROR] Erreur imprévue pendant l'affectation : {e}")
            raise

    raise Exception(f"[FAIL] Impossible d’affecter le ticket à {login} après {max_retry} tentatives.")

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

def modifier_date_previsionnelle_via_calendrier():
    try:
        locale.setlocale(locale.LC_TIME, 'en_US.UTF-8')
    except:
        print("[WARN] Locale en_US non supportée, aria-label pourrait échouer.")

    driver = get_driver()
    wait = get_wait()
    switch_to_main_iframe()
    numero_ticket = get_numero_ticket_suite()

    # ligne du ticket
    rows = driver.find_elements(By.CSS_SELECTOR, "tr[id^='row_u_savftth_'] td:nth-child(3)")
    row = next((cell.find_element(By.XPATH, "../..") for cell in rows if cell.text.strip() == numero_ticket), None)
    if not row:
        raise Exception(f"Ligne du ticket {numero_ticket} introuvable")

    now = datetime.now()
    target = (now + timedelta(hours=1, minutes=2)).replace(microsecond=0)
    print(f"[DEBUG] Now local = {now.strftime('%d/%m/%Y %H:%M:%S')}")
    print(f"[DEBUG] Target date = {target.strftime('%d/%m/%Y %H:%M:%S')}")

    # Ouvrir le calendrier avec double clic
    champ_cal = row.find_element(By.CSS_SELECTOR, "td:nth-child(6) div.datex.date-calendar")
    driver.execute_script("arguments[0].scrollIntoView(true);", champ_cal)
    try:
        ActionChains(driver).double_click(champ_cal).perform()
        print("[INFO] Double clic effectué sur le calendrier.")
        time.sleep(0.5)
    except:
        champ_cal.click()
        print("[WARN] Double clic échoué, clic simple exécuté.")

    # attendre le champ hh preuve de calendrier ouvert 
    try:
        wait.until(lambda d: d.find_element(By.ID, "GwtDateTimePicker_hh").is_displayed())
        print("[INFO] Calendrier bien ouvert (champ heure visible).")
    except Exception as e:
        print("[ERROR] Le calendrier ne s’est pas ouvert correctement.")
        driver.save_screenshot("calendrier_non_ouvert.png")
        raise e

    # selection du jour par ariel label au lieu de jspath
    jour_str = str(target.day)
    label_target = target.strftime(f"%A, %B {jour_str}, %Y")
    print(f"[DEBUG] aria-label attendu = {label_target}")
    try:
        jour_elem = wait.until(lambda d: d.find_element(By.CSS_SELECTOR, f'a[aria-label="{label_target}"]'))
        jour_elem.click()
        print(f"[INFO] Jour sélectionné avec aria-label : {label_target}")
    except Exception as e:
        print(f"[ERROR] Jour introuvable via aria-label : {label_target}")
        driver.save_screenshot("erreur_jour_selection.png")
        raise

    # Heure/minute/seconde
    hh, mm, ss = target.strftime("%H:%M:%S").split(":")
    for suffix, val in (("hh", hh), ("mm", mm), ("ss", ss)):
        champ = wait.until(lambda d: d.find_element(By.ID, f"GwtDateTimePicker_{suffix}"))
        champ.clear()
        champ.send_keys(val)
        print(f"[INFO] Champ {suffix} rempli avec {val}")

    # Valider
    try:
        row.find_element(By.CSS_SELECTOR, "td:nth-child(3)").click()
        print("[INFO] Validation par clic hors calendrier.")
    except:
        champ_cal.send_keys(Keys.TAB)
        print("[INFO] Validation par touche TAB.")

    print(f"[INFO] Date prévisionnelle fixée à : {target.strftime('%d/%m/%Y %H:%M:%S')}")


def cliquer_sur_numero_ticket(timeout=40):
    from selenium.webdriver.support import expected_conditions as EC

    driver = get_driver()
    wait = get_wait()
    numero_ticket = get_numero_ticket_suite()

    row_selector = f"tr[id^='row_u_savftth_'] td:nth-child(3) > a"
    cellules = driver.find_elements(By.CSS_SELECTOR, row_selector)

    for cell in cellules:
        if cell.text.strip() == numero_ticket:
            try:
                driver.execute_script("arguments[0].scrollIntoView(true);", cell)
                print(f"[DEBUG] Tentative de clic sur le numéro de ticket {numero_ticket}")
                wait.until(EC.element_to_be_clickable(cell)).click()
                print(f"[INFO] Clic réussi sur le ticket {numero_ticket}")
                return
            except Exception as e:
                print(f"[ERROR] Échec du clic sur le numéro de ticket : {e}")
                raise

    raise Exception(f"Numéro de ticket {numero_ticket} introuvable dans la liste.")



def attendre_motif_gel(motif_attendu="relance ddi1", timeout=500):
    driver = get_driver()
    wait = get_wait()
    switch_to_main_iframe()

    print(f"[DEBUG] Début de l'attente du motif de gel : {motif_attendu}")

    for _ in range(timeout):
        try:
            champ = driver.find_element(By.ID, "u_savftth.u_geljustif")
            selected = champ.find_element(By.CSS_SELECTOR, "option:checked").text.strip().lower()
            print(f"[DEBUG] Motif gel actuel : {selected}")
            if motif_attendu.lower() in selected:
                print(f"[INFO] ✅ Motif gel attendu détecté : {motif_attendu}")
                return

            time.sleep(1)
            bouton_enregistrer = driver.find_element(By.CSS_SELECTOR, "#sysverb_update_and_stay")
            bouton_enregistrer.click()
        except Exception as e:
            print(f"[WARN] Lecture motif échouée : {e}")
        time.sleep(1)

    raise Exception(f"[ERROR] Motif gel '{motif_attendu}' non détecté après {timeout}s")

def verifier_envoi_sms(version):
    driver = get_driver()
    wait = get_wait()

    wait.until(lambda d: d.find_element(By.ID, "sn_form_inline_stream_entries"))
    ul = driver.find_element(By.CSS_SELECTOR, "#sn_form_inline_stream_entries > ul.activities-form")
    elements_li = ul.find_elements(By.CSS_SELECTOR, "li.h-card")

    contenu_global = ""
    for li in elements_li:
        try:
            metadata = li.find_element(By.CSS_SELECTOR, ".sn-card-component-time").text.lower()
            if "work notes" in metadata:
                bloc = li.find_element(By.CSS_SELECTOR, ".sn-card-component_summary")
                contenu = bloc.text.strip().lower()
                contenu_global += contenu + "\n"
        except Exception:
            continue

    print("[DEBUG] Contenu global des notes de travail :\n" + contenu_global)

    if "l'envoi du sms a été effectué avec succès" in contenu_global:
        print("[INFO] ✅ SMS envoyé avec succès")
    elif f"le sms ftth - ddi - {version}" in contenu_global:
        print(f"[AVERTISSEMENT] ⚠️ SMS '{version.upper()}' non envoyé")
    else:
        print("[AVERTISSEMENT] ⚠️ Aucun message relatif au SMS trouvé")

def cliquer_sur_bouton_degeler():
    driver = get_driver()
    wait = get_wait()
    switch_to_main_iframe()

    bouton = wait.until(lambda d: d.find_element(By.ID, "u_ticketsav_unfreeze"))
    driver.execute_script("arguments[0].scrollIntoView(true);", bouton)
    time.sleep(0.5)
    bouton.click()
    print("[INFO] Bouton 'Dégeler' cliqué.")


def attendre_etat_actif(timeout=60):
    driver = get_driver()
    wait = get_wait()
    switch_to_main_iframe()

    for i in range(timeout):
        try:
            etat_elem = wait.until(lambda d: d.find_element(By.ID, "u_savftth.state"))
            selected = Select(etat_elem).first_selected_option.text.strip().lower()
            print(f"[DEBUG] État actuel : {selected}")
            if "actif" in selected or "active" in selected:
                print("[INFO] ✅ État est devenu 'Actif'")
                return
        except Exception as e:
            print(f"[WARN] Tentative {i+1}/{timeout} - Échec lecture état : {e}")
        time.sleep(1)
    raise Exception("⛔ L'état 'Actif' n'a pas été atteint dans le délai imparti.")

def patienter_groupes_chargés(timeout=600):  # 10 min max
    driver = get_driver()
    wait = get_wait()
    switch_to_main_iframe()

    for i in range(timeout):
        try:
            champ_affectation = driver.find_element(By.ID, "sys_display.u_savftth.assignment_group")
            champ_silo = driver.find_element(By.ID, "sys_display.u_savftth.u_silo_group")

            val_affectation = champ_affectation.get_attribute("value").strip()
            val_silo = champ_silo.get_attribute("value").strip()

            print(f"[DEBUG] t+{i}s | Affectation: '{val_affectation}' | Silo: '{val_silo}'")

            if val_affectation and val_silo:
                print(f"[INFO] ✅ Groupes détectés : Affectation = '{val_affectation}', Silo = '{val_silo}'")
                return
        except Exception as e:
            print(f"[WARN] Erreur lors de la lecture des champs : {e}")

        time.sleep(1)
        bouton_enregistrer = driver.find_element(By.CSS_SELECTOR, "#sysverb_update_and_stay")
        bouton_enregistrer.click()

    raise Exception("⛔ Les groupes assignés (affectation ou silo) n'ont pas été chargés à temps.")



def ajouter_worknote_et_confirmer(message="test DDI terminée"):
    driver = get_driver()
    wait = get_wait()
    switch_to_main_iframe()

    textarea = wait.until(lambda d: d.find_element(By.ID, "activity-stream-work_notes-textarea"))
    textarea.clear()
    textarea.send_keys(message)
    print(f"[INFO] ✅ Worknote saisie : {message}")

    bouton = wait.until(lambda d: d.find_element(By.ID, "sysverb_update_and_stay"))
    bouton.click()
    print("[INFO] Bouton 'Enregistrer' cliqué après saisie de worknote.")
