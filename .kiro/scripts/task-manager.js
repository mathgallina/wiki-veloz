#!/usr/bin/env node

/**
 * Task Manager - Gerenciador Principal de Tarefas .kiro
 *
 * Usage:
 *   node task-manager.js scan           # Escaneia todas as tarefas
 *   node task-manager.js status         # Mostra status geral
 *   node task-manager.js complete <id>  # Marca tarefa como concluída
 *   node task-manager.js list [feature] # Lista tarefas por feature
 */

const fs = require("fs");
const path = require("path");
const { readAllTasks, updateTasksJson } = require("./read-tasks");
const { updateTaskStatus } = require("./update-task");
const {
  loadTasksJson,
  saveTasksJson,
  displayTasksTable,
  readPatternsContext,
  generatePatternsReport,
} = require("./utils");

const COMMANDS = {
  scan: "Escaneia todas as tarefas das features",
  status: "Mostra resumo do status das tarefas",
  complete: "Marca uma tarefa como concluída",
  list: "Lista tarefas (opcionalmente filtrado por feature)",
  patterns: "Mostra status dos padrões de código",
  help: "Mostra esta ajuda",
};

async function main() {
  const [command, ...args] = process.argv.slice(2);

  try {
    switch (command) {
      case "scan":
        await scanAllTasks();
        break;
      case "status":
        await showStatus();
        break;
      case "complete":
        await completeTask(args[0]);
        break;
      case "list":
        await listTasks(args[0]);
        break;
      case "patterns":
        await showPatternsStatus();
        break;
      case "help":
      default:
        showHelp();
        break;
    }
  } catch (error) {
    console.error("❌ Erro:", error.message);
    process.exit(1);
  }
}

async function scanAllTasks() {
  console.log("🔍 Escaneando todas as tarefas...");

  const tasksData = await readAllTasks();
  await saveTasksJson(tasksData);

  const totalTasks = Object.values(tasksData.tasks).reduce(
    (sum, feature) => sum + feature.length,
    0
  );
  const completedTasks = Object.values(tasksData.tasks)
    .flat()
    .filter((task) => task.completed).length;

  console.log(`✅ Escaneamento concluído!`);
  console.log(
    `📊 Total: ${totalTasks} tarefas | Concluídas: ${completedTasks} | Pendentes: ${
      totalTasks - completedTasks
    }`
  );
  console.log(`💾 Status salvo em: .kiro/scripts/tasks-status.json`);
}

async function showStatus() {
  const tasksData = await loadTasksJson();

  if (!tasksData.tasks || Object.keys(tasksData.tasks).length === 0) {
    console.log('📝 Nenhuma tarefa encontrada. Execute "scan" primeiro.');
    return;
  }

  console.log("\n📊 RESUMO GERAL DAS TAREFAS\n");

  let totalTasks = 0;
  let completedTasks = 0;

  for (const [feature, tasks] of Object.entries(tasksData.tasks)) {
    const completed = tasks.filter((t) => t.completed).length;
    const total = tasks.length;
    const percentage = total > 0 ? Math.round((completed / total) * 100) : 0;

    console.log(`🎯 ${feature}: ${completed}/${total} (${percentage}%)`);
    totalTasks += total;
    completedTasks += completed;
  }

  const overallPercentage =
    totalTasks > 0 ? Math.round((completedTasks / totalTasks) * 100) : 0;

  console.log("\n" + "=".repeat(50));
  console.log(
    `📈 TOTAL GERAL: ${completedTasks}/${totalTasks} (${overallPercentage}%)`
  );
  console.log("=".repeat(50));

  if (overallPercentage === 100) {
    console.log("🎉 Parabéns! Todas as tarefas foram concluídas!");
  }
}

async function completeTask(taskId) {
  if (!taskId) {
    console.error("❌ ID da tarefa é obrigatório. Use: complete <id>");
    return;
  }

  console.log(`⏳ Marcando tarefa ${taskId} como concluída...`);

  const result = await updateTaskStatus(taskId, true);

  if (result.success) {
    console.log(`✅ Tarefa ${taskId} marcada como concluída!`);
    console.log(`📁 Feature: ${result.feature}`);
    console.log(`📝 Tarefa: ${result.task.description}`);

    // Atualiza o JSON
    await scanAllTasks();
  } else {
    console.error(`❌ ${result.error}`);
  }
}

