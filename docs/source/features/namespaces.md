# Namespaces
---

## Summary
---
- [Better organization](#better-organization)
- [How to define a namespace](#how-to-define-a-namespace)
- [Adding symbols](#adding-symbols)
- [Accessing symbols from namespaces](#accessing-symbols-from-namespaces)

## Better organization
---
Namespaces are a very useful to better organize your programs. They are used to divide the global space in sub-spaces. This feature looks like the **C++ namespaces** or the **modules** in languages like Python or Rust.

## How to define a namespace
---
A namespace is defined using the `namespace` keyword. The **name** of the namespace is placed right after it and then you can define the **body**, which contains all the namespace symbols.

Namespaces can also be **nested**.

```sd
namespace world {
    namespace animals {
        // ...
    }
    namespace plants {
        // ...
    }
}
```

## Adding symbols
---
To add symbols to a namespace after the namespace definition, just do as if you were redefining it.
```sd
namespace plants {
    struct Flower {}
}

namespace plants {
    var plant_count: i32 = 0;
    // namespace `plants` now contains `Flower` and `plant_count`
}
```

## Accessing symbols from namespaces
---
When you define a symbol in a namespace, its name gets **scoped**. This means that, if you define a structure named `Wolf` in the `animals` namespace, you would have to write `animals::Wolf` every time you want to use this structure, even **inside the namespace**.