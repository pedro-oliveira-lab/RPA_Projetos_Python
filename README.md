Guia de Estudo do Hermes, O Prospector:
Este é o nosso diário de bordo revisado, explicando a lógica de código e a resiliência do nosso Hermes contra os caprichos do Google.
Ideia e Propósito do Projeto
Hermes, o Prospector, é um robô de automação (RPA) que criamos para acelerar a prospecção comercial em São Paulo. Ele busca informações de contato (Endereço, Telefone, Link) de empresas específicas, usando menus interativos para precisão e lógica robusta para garantir a entrega dos dados.
O que o Hermes faz de especial:
•	Usabilidade Amiga: Usa CustomTkinter para menus interativos, eliminando erros de digitação na busca.
•	Resiliência: Lida com bloqueios (Captcha) e instabilidade de HTML usando lógica de backup.
•	Entrega Garantida (O Plano B): Se não achar o contato na hora, ele entrega o link direto para a gente verificar manualmente, garantindo que a informação seja sempre acionável.
Entendendo a Resiliência (Por que às vezes falha?)
Você perguntou: por que ele retorna "Não Encontrado" se a ideia é trazer o link como backup?
A lógica de backup do Hermes é condicional, e o "Não Encontrado" só aparece em um único cenário:
1.	O robô falha em encontrar um link válido (href) dentro daquele bloco de resultado do Google.
Isso acontece quando:
•	O bloco é um resultado genérico (Imagens, Notícias) que não tem uma URL primária útil.
•	O Google usou uma estrutura de HTML tão confusa para aquele bloco que o robô não conseguiu nem ler a tag <a> (link).
Sempre que o Hermes consegue extrair o Link, mas não o Contato, ele preencherá o campo com VERIFICAR MANUAL: [URL].
O "Não Encontrado" só é retornado se o bloco for lixo digital sem nenhuma informação útil (Nome, Contato ou Link).
Última Atualização:
Implementamos a área do administrador e alterar tópicos, ainda sem função e ainda não detectei o erro da senha (o motivo dele).
TENTEM NÃO ME JULGAR POIS FIZ EM TRÊS DIAS E JÁ ESTAVA DOIDO.	
