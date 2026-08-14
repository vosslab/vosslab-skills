# JSX attributes

## Mini-index

- [Event binding: on* and on:*](#event-binding-on-and-on)
- [ref](#ref)
- [class and classList](#class-and-classlist)
- [style](#style)
- [attr:* - force attribute](#attr---force-attribute)
- [prop:* - force property](#prop---force-property)
- [bool:* - boolean attribute presence](#bool---boolean-attribute-presence)
- [use:* - directives](#use---directives)
- [innerHTML and textContent](#innerhtml-and-textcontent)
- [@once - static marker](#once---static-marker)

---

## Event binding: on* and on:*

Solid has two event systems:

### on* - delegated events

Attaches via document-level delegation. Case-insensitive (`onClick` = `onclick`). Best for common UI events.

```tsx
<button onClick={handleClick}>Click</button>
<input onInput={(e) => setValue(e.currentTarget.value)} />
<input onChange={(e) => handleChange(e.currentTarget.value)} />
```

**onInput vs onChange:**
- `onInput` fires immediately as the value changes (native `input` event).
- `onChange` fires only when the field loses focus (native `change` event).

**Bound data form** - avoids closure overhead:

```tsx
const handler = (itemId, event) => console.log(itemId, event);
<button onClick={[handler, item.id]}>Delete</button>
```

Delegated bindings are **not reactive** - swapping the handler reference does not rebind. To conditionally call different handlers, use a wrapper:

```tsx
<div onClick={() => props.handleClick?.()} />
```

### on:* - native events

Attaches directly to the element with `addEventListener`. Case-sensitive. Required for custom events and events where you need `stopPropagation` to work correctly.

```tsx
<div on:scroll={handleScroll}>...</div>
<div on:MyCustomEvent={(e) => handle(e.detail)}>...</div>
```

With listener options (object form, added in Solid 1.9.0):

```tsx
const handler = {
  handleEvent() { setCount(c => c + 1); },
  once: true,
};
<button on:click={handler}>Click once</button>
```

Options supported: `once`, `passive`, `capture`, `signal`.

**Delegated event caveats:**
- `event.stopPropagation()` does not work as expected - switch to `on:` when needed.
- Delegated listeners persist per event type even after the originating element is removed.
- `Portal` events follow the component tree, not the DOM tree.

---

## ref

Captures a reference to a rendered DOM element or forwarded component ref.

```tsx
// Variable ref - assigned during render, before mounting
let myDiv;
onMount(() => console.log(myDiv)); // safe here, element is mounted
<div ref={myDiv} />;
```

```tsx
// Callback ref - called with element during render
<div ref={(el) => setupTooltip(el)} />
```

```tsx
// Component ref - only works if component forwards the prop
function MyComp(props) {
  return <div ref={props.ref} />;
}

let el;
onMount(() => console.log(el.clientWidth));
<MyComp ref={el} />;
```

**Timing:** refs are assigned during rendering, before the element is connected to the DOM. Use `onMount` if you need to access the element after it is in the DOM.

---

## class and classList

### class

Plain string or reactive expression:

```tsx
<div class="card" />
<div class={isActive() ? "card active" : "card"} />
<div class={`card ${theme()}`} />
```

### classList

Toggle classes from an object. Keys are class names; truthy values apply the class, falsy values remove it. Updates per-class instead of replacing the whole `class` attribute.

```tsx
<div
  classList={{
    active: isActive(),
    editing: editId() === row.id,
    "text-danger": hasError(),
  }}
/>

// Dynamic class name
<div classList={{ [className()]: classOn() }} />
```

**Warning:** Do not mix reactive `class` and `classList`. A reactive update to `class` will overwrite all classes set by `classList`. Keep `class` static (or place it before `classList` attributes) when using both.

**Also:** `classList` is a pseudo-attribute and does not work in prop spreads (`{...props}`) or inside `<Dynamic>`.

---

## style

Set inline styles from a string or CSS property object.

```tsx
// String
<div style="color: green; font-size: 14px" />

// Template literal
<div style={`height: ${state.height}px`} />

// Object - use dash-case keys (not camelCase)
<div
  style={{
    color: "green",
    "background-color": state.bgColor,
    height: `${state.height}px`,
  }}
/>

// CSS custom properties
<div style={{ "--my-color": brandColor() }} />
```

Object style notes:
- Keys must use lower-case, dash-separated CSS property names.
- Nullish values remove that property.
- Applied via `element.style.setProperty` (not replacing the whole style string).

---

## attr:* - force attribute

Forces a JSX key to be written as an HTML attribute rather than a DOM property. Useful for custom elements and rare cases where attribute vs. property distinction matters.

```tsx
<my-element attr:status={props.status} />
```

- `attr:name={undefined}` or `attr:name={null}` removes the attribute.
- In SSR, the stripped name and escaped value are written as HTML.

---

## prop:* - force property

Forces a JSX key to be assigned as a DOM property directly (not as an attribute). Useful for properties that should not go through attribute serialization.

```tsx
<input type="checkbox" prop:indeterminate={true} />
<div prop:scrollTop={scrollPos()} />
```

- Strips the `prop:` prefix and assigns directly to the property on the DOM element.
- Does not produce SSR output (client-only).

---

## bool:* - boolean attribute presence

Controls whether an attribute is present based on a truthy/falsy value. Useful for custom elements with boolean attributes.

```tsx
<my-element bool:disabled={isDisabled()} />

// When isDisabled() is truthy: <my-element disabled="">
// When isDisabled() is falsy:  <my-element>
```

- Truthy value -> `name=""` is written.
- Falsy value -> attribute is removed.
- SSR follows the same presence-or-absence behavior.

---

## use:* - directives

Attaches a directive function to a native element. Directives are reusable DOM setup helpers that run during rendering.

```tsx
<input use:model={[value, setValue]} />
```

Directive signature:

```tsx
function model(element: Element, accessor: () => [Accessor<string>, Setter<string>]) {
  const [field, setField] = accessor();
  const onInput = ({ currentTarget }) => setField(currentTarget.value);

  createRenderEffect(() => (element.value = field()));
  element.addEventListener("input", onInput);
  onCleanup(() => element.removeEventListener("input", onInput));
}

const [name, setName] = createSignal("");
<input type="text" use:model={[name, setName]} />;
```

Rules:
- Directives only work on **native elements** (including custom elements), not user-defined components.
- The directive runs during rendering under the current owner, so it can create effects and register cleanup.
- Without an explicit value, the accessor returns `true`.

TypeScript: extend `JSX.Directives` to type custom directives:

```ts
declare module "solid-js" {
  namespace JSX {
    interface Directives {
      model: [Accessor<string>, Setter<string>];
    }
  }
}
```

---

## innerHTML and textContent

### innerHTML

Sets the element's `innerHTML` property - parses the string as HTML markup.

```tsx
<div innerHTML={"<strong>Hello</strong>"} />
```

- Replaces existing children with parsed markup.
- In SSR, the string is emitted as raw child content (no escaping).
- **Security risk:** Never use with unsanitized user input.

### textContent

Sets the element's `textContent` property - inserts as plain text (not parsed as HTML).

```tsx
<div textContent={"<strong>This is shown as text, not bold</strong>"} />
```

- Replaces existing child content.
- In SSR, emits as escaped text.

---

## @once - static marker

The `/*@once*/` compiler comment marks a JSX expression as static. The expression evaluates once at render time and never updates reactively.

```tsx
// Prop - read once, never updates
<MyComponent value={/*@once*/ state.initialValue} />

// Child - read once, never updates
<MyComponent>{/*@once*/ state.initialValue}</MyComponent>
```

- Useful as a micro-optimization when you know a value will not change.
- Some compiler transforms (parts of `classList` and `style` handling) do not fully respect `/*@once*/`.
