# Convinst - Convinient collection instances for Blender

Convinst is a [Blender](https://blender.org/) addon designed to make collection instance workflow a bit nicer.

## Features

- Collapse selected objects into a single collection instance
- Disassemble instance(Turns collection instance into real objects)
- Add objects into instance
- Extract object from instance

All operations take into account position, rotation and scale of instances

### Collapse objects

This operation moves selected objects into a new collection in a different scene and places an instance of this collection. A good way to separate your assets form main scene to be able to easily edit and export them.

`View3D -> Object menu -> convinst -> Collapse objects into instance`

![](./demo_imgs/collapse.gif)

### Disassemble instance

Basically, separates collection instance into its components.

`View3D -> Object menu -> convinst -> Disassemble instance`

### Add objects into instance

Adds selected objects into collection of active instance. Respects location, rotation and scale of instance so object wont change visually when you add it. All instances of this collection will be affected.

`View3D -> Object menu -> convinst -> Add to instance`

### Extract object from collection

The opposite of Add ot instance. You can make "real" a single object from instanced collection, maybe edit it and add back again. All instances of this collection will be affected.

`View3D -> Object menu -> convinst -> Extract from instance`

## Installation

1. Download latest release from [releases page](https://github.com/cmd410/convinst/releases)
2. Open Blender 2.8 or higher
3. Navigate to `edit -> preferences -> addons`
4. Click `Install...` button and choose the downloaded zip archive
5. Check `ConvInst` addon in the list
6. Enjoy!