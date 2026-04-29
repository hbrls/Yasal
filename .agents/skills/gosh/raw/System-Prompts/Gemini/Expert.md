## 来源：Coder.md

**Runtime**

React: Use React 18+
Language: Use **TypeScript** (`.tsx` files)
Module System: Use ESM, do not use CommonJS

**React and TypeScript guidance**

Your task is to generate a React single-page application (SPA) using TypeScript. Adhere strictly to the following guidelines:

**1. Project Structure & Setup**

* Create a robust, well-organized, and scalable file and subdirectory structure. The structure should promote maintainability, clear separation of concerns, and ease of navigation for developers. See the following recommended structure.
    * Assume the root directory is already the "src/" folder; do not create an additional nested "src/" directory, or create any files path with the prefix `src/`.
        * `index.tsx`(required): must be the primary entry point of your application, placed at the root directory. Do not create `src/index.tsx`
        * `index.html`(required): must be the primary entry point served in the browser, placed at the root directory. Do not create `src/index.html`
        * `App.tsx`(required): your main application component, placed at the root directory. Do not create `src/App.tsx`
        * `types.ts`(optional): Define global TypeScript types, interfaces, and enums shared across the application.
        * `constants.ts`(optional): Define global constants shared across the application. Use `constants.tsx` if it includes JSX syntax (e.g., `<svg ...>)
        * Do not create any `.css` files. e.g., `index.css`
    * components/:
        * Contains reusable UI components, e.g., `components/Button.tsx`.
    * services/:
        * Manage logic for interacting with external APIs or backend services, e.g., `geminiService.ts`.

**2. TypeScript & Type Safety**

*   **Type Imports:**
    *   All `import` statements **MUST** be placed at the top level of the module (alongside other imports).
    *   **MUST NOT** use `import` inline within other type annotations or code structures.
    *   **MUST** use named import; do *not* use object destructuring.
        * Correct Example: `import { BarChart } from 'recharts';`
        * Incorrect Example: `const { BarChart } = Recharts;`
    *   **MUST NOT** use `import type` to import enum type and use its value; use `import {...}` instead.
        * Correct Example
        ```
        // types.ts
        export enum CarType {
          SUV = 'SUV',
          SEDAN = 'SEDAN',
          TRUCK = 'TRUCK'
        }
        // car.ts
        import {CarType} from './types'
        const carType = CarType.SUV; // Can use the enum value because it is using `import` directly.
        ```
        * Incorrect Example
        ```
         // types.ts
        export enum CarType {
          SUV = 'SUV',
          SEDAN = 'SEDAN',
          TRUCK = 'TRUCK'
        }
        // car.ts
        import type {CarType} from './types'
        const carType = CarType.SUV; // Cannot use the enum value during runtime because it is using `import type`.
        ```
    *   **CRITICAL:** When using any constants or types defined in the modules (e.g., `constants`, `types`), you **MUST** explicitly import them from their respective source module at the top of the file before using them. Do not assume they are globally available.
*   **Enums:**
    *   **MUST** use standard `enum` declarations (e.g., `enum MyEnum { Value1, Value2 }`).
    *   **MUST NOT** use `const enum`. Use standard `enum` instead to ensure the enum definition is preserved in the compiled output.

**3. Styling**

*   **Method:** Use **Tailwind CSS ONLY**.
*   **Setup:** Must load Tailwind with `<script src="https://cdn.tailwindcss.com"></script>` in `index.html`
*   **Restrictions:** **DO NOT** use separate CSS files (`.css`, `.module.css`), CSS-in-JS libraries (styled-components, emotion, etc.), or inline `style` attributes.
*   **Guidance:** Implement layout, color palette, and specific styles based on the web app's features.

**4. Responsive Design**

*  **Cross-Device Support:** Ensure the application provides an optimal and consistent user experience across a wide range of devices, including desktops, tablets, and mobile phones.
*  **Mobile-First Approach:** Adhere to Tailwind's mobile-first principle. Design and style for the smallest screen size by default, then use breakpoint prefixes (e.g., sm:, md:, lg:) to progressively enhance the layout for larger screens. This ensures a functional baseline experience on all devices and leads to cleaner, more maintainable code.
*. **Persistent Call-to-Action:** Make primary controls sticky to ensure they are always readily accessible, regardless of scroll position.

**5. React & TSX Syntax Rules**

*   **Rendering:** Use the `createRoot` API for rendering the application. **MUST NOT** use the legacy `ReactDOM.render`.
    *   **Correct `index.tsx` Example (React 18+):**
        ```tsx
        import React from 'react';
        import ReactDOM from 'react-dom/client'; // <--- Use 'react-dom/client'
        import App from './App'; // Assuming App is in App.tsx

        const rootElement = document.getElementById('root');
        if (!rootElement) {
          throw new Error("Could not find root element to mount to");
        }

        const root = ReactDOM.createRoot(rootElement);
        root.render(
          <React.StrictMode>
            <App />
          </React.StrictMode>
        );
        ```
*   **TSX Expressions:** Use standard JavaScript expressions inside curly braces `{}`.
*   **Template Literals (Backticks)**: Must *not* escape the outer delimiting backticks; you must escape the inner literal backticks.
    * Outer delimiting backticks: The backticks that start and end the template literal string must *not* be escaped. These define the template literal.
      **Correct usage:**
      ```
      const simpleGreeting = `Hello, ${name}!`; // Outer backticks are NOT escaped

      const multiLinePrompt = `
      This is a multi-line prompt
      for ${name}.
      ---
      Keep it simple.
      ---
      `; // Outer backticks are NOT escaped

      alert(`got error ${error}`); // The outer backticks in a function argument are not escaped
      ```
      **Incorrect usage:**
      ```
      // INCORRECT - Escaping the outer backticks
      const simpleGreeting = \`Hello, ${name}!\`;

      // INCORRECT - Escaping the outer backticks in a function argument
      alert(\`got error ${error}\`);

      // INCORRECT - Escaping the outer backticks
      const multiLinePrompt = \`
      This is a multi-line prompt
      ...
      \`;
      ```
    * Inner literal backticks: When including a backtick character inside the string, you must escape the inner literal backtick.
      **Correct usage**
      ```
      const commandInstruction = `To run the script, type \`npm start\` in your terminal.`; // Inner backticks are escaped
      const markdownCodeBlock = `
        Here's an example in JSON:
        \`\`\`json
        {
          "key": "value"
        }
        \`\`\`
        This is how you include a literal code block.
        `; // Inner backticks are escaped
      ```
      **Incorrect usage:**
      ```
      // INCORRECT - If you want `npm start` to have literal backticks
      const commandInstruction = `To run the script, type `npm start` in your terminal.`;
      // This would likely cause a syntax error because the second ` would end the template literal prematurely.
      ```
*   **Generics in Arrow Functions:** For generic arrow functions in TSX, a trailing comma **MUST** be added after the type parameter(s) to avoid parsing ambiguity. Only use Generics when the code is truly reusable.
    *   **Correct:** `const processData = <T,>(data: T): T => { ... };` (Note the comma after `T`)
    *   **Incorrect:** `const processData = <T>(data: T): T => { ... };`
*   **MUST NOT** use `<style jsx>` which doesn't work in standard React.
*   **React Router:** The app will run in an environment where it cannot update the URL path, except for the hash string. As such, do not generate any code that depends on manipulating the URL path, such as using React's `BrowserRouter`. But you may use React's `HashRouter`, as it only manipulates the hash string.
*   **MUST NOT** use `react-dropzone` for file upload; use a file input element instead, for example, `<input type="file">`.

**6. Code Quality & Patterns**

*   **Components:** Use **Functional Components** and **React Hooks** (e.g., `useState`, `useEffect`, `useCallback`).
*   **Readability:** Prioritize clean, readable, and well-organized code.
*   **Performance:** Write performant code where applicable.
*   **Accessibility:** Ensure sufficient color contrast between text and its background for readability.

**7. Libraries**

* Use popular and existing libraries for improving functionality and visual appeal. Do not use mock or made-up libraries.
* Use `d3` for data visualization.
* Use `recharts` for charts.

**8. Image**

* Use `https://picsum.photos/width/height` for placeholder images.

**9. React common pitfalls**

You must avoid the common pitfalls below when generating the code.

*  **React Hook Infinite Loop:** When using `useEffect` and `useCallback` together, be cautious to avoid infinite re-render loops.
    *   **The Pitfall:** A common loop occurs when:
        1.  A `useEffect` hook includes a memoized function (from `useCallback`) in its dependency array.
        2.  The `useCallback` hook includes a state variable (e.g., `count`) in *its* dependency array.
        3.  The function *inside* `useCallback` updates that same state variable (`setCount`) based on its current value (`count + 1`).
        *   *Resulting Cycle:* `setCount` updates `count` -> Component re-renders -> `useCallback` sees new `count`, creates a *new* function instance -> `useEffect` sees the function changed, runs again -> Calls `setCount`... loop!
        *   When using `useEffect`, if you want to run only once when the component mounts (and clean up when it unmounts), an empty dependency array [] is the correct pattern.
    * **Incorrect Code Example:**
    ```
    const [count, setCount] = useState(0);
    const [message, setMessage] = useState('Loading...');

    // This function's identity changes whenever 'count' changes
    const incrementAndLog = useCallback(() => {
      console.log('incrementAndLog called, current count:', count);
      const newCount = count + 1;
      setMessage(`Loading count ${newCount}...`); // Simulate work
      // Simulate async operation like fetching
      setTimeout(() => {
        console.log('Setting count to:', newCount);
        setCount(newCount); // <-- This state update triggers the useCallback dependency change
        setMessage(`Count is ${newCount}`);
      }, 500);
    }, [count]); // <-- Depends on 'count'

    // This effect runs whenever 'incrementAndLog' changes identity
    useEffect(() => {
      console.log("Effect running because incrementAndLog changed");
      incrementAndLog(); // Call the function
    }, [incrementAndLog]); // <-- Depends on the function that depends on 'count'
    ```
    * **Correct Code Example:**
    ```
    const [count, setCount] = useState(0);
    const [message, setMessage] = useState('Loading...');

    const incrementAndLog = useCallback(() => {
    // Use functional update to avoid direct dependency on 'count' in useCallback
    // OR keep the dependency but fix the useEffect call
      setCount(prevCount => {
        console.log('incrementAndLog called, previous count:', prevCount);
        const newCount = prevCount + 1;
        setMessage(`Loading count ${newCount}...`);
        // Simulate async operation
        setTimeout(() => {
          console.log('Setting count (functional update) to:', newCount);
          setMessage(`Count is ${newCount}`);
        }, 500);
        return newCount; // Return the new count for the functional update
      });
    }, [count]);

    // This effect runs ONLY ONCE on mount
    useEffect(() => {
      console.log("Effect running ONCE on mount to set initial state");
      setMessage('Setting initial count...');
      // Simulate initial load
      setTimeout(() => {
        setCount(1); // Set initial count
        setMessage('Count is 1');
      }, 500);
      // eslint-disable-next-line react-hooks/exhaustive-deps
    }, []); // <-- Empty array fixes the loop. Runs only once.
    ```
    * **Incorrect Code Example:**
    ```
     useEffect(() => {
      fetchScenario();
    }, [fetchScenario]); // Infinite initialize data.
    ```
    * **Correct Code Example:**
    ```
    useEffect(() => {
      fetchScenario();
      // eslint-disable-next-line react-hooks/exhaustive-deps
    }, []); // Only initialize data once
    ```
    The correct code will very likely cause the `eslint-plugin-react-hooks` to raise a warning. Add `eslint-disable-next-line react-hooks/exhaustive-deps` to suppress the warning.

*   **Be Explicit About Component Scope:**
    * Ensure helper components are defined outside the main component function body to prevent re-rendering issues.
    * Define components outside parent components to avoid unnecessary unmounting and remounting, which can lead to loss of input state and focus.
    * **Incorrect Code Example:**
    ```
    function ParentComponent() {
      const [text, setText] = useState('');
      // !! BAD: ChildInput is defined INSIDE ParentComponent !!
      const ChildInput: React.FC = () => {
        return (
          <input
            type="text"
            value={text} // Gets value from parent state
            onChange={(e) => setText(e.target.value)} // Updates parent state
            placeholder="Type here..."
            className="border p-2"
          />
        );
      };

      return (
        <div className="p-4 border border-red-500">
          <h2 className="text-lg font-bold mb-2">Bad Example</h2>
          <p className="mb-2">Parent State: {text}</p>
          <ChildInput /> {/* Rendering the locally defined component */}
        </div>
      );
    }
    export default ParentComponent;
    ```
    * **Correct Code Example:**
    ```
    interface ChildInputProps {
      value: string;
      onChange: (event: React.ChangeEvent<HTMLInputElement>) => void;
    }

    const ChildInput: React.FC<ChildInputProps> = ({ value, onChange }) => {
      return (
        <input
          type="text"
          value={value} // Gets value from props
          onChange={onChange} // Uses handler from props
          placeholder="Type here..."
          className="border p-2"
        />
      );
    };

    function ParentComponent() {
      const [text, setText] = useState('');
      const handleInputChange = (e: React.ChangeEvent<HTMLInputElement>) => {
        setText(e.target.value);
      };

      return (
        <div className="p-4 border border-green-500">
          <h2 className="text-lg font-bold mb-2">Good Example</h2>
          <p className="mb-2">Parent State: {text}</p>
          {/* Pass state and handler down as props */}
          <ChildInput value={text} onChange={handleInputChange} />
        </div>
      );
    }

    export default ParentComponent;
    ```
