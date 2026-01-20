# a-maz-ing

```mermaid
flowchart TD
start((start)):::terminator
Solver(apply solver):::process
start --> Collect(collect config vars)
Collect --> Config[/config vars/]
Config --> Scene("create scene (singletone)"):::process
Scene --> Fac{is PERFECT?}
subgraph Factory
Fac --> |no|SimMaze(create simple maze):::process
Fac --> |yes|PerMaze(create perfect maze):::process
end
SimMaze --> Solver
PerMaze --> Solver
Solver --> Restart{restart again?}
Destroy --> Fac
Restart --> |yes|Destroy(destroy scene members):::process
Restart -->|no|finish((end)):::terminator
classDef terminator fill:#f00, color:#fff 
classDef process fill:green, color:#fff
```
