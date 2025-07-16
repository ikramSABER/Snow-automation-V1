from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from utils import get_driver, get_wait 
from robot.libraries.BuiltIn import BuiltIn
from navigation import switch_to_main_iframe

def remplir_champ_input_id_contrat(id_contrat):
    driver = get_driver()
    wait = get_wait()
    champ_input_id = "IO:7ed859fc37b0de008c8c2b2943990ee3"
    wait.until(EC.presence_of_element_located((By.ID, champ_input_id)))
    driver.execute_script(f"""
        let el = document.querySelector("[id='{champ_input_id}']");
        el.value = "{id_contrat}";
        el.dispatchEvent(new Event('change', {{ bubbles: true }}));
    """)
    print(f"[INFO] ID Contrat rempli : {id_contrat}")

def remplir_champ_origine():
    driver = get_driver()
    wait = get_wait()
    origine_id = "IO:a522e42adb1732006e0970d9bf96193d"
    wait.until(EC.presence_of_element_located((By.ID, origine_id)))
    driver.execute_script(f"""
        let select = document.querySelector("[id='{origine_id}']");
        for (let option of select.options) {{
            if (option.text.trim() === "Mail") {{
                select.value = option.value;
                select.dispatchEvent(new Event('change', {{ bubbles: true }}));
                break;
            }}
        }}
    """)


def attendre_et_remplir_categorie():
    driver = get_driver()
    wait = get_wait()
    categorie_id = "IO:b686ddbc37b0de008c8c2b2943990ece"
    hidden_id = f"sys_original.{categorie_id}"
    print("Attente du champ catégorie dans le DOM...")

    success = driver.execute_async_script(f"""
        var callback = arguments[arguments.length - 1];
        const start = Date.now();

        function checkOptions() {{
            const select = document.querySelector("select[id='{categorie_id}']");
            if (!select) {{
                if (Date.now() - start > 10000) return callback(false);
                return setTimeout(checkOptions, 300);
            }}
            const options = select.options;
            if (!options || options.length === 0) {{
                if (Date.now() - start > 10000) return callback(false);
                return setTimeout(checkOptions, 300);
            }}
            for (let opt of options) {{
                if (opt.textContent.trim() && opt.textContent.trim() !== "-- None --") {{
                    return callback(true);
                }}
            }}
            if (Date.now() - start > 10000) return callback(false);
            setTimeout(checkOptions, 300);
        }}
        checkOptions();
    """)
    if not success:
        raise Exception("Catégorie non peuplée après 10 secondes")
    driver.execute_script(f"""
        const select = document.querySelector("select[id='{categorie_id}']");
        const hidden = document.querySelector("input[id='sys_original.{categorie_id}']");

        if (!select) throw "Sélecteur non trouvé : select[id='{categorie_id}']";
        if (!hidden) throw "Sélecteur non trouvé : input[id='sys_original.{categorie_id}']";

        for (let option of select.options) {{
            if (option.textContent.trim() === "ACCES") {{
                select.value = option.value;
                hidden.value = option.value;
                select.dispatchEvent(new Event('change', {{ bubbles: true }}));
                break;
            }}
        }}
    """)

def attendre_et_remplir_sous_categorie():
    driver = get_driver()
    sous_categorie_id = "IO:fba919fc37b0de008c8c2b2943990e6e"
    hidden_id = f"sys_original.{sous_categorie_id}"
    print("Attente du champ sous-catégorie dans le DOM...")

    success = driver.execute_async_script(f"""
        var callback = arguments[arguments.length - 1];
        const start = Date.now();

        function checkOptions() {{
            const select = document.querySelector("select[id='{sous_categorie_id}']");
            if (!select) {{
                if (Date.now() - start > 10000) return callback(false);
                return setTimeout(checkOptions, 300);
            }}
            const options = select.options;
            if (!options || options.length === 0) {{
                if (Date.now() - start > 10000) return callback(false);
                return setTimeout(checkOptions, 300);
            }}
            for (let opt of options) {{
                if (opt.textContent.trim() && opt.textContent.trim() !== "-- None --") {{
                    return callback(true);
                }}
            }}
            if (Date.now() - start > 10000) return callback(false);
            setTimeout(checkOptions, 300);
        }}
        checkOptions();
    """)
    if not success:
        raise Exception("Sous-catégorie non peuplée après 10 secondes")

    driver.execute_script(f"""
        const select = document.querySelector("select[id='{sous_categorie_id}']");
        const hidden = document.querySelector("input[id='sys_original.{sous_categorie_id}']");

        if (!select) throw "Sélecteur non trouvé : select[id='{sous_categorie_id}']";
        if (!hidden) throw "Sélecteur non trouvé : input[id='sys_original.{sous_categorie_id}']";

        for (let option of select.options) {{
            if (option.textContent.trim() === "DF - Plus de signal") {{
                select.value = option.value;
                hidden.value = option.value;
                select.dispatchEvent(new Event('change', {{ bubbles: true }}));
                break;
            }}
        }}
    """)


