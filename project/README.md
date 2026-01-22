# a-maz-ing

```mermaid
flowchart TD
start((start)):::terminator
HexTrans(translate maze):::process
ShortDist(apply solver):::process
start --> Collect(collect config vars):::process
Collect --> Config[/config vars/]
Config --> Singleton{scene?}
subgraph Singl
Singleton -->|no|Scene("create scene (singleton)"):::process
end
subgraph Factory
Scene --> Fac
Singleton -->|yes|Fac{perfect?}
Fac --> |no|SimMaze(create simple maze):::process
Fac --> |yes|PerMaze(create perfect maze):::process
end
SimMaze --> HexTrans
PerMaze --> HexTrans
subgraph Solver
HexTrans --> ShortDist
end
ShortDist --> Restart{restart again?}
Destroy --> Collect
Restart --> |yes|Destroy(destroy scene members):::process
Restart -->|no|finish((end)):::terminator
classDef terminator fill:#f00, color:#fff 
classDef process fill:green, color:#fff
```
