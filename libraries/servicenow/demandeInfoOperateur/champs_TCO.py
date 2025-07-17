from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from utils_TCO import get_driver, get_wait 
from robot.libraries.BuiltIn import BuiltIn
from navigation_TCO import switch_to_main_iframe
from selenium.webdriver.support.ui import WebDriverWait


def remplir_champ_input_id_contrat(driver, wait):
    champ_input_id = "IO:5ef59274db883b804ea8fd141d961940"
    wait.until(EC.presence_of_element_located((By.ID, champ_input_id)))
    driver.execute_script(f"""
        let el = document.querySelector("[id='{champ_input_id}']");
        el.value = "610020031011";
        el.dispatchEvent(new Event('change', {{ bubbles: true }}));
    """)

def remplir_champ_origine(driver, wait):
    origine_id = "IO:066bda30dbc83b804ea8fd141d9619d9"
    wait.until(EC.presence_of_element_located((By.ID, origine_id)))
    driver.execute_script(f"""
        let select = document.querySelector("[id='{origine_id}']");
        for (let option of select.options) {{
            if (option.text.trim() === "Post-bascule CO") {{
                select.value = option.value;
                select.dispatchEvent(new Event('change', {{ bubbles: true }}));
                break;
            }}
        }}
    """)

def attendre_et_remplir_categorie(driver, wait):
    categorie_id = "IO:cb1a527cdb883b804ea8fd141d961908"
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
            if (option.textContent.trim() === "Action sur ligne") {{
                select.value = option.value;
                hidden.value = option.value;
                select.dispatchEvent(new Event('change', {{ bubbles: true }}));
                break;
            }}
        }}
    """)

def attendre_et_remplir_sous_categorie(driver, wait):
    sous_categorie_id = "IO:2dcd5a34dbc83b804ea8fd141d961951"
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

    # Remplissage (ex: valeur "Service Web")
    driver.execute_script(f"""
        const select = document.querySelector("select[id='{sous_categorie_id}']");
        const hidden = document.querySelector("input[id='sys_original.{sous_categorie_id}']");

        if (!select) throw "Sélecteur non trouvé : select[id='{sous_categorie_id}']";
        if (!hidden) throw "Sélecteur non trouvé : input[id='sys_original.{sous_categorie_id}']";

        for (let option of select.options) {{
            if (option.textContent.trim() === "Abandon pour relance") {{
                select.value = option.value;
                hidden.value = option.value;
                select.dispatchEvent(new Event('change', {{ bubbles: true }}));
                break;
            }}
        }}
    """)

def remplir_champ_technologie(driver, wait):
    technologie_id = "IO:aa881e78db883b804ea8fd141d9619ad"
    hidden_id = f"sys_original.{technologie_id}"

    # Attendre que le champ apparaisse dans le DOM
    wait.until(EC.presence_of_element_located((By.ID, technologie_id)))

    driver.execute_script("""
        const select = document.querySelector("select[id='IO:aa881e78db883b804ea8fd141d9619ad']");
        const hidden = document.querySelector("input[id='sys_original.IO:aa881e78db883b804ea8fd141d9619ad']");

        if (!select) throw "Sélecteur non trouvé : select[id='IO:...']";
        if (!hidden) throw "Sélecteur non trouvé : input[id='sys_original.IO:...']";

        for (let option of select.options) {
            if (option.text.trim() === "FTTH") {
                select.value = option.value;
                hidden.value = option.value;
                select.dispatchEvent(new Event('change', { bubbles: true }));
                break;
            }
        }
    """)

def remplir_description(driver, wait):
    textarea_id = "IO:c62266fcdbc83b804ea8fd141d9619c4"
    hidden_input_id = "sys_original.IO:c62266fcdbc83b804ea8fd141d9619c4"

    # Attendre que le champ description soit présent dans le DOM
    wait.until(EC.presence_of_element_located((By.ID, textarea_id)))

    driver.execute_script(f"""
        const textarea = document.getElementById("{textarea_id}");
        const hidden = document.getElementById("{hidden_input_id}");
        if (!textarea || !hidden) {{
            throw new Error("Champs de description non trouvés");
        }}
        textarea.value = "Ticket test automatisé NR Tco par Robotframework par Aya ";
        hidden.value = "Ticket test automatisé NR Tco SAV par Robotframework par Aya ";
        textarea.dispatchEvent(new Event('input', {{ bubbles: true }}));
        textarea.dispatchEvent(new Event('change', {{ bubbles: true }}));
    """)


def cocher_case_test_ticket(driver, wait):
    checkbox_id = "ni.IO:ce16de4edb387b404ea8fd141d9619f6"

    # Attendre que l’élément soit présent dans le DOM
    checkbox = wait.until(EC.presence_of_element_located((By.ID, checkbox_id)))

    # Vérifier s’il est déjà coché
    if not checkbox.is_selected():
        # Clic forcé via JavaScript (contourne les superpositions)
        driver.execute_script("arguments[0].click();", checkbox)

def soumettre_ticket(driver, wait):
    wait.until(EC.presence_of_element_located((By.ID, "submit_button")))
    driver.execute_script('document.getElementById("submit_button").click();')


def remplir_champs_obligatoires_Tco():
    seleniumlib = BuiltIn().get_library_instance("SeleniumLibrary")
    driver = seleniumlib.driver
    wait = WebDriverWait(driver, 20)

    switch_to_main_iframe(driver)
    remplir_champ_input_id_contrat(driver, wait)
    remplir_champ_origine(driver, wait)
    remplir_champ_technologie(driver, wait)
    attendre_et_remplir_categorie(driver, wait)
    attendre_et_remplir_sous_categorie(driver, wait)
    #attendre_et_remplir_categorie(driver, wait)

    remplir_description(driver, wait)
    cocher_case_test_ticket(driver, wait)
    soumettre_ticket(driver, wait)
    print("Tous les champs obligatoires ont été remplis.")

    print("Tous les champs obligatoires ont été remplis et le ticket a été soumis.")