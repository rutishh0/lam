#!/usr/bin/env node

const fs = require('fs');
const path = require('path');

const indexPath = path.join(__dirname, 'src', 'index.js');

// Check which UI is currently active
function getCurrentUI() {
  const content = fs.readFileSync(indexPath, 'utf8');
  if (content.includes("import App from './AppModern'")) {
    return 'modern';
  } else if (content.includes("import App from './App'")) {
    return 'classic';
  }
  return 'unknown';
}

// Switch to modern UI
function switchToModern() {
  const content = fs.readFileSync(indexPath, 'utf8');
  const updatedContent = content.replace(
    /import App from ['"]\.\/App['"];?/g,
    "import App from './AppModern';"
  );
  fs.writeFileSync(indexPath, updatedContent);
  console.log('✅ Switched to Modern UI (Suna-inspired design)');
}

// Switch to classic UI
function switchToClassic() {
  const content = fs.readFileSync(indexPath, 'utf8');
  const updatedContent = content.replace(
    /import App from ['"]\.\/AppModern['"];?/g,
    "import App from './App';"
  );
  fs.writeFileSync(indexPath, updatedContent);
  console.log('✅ Switched to Classic UI (original design)');
}

// Main function
function main() {
  const args = process.argv.slice(2);
  const command = args[0];

  console.log('🎨 Elevate UI Switcher\n');

  if (!fs.existsSync(indexPath)) {
    console.error('❌ Error: src/index.js not found');
    process.exit(1);
  }

  const currentUI = getCurrentUI();
  console.log(`Current UI: ${currentUI.toUpperCase()}\n`);

  switch (command) {
    case 'modern':
    case 'suna':
      if (currentUI === 'modern') {
        console.log('ℹ️  Already using Modern UI');
      } else {
        switchToModern();
      }
      break;

    case 'classic':
    case 'original':
      if (currentUI === 'classic') {
        console.log('ℹ️  Already using Classic UI');
      } else {
        switchToClassic();
      }
      break;

    case 'status':
      console.log('No changes made.');
      break;

    default:
      console.log(`Usage: node switch-ui.js [command]

Commands:
  modern    Switch to modern UI (Suna-inspired)
  classic   Switch to classic UI (original)
  status    Show current UI status

Examples:
  node switch-ui.js modern
  node switch-ui.js classic
  node switch-ui.js status
`);
      break;
  }

  console.log('\n🚀 Changes will take effect on next app reload');
}

main(); 