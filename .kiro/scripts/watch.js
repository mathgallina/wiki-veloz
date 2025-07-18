#!/usr/bin/env node

/**
 * Watch Script - Monitora mudanças nos arquivos tasks.md
 * e atualiza automaticamente o JSON de status
 */

const fs = require("fs");
const path = require("path");
const { readAllTasks, updateTasksJson } = require("./read-tasks");

let isScanning = false;
let scanTimeout = null;

async function scanTasks() {
  if (isScanning) {
    console.log("⏳ Escaneamento já em andamento...");
    return;
  }

  isScanning = true;

  try {
    console.log("🔍 Detectada mudança, escaneando tarefas...");
    const tasksData = await readAllTasks();

    const jsonPath = path.join(__dirname, "tasks-status.json");
    await fs.promises.writeFile(jsonPath, JSON.stringify(tasksData, null, 2));

    const totalTasks = Object.values(tasksData.tasks).reduce(
      (sum, feature) => sum + feature.length,
      0
    );
    const completedTasks = Object.values(tasksData.tasks)
      .flat()
      .filter((task) => task.completed).length;

    console.log(
      `✅ Atualizado! ${completedTasks}/${totalTasks} tarefas concluídas (${Math.round(
        (completedTasks / totalTasks) * 100
      )}%)`
    );
  } catch (error) {
    console.error("❌ Erro ao escanear:", error.message);
  } finally {
    isScanning = false;
  }
}

function debouncedScan() {
  if (scanTimeout) {
    clearTimeout(scanTimeout);
  }

  scanTimeout = setTimeout(scanTasks, 1000); // Aguarda 1 segundo sem mudanças
}

function watchTaskFiles() {
  const specsDir = path.join(__dirname, "../specs");

  if (!fs.existsSync(specsDir)) {
    console.error("❌ Diretório .kiro/specs não encontrado");
    process.exit(1);
  }

  console.log("👀 Monitorando mudanças em arquivos tasks.md...");
  console.log("🛑 Pressione Ctrl+C para parar");

  // Monitora o diretório specs recursivamente
  fs.watch(specsDir, { recursive: true }, (eventType, filename) => {
    if (filename && filename.endsWith("tasks.md")) {
      console.log(`📝 Mudança detectada: ${filename}`);
      debouncedScan();
    }
  });

  // Escaneamento inicial
  debouncedScan();
}

function main() {
  const args = process.argv.slice(2);

  if (args.includes("--help") || args.includes("-h")) {
    console.log("\n👀 WATCH SCRIPT - Monitor de Tarefas .kiro\n");
    console.log(
      "Monitora mudanças nos arquivos tasks.md e atualiza automaticamente o status.\n"
    );
    console.log("Usage:");
    console.log("  node watch.js        # Inicia monitoramento");
    console.log("  node watch.js --help # Mostra esta ajuda\n");
    console.log(
      "📝 O script monitora alterações em todos os arquivos tasks.md"
    );
    console.log("   e atualiza o tasks-status.json automaticamente.\n");
    return;
  }

  try {
    watchTaskFiles();
  } catch (error) {
    console.error("❌ Erro ao iniciar monitoramento:", error.message);
    process.exit(1);
  }
}

// Tratamento de sinais para parada limpa
process.on("SIGINT", () => {
  console.log("\n👋 Parando monitoramento...");
  process.exit(0);
});

process.on("SIGTERM", () => {
  console.log("\n👋 Parando monitoramento...");
  process.exit(0);
});

if (require.main === module) {
  main();
}

module.exports = { watchTaskFiles, scanTasks };
