# 🚀 Hermes, O Prospector | Robô de Automação de Prospecção (RPA)

## 🛠️ Tecnologias e Funcionalidades

| Recurso | Descrição |
| :--- | :--- | 
| **Tecnologia Base** | Desenvolvido em **Python** utilizando bibliotecas como **Selenium** para Web Scraping e **CustomTkinter** para a UI. |
| **Usabilidade Amiga** | Interface construída com **CustomTkinter** para menus interativos, **eliminando erros de digitação** na busca e facilitando a operação por usuários não técnicos. |
| **Resiliência (Anti-Google)** | Lida com bloqueios comuns, como **CAPTCHA** e instabilidade na estrutura **HTML** do Google, usando lógica de *backup* para garantir a continuidade da operação. |
| **Entrega Garantida (Plano B)** | Se não for possível extrair o contato na hora, o robô fornece o **link direto** da fonte, garantindo que a informação seja sempre acionável (Entrega Garantida). |
| **Gerenciamento** | Implementada uma **Área do Administrador** para alterar tópicos e gerenciar configurações (em desenvolvimento). |

> Diário de Bordo: Guia de Estudo e Resiliência do Hermes.

Este projeto é um robô de automação (RPA) desenvolvido para **acelerar a prospecção comercial** em São Paulo. O Hermes busca informações de contato (Endereço, Telefone, Link) de empresas específicas, utilizando menus interativos para garantir a precisão e a robustez dos dados entregues.

---

## 🎯 Objetivo

O principal objetivo do Hermes é otimizar o processo de vendas e operações, automatizando a coleta de **leads qualificados**, permitindo que o time comercial se concentre na conversão, e não na busca manual de dados.

## 🛠️ Tecnologias e Funcionalidades

| Recurso | Descrição |
| :--- | :--- |
| **Usabilidade Amiga** | Interface construída com **CustomTkinter** para menus interativos, **eliminando erros de digitação** na busca e facilitando a operação por usuários não técnicos. |
| **Resiliência (Anti-Google)** | Lida com bloqueios comuns, como **CAPTCHA** e instabilidade na estrutura **HTML** do Google, usando lógica de *backup* para garantir a continuidade da operação. |
| **Entrega Garantida (Plano B)** | Se não for possível extrair o contato na hora, o robô fornece o **link direto** da fonte, garantindo que a informação seja sempre acionável (Entrega Garantida). |
| **Gerenciamento** | Implementada uma **Área do Administrador** para alterar tópicos e gerenciar configurações (em desenvolvimento). |

## 🛡️ Entendendo a Resiliência e Falhas

A resiliência é um pilar do Hermes. O retorno "Não Encontrado" é **condicional** e só é acionado em um cenário muito específico, demonstrando a lógica de *backup* robusta:

* **Cenário de Falha Único ("Não Encontrado"):**
    * O robô falha ao encontrar um link válido (`href`) dentro do bloco de resultado do Google.
    * *Isso acontece quando:* O bloco é um resultado genérico (Imagens, Notícias) **E** o Google usou uma estrutura de HTML tão confusa que o robô não conseguiu ler a *tag* `<a>` (link).
* **Ação de Backup ("VERIFICAR MANUAL"):**
    * Se o Hermes conseguir extrair o Link (URL) — mas não o Nome ou o Contato —, ele preenche o campo como **VERIFICAR MANUAL: [URL]**.
    * O termo "Não Encontrado" é retornado **apenas** se o bloco for lixo digital **sem nenhuma** informação útil (Nome, Contato ou Link).

---

---

## 📅 Status Atual e Próximos Passos

* **Última Atualização:** 15/12/2025
* **Problemas Conhecidos:** Detecção de falhas de *layout* (sobreposição de botões) e erros de lógica na **Área do Administrador**.
* **Próximos Passos:** Corrigir os *bugs* de *layout* na interface do Administrador e refinar a lógica de gerenciamento de tópicos.
