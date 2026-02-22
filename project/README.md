# a-maz-ing

---

Next iteration we can add:

- [ ] Architecture overview
- [ ] Rendering strategy (frame loop, dirty regions, etc.)
- [ ] Installation & build instructions
- [ ] Controls
- [ ] Design philosophy
- [ ] Performance considerations

Tell me what to expand next.

---

# Maze Generator & Visualizer

## Overview

This project consists of two main parts:

1. **Maze Generator Package**
   A reusable module responsible for generating maze data structures.

2. **Maze Visualization App**
   A graphical application that uses the generator to render mazes and
   allows user interaction with additional visual features.

The generator is independent from the rendering layer, enabling clean
separation between maze logic and graphical presentation.

---

## Project Structure

```
maze_generator/     # Core maze generation logic
app/                # Graphical interface and rendering
```

- The **generator** produces maze data.
- The **app** consumes that data and displays it visually.

---

## Goals

- Keep maze logic independent from rendering.
- Provide an interactive graphical representation.
- Allow future extension with animations and user-driven features.

## Project Flowchart (draft)

```mermaid
flowchart TD
subgraph ErrorHandler
 errorhandlers
end
subgraph Testers
 testers
end
Virt(virtualization) -.-> start
start -.-> ErrorHandler -.-> Testers -.-> finish
start((start)):::terminator
HexTrans(translate maze):::process
ShortDist(apply solver):::process
subgraph LauncherEpic
 Launcher
end
start --> Launcher(launcher):::process
Launcher --> Collect(collect config vars):::process
subgraph DataColl
Collect --> Config[/config vars/]
end
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
SimMaze --> ShortDist
PerMaze --> ShortDist
subgraph Solver
ShortDist --> HexTrans
end
HexTrans --> Restart{restart again?}
subgraph Destructors
Destroy
DestroyAll(destroy all):::process
end
Destroy --> Collect
Restart --> |yes|Destroy(destroy scene members):::process
Restart --> |no|DestroyAll
DestroyAll --> finish((end)):::terminator
classDef terminator fill:#f00, color:#fff
classDef process fill:green, color:#fff
```
