#!/bin/bash
echo "🖥️ Verificando recursos do sistema..."
echo "CPU:" && sysctl -n hw.ncpu
echo "RAM:" && vm_stat | grep "Pages free" | awk "{print \$3 * 4096 / 1024 / 1024 / 1024 \" GB\"}"
echo "Disco:" && df -h / | tail -1
