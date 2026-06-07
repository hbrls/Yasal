{
  "guidelines": {
    "code_quality": [
      "Use 2 spaces for indentation",
      "Split functionality into smaller, focused modules",
      "Keep files as small as possible",
      "Use proper TypeScript typing throughout",
      "Follow consistent naming conventions",
      "Include comprehensive error handling",
      "Add meaningful comments for complex logic"
    ],
    "backend_requirements": [
      "All backend code must use Encore.ts",
      "Store data using SQL Database or Object Storage",
      "All services go under backend/ folder",
      "Each API endpoint in its own file",
      "Unique endpoint names across the application",
      "Use template literals for database queries",
      "Document all API endpoints with comments"
    ],
    "frontend_requirements": [
      "Use React with TypeScript and Tailwind CSS",
      "Import backend client as: import backend from '~backend/client'",
      "Use shadcn/ui components when appropriate",
      "Create responsive designs for all screen sizes",
      "Include subtle animations and interactions",
      "Use proper error handling with console.error logs",
      "Split components into smaller, reusable modules",
      "Frontend code goes in frontend/ folder (no src/ subfolder)"
    ],
    "file_handling": [
      "Only output files that need changes"
    ],
    "security": [
      "Use secrets for all sensitive data",
      "Implement proper authentication when requested",
      "Validate all user inputs",
      "Use proper CORS settings",
      "Follow security best practices for APIs"
    ]
  }
}