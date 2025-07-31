const fs = require("fs").promises;
const path = require("path");

const TASKS_JSON_PATH = path.join(__dirname, "tasks-status.json");

/**
 * Carrega o arquivo JSON de status das tarefas
 */
async function loadTasksJson() {
  try {
    const content = await fs.readFile(TASKS_JSON_PATH, "utf8");
    return JSON.parse(content);
  } catch (error) {
    if (error.code === "ENOENT") {
      // Arquivo não existe, retorna estrutura vazia
      return {
        lastUpdated: null,
        tasks: {},
      };
    }
    throw new Error(`Erro ao carregar tasks-status.json: ${error.message}`);
  }
}

/**
 * Salva dados no arquivo JSON de status das tarefas
 */
async function saveTasksJson(data) {
  try {
    await fs.writeFile(TASKS_JSON_PATH, JSON.stringify(data, null, 2));
  } catch (error) {
    throw new Error(`Erro ao salvar tasks-status.json: ${error.message}`);
  }
}

/**
 * Exibe tabela formatada de tarefas
 */
function displayTasksTable(tasksData) {
  if (!tasksData.tasks || Object.keys(tasksData.tasks).length === 0) {
    console.log("📝 Nenhuma tarefa encontrada.");
    return;
  }

  console.log("\n📊 STATUS DAS TAREFAS POR FEATURE\n");

  // Cabeçalho
  console.log(
    "Feature".padEnd(20) +
      "Total".padEnd(8) +
      "Concluídas".padEnd(12) +
      "Progresso"
  );
  console.log("─".repeat(50));

  for (const [feature, tasks] of Object.entries(tasksData.tasks)) {
    const total = tasks.length;
    const completed = tasks.filter((t) => t.completed).length;
    const percentage = total > 0 ? Math.round((completed / total) * 100) : 0;
    const progressBar = createProgressBar(percentage);

    console.log(
      feature.padEnd(20) +
        total.toString().padEnd(8) +
        completed.toString().padEnd(12) +
        `${progressBar} ${percentage}%`
    );
  }

  console.log("─".repeat(50));

  const totalTasks = Object.values(tasksData.tasks).reduce(
    (sum, tasks) => sum + tasks.length,
    0
  );
  const totalCompleted = Object.values(tasksData.tasks)
    .flat()
    .filter((task) => task.completed).length;
  const overallPercentage =
    totalTasks > 0 ? Math.round((totalCompleted / totalTasks) * 100) : 0;

  console.log(
    "TOTAL".padEnd(20) +
      totalTasks.toString().padEnd(8) +
      totalCompleted.toString().padEnd(12) +
      `${createProgressBar(overallPercentage)} ${overallPercentage}%`
  );
}

/**
 * Cria barra de progresso visual
 */
function createProgressBar(percentage, length = 20) {
  const filled = Math.round((percentage / 100) * length);
  const empty = length - filled;
  return "█".repeat(filled) + "░".repeat(empty);
}

/**
 * Formata data para exibição
 */
function formatDate(isoString) {
  if (!isoString) return "Nunca";

  const date = new Date(isoString);
  return date.toLocaleString("pt-BR", {
    year: "numeric",
    month: "2-digit",
    day: "2-digit",
    hour: "2-digit",
    minute: "2-digit",
  });
}

/**
 * Encontra tarefa por ID
 */
function findTaskById(tasksData, taskId) {
  for (const [feature, tasks] of Object.entries(tasksData.tasks)) {
    const task = tasks.find((t) => t.id === taskId);
    if (task) {
      return { task, feature };
    }
  }
  return null;
}

/**
 * Obtém estatísticas gerais das tarefas
 */
