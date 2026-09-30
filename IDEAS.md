# aspython

Framework de backend em Python inspirado no .NET (ASP.NET Core).

## Objetivo

Estudo de fundamentos. Python não foi criada pra backend — foi adaptada. A ideia é
justamente construir do zero, em cima dela, as peças que o .NET entrega prontas, pra
entender na raiz como cada uma funciona.

**Não é pra produção.** Não é pra empresa usar. É pra aprender e pra amigos verem.

## Regra do projeto

**Codar sem IA.** O ponto do projeto é o processo de descobrir como fazer, não o
resultado funcionando. Usar IA pra escrever o código mata o objetivo.

## Ideias / o que eu quero construir

- [ ] **"Buildador" de aplicação** — entender como funciona um host/builder de
      aplicação, tipo o `WebApplicationBuilder`. Como a app se monta, o que acontece
      entre `CreateBuilder()` e `Run()`.

- [ ] **Estrutura pro design pattern Builder** — montar o Builder de verdade, não só
      usar. Encadeamento de configuração, separação entre fase de configuração e fase
      de execução.

- [ ] **Inversão de controle + injeção de dependência automática** — container de DI
      que resolve dependências sozinho. Registrar serviços, resolver por tipo,
      lifetimes (singleton / scoped / transient).

- [ ] **Módulo nativo de acesso e operação a banco** — algo no espírito do EF Core:
      Unit of Work, repositórios, transação controlada, tracking de mudanças.

- [ ] **Decorators nativos pra mapeamento de rotas HTTP** — `@get`, `@post` etc.
      Descoberta e registro automático das rotas, mapeamento prático tipo os
      atributos de controller do ASP.NET.

## Tipagem estática (descoberto em 30/09/2026)

Type hint em Python é quase um comentário — o interpretador ignora. Isso executa
normal, sem erro nenhum:

```python
def soma(n1: float, n2: float) -> str:
    return n1 + n2

soma(1, 2)  # 3
```

Quero o equivalente ao `tsconfig.json`: um arquivo de config que faça hint quebrado
virar erro de verdade, na IDE e no CI.

- [ ] Configurar checagem estática estrita no projeto desde o primeiro commit.

### O que dá e o que não dá

- **Não existe "build" em Python.** Não tem etapa pra abortar. Nenhum arquivo de
  config faz o interpretador recusar rodar código mal tipado. O gate é externo:
  CI, pre-commit hook ou a própria IDE.
- **Lint não checa tipo.** Ruff só força que a anotação *exista* (regras `ANN`).
  Se a anotação está errada, quem pega é o type checker.
- **O checker é opcional pra sempre.** Diferente do TS, onde o `tsc` é obrigatório
  porque o browser não entende TypeScript.

### Escolher UM checker

| | mypy | pyright |
|---|---|---|
| Quem faz | Python / Dropbox | Microsoft |
| É o motor do Pylance (VS Code) | não | **sim** |
| Velocidade | lento | bem mais rápido |
| Inferência (narrowing, generics) | mais fraca | melhor |

Misturar os dois dá erro divergente no mesmo arquivo. Decidir e ficar com um.

Inclinação: **pyright**, porque o Pylance no VS Code já é ele. Ativando
`python.analysis.typeCheckingMode: "strict"` o que aparece na tela é exatamente o
que o CI vai acusar. Com mypy + Pylance os dois discordam.

Config no `pyproject.toml` (vale pros dois). `strict = true` já liga
`disallow_untyped_defs` e `warn_return_any` — não precisa repetir.

No CI: rodar o checker como step do GitHub Actions a cada push.

### Runtime (outra coisa, não confundir)

Checker estático não roda nada — só lê o código. Se eu quiser `TypeError` de
verdade durante a execução quando alguém passa tipo errado: `typeguard`
(decorator `@typechecked`) ou `pydantic` (valida no construtor do modelo).

**Isso interessa direto pro projeto**: o container de DI vai precisar resolver
dependência lendo a assinatura em runtime, via `inspect.signature()` e
`typing.get_type_hints()`. É a mesma introspecção que essas libs usam por baixo.
Vale olhar como elas fazem antes de escrever o container.

## Nome

`aspython` = ASP.NET + Python. Lê também como "as python".

Alternativas descartadas: `snakesharp` (Snake#), `dotsnake`, `dotpy`, `pynet`.

Disponibilidade checada em 2026-09-30:

- PyPI `aspython` — livre
- GitHub: org `aspython` tomada desde 2019 mas com 0 repos públicos; nenhum repo
  relevante com esse nome. Sem conflito prático.
