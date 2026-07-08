```markdown
# Construction-scheduler-AI-with-LLM-integration Development Patterns

> Auto-generated skill from repository analysis

## Overview
This skill teaches you the development conventions and workflows used in the `Construction-scheduler-AI-with-LLM-integration` TypeScript codebase. You'll learn about file organization, code style, commit message patterns, and how to write and run tests. This repository focuses on building AI-powered construction scheduling tools with LLM (Large Language Model) integration.

## Coding Conventions

### File Naming
- Use **kebab-case** for all filenames.
  - Example:  
    ```
    project-scheduler.ts
    llm-integration.test.ts
    ```

### Import Style
- Use **relative imports** for modules within the project.
  - Example:
    ```typescript
    import { scheduleProject } from './project-scheduler';
    ```

### Export Style
- Use **named exports** for all exported functions, types, or constants.
  - Example:
    ```typescript
    // project-scheduler.ts
    export function scheduleProject(data: ProjectData): ScheduleResult { ... }
    ```

### Commit Messages
- Follow **Conventional Commits** with prefixes like `feat` and `fix`.
- Keep commit messages concise (average ~58 characters).
  - Example:
    ```
    feat: add LLM integration for schedule optimization
    fix: correct date calculation in scheduler
    ```

## Workflows

### Code Development
**Trigger:** When adding new features or fixing bugs  
**Command:** `/dev`

1. Create a new branch for your feature or fix.
2. Write code using TypeScript, following the file naming and import/export conventions.
3. Write or update tests in files matching `*.test.*`.
4. Commit changes using the conventional commit format.
5. Push your branch and open a pull request.

### Testing
**Trigger:** Before pushing or merging code  
**Command:** `/test`

1. Identify or create test files with the `*.test.*` pattern.
2. Run the test suite using your preferred TypeScript test runner (framework not specified).
   - Example (if using Jest):
     ```
     npx jest
     ```
3. Ensure all tests pass before submitting code.

### Code Review
**Trigger:** When reviewing a pull request  
**Command:** `/review`

1. Check that file naming, import, and export conventions are followed.
2. Verify that commit messages use the correct format.
3. Confirm that tests exist and pass.
4. Approve or request changes as needed.

## Testing Patterns

- Test files use the `*.test.*` naming pattern (e.g., `llm-integration.test.ts`).
- The specific test framework is not defined; choose one compatible with TypeScript (e.g., Jest, Mocha).
- Tests should cover both core logic and LLM integration points.

**Example Test File:**
```typescript
// project-scheduler.test.ts
import { scheduleProject } from './project-scheduler';

describe('scheduleProject', () => {
  it('should return a valid schedule for sample data', () => {
    const result = scheduleProject(sampleProjectData);
    expect(result).toBeDefined();
    // Add more assertions as needed
  });
});
```

## Commands
| Command   | Purpose                                      |
|-----------|----------------------------------------------|
| /dev      | Start a new feature or bugfix workflow       |
| /test     | Run the test suite before pushing/merging    |
| /review   | Perform code review on a pull request        |
```