function getTasksStats(tasksData) {
  const stats = {
    totalFeatures: Object.keys(tasksData.tasks).length,
    totalTasks: 0,
    completedTasks: 0,
    pendingTasks: 0,
    totalSubtasks: 0,
    completedSubtasks: 0,
    byFeature: {},
  };

  for (const [feature, tasks] of Object.entries(tasksData.tasks)) {
    const featureStats = {
      total: tasks.length,
      completed: 0,
      pending: 0,
      subtasks: 0,
      completedSubtasks: 0,
    };

    tasks.forEach((task) => {
      stats.totalTasks++;
      featureStats.total++;

      if (task.completed) {
        stats.completedTasks++;
        featureStats.completed++;
      } else {
        stats.pendingTasks++;
        featureStats.pending++;
      }

      if (task.subtasks) {
        task.subtasks.forEach((subtask) => {
          stats.totalSubtasks++;
          featureStats.subtasks++;

          if (subtask.completed) {
            stats.completedSubtasks++;
            featureStats.completedSubtasks++;
          }
        });
      }
    });

    stats.byFeature[feature] = featureStats;
  }

  return stats;
}

/**
 * Valida ID de tarefa
 */
function validateTaskId(taskId) {
  if (!taskId) {
    throw new Error("ID da tarefa é obrigatório");
  }

  if (!taskId.includes("-")) {
    throw new Error("ID da tarefa deve estar no formato: feature-X.Y");
  }

  return true;
}

/**
 * Gera relatório em markdown
 */
async function generateMarkdownReport(tasksData, outputPath) {
  const stats = getTasksStats(tasksData);
  const lastUpdated = formatDate(tasksData.lastUpdated);

  let markdown = `# Relatório de Tarefas .kiro\n\n`;
  markdown += `**Última atualização:** ${lastUpdated}\n\n`;

  markdown += `## 📊 Resumo Geral\n\n`;
  markdown += `- **Features:** ${stats.totalFeatures}\n`;
  markdown += `- **Tarefas:** ${stats.completedTasks}/${stats.totalTasks} concluídas\n`;
  markdown += `- **Progresso:** ${Math.round(
    (stats.completedTasks / stats.totalTasks) * 100
  )}%\n\n`;

  markdown += `## 📋 Por Feature\n\n`;

  for (const [feature, featureStats] of Object.entries(stats.byFeature)) {
    const percentage = Math.round(
      (featureStats.completed / featureStats.total) * 100
    );
    markdown += `### ${feature}\n\n`;
    markdown += `- **Progresso:** ${featureStats.completed}/${featureStats.total} (${percentage}%)\n`;
    markdown += `- **Subtarefas:** ${featureStats.completedSubtasks}/${featureStats.subtasks}\n\n`;
  }

  if (outputPath) {
    await fs.writeFile(outputPath, markdown);
    console.log(`📄 Relatório salvo em: ${outputPath}`);
  }

  return markdown;
}

/**
 * === FUNÇÕES RELACIONADAS A PATTERNS ===
 */

/**
 * Verifica se a pasta patterns existe
 */
async function patternsExists() {
  try {
    const patternsPath = path.join(__dirname, "../patterns");
    await fs.access(patternsPath);
    return true;
  } catch {
    return false;
  }
}

/**
 * Lê arquivos de patterns para contexto
 */
async function readPatternsContext() {
  const patternsPath = path.join(__dirname, "../patterns");
  const context = {
    hasPatterns: false,
    conventions: null,
    typescript: null,
    frontend: null,
    backend: null,
    examples: null,
  };

  if (!(await patternsExists())) {
    return context;
  }

  context.hasPatterns = true;

  try {
    // Ler conventions.md
    const conventionsPath = path.join(patternsPath, "conventions.md");
    if (await fileExists(conventionsPath)) {
      context.conventions = await fs.readFile(conventionsPath, "utf8");
    }

    // Ler typescript.md
    const typescriptPath = path.join(patternsPath, "typescript.md");
    if (await fileExists(typescriptPath)) {
      context.typescript = await fs.readFile(typescriptPath, "utf8");
    }

    // Ler frontend patterns
    const frontendPath = path.join(patternsPath, "frontend");
    if (await directoryExists(frontendPath)) {
      const frontendFiles = await fs.readdir(frontendPath);
      context.frontend = {};
      for (const file of frontendFiles) {
        if (file.endsWith(".md")) {
          const content = await fs.readFile(
            path.join(frontendPath, file),
            "utf8"
          );
          context.frontend[file.replace(".md", "")] = content;
        }
      }
    }

    // Ler backend patterns
    const backendPath = path.join(patternsPath, "backend");
    if (await directoryExists(backendPath)) {
      const backendFiles = await fs.readdir(backendPath);
      context.backend = {};
      for (const file of backendFiles) {
        if (file.endsWith(".md")) {
          const content = await fs.readFile(
            path.join(backendPath, file),
            "utf8"
          );
          context.backend[file.replace(".md", "")] = content;
        }
      }
    }

    // Verificar se há exemplos
    const examplesPath = path.join(patternsPath, "examples");
    if (await directoryExists(examplesPath)) {
      const exampleFiles = await fs.readdir(examplesPath, { recursive: true });
      context.examples = exampleFiles.length;
    }
  } catch (error) {
    console.warn(`⚠️  Erro ao ler patterns: ${error.message}`);
  }

  return context;
}

