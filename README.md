# 📧 Disparador de E-mails

Sistema em Python que lê uma lista de contatos, personaliza o texto do e-mail por nome e envia anexos automáticos individualmente para cada destinatário — usando apenas `smtplib`, `email.mime` e `pandas`.

> ⚠️ **Uso ético**: este projeto foi criado para fins educacionais e de portfólio, destinado a envios legítimos (ex.: comunicação com clientes que optaram por receber e-mails). Não deve ser usado para spam ou envio de mensagens não solicitadas.

## ✨ Funcionalidades

- 📋 Leitura de lista de contatos via CSV (com `pandas`)
- ✏️ Personalização automática do texto por nome (e outros campos, se desejado)
- 📎 Anexo automático de arquivos individuais por contato
- 🔐 Autenticação segura via variáveis de ambiente (`.env`)
- 📝 Log de sucesso/falha por envio
- 🛡️ Tratamento de erro isolado — um contato com problema não interrompe os demais

## 🗂️ Estrutura do projeto

```
disparador-emails/
├── README.md
├── requirements.txt
├── .env.example
├── .gitignore
├── config.py
├── main.py
├── src/
│   ├── __init__.py
│   ├── email_sender.py
│   ├── contact_loader.py
│   └── template_engine.py
├── templates/
│   └── email_template.html
├── data/
│   └── contatos_exemplo.csv
├── anexos/
│   └── (anexos de exemplo)
└── tests/
    └── test_email_sender.py
```

## 🚀 Como rodar

### 1. Clone o repositório

```bash
git clone https://github.com/seu-usuario/disparador-emails.git
cd disparador-emails
```

### 2. Crie um ambiente virtual e instale as dependências

```bash
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### 3. Configure as credenciais

Copie o arquivo de exemplo e preencha com suas credenciais:

```bash
cp .env.example .env
```

```env
EMAIL_REMETENTE=seuemail@gmail.com
EMAIL_SENHA=sua_senha_de_app
```

> 💡 **Gmail**: a senha normal da conta não funciona com SMTP. É necessário gerar uma [senha de app](https://support.google.com/accounts/answer/185833) na sua conta Google.

### 4. Prepare a lista de contatos

Edite `data/contatos_exemplo.csv` no formato:

```csv
nome,email,anexo
João Silva,joao@exemplo.com,anexos/proposta_joao.pdf
Maria Souza,maria@exemplo.com,anexos/proposta_maria.pdf
```

### 5. Execute

```bash
python main.py
```

## 🧪 Rodando os testes

```bash
pytest tests/
```

## ⚙️ Configuração SMTP

Por padrão, o projeto está configurado para o Gmail (`smtp.gmail.com`, porta `465`, SSL). Para usar outro provedor, ajuste os parâmetros em `config.py` ou na instância de `EmailSender` em `main.py`.

## 📌 Tecnologias utilizadas

- **Python 3.11+**
- **pandas** — leitura e manipulação da lista de contatos
- **smtplib** — envio via protocolo SMTP
- **email.mime** — montagem de e-mails com corpo HTML e anexos
- **python-dotenv** — gerenciamento seguro de credenciais

## 🗺️ Roadmap

Veja o [roadmap.md](./roadmap.md) para as próximas melhorias planejadas, como suporte a Jinja2, dashboard de status e envio assíncrono.

## 📄 Licença

Este projeto está sob a licença MIT. Sinta-se livre para usar como referência ou ponto de partida para seus próprios projetos.

## 👤 Autor

Desenvolvido por `Gian Ferreira` como projeto de portfólio.
🔗 [LinkedIn](https://www.linkedin.com/in/gian-ferreira-dev/) · [GitHub](https://github.com/GianFerreiraDev/)
