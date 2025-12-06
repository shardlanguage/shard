# Structures
---

## Summary
---
- [What is a structure?](#what-is-a-structure)
- [How to define a structure](#how-to-define-a-structure)
- [Structure instances](#structure-instances)

## What is a structure?
---
In C-like programming languages, a structure is **a user-defined data type that can be used to group items of possibly different types into a single type**. The variables defined inside a structure can only be accessed in this structure or from an [**instance**](#structure-instances).

## How to define a structure
---
In Shard, structures are defined using the `struct` keyword. The **name** is placed right after it, and then you can define the **body**, which contains all the structure **fields**. A field is an item inside a structure.

For example, let's define a structure to represent a point in a 2D space:
```sd
struct Point {
    var x: i32;
    var y: i32;
    var name: i8;
}
```
The structure contains a variable field named `x` of type `i32` which represents the X position of the point, another variable field named `y` of type `i32` which represents the Y position of the point, and a last field named `name` of type `i8`, used to store a single character which represents the name of the point.

Defining a structure will create a new type which has the name of this structure.

## Structure instances
---
You can now create instances of your structures, using the new types defined because of your structures.
```sd
var p: Point;       // create an instance of Point
```
The fields of the structure can be acessed using `.`.
```sd
var px: i32 = p.x;
var py: i32 = p.y;
var pname: i8 =  p.name;
```
Here is an example of a function that moves a point to a new position:
```sd
func move_point(var p: *Point, var new_x: i32, var new_y: i32) {
    p[0].x = new_x;
    p[0].y = new_y;
}
```