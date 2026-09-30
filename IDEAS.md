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

## Nome

`aspython` = ASP.NET + Python. Lê também como "as python".

Alternativas descartadas: `snakesharp` (Snake#), `dotsnake`, `dotpy`, `pynet`.

Disponibilidade checada em 2026-09-30:

- PyPI `aspython` — livre
- GitHub: org `aspython` tomada desde 2019 mas com 0 repos públicos; nenhum repo
  relevante com esse nome. Sem conflito prático.
