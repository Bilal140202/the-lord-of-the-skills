# GitHub Copilot Instructions — CLI Tool

## Project Context
This is a command-line interface tool for developer productivity, automation, or system administration.

## Code Generation Rules

### Command Definition
```typescript
// Commander.js example
program
  .command('deploy')
  .description('Deploy application')
  .option('-e, --env <env>', 'Environment', 'dev')
  .option('-f, --force', 'Skip confirmation')
  .action(async (options) => {
    // Implementation
  });
```

### User-Friendly Errors
```typescript
// ✅ Helpful error with suggestion
if (!apiKey) {
  console.error('Error: API key not found');
  console.error('Run "tool login" or set TOOL_API_KEY environment variable');
  process.exit(1);
}

// ❌ Raw error
throw new Error('Missing API key');
```

### Progress Indicators
```typescript
// For long operations
import ora from 'ora';

const spinner = ora('Deploying...').start();
try {
  await deploy();
  spinner.succeed('Deployed successfully');
} catch (err) {
  spinner.fail('Deployment failed');
}
```

### Output Formatting
```typescript
// Support multiple formats
if (options.format === 'json') {
  console.log(JSON.stringify(data));
} else {
  // Human-readable table
  console.table(data);
}
```

### Interactive Prompts
```typescript
import inquirer from 'inquirer';

const { confirmed } = await inquirer.prompt([{
  type: 'confirm',
  name: 'confirmed',
  message: 'Are you sure?',
  default: false
}]);

if (!confirmed) process.exit(0);
```

### Configuration Management
```typescript
// Load config with precedence
const config = {
  ...loadConfigFile(),
  ...loadEnvVars(),
  ...cliFlags
};
```

### Exit Codes
```typescript
// Proper exit codes
process.exit(0);   // Success
process.exit(1);   // General error
process.exit(2);   // Misuse/invalid args
```

## When Generating Code
1. Validate all inputs before execution
2. Provide helpful error messages with next steps
3. Show progress for long operations
4. Support --help for all commands
5. Use proper exit codes
6. Colorize output for readability
7. Confirm destructive actions
8. Support --format for machine-readable output
9. Handle Ctrl+C gracefully
10. Test cross-platform compatibility