async function listTasks(featureFilter) {
  const tasksData = await loadTasksJson();

  if (!tasksData.tasks || Object.keys(tasksData.tasks).length === 0) {
    console.log('📝 Nenhuma tarefa encontrada. Execute "scan" primeiro.');
    return;
  }

  console.log("\n📋 LISTA DE TAREFAS\n");

  for (const [feature, tasks] of Object.entries(tasksData.tasks)) {
    if (
      featureFilter &&
      !feature.toLowerCase().includes(featureFilter.toLowerCase())
    ) {
      continue;
    }

    console.log(`\n🎯 Feature: ${feature}`);
    console.log("─".repeat(40));

    tasks.forEach((task) => {
      const status = task.completed ? "✅" : "⏳";
      const phase = task.phase ? `[${task.phase}]` : "";
      console.log(`${status} ${task.id} ${phase} ${task.description}`);
    });
  }
}

function showHelp() {
  console.log("\n🛠️  TASK MANAGER - Gerenciador de Tarefas .kiro\n");

  Object.entries(COMMANDS).forEach(([cmd, desc]) => {
    console.log(`  ${cmd.padEnd(12)} ${desc}`);
  });

  console.log("\n📖 Exemplos:");
  console.log("  node task-manager.js scan");
  console.log("  node task-manager.js complete design-system-1.1");
  console.log("  node task-manager.js list design-system");
  console.log("  node task-manager.js patterns");
  console.log("");
  console.log("📚 Documentação:");
  console.log("  README.md       - Documentação completa");
  console.log("  quick-start.md  - Guia de início rápido");
  console.log("");
}

/**
 * Mostra o status dos padrões de código
 */
async function showPatternsStatus() {
  console.log("📐 Status dos Padrões de Código .kiro\n");

  try {
    const patternsContext = await readPatternsContext();

    if (!patternsContext.hasPatterns) {
      console.log("⚠️  Padrões não configurados");
      console.log("");
      console.log("🚀 Para configurar patterns:");
      console.log("1. Execute: docs/patterns-prompt-direto.md");
      console.log("2. Configure padrões específicos do projeto");
      console.log("3. Regenere .cursorrules para incluir patterns");
      console.log("");
      return;
    }

    console.log("✅ Padrões configurados!\n");

    // Mostrar detalhes dos patterns
    if (patternsContext.conventions) {
      console.log("📝 Convenções de nomenclatura: ✅ Configuradas");
    } else {
      console.log("📝 Convenções de nomenclatura: ❌ Não encontradas");
    }

    if (patternsContext.typescript) {
      console.log("🔷 Padrões TypeScript: ✅ Configurados");
    } else {
      console.log("🔷 Padrões TypeScript: ❌ Não encontrados");
    }

    if (
      patternsContext.frontend &&
      Object.keys(patternsContext.frontend).length > 0
    ) {
      const frontendCount = Object.keys(patternsContext.frontend).length;
      console.log(`⚛️  Padrões Frontend: ✅ ${frontendCount} arquivo(s)`);
      Object.keys(patternsContext.frontend).forEach((file) => {
        console.log(`   - ${file}.md`);
      });
    } else {
      console.log("⚛️  Padrões Frontend: ❌ Não encontrados");
    }

    if (
      patternsContext.backend &&
      Object.keys(patternsContext.backend).length > 0
    ) {
      const backendCount = Object.keys(patternsContext.backend).length;
      console.log(`🔧 Padrões Backend: ✅ ${backendCount} arquivo(s)`);
      Object.keys(patternsContext.backend).forEach((file) => {
        console.log(`   - ${file}.md`);
      });
    } else {
      console.log("🔧 Padrões Backend: ❌ Não encontrados");
    }

    if (patternsContext.examples) {
      console.log(
        `💡 Exemplos práticos: ✅ ${patternsContext.examples} arquivo(s)`
      );
    } else {
      console.log("💡 Exemplos práticos: ❌ Não encontrados");
    }

    console.log("");
    console.log("🎯 Próximos passos:");
    console.log("- Use os padrões durante desenvolvimento");
    console.log("- Regenere .cursorrules se atualizar patterns");
    console.log("- Consulte patterns/README.md para detalhes");
  } catch (error) {
    console.error("❌ Erro ao verificar patterns:", error.message);
  }
}

if (require.main === module) {
  main();
}

module.exports = { scanAllTasks, showStatus, completeTask, listTasks };
