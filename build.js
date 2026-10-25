const fs = require('fs');
const path = require('path');

console.log('--- Starting Static Build ---');

const publicDir = path.join(__dirname, 'public');
if (!fs.existsSync(publicDir)) {
  fs.mkdirSync(publicDir, { recursive: true });
}

const items = fs.readdirSync(__dirname);
let copied = 0;

for (const item of items) {
  if (['node_modules', '.git', 'public', '.gitignore', 'build.js'].includes(item)) continue;
  const src = path.join(__dirname, item);
  const dest = path.join(publicDir, item);
  try {
    const stat = fs.statSync(src);
    if (stat.isFile()) {
      fs.copyFileSync(src, dest);
      copied++;
    }
  } catch (err) {
    console.error('Error copying ' + item + ':', err.message);
  }
}

console.log(`--- Build complete: ${copied} files copied to public/ ---`);
