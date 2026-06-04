# Stores

## Mini-index

- [Stores vs signals](#stores-vs-signals)
- [createStore](#createstore)
- [Accessing store values](#accessing-store-values)
- [Path syntax for nested updates](#path-syntax-for-nested-updates)
- [Array operations](#array-operations)
- [produce - draft-style mutations](#produce---draft-style-mutations)
- [reconcile - diff and sync](#reconcile---diff-and-sync)
- [unwrap - extract raw data](#unwrap---extract-raw-data)
- [createMutable](#createmutable)
- [modifyMutable](#modifymutable)

---

## Stores vs signals

Signals track a **single value** - any change to that value notifies all subscribers. If you store an object in a signal, any property change requires replacing the whole object, which notifies all subscribers even if they only care about one property.

Stores use a **proxy** to track reads and writes at the **property level**. Reading `store.user.name` creates a dependency only on `user.name`, not on `user` or the whole store. This enables fine-grained reactivity: changing `store.user.age` does not notify components that only read `store.user.name`.

```tsx
// Signal: changing one property re-notifies all subscribers
const [user, setUser] = createSignal({ name: "Alice", age: 30 });
setUser({ ...user(), age: 31 }); // replaces whole object

// Store: changing one property notifies only subscribers of that property
const [state, setState] = createStore({ user: { name: "Alice", age: 30 } });
setState("user", "age", 31); // fine-grained - only subscribers of user.age are notified
```

Use stores for **complex nested objects and arrays** where you want fine-grained reactivity. Use signals for primitive values or small objects where you always replace the whole thing.

---

## createStore

```tsx
import { createStore } from "solid-js/store";

const [store, setStore] = createStore(initialValue);
```

- Returns a `[store, setStore]` tuple.
- `store` is a reactive proxy. Property reads inside a tracking scope register dependencies at the property level.
- `setStore` accepts path syntax for nested updates or a function to replace the top level.
- Signals in the store are created **lazily** - only when a property is first read in a tracking scope.

```tsx
const [state, setState] = createStore({
  userCount: 3,
  users: [
    { id: 0, username: "alice", loggedIn: false },
    { id: 1, username: "bob",   loggedIn: true  },
  ],
});
```

Store values can be read directly (no function call needed):

```tsx
// In JSX (tracking scope) - reactive
<h1>{state.users[0].username}</h1>

// Outside tracking scope - not reactive
console.log(state.userCount); // reads once, not tracked
```

To track store values outside JSX, wrap in a reactive scope:

```tsx
createEffect(() => {
  console.log(state.users.at(-1)); // reactive - re-runs when users changes
});
```

---

## Accessing store values

Store properties are read directly through dot notation (no calling a function like signals):

```tsx
console.log(state.userCount);      // 3
console.log(state.users[0].username);  // "alice"
```

Stores support getters on the initial object:

```tsx
const [state] = createStore({
  user: {
    firstName: "John",
    lastName: "Smith",
    get fullName() {
      return `${this.firstName} ${this.lastName}`;
    },
  },
});

console.log(state.user.fullName); // "John Smith"
```

---

## Path syntax for nested updates

The store setter uses a path syntax where the last argument is the new value and earlier arguments navigate to the target:

```tsx
// setStore(key1, key2, ..., newValue)
setState("user", "firstName", "Jane");
setState("users", 0, "loggedIn", true);

// Function as final arg: receives current value, returns new value
setState("users", 3, "loggedIn", (current) => !current);

// Object merge: shallow-merges with existing value (no spread needed)
setState("users", 0, { id: 109 });
// Equivalent to: setState("users", 0, (u) => ({ ...u, id: 109 }))
```

**Top-level updates (replace entire store):**

```tsx
setState({ userCount: 4, users: [...state.users, newUser] });
```

**Setting a property to `undefined` deletes it.**

---

## Array operations

**Append a new item (fine-grained, no full array re-render):**

```tsx
setState("users", state.users.length, {
  id: 3,
  username: "carol",
  loggedIn: false,
});
```

**Append using spread (replaces entire array, triggers all subscribers):**

```tsx
setState("users", (users) => [
  ...users,
  { id: 3, username: "carol", loggedIn: false },
]);
```

**Update multiple indices at once:**

```tsx
setState("users", [2, 7, 10], "loggedIn", false);
```

**Update a range of indices:**

```tsx
// Indices 1 through end (inclusive)
setState("users", { from: 1, to: state.users.length - 1 }, "loggedIn", false);

// Every other item (with step)
setState("users", { from: 0, to: state.users.length - 1, by: 2 }, "loggedIn", false);
```

**Filter/condition-based update:**

```tsx
// Log out all users from Canada
setState("users", (user) => user.location === "Canada", "loggedIn", false);

// Log out users with specific ids
const ids = [1, 2, 3];
setState("users", (user) => ids.includes(user.id), "loggedIn", false);
```

Multi-setter calls on the same call are automatically wrapped in a `batch` so effects fire once after all updates.

---

## produce - draft-style mutations

`produce` lets you mutate a temporary draft of the state, then applies the changes. Useful when updating multiple properties of the same object to avoid multiple setter calls.

```tsx
import { produce } from "solid-js/store";

// Without produce (two setter calls)
setState("users", 0, "username", "newUsername");
setState("users", 0, "location", "newLocation");

// With produce (one setter call, multiple mutations)
setState(
  "users",
  0,
  produce((user) => {
    user.username = "newUsername";
    user.location = "newLocation";
  })
);
```

- `produce` works with `createStore` setters and `modifyMutable`.
- The function receives a proxy of the current state and can mutate it directly.
- Works only with **objects and arrays** - not Maps or Sets.
- Can also be used at the top level: `setState(produce(draft => { draft.count++ }))`.

---

## reconcile - diff and sync

`reconcile` diffs incoming data against existing store state and only triggers updates for values that actually changed. Use it when replacing store data with a fresh snapshot (e.g., from an API refetch).

```tsx
import { reconcile } from "solid-js/store";

const [data, setData] = createStore({
  animals: ["cat", "dog", "bird"],
});

// Only "koala" triggers an update - "cat", "dog", "bird" are unchanged
setData("animals", reconcile(["cat", "dog", "bird", "koala"]));
```

Options:
- `key` (default `"id"`) - property used to match array items by identity.
- `merge` (default `false`) - when `true`, pushes updates deeper into the tree instead of replacing non-matching branches.

This is critical for performance when receiving server updates - without `reconcile`, the whole array would be replaced triggering all list item re-renders.

---

## unwrap - extract raw data

`unwrap` removes the reactive proxy and returns the underlying plain JavaScript object. Use it when you need to:
- Pass store data to a non-Solid library that does not understand proxies.
- Take a non-reactive snapshot for serialization or logging.

```tsx
import { unwrap } from "solid-js/store";

const [state] = createStore({ user: { name: "John" } });
const rawUser = unwrap(state.user);

// rawUser is a plain object - mutations to it can mutate the underlying store
rawUser.name = "Jane"; // may affect the store
```

> **Warning:** `unwrap` does not produce a deep clone. Mutating the returned value can mutate the underlying store data.

---

## createMutable

`createMutable` creates a mutable store proxy where you read and write through the same object (no separate setter). Use it for interop with systems that expect mutable objects.

```tsx
import { createMutable } from "solid-js/store";

const state = createMutable({
  someValue: 0,
  list: [],
});

// Direct mutation - reactive reads still work
state.someValue = 5;
state.list.push("item");
```

Supports getters and setters:

```tsx
const user = createMutable({
  firstName: "John",
  lastName: "Smith",
  get fullName() {
    return `${this.firstName} ${this.lastName}`;
  },
  set fullName(value) {
    [this.firstName, this.lastName] = value.split(" ");
  },
});

user.fullName = "Jane Doe";
```

Writes, deletes, and array mutator methods on a `createMutable` proxy are batched automatically.

**Prefer `createStore` over `createMutable`** in most cases - the separated read/write design of `createStore` makes data flow easier to trace and debug.

---

## modifyMutable

`modifyMutable` applies a store modifier (like `produce` or `reconcile`) to a mutable store inside a `batch`.

```tsx
import { createMutable, modifyMutable, produce } from "solid-js/store";

const state = createMutable({
  user: { firstName: "John", lastName: "Smith" },
});

modifyMutable(
  state,
  produce((draft) => {
    draft.user.firstName = "Jane";
    draft.user.lastName = "Doe";
  })
);
```

- Runs inside a `batch` so all changes notify dependents after the modifier completes.
- The modifier receives the unwrapped underlying state object, not the proxy.
- Accepts any modifier function returned by `produce` or `reconcile`.
