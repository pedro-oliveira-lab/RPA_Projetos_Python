import customtkinter as ctk
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import pandas as pd
import time

# --- HERMES, O PROSPECTOR (RPA) ---
# IDEIA DO PROJETO: Correção final do fluxo de verificação de senha e limpeza do código.

# Configurações iniciais da nossa interface
ctk.set_appearance_mode("Light")
ctk.set_default_color_theme("blue") 

class HermesProspector(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.driver = None 
        self.is_admin_mode = False 
        
        # Opções Padrão (Agora dinâmicas, para serem configuradas)
        self.default_tipos = ["Hospitais", "Açougue"]
        self.default_zonas = ["Zona Norte", "Zona Leste"]

        self.title("Hermes, o Prospector (RPA)")
        self.geometry("800x650") 
        self.configure(fg_color="#F5F5F5") 

        # Configuração do Layout Grid
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)
        self.grid_rowconfigure(3, weight=0) 

        self.label = ctk.CTkLabel(
            self, 
            text="Hermes, o Prospector", 
            text_color="#808000",
            font=ctk.CTkFont(size=24, weight="bold")
        )
        self.label.grid(row=0, column=0, padx=20, pady=20, sticky="n")
        
        self.tab_view = ctk.CTkTabview(
            self, 
            fg_color="#F0F0F0",
            segmented_button_fg_color="#808000",
            segmented_button_selected_color="#556B2F",
        )
        self.tab_view.grid(row=1, column=0, padx=20, pady=20, sticky="nsew")

        self.tab_view.add("Configuração")
        self.tab_view.add("Resultados")
        
        self.tab_view.tab("Configuração").grid_columnconfigure(0, weight=1)
        self.tab_view.tab("Resultados").grid_columnconfigure(0, weight=1)
        self.tab_view.tab("Resultados").grid_rowconfigure(0, weight=1)
        
        # --- 1A. MODO PADRÃO (ComboBox - VISÍVEL INICIALMENTE) ---
        self.label_tipo_default = ctk.CTkLabel(
            self.tab_view.tab("Configuração"),
            text="1. Amiga, qual tipo de empresa vamos prospectar?",
            font=ctk.CTkFont(size=14, weight="bold")
        )
        self.label_tipo_default.grid(row=0, column=0, padx=20, pady=(20, 0), sticky="s")
        
        self.combo_tipo_empresa = ctk.CTkComboBox(
            self.tab_view.tab("Configuração"),
            values=self.default_tipos, # Usa a lista dinâmica
            command=self.check_default_inputs, 
            width=300, 
            height=40,
            border_color="#808000"
        )
        self.combo_tipo_empresa.set("Selecione...")
        self.combo_tipo_empresa.grid(row=1, column=0, padx=20, pady=(5, 10), sticky="n")

        self.label_zona_default = ctk.CTkLabel(
            self.tab_view.tab("Configuração"),
            text="2. Em qual zona de SP Capital vamos focar?",
            font=ctk.CTkFont(size=14, weight="bold")
        )

        self.combo_zona = ctk.CTkComboBox(
            self.tab_view.tab("Configuração"),
            values=self.default_zonas, # Usa a lista dinâmica
            command=self.check_default_inputs, 
            width=300, 
            height=40,
            border_color="#808000"
        )
        self.combo_zona.set("Selecione...")
        
        # --- 1B. MODO ADMINISTRADOR (Entry - ESCONDIDO INICIALMENTE) ---
        self.entry_tipo_empresa = ctk.CTkEntry(self.tab_view.tab("Configuração"), 
                                               placeholder_text="Ex: 'Padarias' ou 'Clínicas Odontológicas'", 
                                               width=300, height=40, border_color="#808000")
        self.entry_zona = ctk.CTkEntry(self.tab_view.tab("Configuração"), 
                                       placeholder_text="Ex: 'Zona Norte SP' ou 'Campinas'", 
                                       width=300, height=40, border_color="#808000")
        
        self.entry_tipo_empresa.bind("<KeyRelease>", self.check_admin_inputs)
        self.entry_zona.bind("<KeyRelease>", self.check_admin_inputs)
        
        # --- 2. BOTÕES DE AÇÃO ---
        self.button_iniciar = ctk.CTkButton(
            self.tab_view.tab("Configuração"),
            text="INICIAR PROSPECÇÃO (VAMOS COM TUDO!)", 
            command=self.iniciar_prospeccao,
            fg_color="#808000",
            hover_color="#556B2F",
            state="disabled" 
        )
        self.button_iniciar.grid(row=4, column=0, padx=20, pady=(10, 5), sticky="n")
        
        self.button_continuar = ctk.CTkButton(
            self.tab_view.tab("Configuração"),
            text="REFAZER BUSCA (RESOLVI O CAPTCHA, AMIGA!)", 
            command=self.continuar_extracao,
            fg_color="orange",
            hover_color="#CC8400" 
        )
        
        # Botão 1: Entrar no Modo Administrador (Busca Livre)
        self.button_admin = ctk.CTkButton(
            self.tab_view.tab("Configuração"),
            text="🔑 ENTRAR NO MODO ADMINISTRADOR (BUSCA LIVRE)", 
            command=lambda: self.open_password_dialog(self.switch_to_admin_mode), # Passa a função como callback
            fg_color="gray",
            hover_color="#696969" 
        )
        self.button_admin.grid(row=5, column=0, padx=20, pady=(20, 5), sticky="n")
        
        # Botão 2: Configurar Menus Padrão (Novo)
        self.button_config = ctk.CTkButton(
            self.tab_view.tab("Configuração"),
            text="⚙️ CONFIGURAR OPÇÕES PADRÃO (EDITAR MENUS)", 
            command=lambda: self.open_password_dialog(self.create_config_window), # Passa a função como callback
            fg_color="darkred",
            hover_color="#8b0000" 
        )
        self.button_config.grid(row=5, column=0, padx=20, pady=(60, 10), sticky="n") 

        # Label de Status
        self.label_status = ctk.CTkLabel(
            self.tab_view.tab("Configuração"),
            text="Status: Hermes no aguardo da sua seleção...",
            text_color="gray",
            font=ctk.CTkFont(size=14)
        )
        self.label_status.grid(row=6, column=0, padx=20, pady=(30, 20), sticky="n")
        
        # Textbox para Exibir Resultados (Aba Resultados)
        self.results_textbox = ctk.CTkTextbox(
            self.tab_view.tab("Resultados"),
            fg_color="#F5F5F5",
            text_color="black", 
            width=650, 
            height=400,
            border_color="#808000",
            border_width=2
        )
        self.results_textbox.grid(row=0, column=0, padx=20, pady=20, sticky="nsew")
        self.results_textbox.insert("0.0", "Os resultados da prospecção aparecerão aqui...")
        self.results_textbox.configure(state="disabled")
        
        self.check_default_inputs() 

    # --- LÓGICAS DE CONTROLE DE MODO ---
    
    # Função unificada para checar senha e executar um callback (CORREÇÃO FINAL)
    def open_password_dialog(self, callback_func):
        dialog = ctk.CTkInputDialog(text="Digite a senha de Administrador:", title="Acesso Restrito")
        
        senha_digitada = dialog.get_input()
        
        # VERIFICAÇÃO CORRIGIDA com .strip()
        if senha_digitada is not None:
            # Remove espaços em branco antes e depois da senha digitada
            senha_limpa = senha_digitada.strip() 
            
            if senha_limpa == "adm123":
                self.label_status.configure(text="Status: Senha correta. Abrindo modo Admin...")
                callback_func() 
            else:
                self.label_status.configure(text="Status: Senha incorreta. Tente novamente.")
            
    # Lógica para o Modo Padrão (ComboBoxes)
    def check_default_inputs(self, choice=None):
        self.is_admin_mode = False
        
        # Garante que os campos de entrada livre (Admin) não estejam visíveis
        self.entry_tipo_empresa.grid_forget()
        self.entry_zona.grid_forget()
        
        # Garante que os ComboBoxes (Padrão) estejam visíveis
        self.label_tipo_default.configure(text="1. Amiga, qual tipo de empresa vamos prospectar?")
        self.label_tipo_default.grid(row=0, column=0, padx=20, pady=(20, 0), sticky="s")
        self.combo_tipo_empresa.grid(row=1, column=0, padx=20, pady=(5, 10), sticky="n")
        
        self.label_zona_default.configure(text="2. Em qual zona de SP Capital vamos focar?")
        self.label_zona_default.grid(row=2, column=0, padx=20, pady=(10, 0), sticky="s")
        self.combo_zona.grid(row=3, column=0, padx=20, pady=(5, 10), sticky="n")
        
        empresa = self.combo_tipo_empresa.get()
        zona = self.combo_zona.get()
        
        if empresa != "Selecione..." and zona != "Selecione...":
            self.button_iniciar.configure(state="normal")
        else:
            self.button_iniciar.configure(state="disabled")

    # Lógica para o Modo Administrador (Entry Fields)
    def check_admin_inputs(self, event=None):
        tipo = self.entry_tipo_empresa.get().strip()
        zona = self.entry_zona.get().strip()
        
        if tipo and zona:
            self.button_iniciar.configure(state="normal")
        else:
            self.button_iniciar.configure(state="disabled")

    # Função que troca a interface para o Modo Administrador (Busca Livre)
    def switch_to_admin_mode(self):
        self.is_admin_mode = True
        
        # 1. Esconde os elementos do Modo Padrão
        self.combo_tipo_empresa.grid_forget()
        self.combo_zona.grid_forget()
        
        # 2. Mostra os labels e campos de entrada livre (Admin)
        self.label_tipo_default.configure(text="1. Digite o Tipo de Empresa (Livre):")
        self.label_tipo_default.grid(row=0, column=0, padx=20, pady=(20, 0), sticky="s")
        self.entry_tipo_empresa.grid(row=1, column=0, padx=20, pady=(5, 10), sticky="n")

        self.label_zona_default.configure(text="2. Digite a Zona ou Região (Livre):")
        self.label_zona_default.grid(row=2, column=0, padx=20, pady=(10, 0), sticky="s")
        self.entry_zona.grid(row=3, column=0, padx=20, pady=(5, 10), sticky="n")
        
        # 3. Atualiza o status e desabilita os botões ADMIN
        self.label_status.configure(text="Status: MODO ADMINISTRADOR ATIVO. Digite sua busca.")
        self.button_admin.configure(text="MODO ADMINISTRADOR ATIVO", state="disabled", fg_color="green")
        self.button_config.grid_forget()
        self.button_iniciar.configure(state="disabled")

    # --- NOVO MENU DE CONFIGURAÇÃO ADMIN ---

    def create_config_window(self):
        # Garante que a janela só possa ser aberta uma vez
        if hasattr(self, 'config_window') and self.config_window.winfo_exists():
            self.config_window.focus()
            return
            
        self.config_window = ctk.CTkToplevel(self)
        self.config_window.title("Configuração de Opções Padrão")
        self.config_window.geometry("500x500")
        self.config_window.transient(self) 
        
        self.config_window.grid_columnconfigure(0, weight=1)

        # Frame Tipos de Empresa
        frame_tipos = ctk.CTkFrame(self.config_window, fg_color="transparent")
        frame_tipos.grid(row=0, column=0, padx=20, pady=10, sticky="ew")
        frame_tipos.grid_columnconfigure(0, weight=1)
        
        ctk.CTkLabel(frame_tipos, text="OPÇÕES DE TIPO DE EMPRESA:", font=ctk.CTkFont(weight="bold")).grid(row=0, column=0, pady=(10, 5), sticky="w")
        
        self.entry_add_tipo = ctk.CTkEntry(frame_tipos, placeholder_text="Novo Tipo (ex: 'Construtoras')")
        self.entry_add_tipo.grid(row=1, column=0, sticky="ew", padx=(0, 5))
        ctk.CTkButton(frame_tipos, text="+ Adicionar", command=lambda: self.add_option(self.default_tipos, self.entry_add_tipo.get().strip(), self.listbox_tipos)).grid(row=1, column=1, padx=(5, 0))

        # Listbox para Tipos
        self.listbox_tipos = ctk.CTkScrollableFrame(frame_tipos, label_text="Tipos Atuais:", height=100)
        self.listbox_tipos.grid(row=2, column=0, columnspan=2, pady=(10, 0), sticky="ew")
        self.listbox_tipos.grid_columnconfigure(0, weight=1)
        
        # Frame Zonas
        frame_zonas = ctk.CTkFrame(self.config_window, fg_color="transparent")
        frame_zonas.grid(row=1, column=0, padx=20, pady=10, sticky="ew")
        frame_zonas.grid_columnconfigure(0, weight=1)
        
        ctk.CTkLabel(frame_zonas, text="OPÇÕES DE ZONA/REGIÃO:", font=ctk.CTkFont(weight="bold")).grid(row=0, column=0, pady=(10, 5), sticky="w")

        self.entry_add_zona = ctk.CTkEntry(frame_zonas, placeholder_text="Nova Zona (ex: 'Zona Oeste SP')")
        self.entry_add_zona.grid(row=1, column=0, sticky="ew", padx=(0, 5))
        ctk.CTkButton(frame_zonas, text="+ Adicionar", command=lambda: self.add_option(self.default_zonas, self.entry_add_zona.get().strip(), self.listbox_zonas)).grid(row=1, column=1, padx=(5, 0))

        # Listbox para Zonas
        self.listbox_zonas = ctk.CTkScrollableFrame(frame_zonas, label_text="Zonas Atuais:", height=100)
        self.listbox_zonas.grid(row=2, column=0, columnspan=2, pady=(10, 0), sticky="ew")
        self.listbox_zonas.grid_columnconfigure(0, weight=1)

        # Botão Fechar e Salvar
        ctk.CTkButton(self.config_window, text="FECHAR E SALVAR", command=self.close_config_window, fg_color="darkred", hover_color="#8b0000").grid(row=2, column=0, pady=20)
        
        # Carrega as opções iniciais
        self.refresh_listbox(self.default_tipos, self.listbox_tipos)
        self.refresh_listbox(self.default_zonas, self.listbox_zonas)
        
    def add_option(self, options_list, new_option, listbox_widget):
        if new_option and new_option not in options_list:
            options_list.append(new_option)
            self.refresh_listbox(options_list, listbox_widget)
            self.label_status.configure(text=f"Status: Opção '{new_option}' adicionada (será aplicada ao fechar).")
            # Limpa o campo de entrada para nova digitação
            if listbox_widget == self.listbox_tipos:
                self.entry_add_tipo.delete(0, 'end')
            elif listbox_widget == self.listbox_zonas:
                self.entry_add_zona.delete(0, 'end')

    def remove_option(self, options_list, option_to_remove, listbox_widget):
        if option_to_remove in options_list:
            options_list.remove(option_to_remove)
            self.refresh_listbox(options_list, listbox_widget)
            self.label_status.configure(text=f"Status: Opção '{option_to_remove}' removida.")

    def refresh_listbox(self, options_list, listbox_widget):
        # Limpa o frame
        for widget in listbox_widget.winfo_children():
            widget.destroy()
            
        # Adiciona os itens atualizados
        for i, option in enumerate(options_list):
            label = ctk.CTkLabel(listbox_widget, text=option, anchor="w")
            label.grid(row=i, column=0, padx=5, pady=2, sticky="ew")
            
            # Botão de remover
            btn_remove = ctk.CTkButton(listbox_widget, text="X", width=30, fg_color="red", hover_color="#cc0000",
                                       command=lambda opt=option, lst=options_list, wid=listbox_widget: self.remove_option(lst, opt, wid))
            btn_remove.grid(row=i, column=1, padx=5, pady=2)
            
    def close_config_window(self):
        # Atualiza os ComboBoxes com as novas listas
        self.update_comboboxes()
        self.config_window.destroy()
        self.label_status.configure(text="Status: Configurações padrão salvas e aplicadas aos menus.")
        
    def update_comboboxes(self):
        # Atualiza a lista de opções do ComboBox Tipo de Empresa
        self.combo_tipo_empresa.configure(values=self.default_tipos)
        self.combo_tipo_empresa.set("Selecione...") 
        
        # Atualiza a lista de opções do ComboBox Zona
        self.combo_zona.configure(values=self.default_zonas)
        self.combo_zona.set("Selecione...") 
        
        self.button_iniciar.configure(state="disabled")

    # --- LÓGICAS DE EXECUÇÃO (SEM ALTERAÇÃO) ---

    def iniciar_prospeccao(self):
        # Lógica de pegar os valores de acordo com o modo Admin ou Padrão
        if self.is_admin_mode:
            tipo = self.entry_tipo_empresa.get().strip()
            zona = self.entry_zona.get().strip()
            termo_busca = f"{tipo} {zona} contato"
        else:
            tipo = self.combo_tipo_empresa.get()
            zona = self.combo_zona.get()
            if tipo == "Selecione..." or zona == "Selecione...":
                self.label_status.configure(text="Status: Amiga, selecione os campos corretamente, por favor.")
                return

            termo_busca = f"{tipo} {zona} São Paulo contato"
        
        self.results_textbox.configure(state="normal")
        self.results_textbox.delete("0.0", "end")
        self.label_status.configure(text=f"Status: Iniciando busca por '{termo_busca}'. Abrindo o Chrome...")
        self.update()

        try:
            if not self.driver:
                chrome_options = Options()
                chrome_options.add_experimental_option("detach", True) 
                self.driver = webdriver.Chrome(options=chrome_options)
            
            self.realizar_extracao(termo_busca)

        except Exception as e:
            self.label_status.configure(text=f"Status: ERRO CRÍTICO ao abrir o Chrome. Amiga, veja se o Chrome está instalado. Erro: {e}")
            self.results_textbox.configure(state="disabled")

    def continuar_extracao(self):
        if self.driver:
            if self.is_admin_mode:
                tipo = self.entry_tipo_empresa.get().strip()
                zona = self.entry_zona.get().strip()
                termo_busca = f"{tipo} {zona} contato"
            else:
                tipo = self.combo_tipo_empresa.get()
                zona = self.combo_zona.get()
                termo_busca = f"{tipo} {zona} São Paulo contato"

            self.realizar_extracao(termo_busca)
        else:
            self.label_status.configure(text="Status: ERRO! Amiga, clique em INICIAR PROSPECÇÃO primeiro.")

    def realizar_extracao(self, termo_busca):
        self.button_continuar.grid_forget()
        
        driver = self.driver
        
        self.label_status.configure(text=f"Status: Hermes prosseguindo com a busca por '{termo_busca}'...")
        self.update()

        try:
            url_pesquisa = f"https://www.google.com/search?q={termo_busca}"
            driver.get(url_pesquisa)
            time.sleep(4)

            # --- 🛑 VERIFICAÇÃO DE BLOQUEIO (o Google nos pegou!) ---
            if "sorry/index" in driver.current_url or "unusual traffic" in driver.page_source:
                self.button_continuar.grid(row=5, column=0, padx=20, pady=10, sticky="n") 
                self.label_status.configure(text="Status: 🛑 BLOQUEIO DETECTADO. Resolve o Captcha no Chrome e clica no botão, amiga!")
                return
            
            self.label_status.configure(text="Status: Analisando resultados. Quase lá...")

            # --- EXTRAÇÃO DE DADOS ---
            elementos_locais = driver.find_elements(By.CSS_SELECTOR, 'div.rllt__details')
            
            if not elementos_locais:
                elementos_locais = driver.find_elements(By.XPATH, "//div[contains(@class, 'g')]")
            
            dados_encontrados = []
            output_texto = ""

            for i, elemento in enumerate(elementos_locais):
                link_site = "Link Não Encontrado" 
                
                try:
                    # 1. CAPTURAR O LINK DE BACKUP (HREF)
                    try:
                        link_element = elemento.find_element(By.TAG_NAME, 'a')
                        link_site = link_element.get_attribute('href')
                    except Exception:
                        link_site = "Link Não Encontrado"

                    # 2. Tenta encontrar o nome
                    try:
                        nome_element = elemento.find_element(By.CSS_SELECTOR, 'h3')
                    except:
                        nome_element = elemento.find_element(By.CSS_SELECTOR, 'div.dbg0pd')

                    nome = nome_element.text if nome_element.text else "Nome Não Encontrado"
                    
                    if nome in ["Imagens", "Vídeos", "Notícias"]:
                        continue

                    # 3. Tenta encontrar Endereço e Telefone (busca detalhada)
                    endereco = "Endereço Não Encontrado"
                    telefone = "Telefone Não Encontrado"
                    
                    detalhes = elemento.find_elements(By.XPATH, ".//span[@class='rllt__details']")
                    
                    for detalhe in detalhes:
                        texto_detalhe = detalhe.text
                        if "Endereço:" in texto_detalhe:
                            endereco = texto_detalhe.replace("Endereço: ", "").strip()
                        if "Telefone:" in texto_detalhe or texto_detalhe.replace(' ', '').isdigit():
                            telefone = texto_detalhe.replace("Telefone: ", "").strip()
                    
                    # 4. LÓGICA DE BACKUP: O nosso Plano B!
                    if endereco == "Endereço Não Encontrado" and link_site != "Link Não Encontrado":
                         endereco = f"VERIFICAR MANUAL: {link_site}"
                         
                    if telefone == "Telefone Não Encontrado" and link_site != "Link Não Encontrado" and not endereco.startswith("VERIFICAR MANUAL"):
                         telefone = f"VERIFICAR MANUAL: {link_site}"
                         
                    # 5. Salva o resultado
                    if nome != "Nome Não Encontrado":
                        dados_encontrados.append({"Nome": nome, "Endereco": endereco, "Telefone": telefone})
                        
                        output_texto += f"--- Empresa {i+1} ---\nNome: {nome}\nEndereço: {endereco}\nTelefone: {telefone}\n\n"
                    
                except Exception:
                    continue 

            if dados_encontrados:
                df = pd.DataFrame(dados_encontrados)
                df.to_csv("resultados_hermes.csv", index=False, encoding='utf-8')
                
                self.results_textbox.insert("0.0", output_texto)
                self.results_textbox.configure(state="disabled")

                self.label_status.configure(text=f"Status: SUCESSO! Amiga, {len(dados_encontrados)} empresas extraídas e salvas no arquivo 'resultados_hermes.csv' e na aba 'Resultados'.")
                self.tab_view.set("Resultados")
                
            else:
                self.results_textbox.insert("0.0", "Ops! Nenhuma empresa encontrada com a estrutura esperada nesta busca.")
                self.results_textbox.configure(state="disabled")
                self.label_status.configure(text="Status: Nenhuma empresa encontrada com essa estrutura de resultados.")

        except Exception as e:
            self.label_status.configure(text=f"Status: ERRO CRÍTICO! Amiga, falha na automação. Erro: {e}")
            self.results_textbox.configure(state="disabled")

if __name__ == "__main__":
    app = HermesProspector()
    app.mainloop()