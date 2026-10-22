# Команды установленных CLI

Текст ниже снят с `--help` установленного бинарника. Это не пересказ. Ссылки вырезаны, чтобы страница оставалась самодостаточной.

## OpenSpec 1.14.3

Команда: `python3 cli/mazu.py upstream openspec -- --help`

Код выхода: 0

```
Usage: openspec [options] [command]

AI-native system for spec-driven development

Options:
  -V, --version                      output the version number
  --no-color                         Disable color output
  -h, --help                         display help for command

Commands:
  version [options]                  Report the installed OpenSpec version and
                                     update availability
  init [options] [path]              Initialize OpenSpec in your project
  update [options] [path]            Update OpenSpec instruction files
  list [options]                     List items (changes by default). Use
                                     --specs to list specs.
  view [options]                     Display an interactive dashboard of specs
                                     and changes
  change                             Manage OpenSpec change proposals
  archive [options] [change-name]    Archive a completed change and update main
                                     specs
  spec                               Manage and view OpenSpec specifications
  config [options]                   View and modify global OpenSpec
                                     configuration
  schema                             Manage workflow schemas [experimental]
  store                              Create and manage stores - standalone
                                     OpenSpec repos you register on this machine
  doctor [options]                   Report relationship health for the resolved
                                     OpenSpec root
  context [options]                  Print the working context for the resolved
                                     OpenSpec root
  workset [options]                  Compose, keep, and open personal working
                                     views (purely local)
  validate [options] [item-name]     Validate changes and specs
  show [options] [item-name]         Show a change or spec
  feedback [options] <message>       Submit feedback about OpenSpec
  completion                         Manage shell completions for OpenSpec CLI
  status [options]                   Display artifact completion status for a
                                     change
  instructions [options] [artifact]  Output enriched instructions for artifacts,
                                     apply, or archive
  templates [options]                Show resolved template paths for all
                                     artifacts in a schema
  schemas [options]                  List available workflow schemas with
                                     descriptions
  new                                Create new items
  help [command]                     display help for command
```

## OpenSpec new

Команда: `python3 cli/mazu.py upstream openspec -- new --help`

Код выхода: 0

```
Usage: openspec new [options] [command]

Create new items

Options:
  -h, --help               display help for command

Commands:
  change [options] <name>  Create a new change directory
  help [command]           display help for command
```

## OpenSpec change

Команда: `python3 cli/mazu.py upstream openspec -- change --help`

Код выхода: 0

```
Usage: openspec change [options] [command]

Manage OpenSpec change proposals

Options:
  -h, --help                        display help for command

Commands:
  show [options] [change-name]      Show a change proposal in JSON or markdown
                                    format
  list [options]                    List all active changes (DEPRECATED: use
                                    "openspec list" instead)
  validate [options] [change-name]  Validate a change proposal
  help [command]                    display help for command
```

## CALM 1.65.0

Команда: `python3 cli/mazu.py upstream calm -- --help`

Код выхода: 0

```
Usage: calm [options] [command]

A set of tools for interacting with the Common Architecture Language Model
(CALM)

Options:
  -V, --version          output the version number
  -h, --help             display help for command

Commands:
  generate [options]     Generate an architecture from a CALM pattern file.
  validate [options]     Validate a CALM document.
  template [options]     Generate files from a CALM model using a template
                         bundle, a single file, or a directory of templates
  docify [options]       Generate a documentation website from your CALM model
                         using a template or template directory
  init-ai [options]      Augment a git repository with AI assistance for CALM
  diff [options]         Compare two CALM documents (architectures or patterns),
                         or the moments of a CALM timeline, and report what
                         changed.
  timeline [options]     Synthesise an implied CALM timeline from a set of local
                         versioned architecture files.
  init-config [options]  Create or update the CALM CLI configuration file
                         (~/.calm.json).
  hub                    Interact with CALM Hub
  workspace              Manage CALM workspace bundle and development helpers
  help [command]         display help for command
```

## BMAD 6.12.4

Команда: `python3 cli/mazu.py upstream bmad -- --help`

Код выхода: 0

```
Usage: bmad [options] [command]

BMAD Core CLI - Universal AI agent framework

Options:
  -V, --version        output the version number
  -h, --help           display help for command

Commands:
  install [options]    Install BMAD Core agents and tools
  status               Display BMAD installation status and module versions
  uninstall [options]  Remove BMAD installation from the current project
  help [command]       display help for command
```

## Cucumber 13.3.0

Команда: `python3 cli/mazu.py upstream cucumber -- --help`

Код выхода: 0

