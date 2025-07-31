#!/usr/bin/env node

/**
 * Gerador de Relatórios - Cria relatórios das tarefas .kiro
 *
 * Usage:
 *   node generate-report.js           # Gera relatório completo
 *   node generate-report.js --json    # Exporta JSON
 *   node generate-report.js --feature <name>  # Relatório de feature específica
 */

const fs = require("fs").promises;
const path = require("path");
const {
  loadTasksJson,
  generateMarkdownReport,
  getTasksStats,
  formatDate,
  readPatternsContext,
  generatePatternsReport,
} = require("./utils");

async function main() {
  const args = process.argv.slice(2);

  try {
    if (args.includes("--json")) {
      await generateJsonReport();
    } else if (args.includes("--feature")) {
      const featureName = args[args.indexOf("--feature") + 1];
      await generateFeatureReport(featureName);
    } else {
      await generateFullReport();
    }
  } catch (error) {
    console.error("❌ Erro ao gerar relatório:", error.message);
    process.exit(1);
  }
}

async function generateFullReport() {
  console.log("📄 Gerando relatório completo...");

  const tasksData = await loadTasksJson();

  if (!tasksData.tasks || Object.keys(tasksData.tasks).length === 0) {
    console.log(
      '📝 Nenhuma tarefa encontrada. Execute "npm run scan" primeiro.'
    );
    return;
  }

  // Ler contexto de patterns
  const patternsContext = await readPatternsContext();

  const reportPath = path.join(__dirname, "task-report.md");
  await generateEnhancedMarkdownReport(tasksData, patternsContext, reportPath);

  // Gera também um resumo no console
  const stats = getTasksStats(tasksData);
  console.log("\n📊 RESUMO DO RELATÓRIO\n");
  console.log(`📁 Features: ${stats.totalFeatures}`);
  console.log(`📋 Tarefas: ${stats.completedTasks}/${stats.totalTasks}`);
  console.log(
    `📈 Progresso: ${Math.round(
      (stats.completedTasks / stats.totalTasks) * 100
    )}%`
  );
  console.log(`🔄 Última atualização: ${formatDate(tasksData.lastUpdated)}`);

  // Mostrar informações de patterns
  if (patternsContext.hasPatterns) {
    console.log(`📐 Patterns: Configurados e incluídos no relatório`);
  } else {
    console.log(
      `📐 Patterns: Não configurados (use patterns-prompt-direto.md)`
    );
  }
}

async function generateJsonReport() {
  console.log("📊 Gerando relatório JSON...");

  const tasksData = await loadTasksJson();
  const stats = getTasksStats(tasksData);

  const jsonReport = {
    generatedAt: new Date().toISOString(),
    summary: {
      totalFeatures: stats.totalFeatures,
      totalTasks: stats.totalTasks,
      completedTasks: stats.completedTasks,
      pendingTasks: stats.pendingTasks,
      overallProgress: Math.round(
        (stats.completedTasks / stats.totalTasks) * 100
      ),
    },
    features: stats.byFeature,
    lastDataUpdate: tasksData.lastUpdated,
  };

  const jsonPath = path.join(__dirname, "task-report.json");
  await fs.writeFile(jsonPath, JSON.stringify(jsonReport, null, 2));

  console.log(`✅ Relatório JSON salvo em: ${jsonPath}`);
}

async function generateFeatureReport(featureName) {
  if (!featureName) {
    console.error("❌ Nome da feature é obrigatório");
    return;
  }

  console.log(`📋 Gerando relatório para feature: ${featureName}`);

  const tasksData = await loadTasksJson();

  if (!tasksData.tasks[featureName]) {
    console.error(`❌ Feature '${featureName}' não encontrada`);
    return;
  }

  const featureTasks = tasksData.tasks[featureName];
  const completed = featureTasks.filter((t) => t.completed).length;
  const total = featureTasks.length;
  const percentage = Math.round((completed / total) * 100);

  let markdown = `# Relatório - ${featureName}\n\n`;
  markdown += `**Data:** ${formatDate(new Date().toISOString())}\n\n`;
  markdown += `## 📊 Resumo\n\n`;
  markdown += `- **Progresso:** ${completed}/${total} tarefas (${percentage}%)\n`;
  markdown += `- **Status:** ${
    percentage === 100 ? "✅ Concluída" : "⏳ Em Andamento"
  }\n\n`;

  markdown += `## 📋 Tarefas\n\n`;

  featureTasks.forEach((task) => {
    const status = task.completed ? "✅" : "⏳";
    markdown += `### ${status} ${task.id}\n\n`;
    markdown += `**Descrição:** ${task.description}\n`;
    if (task.phase) markdown += `**Fase:** ${task.phase}\n`;

    if (task.subtasks && task.subtasks.length > 0) {
      markdown += `\n**Subtarefas:**\n`;
      task.subtasks.forEach((subtask) => {
        const subtaskStatus = subtask.completed ? "✅" : "⏳";
        markdown += `- ${subtaskStatus} ${subtask.description}\n`;
      });
    }
    markdown += "\n";
  });

  const reportPath = path.join(__dirname, `${featureName}-report.md`);
  await fs.writeFile(reportPath, markdown);

  console.log(`✅ Relatório da feature salvo em: ${reportPath}`);
}

