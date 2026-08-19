# Roadmap — Disparador de E-mails

Este documento organiza a evolução planejada do projeto, da versão MVP até funcionalidades mais avançadas. Serve tanto como guia de desenvolvimento quanto como demonstração, para quem visitar o repositório, de visão de produto e capacidade de planejamento técnico.

## 🚧 Fase 0 — MVP (em andamento)

- [x] Estrutura inicial do projeto
- [ ] Leitura de contatos via CSV com `pandas`
- [ ] Personalização do corpo do e-mail com placeholders (`{nome}`)
- [ ] Montagem de e-mail com `email.mime` (corpo + anexo)
- [ ] Envio via `smtplib` (SMTP_SSL)
- [ ] Autenticação via variáveis de ambiente (`.env`)
- [ ] Log de sucesso/falha por contato
- [x] README com instruções de setup

## 🔜 Fase 1 — Robustez e qualidade

- [ ] Testes unitários cobrindo `email_sender.py` e `contact_loader.py` (mockando SMTP)
- [ ] Validação de e-mails antes do envio (formato válido)
- [ ] Rate limiting configurável entre envios (`time.sleep`) para evitar bloqueio por spam
- [ ] Retry automático em caso de falha temporária de conexão
- [ ] Log estruturado em arquivo (`.log`) além do console
- [ ] Relatório final ao término da execução (X enviados, Y falhas, lista de erros)

## 🔜 Fase 2 — Templates mais ricos

- [ ] Migrar personalização de `.format()` para **Jinja2**, permitindo templates HTML mais elaborados
- [ ] Suporte a múltiplos campos personalizáveis além do nome (empresa, cargo, etc.)
- [ ] Biblioteca de templates prontos (ex.: convite, cobrança, newsletter)
- [ ] Pré-visualização do e-mail renderizado antes do envio (modo `--dry-run`)

## 🔜 Fase 3 — Usabilidade

- [ ] Interface via linha de comando com `argparse` ou `click` (escolher CSV, template e remetente na hora de rodar)
- [ ] Dashboard simples com **Streamlit** mostrando status dos envios em tempo real
- [ ] Exportação do relatório de envios em CSV/Excel

## 🔜 Fase 4 — Escala e integrações

- [ ] Suporte a envio assíncrono com `asyncio` para grandes volumes
- [ ] Fila de processamento com **Celery** + Redis para envios em background
- [ ] Suporte a provedores alternativos ao SMTP puro (SendGrid, Amazon SES)
- [ ] Webhook de confirmação de entrega/abertura (quando suportado pelo provedor)

## 💡 Ideias em avaliação (não priorizadas)

- Suporte a envio de SMS/WhatsApp como canal alternativo
- Autenticação OAuth2 para provedores que exigem (em vez de senha de app)
- Empacotamento como CLI instalável via `pip install`

## Como contribuir com o roadmap

Sugestões são bem-vindas via issues no repositório. Ao abrir uma proposta, descreva o problema que a funcionalidade resolve antes de detalhar a implementação.