```
Usage: cucumber-js [options] [<GLOB|DIR|FILE[:LINE]>...]

Options:
  -v, --version                    output the version number
  -b, --backtrace                  show full backtrace for errors
  -c, --config <PATH>              specify configuration file
  -d, --dry-run                    invoke formatters without executing steps
  --exit, --force-exit             force shutdown of the event loop when the
                                   test run has finished: cucumber will call
                                   process.exit
  --fail-fast                      abort the run on first failure
  -f, --format <TYPE[:PATH]>       specify the output format, optionally supply PATH to redirect formatter output (repeatable).  Available formats:
      html: Outputs a HTML report
      junit: Produces a JUnit XML report
      message: Emits Cucumber messages in newline-delimited JSON
      pretty: Writes a rich report of the scenario and example execution as it happens
      progress: Prints one character per scenario.
      progress-bar: Provides a real-time updating progress bar
      summary: Summary output of feature and scenarios
      json: Prints the feature as JSON. The JSON format is in maintenance mode. Please consider using the message formatter with the standalone json-formatter ([ссылка удалена]
      rerun: Prints failing files with line numbers.
      snippets: The Snippets Formatter doesn't output anything regarding the test run; it just prints snippets to implement any undefined steps
      usage: Prints where step definitions are used. The slowest step definitions (with duration) are listed first. If --dry-run is used the duration is not shown, and step definitions are sorted by filename instead.
      usage-json: Does what the Usage Formatter does, but outputs JSON, which can be output to a file and then consumed by other tools.
  
  --format-options <JSON>          provide options for formatters (repeatable)
  --i18n-keywords <ISO 639-1>      list language keywords
  --i18n-languages                 list languages
  -i, --import <GLOB|DIR|FILE>     import files before executing features
                                   (repeatable)
  -l, --loader <NODE_MODULE>       module specifier(s) for loaders to be
                                   registered ahead of loading support code
  --language <ISO 639-1>           provide the default language for feature
                                   files
  --name <REGEXP>                  only execute the scenarios with name matching
                                   the expression (repeatable)
  --order <TYPE[:SEED]>            run scenarios in the specified order. Type
                                   should be `defined`, `reverse` or `random`
  -p, --profile <NAME>             specify the profile to use (repeatable)
                                   (default: [])
  --parallel <NUMBER_OF_WORKERS>   run in parallel with the given number of
                                   workers
  --plugin <SPECIFIER>             load a plugin (repeatable)
  --plugin-options <JSON>          provide options for plugins (repeatable)
  --publish                        Publish a report to
                                   [ссылка удалена]
  -r, --require <GLOB|DIR|FILE>    require files before executing features
                                   (repeatable)
  --require-module <NODE_MODULE>   require node modules before requiring files
                                   (repeatable)
  --retry <NUMBER_OF_RETRIES>      specify the number of times to retry failing
                                   test cases (default: 0)
  --retry-tag-filter <EXPRESSION>  only retries the features or scenarios with tags matching the expression (repeatable).
          This option requires '--retry' to be specified.
  --shard <INDEX/TOTAL>            run shard INDEX of TOTAL shards. The index
                                   starts at 1
  --strict                         fail if there are pending steps
  --no-strict                      succeed even if there are pending steps
  -t, --tags <EXPRESSION>          only execute the features or scenarios with
                                   tags matching the expression (repeatable)
  --world-parameters <JSON>        provide parameters that will be passed to the
                                   world constructor (repeatable)
  -h, --help                       display help for command
For more details please visit [ссылка удалена]
```

## adr-tools

Команда: `python3 cli/mazu.py upstream adr -- help`

Код выхода: 0

```
usage: adr help COMMAND [ARG] ...
COMMAND is one of: 
  upgrade-repository
  help
  new
  init
  config
  list
  generate
  link
Run 'adr help COMMAND' for help on a specific command.
```

## Sysl 0.792.0

Команда: `python3 cli/mazu.py upstream sysl -- --help`

Код выхода: 0

