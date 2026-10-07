#!/bin/sh
set -eu

# tsconfig образа лежит в корне контейнера. Без include проверка типов
# следит за /, уходит в /proc/*/root и зацикливается.
node <<'EOF'
const fs = require('fs');
const cfg = JSON.parse(fs.readFileSync('/tsconfig.json', 'utf8'));
cfg.include = ['src/**/*', 'declarations.d.ts'];
cfg.exclude = ['node_modules', 'build', 'public'];
fs.writeFileSync('/tsconfig.json', JSON.stringify(cfg, null, 2));
EOF

node src/assets/config_generator.js
node build-notifications-index.js
npm run build-index
exec npm run serve -- --host 0.0.0.0 --port 4567
