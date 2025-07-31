#!/usr/bin/env node

/**
 * Check Patterns - Validador de Conformidade com Padrões .kiro
 *
 * Usage:
 *   node check-patterns.js              # Verificação completa
 *   node check-patterns.js --naming     # Apenas nomenclatura
 *   node check-patterns.js --imports    # Apenas imports
 *   node check-patterns.js --fix        # Corrigir problemas automaticamente
 */

const {
  readPatternsContext,
  getAllFiles,
  isPascalCase,
  isCamelCase,
  isKebabCase,
  fileExists,
} = require("./utils");

const fs = require("fs").promises;
const path = require("path");

/**
 * Executa todas as verificações de patterns
 */
async function main() {
  const args = process.argv.slice(2);

  console.log("🔍 Verificando conformidade com padrões de código...\n");

  try {
    const patternsContext = await readPatternsContext();

    if (!patternsContext.hasPatterns) {
      console.log("⚠️  Padrões não configurados");
      console.log("📝 Execute: docs/patterns-prompt-direto.md");
      process.exit(1);
    }

    let hasViolations = false;

    // Verificações específicas baseadas em argumentos
    if (args.includes("--naming") || args.length === 0) {
      hasViolations = (await checkNamingConventions()) || hasViolations;
    }

    if (args.includes("--imports") || args.length === 0) {
      hasViolations = (await checkImportOrder()) || hasViolations;
    }

    if (args.includes("--types") || args.length === 0) {
      hasViolations = (await checkTypeScriptPatterns()) || hasViolations;
    }

    if (hasViolations) {
      console.log("\n❌ Violações de padrões encontradas!");
      console.log("💡 Consulte .kiro/patterns/ para corrigir");
      if (!args.includes("--fix")) {
        console.log("🔧 Use --fix para corrigir automaticamente onde possível");
      }
      process.exit(1);
    } else {
      console.log("\n✅ Todos os padrões estão sendo seguidos!");
      console.log("🎉 Código em conformidade com .kiro/patterns/");
    }
  } catch (error) {
    console.error("❌ Erro na verificação:", error.message);
    process.exit(1);
  }
}

/**
 * Verifica convenções de nomenclatura
 */
async function checkNamingConventions() {
  console.log("📝 Verificando convenções de nomenclatura...");

  const srcFiles = await getAllFiles("./src");
  const violations = [];

  for (const file of srcFiles) {
    const fileName = path.basename(file);
    const relativePath = path.relative(".", file);

    // Componentes React devem ser PascalCase
    if (file.includes("/components/") && fileName.endsWith(".tsx")) {
      const componentName = fileName.replace(".tsx", "");
      if (!isPascalCase(componentName)) {
        violations.push({
          file: relativePath,
          issue: `Componente deve usar PascalCase: ${componentName}`,
          suggestion: `Renomear para ${toPascalCase(componentName)}.tsx`,
        });
      }
    }

    // Services devem ser kebab-case
    if (file.includes("/services/") && fileName.endsWith(".ts")) {
      const serviceName = fileName.replace(".ts", "");
      if (!isKebabCase(serviceName) && !serviceName.includes(".service")) {
        violations.push({
          file: relativePath,
          issue: `Service deve usar kebab-case: ${serviceName}`,
          suggestion: `Renomear para ${toKebabCase(serviceName)}.ts`,
        });
      }
    }

    // Utils/helpers devem ser camelCase
    if (
      (file.includes("/utils/") || file.includes("/helpers/")) &&
      fileName.endsWith(".ts")
    ) {
      const utilName = fileName.replace(".ts", "");
      if (!isCamelCase(utilName) && !isKebabCase(utilName)) {
        violations.push({
          file: relativePath,
          issue: `Utility deve usar camelCase ou kebab-case: ${utilName}`,
          suggestion: `Renomear para ${toCamelCase(utilName)}.ts`,
        });
      }
    }
  }

  if (violations.length > 0) {
    console.log(`❌ ${violations.length} violação(ões) de nomenclatura:`);
    violations.forEach((v) => {
      console.log(`  • ${v.file}: ${v.issue}`);
      console.log(`    💡 ${v.suggestion}`);
    });
    return true;
  } else {
    console.log("✅ Nomenclatura conforme padrões");
    return false;
  }
}

/**
 * Verifica ordem de imports
 */
