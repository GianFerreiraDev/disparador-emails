# Project Context — Disparador de E-mails

## Visão geral

Sistema em Python para automatizar o disparo de e-mails personalizados em massa, com suporte a anexos individuais por contato. O projeto foi criado como peça de portfólio para demonstrar domínio de automação, manipulação de dados e boas práticas de engenharia de software.

## Problema que resolve

Envio manual de e-mails personalizados para listas de contatos é repetitivo, sujeito a erro humano (nome errado, anexo trocado, esquecimento) e não escala. Este sistema automatiza o processo inteiro: leitura da lista, personalização do texto, montagem do e-mail com anexo e envio via SMTP, registrando o resultado de cada tentativa.

## Objetivo do projeto

- Servir como demonstração prática de habilidades técnicas em um repositório público no GitHub.
- Mostrar conhecimento de bibliotecas nativas do Python (`smtplib`, `email.mime`) combinadas com `pandas` para dados tabulares.
- Aplicar boas práticas: separação de responsabilidades, tratamento de erros, variáveis de ambiente, logging e testes.

## Escopo

**Dentro do escopo (MVP):**
- Leitura de contatos via CSV (colunas: nome, email, anexo).
- Personalização do corpo do e-mail com placeholders (`{nome}`).
- Envio via SMTP (SMTP_SSL), com autenticação via `.env`.
- Anexo automático de arquivo por contato.
- Log de sucesso/falha por envio.
- Testes unitários básicos (mockando o SMTP).

**Fora do escopo (por enquanto):**
- Interface gráfica.
- Fila assíncrona de envio em larga escala.
- Suporte a múltiplos provedores de e-mail (SendGrid, SES) — ver `roadmap.md`.
- Agendamento de envios recorrentes.

## Público-alvo do projeto (portfólio)

Recrutadores técnicos e desenvolvedores avaliando o repositório no GitHub. O código deve ser legível, bem documentado e demonstrar decisões de design conscientes (por exemplo, por que usar variáveis de ambiente em vez de credenciais hardcoded).

## Stack técnica

| Camada | Tecnologia |
|---|---|
| Linguagem | Python 3.11+ |
| Dados | pandas |
| E-mail | smtplib, email.mime |
| Configuração | python-dotenv |
| Testes | unittest / pytest |
| Logs | logging (módulo padrão) |

## Decisões de design

- **Sem credenciais no código**: todas as credenciais SMTP ficam em `.env`, nunca commitado (presente no `.gitignore`).
- **Falha isolada por contato**: um erro de envio (e-mail inválido, anexo ausente) não interrompe o processamento dos demais contatos.
- **Template simples primeiro**: uso de `.format()` com placeholders no MVP, com plano de migrar para Jinja2 conforme o roadmap.
- **SMTP puro no MVP**: evita dependência de serviços pagos/externos na primeira versão, mantendo o projeto simples de rodar localmente.

## Riscos e considerações éticas

- O projeto é destinado a envios legítimos (ex.: comunicação com clientes que optaram por receber e-mails). O README deixa isso explícito para evitar uso como ferramenta de spam.
- Provedores como Gmail exigem "senha de app" (App Password) para autenticação via SMTP — isso deve estar documentado no README.
- Rate limiting é necessário para evitar bloqueio da conta de envio por comportamento suspeito.

## Status atual

Em desenvolvimento — estrutura do projeto definida, próximos passos detalhados no `roadmap.md`.