/**
 * Gera resumo de patterns para relatórios
 */
function generatePatternsReport(patternsContext) {
  if (!patternsContext.hasPatterns) {
    return "📐 **Patterns:** Não configurados";
  }

  let report = "📐 **Patterns de Código:**\n";

  if (patternsContext.conventions) {
    report += "- ✅ Convenções definidas\n";
  }

  if (patternsContext.typescript) {
    report += "- ✅ Padrões TypeScript configurados\n";
  }

  if (
    patternsContext.frontend &&
    Object.keys(patternsContext.frontend).length > 0
  ) {
    const frontendCount = Object.keys(patternsContext.frontend).length;
    report += `- ✅ ${frontendCount} padrão(ões) de frontend\n`;
  }

  if (
    patternsContext.backend &&
    Object.keys(patternsContext.backend).length > 0
  ) {
    const backendCount = Object.keys(patternsContext.backend).length;
    report += `- ✅ ${backendCount} padrão(ões) de backend\n`;
  }

  if (patternsContext.examples) {
    report += `- ✅ ${patternsContext.examples} exemplo(s) práticos\n`;
  }

  return report;
}

/**
 * Funções de validação de nomenclatura
 */
function isPascalCase(str) {
  return /^[A-Z][a-zA-Z0-9]*$/.test(str);
}

function isCamelCase(str) {
  return /^[a-z][a-zA-Z0-9]*$/.test(str);
}

function isKebabCase(str) {
  return /^[a-z][a-z0-9-]*$/.test(str);
}

function isSnakeCase(str) {
  return /^[a-z][a-z0-9_]*$/.test(str);
}

function isUpperSnakeCase(str) {
  return /^[A-Z][A-Z0-9_]*$/.test(str);
}

/**
 * Verifica se arquivo existe
 */
async function fileExists(filePath) {
  try {
    await fs.access(filePath);
    return true;
  } catch {
    return false;
  }
}

/**
 * Verifica se diretório existe
 */
async function directoryExists(dirPath) {
  try {
    const stat = await fs.stat(dirPath);
    return stat.isDirectory();
  } catch {
    return false;
  }
}

/**
 * Obtém todos os arquivos de um diretório recursivamente
 */
async function getAllFiles(
  dirPath,
  extensions = [".js", ".ts", ".jsx", ".tsx"]
) {
  const files = [];

  async function walkDir(currentPath) {
    try {
      const entries = await fs.readdir(currentPath, { withFileTypes: true });

      for (const entry of entries) {
        const fullPath = path.join(currentPath, entry.name);

        if (entry.isDirectory()) {
          await walkDir(fullPath);
        } else if (entry.isFile()) {
          const ext = path.extname(entry.name);
          if (extensions.length === 0 || extensions.includes(ext)) {
            files.push(fullPath);
          }
        }
      }
    } catch (error) {
      // Ignorar diretórios que não podem ser lidos
    }
  }

  if (await directoryExists(dirPath)) {
    await walkDir(dirPath);
  }

  return files;
}

module.exports = {
  loadTasksJson,
  saveTasksJson,
  displayTasksTable,
  createProgressBar,
  formatDate,
  findTaskById,
  getTasksStats,
  validateTaskId,
  generateMarkdownReport,
  TASKS_JSON_PATH,
  // Funções de patterns
  patternsExists,
  readPatternsContext,
  generatePatternsReport,
  isPascalCase,
  isCamelCase,
  isKebabCase,
  isSnakeCase,
  isUpperSnakeCase,
  fileExists,
  directoryExists,
  getAllFiles,
};
