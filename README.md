# Calculadora de Sistemas Lineares

Aplicação web para resolver sistemas de equações lineares, desenvolvida como trabalho da faculdade.

O projeto é um monorepo com duas partes:

- **backend/**: API REST em **FastAPI**
- **frontend/**: interface em **React** + **TypeScript**, criada com **Vite**

> Por enquanto o projeto contém a estrutura inicial: um endpoint de verificação (`GET /api/health/`), o endpoint `POST /api/linear-system/solve/` (por enquanto só responde `{"message": "não implementado"}`) e uma tela que mostra se o frontend consegue falar com o backend.

---

## Pré-requisitos

| Ferramenta | Versão mínima | Recomendada |
| ---------- | ------------- | ----------- |
| Python     | 3.10          | 3.13 (mais recente) |
| Node.js    | 22.12         | 24 LTS |
| npm        | vem junto com o Node.js | |
| Git        | qualquer versão recente | |

Para conferir as versões instaladas:

```bash
python --version
node --version
npm --version
```

> É comum ter mais de uma versão de Python instalada e o comando `python` apontar para uma antiga. No Windows, veja todas as versões com `py --list`.

---

## Rodando o backend (FastAPI)

Todos os comandos abaixo são executados **dentro da pasta `backend/`**:

```bash
cd backend
```

### 1. Criar o ambiente virtual (venv)

**Windows:** use o launcher `py` com a versão desejada (veja as instaladas com `py --list`):

```powershell
py -3.13 -m venv venv
```

**Linux / Mac:**

```bash
python3 -m venv venv
```

**Criou o venv com a versão errada?** Rodar o comando de novo por cima **não resolve**, porque os pacotes antigos continuam na pasta. Recrie do zero com `--clear` (ex.: `py -3.13 -m venv --clear venv`) e repita o passo 2.

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

Confira se o venv está com a versão certa:

```bash
python --version
```

### 3. Instalar as dependências

```bash
pip install -r requirements.txt
```

### 4. Iniciar o servidor

```bash
uvicorn main:app --reload
```

O backend fica disponível em **http://localhost:8000**. Para testar, abra http://localhost:8000/api/health/ no navegador. A resposta deve ser:

```json
{"status": "ok", "message": "Backend funcionando"}
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

1. Deixe o **backend** rodando (`uvicorn main:app --reload`, porta 8000).
2. Deixe o **frontend** rodando (`npm run dev`, porta 5173).
3. Abra **http://localhost:5173** no navegador.

Você deve ver o título **Calculadora de Sistemas Lineares** e a mensagem:

> Backend funcionando (status: ok)

Se aparecer a mensagem **"Não foi possível conectar ao backend..."**, o backend não está rodando (ou não está na porta 8000).

**Como funciona a conexão:** o frontend sempre chama caminhos relativos como `/api/health/`. Em desenvolvimento, o servidor do Vite tem um *proxy* (configurado em `frontend/vite.config.ts`) que repassa tudo que começa com `/api` para o FastAPI em `http://localhost:8000`. Por isso o frontend não precisa saber a porta do backend. O FastAPI também está com CORS liberado para `http://localhost:5173` em modo de desenvolvimento.

---

## Problemas comuns

**PowerShell: "a execução de scripts foi desabilitada neste sistema"**

Rode uma vez `Set-ExecutionPolicy -Scope CurrentUser RemoteSigned` e ative o venv de novo.

**A tela mostra "Não foi possível conectar ao backend..."**

O backend não está rodando, ou não está na porta 8000. Suba o backend com `uvicorn main:app --reload` (com o venv ativo) e recarregue a página.

---

## Estrutura de pastas

```
calculadora-sistemas-lineares/
├── backend/                  # API em FastAPI
│   ├── main.py               # ponto de entrada: instância do FastAPI e inclusão dos routers
│   ├── api/
│   │   └── routes/           #   endpoints (um arquivo por recurso)
│   │       ├── health.py     #     GET /api/health/
│   │       └── linear_system.py  # POST /api/linear-system/solve/ (não implementado)
│   ├── schemas/              #   modelos Pydantic (request/response de cada rota)
│   ├── services/             #   regras de negócio (sem depender do FastAPI)
│   ├── requirements.txt      # Dependências Python com versões fixadas
│   └── venv/                 # ambiente virtual (não vai para o Git)
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
├── .gitignore                # Ignora venv, node_modules, .env, IDEs...
└── README.md
```

### Onde colocar cada coisa

**Backend**

O backend segue a separação clássica de responsabilidades: **rota → schema → service**.

- **Novo endpoint:** crie (ou adicione em) um arquivo em `backend/api/routes/`, usando `APIRouter` com prefixo começando por `/api/`. A função da rota só deve receber o request, chamar o `service` e devolver o resultado — sem lógica de negócio ali.
- **Formato de entrada/saída (request/response):** defina as classes Pydantic em `backend/schemas/`. É aqui que fica a validação do formato dos dados recebidos.
- **Regra de negócio:** implemente em `backend/services/` como funções Python normais, sem depender do FastAPI. Isso deixa a lógica testável isoladamente, sem precisar subir o servidor.
- **Registrar a rota:** depois de criar o router em `api/routes/`, inclua-o em `backend/main.py` com `app.include_router(...)`.

> Os nomes de arquivos, classes e variáveis do código ficam em inglês (mesmo padrão do frontend); textos voltados ao usuário continuam em português.

**Frontend**

- **Nova tela:** crie em `src/pages/`.
- **Componente reutilizável:** crie em `src/components/`.
- **Chamada ao backend:** use a função `apiFetch` de `src/api/client.ts`, sempre com caminhos começando por `/api/` (ex.: `apiFetch<MeuTipo>('/api/minha-rota/')`).

### O que não vai para o Git

O `.gitignore` já cuida disso, mas vale saber: **não versione** `venv/` nem `node_modules/`/`dist/`. Cada integrante gera essas pastas localmente seguindo os passos acima.
