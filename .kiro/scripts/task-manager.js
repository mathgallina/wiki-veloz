#!/usr/bin/env node

const fs = require('fs');
const path = require('path');
const { execSync } = require('child_process');

class TaskManager {
  constructor() {
    this.specsDir = path.join(__dirname, '../specs');
    this.statusFile = path.join(__dirname, 'tasks-status.json');
  }

  scan() {
    console.log('🔍 Scanning for tasks...');
    const features = this.getFeatures();
    const allTasks = [];

    features.forEach(feature => {
      const tasks = this.extractTasks(feature);
      allTasks.push(...tasks);
    });

    this.saveStatus(allTasks);
    console.log(`✅ Found ${allTasks.length} tasks across ${features.length} features`);
  }

  getFeatures() {
    return fs
      .readdirSync(this.specsDir)
      .filter(dir => dir !== '_template')
      .filter(dir => fs.statSync(path.join(this.specsDir, dir)).isDirectory());
  }

  extractTasks(featureName) {
    const tasksFile = path.join(this.specsDir, featureName, 'tasks.md');
    if (!fs.existsSync(tasksFile)) return [];

    const content = fs.readFileSync(tasksFile, 'utf8');
    const tasks = [];

    // Extract tasks with pattern: - [ ] X.Y Description
    const taskRegex = /^-\s\[([x ])\]\s+(\d+\.\d+)\s+(.+)$/gm;
    let match;

    while ((match = taskRegex.exec(content)) !== null) {
      const [, status, number, description] = match;
      const taskId = `${featureName}-${number}`;

      tasks.push({
        id: taskId,
        feature: featureName,
        number: number,
        description: description.trim(),
        completed: status === 'x',
        file: tasksFile,
      });
    }

    return tasks;
  }

  saveStatus(tasks) {
    const status = {
      lastUpdate: new Date().toISOString(),
      tasks: tasks,
      summary: {
        total: tasks.length,
        completed: tasks.filter(t => t.completed).length,
        pending: tasks.filter(t => !t.completed).length,
      },
    };

    fs.writeFileSync(this.statusFile, JSON.stringify(status, null, 2));
  }

  list(featureName = null) {
    const status = this.loadStatus();
    if (!status) {
      console.log('❌ No tasks found. Run: npm run scan');
      return;
    }

    let tasks = status.tasks;
    if (featureName) {
      tasks = tasks.filter(t => t.feature === featureName);
    }

    console.log(`\n📋 Tasks ${featureName ? `for ${featureName}` : '(all features)'}`);
    console.log('='.repeat(50));

    const features = [...new Set(tasks.map(t => t.feature))];

    features.forEach(feature => {
      const featureTasks = tasks.filter(t => t.feature === feature);
      console.log(`\n🎯 ${feature}:`);

      featureTasks.forEach(task => {
        const status = task.completed ? '✅' : '⏸️';
        console.log(`  ${status} ${task.id}: ${task.description}`);
      });
    });

    this.showSummary(tasks);
  }

  complete(taskId) {
    if (!taskId) {
      console.log('❌ Usage: npm run complete <task-id>');
      console.log('   Example: npm run complete user-auth-1.1');
      return;
    }

    const status = this.loadStatus();
    if (!status) {
      console.log('❌ No tasks found. Run: npm run scan');
      return;
    }

    const task = status.tasks.find(t => t.id === taskId);
    if (!task) {
      console.log(`❌ Task not found: ${taskId}`);
      this.suggestSimilarTasks(taskId, status.tasks);
      return;
    }

    if (task.completed) {
      console.log(`⚠️  Task already completed: ${taskId}`);
      return;
    }

    // Update file
    this.markTaskComplete(task);

    // Update status
    task.completed = true;
    status.lastUpdate = new Date().toISOString();
    status.summary.completed++;
    status.summary.pending--;

    this.saveStatus(status.tasks);

    console.log(`✅ Task completed: ${taskId}`);
    console.log(
      `📊 Progress: ${status.summary.completed}/${status.summary.total} (${Math.round((status.summary.completed / status.summary.total) * 100)}%)`
    );
  }

  markTaskComplete(task) {
    const content = fs.readFileSync(task.file, 'utf8');
    const pattern = new RegExp(
      `^(-\\s\\[)( )(\\]\\s+${task.number.replace('.', '\\.')})`,
      'gm'
    );
    const updated = content.replace(pattern, '$1x$3');
    fs.writeFileSync(task.file, updated);
  }

  status() {
    const status = this.loadStatus();
    if (!status) {
      console.log('❌ No tasks found. Run: npm run scan');
      return;
    }

    console.log('\n📊 PROJECT STATUS');
    console.log('='.repeat(30));
    console.log(`Total Tasks: ${status.summary.total}`);
    console.log(`Completed: ${status.summary.completed}`);
    console.log(`Pending: ${status.summary.pending}`);
    console.log(
      `Progress: ${Math.round((status.summary.completed / status.summary.total) * 100)}%`
    );
    console.log(`Last Update: ${new Date(status.lastUpdate).toLocaleString()}`);

    // Show by feature
    const features = [...new Set(status.tasks.map(t => t.feature))];

    console.log('\n🎯 By Feature:');
    features.forEach(feature => {
      const featureTasks = status.tasks.filter(t => t.feature === feature);
      const completed = featureTasks.filter(t => t.completed).length;
      const progress = Math.round((completed / featureTasks.length) * 100);
      console.log(`  ${feature}: ${completed}/${featureTasks.length} (${progress}%)`);
    });
  }

  watch() {
    console.log('👀 Watching for task file changes...');
    console.log('Press Ctrl+C to stop');

    const chokidar = require('chokidar');
    const watcher = chokidar.watch(`${this.specsDir}/**/tasks.md`, {
      ignored: /node_modules/,
      persistent: true,
    });

    watcher.on('change', path => {
      console.log(`\n📝 File changed: ${path}`);
      console.log('🔄 Rescanning tasks...');
      this.scan();
      this.status();
    });
  }

  loadStatus() {
    if (!fs.existsSync(this.statusFile)) return null;
    return JSON.parse(fs.readFileSync(this.statusFile, 'utf8'));
  }

  showSummary(tasks) {
    const completed = tasks.filter(t => t.completed).length;
    const progress = Math.round((completed / tasks.length) * 100);

    console.log('\n📊 Summary:');
    console.log(`Total: ${tasks.length} tasks`);
    console.log(`Completed: ${completed} tasks`);
    console.log(`Progress: ${progress}%`);
  }

  suggestSimilarTasks(taskId, tasks) {
    const similar = tasks
      .filter(t => t.id.includes(taskId.split('-')[0]) || taskId.includes(t.feature))
      .slice(0, 3);

    if (similar.length > 0) {
      console.log('\n💡 Similar tasks:');
      similar.forEach(t => console.log(`  - ${t.id}: ${t.description}`));
    }
  }
}

// CLI Interface
const manager = new TaskManager();
const command = process.argv[2];
const arg = process.argv[3];

switch (command) {
  case 'scan':
    manager.scan();
    break;
  case 'list':
    manager.list(arg);
    break;
  case 'status':
    manager.status();
    break;
  case 'complete':
    manager.complete(arg);
    break;
  case 'watch':
    manager.watch();
    break;
  default:
    console.log('Available commands:');
    console.log('  scan     - Scan for tasks');
    console.log('  list     - List all tasks');
    console.log('  status   - Show project status');
    console.log('  complete - Mark task as complete');
    console.log('  watch    - Watch for changes');
}