```
usage: sysl [<flags>] <command> [<args> ...]

System Specification Language Toolkit

Optional flags:
      --[no-]help               Show context-sensitive help (also try
                                --help-long and --help-man).
      --[no-]version            Show application version.
      --log="warn"              log level: [debug,info,warn,trace,off]
  -v, --[no-]verbose            enable verbose logging
      --root=ROOT               Sysl root directory for input model file. If
                                root is not found, the module directory becomes
                                the root, but the module can not import with
                                absolute paths (or imports must be relative).
      --clone-version=CLONE-VERSION  
                                Before running the command it will clone the
                                local repo into memory and checkout the specific
                                version
      --[no-]no-forced-fetch    When retrieving files from external repos,
                                if the cache has the repo don't force a fetch
      --max-import-depth=MAX-IMPORT-DEPTH  
                                Maximum depth to follow imports, including the
                                original file (ignores any that are deeper).
                                0 (default) for unlimited. eg 1 means just the
                                original file with no imports.
      --[no-]operation-summary  Currently just outputs the names of the files
                                parsed.
      --[no-]no-different-version-check  
                                When parsing imports don't error when a file is
                                imported from multiple branches or into multiple
                                app-names.
      --cache-dir=CACHE-DIR     Where to cache the repos for imported files

Commands:
help [<command>...]
    Show help.

codegen --transform=TRANSFORM --grammar=GRAMMAR [<flags>] [<MODULE>...]
    Generate code

datamodel [<flags>] [<MODULE>...]
    Generate data models

diagram [<flags>] [<MODULE>...]
    Generate mermaid diagrams

display-summary [<MODULE>...]
    Display summary without parsing (currently just includes)

env
    Print sysl environment information.

export [<flags>] [<MODULE>...]
    Export sysl to external types. Supported types:
    Swagger,openapi2,openapi3,spanner, proto

generate-db-scripts [<flags>] [<MODULE>...]
    Generate db script

generate-db-scripts-delta [<flags>] [<MODULE>...]
    Generate delta db scripts

import --input=INPUT [<flags>]
    Import foreign type to Sysl. Supported types: [avro, bigquery, grammar,
    jsonschema, mysql, mysqlDir, openapi3, postgres, postgresDir, protobuf,
    protobufDir, spannerSQL, spannerSQLdir, swagger, sysl.pb, xsd]

info
    Show binary information

integrations [<flags>] [<MODULE>...]
    Generate integrations

lsp
    Handle an LSP request as a language server

protobuf [<flags>] [<MODULE>...]
    Generate textpb/json/binary

repl
    Enter a sysl REPL

sd [<flags>] [<MODULE>...]
    Generate Sequence Diagram

template --template=TEMPLATE --start=START [<flags>] [<MODULE>...]
    Apply a model to a template for custom text output

test-rig --template=TEMPLATE [<flags>] [<MODULE>...]
    Generate test rig

transform --script=SCRIPT [<flags>] [<MODULE>...]
    Transform one or more Sysl models using an arr.ai script

validate [<MODULE>...]
    Validate the sysl file
```

## Specify 1.2.3

Команда: `python3 cli/mazu.py upstream specify -- --help`

Код выхода: 0

```
███████╗██████╗ ███████╗ ██████╗██╗███████╗██╗   ██╗              
              ██╔════╝██╔══██╗██╔════╝██╔════╝██║██╔════╝╚██╗ ██╔╝              
              ███████╗██████╔╝█████╗  ██║     ██║█████╗   ╚████╔╝               
              ╚════██║██╔═══╝ ██╔══╝  ██║     ██║██╔══╝    ╚██╔╝                
              ███████║██║     ███████╗╚██████╗██║██║        ██║                 
              ╚══════╝╚═╝     ╚══════╝ ╚═════╝╚═╝╚═╝        ╚═╝                 
                                                                                
               GitHub Spec Kit - Spec-Driven Development Toolkit                

                                                                                
 Usage: -c [OPTIONS] COMMAND [ARGS]...                                          
                                                                                
 Setup tool for Specify spec-driven development projects                        
                                                                                
╭─ Options ────────────────────────────────────────────────────────────────────╮
│ --version  -V        Show version and exit.                                  │
│ --help               Show this message and exit.                             │
╰──────────────────────────────────────────────────────────────────────────────╯
╭─ Commands ───────────────────────────────────────────────────────────────────╮
│ init         Initialize a new Specify project.                               │
│ check        Check that all required tools are installed.                    │
│ version      Display version and system information.                         │
│ mcp          Run the experimental MCP server over stdio.                     │
│ self         Manage the specify CLI itself: check for newer releases,        │
│              preview upgrades with --dry-run, and upgrade in place.          │
│ extension    Manage spec-kit extensions                                      │
│ integration  Manage coding agent integrations                                │
│ event        Manage and execute event-driven commands                        │
│ preset       Manage spec-kit presets                                         │
│ artifact     Introspect commands, templates, scripts, and hooks Spec Kit     │
│              exposes.                                                        │
│ bundle       Discover, install, and author Spec Kit bundles                  │
│ workflow     Manage and run automation workflows                             │
╰──────────────────────────────────────────────────────────────────────────────╯
```