/**
 * Gera relatório markdown incluindo informações de patterns
 */
async function generateEnhancedMarkdownReport(
  tasksData,
  patternsContext,
  outputPath
) {
  const stats = getTasksStats(tasksData);
  const lastUpdated = formatDate(tasksData.lastUpdated);

  let markdown = `# Relatório Completo .kiro\n\n`;
  markdown += `**Última atualização:** ${lastUpdated}\n\n`;

  // Seção de resumo geral
  markdown += `## 📊 Resumo Geral\n\n`;
  markdown += `- **Features:** ${stats.totalFeatures}\n`;
  markdown += `- **Tarefas:** ${stats.completedTasks}/${stats.totalTasks} concluídas\n`;
  markdown += `- **Progresso:** ${Math.round(
    (stats.completedTasks / stats.totalTasks) * 100
  )}%\n\n`;

  // Incluir informações de patterns
  markdown += generatePatternsReport(patternsContext);
  markdown += `\n\n`;

  // Resumo por feature
  markdown += `## 📋 Progresso por Feature\n\n`;

  for (const [feature, featureStats] of Object.entries(stats.byFeature)) {
    const percentage = Math.round(
      (featureStats.completed / featureStats.total) * 100
    );

    // Barra de progresso visual
    const progressBar =
      "█".repeat(Math.floor(percentage / 10)) +
      "░".repeat(10 - Math.floor(percentage / 10));

    markdown += `### ${feature}\n\n`;
    markdown += `**Progresso:** ${featureStats.completed}/${featureStats.total} (${percentage}%)\n\n`;
    markdown += `\`${progressBar}\` ${percentage}%\n\n`;

    if (featureStats.subtasks > 0) {
      markdown += `**Subtarefas:** ${featureStats.completedSubtasks}/${featureStats.subtasks}\n\n`;
    }
  }

  // Tarefas pendentes
  markdown += `## ⏳ Próximas Tarefas\n\n`;

  for (const [feature, tasks] of Object.entries(tasksData.tasks)) {
    const pendingTasks = tasks.filter((task) => !task.completed);

    if (pendingTasks.length > 0) {
      markdown += `### ${feature}\n\n`;

      pendingTasks.slice(0, 3).forEach((task) => {
        markdown += `- **${task.id}**: ${task.description}\n`;
        if (task.phase) {
          markdown += `  - *Fase: ${task.phase}*\n`;
        }
      });

      if (pendingTasks.length > 3) {
        markdown += `- ... e mais ${pendingTasks.length - 3} tarefa(s)\n`;
      }

      markdown += `\n`;
    }
  }

  // Recomendações baseadas em patterns
  if (patternsContext.hasPatterns) {
    markdown += `## 🎯 Recomendações de Desenvolvimento\n\n`;
    markdown += `✅ **Patterns configurados** - Use sempre os padrões estabelecidos:\n\n`;

    if (patternsContext.conventions) {
      markdown += `- 📝 Consulte \`.kiro/patterns/conventions.md\` para nomenclatura\n`;
    }

    if (patternsContext.typescript) {
      markdown += `- 🔷 Siga regras TypeScript em \`.kiro/patterns/typescript.md\`\n`;
    }

    if (patternsContext.frontend) {
      markdown += `- ⚛️ Use padrões frontend de \`.kiro/patterns/frontend/\`\n`;
    }

    if (patternsContext.backend) {
      markdown += `- 🔧 Aplique padrões backend de \`.kiro/patterns/backend/\`\n`;
    }

    if (patternsContext.examples) {
      markdown += `- 💡 Consulte exemplos em \`.kiro/patterns/examples/\`\n`;
    }

    markdown += `\n`;
  } else {
    markdown += `## 📐 Configurar Patterns\n\n`;
    markdown += `⚠️ **Patterns não configurados** - Para máxima eficiência:\n\n`;
    markdown += `1. Execute o prompt: \`docs/patterns-prompt-direto.md\`\n`;
    markdown += `2. Configure padrões específicos do projeto\n`;
    markdown += `3. Regenere .cursorrules para incluir patterns\n\n`;
  }

  if (outputPath) {
    await fs.writeFile(outputPath, markdown);
    console.log(`📄 Relatório completo salvo em: ${outputPath}`);
  }

  return markdown;
}

if (require.main === module) {
  main();
}

module.exports = {
  generateFullReport,
  generateJsonReport,
  generateFeatureReport,
};
