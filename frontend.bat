cd "frontend"
if not exist node_modules\ (call npm i)
if not exist build\ (call npm run build)
call node index.js