async function checkImportOrder() {
  console.log("📦 Verificando ordem de imports...");

  const tsFiles = await getAllFiles("./src", [".ts", ".tsx"]);
  const violations = [];

  for (const file of tsFiles) {
    try {
      const content = await fs.readFile(file, "utf8");
      const lines = content.split("\n");

      const imports = [];
      let importStarted = false;

      for (let i = 0; i < lines.length; i++) {
        const line = lines[i].trim();

        if (line.startsWith("import ")) {
          importStarted = true;
          imports.push({
            line: i + 1,
            content: line,
            type: getImportType(line),
          });
        } else if (importStarted && line && !line.startsWith("//")) {
          break; // Fim dos imports
        }
      }

      // Verificar se imports estão ordenados
      for (let i = 1; i < imports.length; i++) {
        if (imports[i].type < imports[i - 1].type) {
          violations.push({
            file: path.relative(".", file),
            line: imports[i].line,
            issue: "Imports fora de ordem",
            suggestion: "Organize: external → internal → components → types",
          });
          break; // Uma violação por arquivo é suficiente
        }
      }
    } catch (error) {
      // Ignorar arquivos que não podem ser lidos
    }
  }

  if (violations.length > 0) {
    console.log(`❌ ${violations.length} violação(ões) de ordem de imports:`);
    violations.forEach((v) => {
      console.log(`  • ${v.file}:${v.line} - ${v.issue}`);
      console.log(`    💡 ${v.suggestion}`);
    });
    return true;
  } else {
    console.log("✅ Imports organizados conforme padrões");
    return false;
  }
}

/**
 * Verifica padrões TypeScript
 */
async function checkTypeScriptPatterns() {
  console.log("🔷 Verificando padrões TypeScript...");

  const tsFiles = await getAllFiles("./src", [".ts", ".tsx"]);
  const violations = [];

  for (const file of tsFiles) {
    try {
      const content = await fs.readFile(file, "utf8");

      // Verificar uso de 'any'
      const anyMatches = content.match(/:\s*any\b/g);
      if (anyMatches) {
        violations.push({
          file: path.relative(".", file),
          issue: `Uso de 'any' encontrado (${anyMatches.length} ocorrência(s))`,
          suggestion: "Substitua por tipos específicos",
        });
      }

      // Verificar @ts-ignore sem comentário
      const ignoreMatches = content.match(/@ts-ignore(?!\s*-)/g);
      if (ignoreMatches) {
        violations.push({
          file: path.relative(".", file),
          issue: `@ts-ignore sem explicação (${ignoreMatches.length} ocorrência(s))`,
          suggestion: "Adicione comentário explicativo após @ts-ignore",
        });
      }
    } catch (error) {
      // Ignorar arquivos que não podem ser lidos
    }
  }

  if (violations.length > 0) {
    console.log(`❌ ${violations.length} violação(ões) de TypeScript:`);
    violations.forEach((v) => {
      console.log(`  • ${v.file}: ${v.issue}`);
      console.log(`    💡 ${v.suggestion}`);
    });
    return true;
  } else {
    console.log("✅ Padrões TypeScript seguidos");
    return false;
  }
}

/**
 * Determina o tipo de import
 */
function getImportType(importLine) {
  if (
    importLine.includes("from 'react'") ||
    importLine.includes('from "react"')
  )
    return 1;
  if (importLine.includes("from '@") || importLine.includes('from "@'))
    return 1; // external
  if (
    importLine.includes("from '@/services") ||
    importLine.includes("from '@/utils") ||
    importLine.includes("from '@/lib")
  )
    return 2; // internal
  if (importLine.includes("from '@/components")) return 3; // components
  if (importLine.includes("type ")) return 4; // types
  return 1; // default external
}

/**
 * Utilitários de conversão de nomenclatura
 */
function toPascalCase(str) {
  return str.replace(/(?:^|[_-])([a-z])/g, (_, letter) => letter.toUpperCase());
}

function toCamelCase(str) {
  const pascal = toPascalCase(str);
  return pascal.charAt(0).toLowerCase() + pascal.slice(1);
}

function toKebabCase(str) {
  return str
    .replace(/[A-Z]/g, (letter) => `-${letter.toLowerCase()}`)
    .replace(/^-/, "");
}

if (require.main === module) {
  main();
}

module.exports = {
  checkNamingConventions,
  checkImportOrder,
  checkTypeScriptPatterns,
};