def remplir_champ_technologie():
    driver = get_driver()
    wait = get_wait()

    technologie_id = "IO:72b05ce2db1732006e0970d9bf96190c"
    hidden_id = f"sys_original.{technologie_id}"

    wait.until(EC.presence_of_element_located((By.ID, technologie_id)))

    driver.execute_script(f"""
        const select = document.getElementById("{technologie_id}");
        const hidden = document.getElementById("{hidden_id}");
        if (!select || !hidden) throw "Champs technologie manquants";
        for (let opt of select.options) {{
            if (opt.text.trim() === "FTTH") {{
                select.value = opt.value;
                hidden.value = opt.value;
                select.dispatchEvent(new Event('change', {{ bubbles: true }}));
                break;
            }}
        }}
    """)


def remplir_numero_mobile_disponible():
    driver = get_driver()
    wait = get_wait()

    visible_input_id = "IO:c526c415375996408c8c2b2943990e65"
    hidden_input_id = "sys_original.IO:c526c415375996408c8c2b2943990e65"

    wait.until(EC.presence_of_element_located((By.ID, visible_input_id)))

    driver.execute_script(f"""
        const input = document.getElementById("{visible_input_id}");
        const hidden = document.getElementById("{hidden_input_id}");
        if (!input || !hidden) {{
            throw new Error("Champs de numéro mobile non trouvés");
        }}
        input.value = "0612345678";
        hidden.value = "0612345678";
        input.dispatchEvent(new Event('input', {{ bubbles: true }}));
        input.dispatchEvent(new Event('change', {{ bubbles: true }}));
    """)


def remplir_description():
    driver = get_driver()
    wait = get_wait()

    textarea_id = "IO:228ad13037f0de008c8c2b2943990eba"
    hidden_input_id = "sys_original.IO:228ad13037f0de008c8c2b2943990eba"

    wait.until(EC.presence_of_element_located((By.ID, textarea_id)))

    driver.execute_script(f"""
        const textarea = document.getElementById("{textarea_id}");
        const hidden = document.getElementById("{hidden_input_id}");
        if (!textarea || !hidden) {{
            throw new Error("Champs de description non trouvés");
        }}
        textarea.value = "Ticket test automatisé NR FTTH SAV par Robotframework, Crée par Riad";
        hidden.value = "Ticket test automatisé NR FTTH SAV par Robotframework, Crée par Riad";
        textarea.dispatchEvent(new Event('input', {{ bubbles: true }}));
        textarea.dispatchEvent(new Event('change', {{ bubbles: true }}));
    """)


def cocher_case_test_ticket():
    driver = get_driver()
    wait = get_wait()

    checkbox_id = "ni.IO:5ccff1eddba60f00fb17fb261d961995"
    checkbox = wait.until(EC.presence_of_element_located((By.ID, checkbox_id)))

    if not checkbox.is_selected():
        driver.execute_script("arguments[0].click();", checkbox)


def soumettre_ticket():
    driver = get_driver()
    wait = get_wait()

    wait.until(EC.presence_of_element_located((By.ID, "submit_button")))
    driver.execute_script('document.getElementById("submit_button").click();')


def attendre_redirection_et_obtenir_url_ticket():
    wait = get_wait(15)
    try:
        wait.until(lambda d: "u_savftth.do" in d.current_url and "sys_id=" in d.current_url)
        url = get_driver().current_url
        print(f"Redirection réussie. Ticket créé : {url}")
        return url
    except TimeoutException:
        current_url = get_driver().current_url
        print(f"[WARN] Timeout d’attente de redirection. URL actuelle : {current_url}")
        return current_url  # on retourne quand même quelque chose


def remplir_champs_obligatoires_iu(id_contrat):
    switch_to_main_iframe()

    remplir_champ_input_id_contrat(id_contrat) 
    remplir_champ_technologie()
    attendre_et_remplir_categorie()        
    attendre_et_remplir_sous_categorie()
    remplir_numero_mobile_disponible()
    remplir_description()
    cocher_case_test_ticket()
    soumettre_ticket()

    ticket_url = attendre_redirection_et_obtenir_url_ticket()

    return ticket_url