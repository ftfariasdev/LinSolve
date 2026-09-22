# Calculadora de Sistemas Lineares

Aplicação web para resolver sistemas de equações lineares, desenvolvida como trabalho da faculdade.

O projeto é um monorepo com duas partes:

- **backend/**: API REST em **Django** + **Django REST Framework**
- **frontend/**: interface em **React** + **TypeScript**, criada com **Vite**

> Por enquanto o projeto contém só a estrutura inicial: um endpoint de verificação (`GET /api/health/`) e uma tela que mostra se o frontend consegue falar com o backend.

---

## Pré-requisitos

| Ferramenta | Versão mínima | Recomendada |
| ---------- | ------------- | ----------- |
| Python     | 3.12          | 3.14 (mais recente) |
| Node.js    | 22.12         | 24 LTS |
| npm        | vem junto com o Node.js | |
| Git        | qualquer versão recente | |

Para conferir as versões instaladas:

```bash
python --version
node --version
npm --version
```

> **Atenção:** o Django 6.1 **não funciona com Python 3.11 ou anterior**. É comum ter mais de uma versão instalada e o comando `python` apontar para uma antiga. No Windows, veja todas as versões com `py --list`. O passo 1 do backend explica como escolher a versão certa.

---

## Rodando o backend (Django)

Todos os comandos abaixo são executados **dentro da pasta `backend/`**:

```bash
cd backend
```

### 1. Criar o ambiente virtual (venv)

O venv precisa ser criado com **Python 3.12 ou superior**. Por isso, escolha a versão explicitamente em vez de usar só `python`, que pode apontar para uma versão antiga.

**Windows:** use o launcher `py` com a versão desejada (veja as instaladas com `py --list`):

```powershell
py -3.13 -m venv venv
```

> Troque `3.13` pela versão (3.12 ou superior) que você tiver instalada, por exemplo `py -3.14`.

**Linux / Mac:**

```bash
python3 -m venv venv
```

> Se `python3 --version` mostrar uma versão menor que 3.12, use o executável da versão certa, por exemplo `python3.13 -m venv venv`.

**Criou o venv com a versão errada?** Rodar o comando de novo por cima **não resolve**, porque os pacotes antigos continuam na pasta. Recrie do zero com `--clear` (ex.: `py -3.13 -m venv --clear venv`) e repita os passos 2 e 3.

### 2. Ativar o ambiente virtual

**Windows (PowerShell):**

```powershell
.\venv\Scripts\Activate.ps1
```

> Se aparecer um erro dizendo que a execução de scripts está desabilitada, rode uma vez
> `Set-ExecutionPolicy -Scope CurrentUser RemoteSigned` e tente de novo.

**Windows (Prompt de Comando / cmd):**

```bat
venv\Scripts\activate.bat
```

**Windows (Git Bash):**

```bash
source venv/Scripts/activate
```

**Linux / Mac:**

```bash
source venv/bin/activate
```

Com o venv ativo, o terminal passa a mostrar `(venv)` no início da linha. **Ative o venv sempre que abrir um terminal novo para trabalhar no backend.**

Confira se o venv está com a versão certa. O comando abaixo deve mostrar 3.12 ou superior:

```bash
python --version
```

### 3. Instalar as dependências

```bash
pip install -r requirements.txt
```

### 4. Criar o arquivo `.env`

Copie o modelo `.env.example` para `.env`:

**Windows:**

```powershell
copy .env.example .env
```

**Linux / Mac:**

```bash
cp .env.example .env
```

O `.env` guarda a `SECRET_KEY` e o `DEBUG`. Ele **não vai para o Git**, então cada um tem o seu.

### 5. Aplicar as migrações (cria o banco SQLite local)

```bash
python manage.py migrate
```

### 6. Iniciar o servidor

```bash
python manage.py runserver
```

O backend fica disponível em **http://localhost:8000**. Para testar, abra http://localhost:8000/api/health/ no navegador. A resposta deve ser:

```json
{"status": "ok", "message": "Backend funcionando"}
```

### Rodando os testes do backend

```bash
python manage.py test
```

---

## Rodando o frontend (React + Vite)

Abra **outro terminal** (o backend continua rodando no primeiro) e execute:

```bash
cd frontend
npm install
npm run dev
```

O frontend fica disponível em **http://localhost:5173**.

O `npm install` só é necessário na primeira vez ou quando o `package.json` mudar (por exemplo, depois de um `git pull`).

Outros comandos úteis (dentro de `frontend/`):

| Comando           | O que faz |
| ----------------- | --------- |
| `npm run dev`     | Inicia o servidor de desenvolvimento |
| `npm run build`   | Verifica os tipos (TypeScript) e gera a versão de produção em `dist/` |
| `npm run lint`    | Procura problemas no código com o Oxlint |
| `npm run preview` | Serve localmente a versão gerada pelo build |

> O frontend **não precisa** de `.env` para rodar em desenvolvimento. O `frontend/.env.example` só existe caso seja necessário apontar para outra URL de API no futuro.

---

## Testando se está tudo conectado

1. Deixe o **backend** rodando (`python manage.py runserver`, porta 8000).
2. Deixe o **frontend** rodando (`npm run dev`, porta 5173).
3. Abra **http://localhost:5173** no navegador.

Você deve ver o título **Calculadora de Sistemas Lineares** e a mensagem:

> Backend funcionando (status: ok)

Se aparecer a mensagem **"Não foi possível conectar ao backend..."**, o backend não está rodando (ou não está na porta 8000).

**Como funciona a conexão:** o frontend sempre chama caminhos relativos como `/api/health/`. Em desenvolvimento, o servidor do Vite tem um *proxy* (configurado em `frontend/vite.config.ts`) que repassa tudo que começa com `/api` para o Django em `http://localhost:8000`. Por isso o frontend não precisa saber a porta do backend. O Django também está com CORS liberado para `http://localhost:5173` em modo de desenvolvimento.

---

## Problemas comuns

**`ImportError: cannot import name 'markcoroutinefunction' from 'inspect'`** (seguido de *"Couldn't import Django. Are you sure it's installed...?"*)

O venv foi criado com Python 3.11 ou anterior. Repare no caminho do `inspect.py` no erro: ele mostra a versão usada (ex.: `Python311`). A segunda mensagem engana, porque o Django está instalado. O problema é a versão do Python. Para resolver, recrie o venv do zero com uma versão 3.12 ou superior e reinstale as dependências (dentro de `backend/`):

```powershell
deactivate
py -3.13 -m venv --clear venv
.\venv\Scripts\Activate.ps1
python --version
pip install -r requirements.txt
```

No Linux/Mac, use `python3.13 -m venv --clear venv` e `source venv/bin/activate`.

**`django.core.exceptions.ImproperlyConfigured: SECRET_KEY não definida`**

Falta o arquivo `backend/.env`. Veja o passo 4 do backend.

**PowerShell: "a execução de scripts foi desabilitada neste sistema"**

Rode uma vez `Set-ExecutionPolicy -Scope CurrentUser RemoteSigned` e ative o venv de novo.

**A tela mostra "Não foi possível conectar ao backend..."**

O backend não está rodando, ou não está na porta 8000. Suba o backend com `python manage.py runserver` (com o venv ativo) e recarregue a página.

---

## Estrutura de pastas

```
calculadora-sistemas-lineares/
├── backend/                  # API em Django
│   ├── config/               # Configuração do projeto Django
│   │   ├── settings.py       #   configurações (apps, CORS, banco, leitura do .env)
│   │   ├── urls.py           #   rotas principais: /admin/ e /api/
│   │   └── asgi.py / wsgi.py #   pontos de entrada para servidores
│   ├── apps/                 # Apps Django do projeto (cada funcionalidade em um app)
│   │   └── core/             #   app de exemplo com o endpoint /api/health/
│   │       ├── views.py      #     views (o que cada rota responde)
│   │       ├── urls.py       #     rotas do app (incluídas sob /api/)
│   │       ├── tests.py      #     testes do app
│   │       ├── apps.py       #     configuração do app
│   │       └── models.py, admin.py, migrations/  # padrão do Django (vazios por enquanto)
│   ├── manage.py             # CLI do Django (runserver, migrate, test...)
│   ├── requirements.txt      # Dependências Python com versões fixadas
│   └── .env.example          # Modelo do arquivo .env
│
├── frontend/                 # Interface em React + TypeScript (Vite)
│   ├── public/               # Arquivos estáticos servidos como estão (imagens, ícones)
│   ├── src/
│   │   ├── api/
│   │   │   └── client.ts     #   função base (apiFetch) para chamar o backend
│   │   ├── components/       #   componentes reutilizáveis (botões, campos, tabelas...)
│   │   ├── pages/            #   telas da aplicação
│   │   │   └── HealthPage.tsx  # tela de exemplo que chama /api/health/
│   │   ├── App.tsx           #   componente raiz (hoje renderiza só a HealthPage)
│   │   ├── main.tsx          #   ponto de entrada do React
│   │   └── index.css         #   estilos globais
│   ├── index.html            # HTML base onde o React é montado
│   ├── package.json          # Dependências e scripts (dev, build, lint)
│   ├── vite.config.ts        # Configuração do Vite (inclui o proxy /api)
│   ├── tsconfig*.json        # Configuração do TypeScript
│   └── .env.example          # Modelo do arquivo .env (opcional)
│
├── .gitignore                # Ignora venv, node_modules, .env, banco local, IDEs...
└── README.md
```

### Onde colocar cada coisa

**Backend**

- **Nova rota da API:** crie a view em `apps/<app>/views.py` e registre em `apps/<app>/urls.py`. Todas as rotas ficam automaticamente sob `/api/`.
- **Novo app Django:** crie a pasta e o app dentro de `apps/`:

  ```bash
  mkdir apps/nome_do_app
  python manage.py startapp nome_do_app apps/nome_do_app
  ```

  Depois, em `apps/nome_do_app/apps.py`, troque `name = 'nome_do_app'` por `name = 'apps.nome_do_app'`, adicione `'apps.nome_do_app'` em `INSTALLED_APPS` (`config/settings.py`) e inclua as rotas em `config/urls.py`.

**Frontend**

- **Nova tela:** crie em `src/pages/`.
- **Componente reutilizável:** crie em `src/components/`.
- **Chamada ao backend:** use a função `apiFetch` de `src/api/client.ts`, sempre com caminhos começando por `/api/` (ex.: `apiFetch<MeuTipo>('/api/minha-rota/')`).

### O que não vai para o Git

O `.gitignore` já cuida disso, mas vale saber: **não versione** `venv/`, `node_modules/`, `dist/`, `db.sqlite3` nem arquivos `.env`. Cada integrante gera esses arquivos localmente seguindo os passos acima.
