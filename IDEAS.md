# aspython

A backend framework in Python, inspired by .NET (ASP.NET Core).

## Goal

A fundamentals study. Python wasn't created for backend work — it was adapted for
it. The whole point is to build, from scratch and on top of it, the pieces that
.NET hands you ready-made, so I understand how each one actually works underneath.

**Not for production.** Not for a company to use. It's for learning, and for
friends to look at.

## Project rule

**No AI for the code.** The point of this project is the process of figuring out
how to do it, not having a working result. Using AI to write the code defeats the
purpose.

## Ideas / what I want to build

- [ ] **Application "builder"** — understand how an application host/builder works,
      like `WebApplicationBuilder`. How the app assembles itself, what happens
      between `CreateBuilder()` and `Run()`.

- [ ] **Structure for the Builder design pattern** — actually build the Builder, not
      just use one. Fluent configuration chaining, and a clear split between the
      configuration phase and the execution phase.

- [ ] **Inversion of control + automatic dependency injection** — a DI container
      that resolves dependencies on its own. Register services, resolve by type,
      lifetimes (singleton / scoped / transient).

- [ ] **Native database access and operation module** — something in the spirit of
      EF Core: Unit of Work, repositories, controlled transactions, change tracking.

- [ ] **Native decorators for HTTP route mapping** — `@get`, `@post`, and so on.
      Automatic route discovery and registration, the same practical mapping as
      ASP.NET controller attributes.

- [ ] **CLI** — three commands, following the .NET mental model:
      - `aspython new` — creates the project (= `dotnet new`), with `pyproject.toml`
        already configured
      - `aspython run` — starts the application (= `dotnet run`)
      - `aspython check` — runs the type checker (= the build that fails on warnings)

## Static typing (found out on 2026-09-30)

A type hint in Python is almost a comment — the interpreter ignores it. This runs
fine, no error at all:

```python
def add(n1: float, n2: float) -> str:
    return n1 + n2

add(1, 2)  # 3
```

I want the equivalent of `tsconfig.json`: a config file that turns a broken hint
into a real error, both in the IDE and in CI.

- [ ] Set up strict static checking in the project from the very first commit.

### What is and isn't possible

- **There is no "build" in Python.** There's no step to abort. No config file makes
  the interpreter refuse to run badly typed code. The gate is external: CI, a
  pre-commit hook, or the IDE itself.
- **Linting doesn't check types.** Ruff only enforces that the annotation *exists*
  (the `ANN` rules). If the annotation is wrong, only a type checker catches it.
- **The checker is opt-in forever.** Unlike TS, where `tsc` is mandatory because the
  browser doesn't understand TypeScript.

### Pick ONE checker

| | mypy | pyright |
|---|---|---|
| Who makes it | Python / Dropbox | Microsoft |
| Is the engine behind Pylance (VS Code) | no | **yes** |
| Speed | slow | much faster |
| Inference (narrowing, generics) | weaker | better |

Mixing both gives you divergent errors in the same file. Pick one and stick with it.

Leaning towards **pyright**, because Pylance in VS Code already is pyright. Turning
on `python.analysis.typeCheckingMode: "strict"` means what shows up on screen is
exactly what CI will flag. With mypy + Pylance the two disagree.

Config lives in `pyproject.toml` (works for both). `strict = true` already turns on
`disallow_untyped_defs` and `warn_return_any` — no need to repeat them.

In CI: run the checker as a GitHub Actions step on every push.

### Runtime (a different thing — don't confuse them)

A static checker doesn't run anything — it only reads the code. If I want a real
`TypeError` at execution time when someone passes the wrong type: `typeguard` (the
`@typechecked` decorator) or `pydantic` (validates in the model constructor).

**This matters directly for the project**: the DI container will have to resolve
dependencies by reading signatures at runtime, via `inspect.signature()` and
`typing.get_type_hints()`. That's the same introspection those libraries use
underneath. Worth looking at how they do it before writing the container.

### Decision: how the CLI ties this together

`aspython new` generates `pyproject.toml` already configured. The user decides the
severity, in that same config:

```toml
[tool.pyright]
strict = ["src"]

[tool.aspython]
typecheck = "error"   # error | warn | off
```

**One file only.** Don't create a separate `aspython.toml` — `[tool.pyright]`
already lives in `pyproject.toml` and that's where Pylance reads from. Config in two
places splits the source of truth.

`check` runs pyright as a subprocess and gates on its **exit code** (≠ 0 means it
found something). `run` reads `typecheck` and only calls `check` before starting up
if it's set to `"error"`:

```
if config.typecheck == "error":
    check()  # abort if exit code != 0
run_server()
```

### Careful: don't turn it into compilation

A full type check takes seconds. If `run` always checks, I pay that every single
time I restart in dev. `dotnet run` can get away with it because C# *has* to compile
either way — Python doesn't. This reintroduces latency the language doesn't have.

So the template default should be `"warn"` or `"off"`. Whoever wants the hard gate
turns it on, and CI calls `aspython check` directly, without going through `run`.

### Open question: pyright drags Node along

`pip install pyright` is a wrapper that downloads Node on first run. If the framework
invokes pyright internally, a Python framework ends up with a hidden dependency on
Node. Mypy is pure Python, but diverges from Pylance.

| | IDE | invoked by the framework |
|---|---|---|
| pyright | already is Pylance | drags Node along |
| mypy | diverges from Pylance | pure pip |

There's no clean choice. Current decision: pyright, accepting the Node dependency.
Alternative to consider later — make the checker command configurable and run it as
a generic subprocess, instead of the framework picking for me.

## Name

`aspython` = ASP.NET + Python. It also reads as "as python".

Rejected alternatives: `snakesharp` (Snake#), `dotsnake`, `dotpy`, `pynet`.

Availability checked on 2026-09-30:

- PyPI `aspython` — free
- GitHub: the `aspython` org has been taken since 2019 but has 0 public repos; no
  relevant repo under that name. No practical conflict.
