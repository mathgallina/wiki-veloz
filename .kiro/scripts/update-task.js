const fs = require("fs").promises;
const path = require("path");
const { loadTasksJson } = require("./utils");

/**
 * Atualiza o status de uma tarefa específica
 */
async function updateTaskStatus(taskId, completed = true) {
  try {
    const tasksData = await loadTasksJson();

    // Encontra a tarefa
    let targetTask = null;
    let targetFeature = null;

    for (const [feature, tasks] of Object.entries(tasksData.tasks)) {
      const task = tasks.find((t) => t.id === taskId);
      if (task) {
        targetTask = task;
        targetFeature = feature;
        break;
      }
    }

    if (!targetTask) {
      return {
        success: false,
        error: `Tarefa ${taskId} não encontrada`,
      };
    }

    // Atualiza o arquivo tasks.md
    const tasksFile = path.join(
      __dirname,
      "../specs",
      targetFeature,
      "tasks.md"
    );
    const success = await updateTaskInFile(tasksFile, targetTask, completed);

    if (success) {
      return {
        success: true,
        feature: targetFeature,
        task: targetTask,
      };
    } else {
      return {
        success: false,
        error: "Falha ao atualizar arquivo",
      };
    }
  } catch (error) {
    return {
      success: false,
      error: error.message,
    };
  }
}

/**
 * Atualiza uma tarefa específica no arquivo
 */
async function updateTaskInFile(filePath, task, completed) {
  try {
    const content = await fs.readFile(filePath, "utf8");
    const lines = content.split("\n");

    let updated = false;

    // Encontra e atualiza a linha da tarefa
    for (let i = 0; i < lines.length; i++) {
      const line = lines[i];

      // Verifica se é a linha da tarefa (usando o número da linha ou padrão)
      if (i + 1 === task.lineNumber || isTaskLine(line, task)) {
        const newStatus = completed ? "x" : " ";
        lines[i] = line.replace(/^(\s*-\s+)\[([ x])\]/, `$1[${newStatus}]`);
        updated = true;

        // Se marcando como concluída, marca todas as subtarefas também
        if (completed && task.subtasks && task.subtasks.length > 0) {
          let j = i + 1;
          while (j < lines.length && isSubtaskLine(lines[j])) {
            lines[j] = lines[j].replace(/^(\s+-\s+)\[([ x])\]/, `$1[x]`);
            j++;
          }
        }
        break;
      }
    }

    if (updated) {
      await fs.writeFile(filePath, lines.join("\n"));
      return true;
    }

    return false;
  } catch (error) {
    console.error("Erro ao atualizar arquivo:", error);
    return false;
  }
}

/**
 * Verifica se uma linha corresponde à tarefa
 */
function isTaskLine(line, task) {
  // Verifica se a linha contém a descrição da tarefa
  const taskMatch = line.match(/^-\s+\[([ x])\]\s+(.+)/);
  if (!taskMatch) return false;

  const lineDesc = taskMatch[2].trim();

  // Verifica se a descrição bate
  return (
    lineDesc.includes(task.description) ||
    lineDesc.includes(task.id.split("-").slice(1).join("."))
  );
}

/**
 * Verifica se uma linha é uma subtarefa
 */
function isSubtaskLine(line) {
  return line.match(/^\s+-\s+\[([ x])\]\s+/) && line.startsWith("  ");
}

/**
 * Marca todas as subtarefas de uma tarefa como concluídas
 */
async function completeAllSubtasks(taskId) {
  const tasksData = await loadTasksJson();

  for (const [feature, tasks] of Object.entries(tasksData.tasks)) {
    const task = tasks.find((t) => t.id === taskId);
    if (task && task.subtasks) {
      const tasksFile = path.join(__dirname, "../specs", feature, "tasks.md");

      for (const subtask of task.subtasks) {
        await updateSubtaskInFile(tasksFile, subtask, true);
      }
      break;
    }
  }
}

/**
 * Atualiza uma subtarefa específica no arquivo
 */
async function updateSubtaskInFile(filePath, subtask, completed) {
  try {
    const content = await fs.readFile(filePath, "utf8");
    const lines = content.split("\n");

    // Encontra a linha da subtarefa
    for (let i = 0; i < lines.length; i++) {
      if (i + 1 === subtask.lineNumber) {
        const newStatus = completed ? "x" : " ";
        lines[i] = lines[i].replace(/^(\s+-\s+)\[([ x])\]/, `$1[${newStatus}]`);
        break;
      }
    }

    await fs.writeFile(filePath, lines.join("\n"));
    return true;
  } catch (error) {
    console.error("Erro ao atualizar subtarefa:", error);
    return false;
  }
}

module.exports = {
  updateTaskStatus,
  updateTaskInFile,
  completeAllSubtasks,
};
