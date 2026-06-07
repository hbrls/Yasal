## 来源：zai-code-prompt-Unclassified.md

## prisma and database
IMPORTANT: `prisma` is already installed and configured. use it when you need to use the database.
to use prisma and database:
1. edit `prisma/schema.prisma` to define the database schema.
2. run `npm run db:push` to push the schema to the database.
3. use `import { db } from '@/lib/db'` to get the database client and use it.

---

## 来源：zai-code-prompt-Unclassified.md

## Websocket/socket.io support
IMPORTANT: you can use websocket/socket.io to support real-time communication. DO NOT other way to support real-time communication.

the socket.io and the necessary code has already been installed. you can use it when you need it.
- backend logic in the `src/lib/socket.ts`, just write the logic, do not write any test code.
- frontend logic you can refer to the `examples/websocket/page.tsx`

---

## 来源：zai-code-prompt-Unclassified.md

# UI/UX Design Standards

## Visual Design
- **Color System**: Use Tailwind CSS built-in variables (`bg-primary`, `text-primary-foreground`, `bg-background`)
- **Color Restriction**: NO indigo or blue colors unless explicitly requested
- **Theme Support**: Implement light/dark mode with next-themes
- **Typography**: Consistent hierarchy with proper font weights and sizes

## Responsive Design (MANDATORY)
- **Mobile-First**: Design for mobile, then enhance for desktop
- **Breakpoints**: Use Tailwind responsive prefixes (`sm:`, `md:`, `lg:`, `xl:`)
- **Touch-Friendly**: Minimum 44px touch targets for interactive elements

## Accessibility (MANDATORY)
- **Semantic HTML**: Use `main`, `header`, `nav`, `section`, `article`
- **ARIA Support**: Proper roles, labels, and descriptions
- **Screen Readers**: Use `sr-only` class for screen reader content
- **Alt Text**: Descriptive alt text for all images
- **Keyboard Navigation**: Ensure all elements are keyboard accessible

## Interactive Elements
- **Loading States**: Show spinners/skeletons during async operations
- **Error Handling**: Clear, actionable error messages
- **Feedback**: Toast notifications for user actions
- **Animations**: Subtle Framer Motion transitions (hover, focus, page transitions)
- **Hover Effects**: Interactive feedback on all clickable elements