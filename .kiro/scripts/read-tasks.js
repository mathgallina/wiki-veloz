const fs = require("fs").promises;
const path = require("path");

/**
 * Lê todas as tarefas de todos os arquivos tasks.md nas specs
 */
async function readAllTasks() {
  const specsDir = path.join(__dirname, "../specs");
  const tasksData = {
    lastUpdated: new Date().toISOString(),
    tasks: {},
  };

  try {
    const features = await getFeatureDirectories(specsDir);

    for (const feature of features) {
      if (feature === "_template") continue; // Pula o template

      const tasksFile = path.join(specsDir, feature, "tasks.md");

      if (await fileExists(tasksFile)) {
        const tasks = await parseTasksFile(tasksFile, feature);
        if (tasks.length > 0) {
          tasksData.tasks[feature] = tasks;
        }
      }
    }

    return tasksData;
  } catch (error) {
    throw new Error(`Erro ao ler tarefas: ${error.message}`);
  }
}

/**
 * Obtém lista de diretórios de features
 */
async function getFeatureDirectories(specsDir) {
  try {
    const items = await fs.readdir(specsDir, { withFileTypes: true });
    return items.filter((item) => item.isDirectory()).map((item) => item.name);
  } catch (error) {
    if (error.code === "ENOENT") {
      throw new Error("Diretório .kiro/specs não encontrado");
    }
    throw error;
  }
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
 * Faz parse de um arquivo tasks.md
 */
async function parseTasksFile(filePath, feature) {
  const content = await fs.readFile(filePath, "utf8");
  const tasks = [];

  const lines = content.split("\n");
  let currentPhase = null;
  let taskCounter = 1;

  for (let i = 0; i < lines.length; i++) {
    const line = lines[i].trim();

    // Detecta fases (### Phase X:)
    const phaseMatch = line.match(/^###\s+(.*?):/);
    if (phaseMatch) {
      currentPhase = phaseMatch[1].trim();
      continue;
    }

    // Detecta tarefas principais (- [ ] ou - [x])
    const mainTaskMatch = line.match(/^-\s+\[([ x])\]\s+(.+)/);
    if (mainTaskMatch) {
      const completed = mainTaskMatch[1] === "x";
      const description = mainTaskMatch[2].trim();

      // Extrai ID da tarefa (ex: "1.1 Configurar...")
      const taskIdMatch = description.match(/^(\d+\.\d+)\s+(.+)/);
      const taskId = taskIdMatch
        ? `${feature}-${taskIdMatch[1]}`
        : `${feature}-${taskCounter}`;
      const taskDesc = taskIdMatch ? taskIdMatch[2] : description;

      const task = {
        id: taskId,
        description: taskDesc,
        completed,
        phase: currentPhase,
        file: path.basename(filePath),
        lineNumber: i + 1,
        subtasks: [],
      };

      // Lê subtarefas (  - [ ] ou  - [x])
      let j = i + 1;
      while (j < lines.length) {
        const subtaskLine = lines[j].trim();
        const subtaskMatch = subtaskLine.match(/^-\s+\[([ x])\]\s+(.+)/);

        if (subtaskMatch && lines[j].startsWith("  ")) {
          const subtaskCompleted = subtaskMatch[1] === "x";
          const subtaskDesc = subtaskMatch[2].trim();

          task.subtasks.push({
            description: subtaskDesc,
            completed: subtaskCompleted,
            lineNumber: j + 1,
          });
          j++;
        } else if (
          subtaskLine.startsWith("_Requirements:") ||
          subtaskLine.startsWith("_Estimated:")
        ) {
          // Pula linhas de metadata
          j++;
        } else if (subtaskLine.length === 0) {
          // Pula linhas vazias
          j++;
        } else {
          // Para se encontrar algo que não é subtask
          break;
        }
      }

      tasks.push(task);
      taskCounter++;
      i = j - 1; // Ajusta o loop principal
    }
  }

  return tasks;
}

/**
 * Atualiza o arquivo JSON com os dados das tarefas
 */
async function updateTasksJson(tasksData) {
  const jsonPath = path.join(__dirname, "tasks-status.json");
  await fs.writeFile(jsonPath, JSON.stringify(tasksData, null, 2));
}

module.exports = {
  readAllTasks,
  updateTasksJson,
  parseTasksFile,
  getFeatureDirectories,
};
