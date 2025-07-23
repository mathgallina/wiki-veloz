# Padrões PostgreSQL - CDD v2.0

## Estrutura de Banco de Dados

### Convenções de Nomenclatura

#### Tabelas

- **Nomes**: `snake_case` (ex: `user_profiles`, `order_items`)
- **Plural**: Sempre use plural para tabelas
- **Prefixo**: Evite prefixos desnecessários

#### Colunas

- **Nomes**: `snake_case` (ex: `created_at`, `user_id`)
- **Timestamps**: Sempre inclua `created_at` e `updated_at`
- **IDs**: Use `id` como chave primária, `table_id` para foreign keys

#### Índices

- **Nomes**: `idx_table_column` (ex: `idx_users_email`)
- **Únicos**: `unq_table_column` (ex: `unq_users_email`)

## Esquemas de Tabelas

### Tabela de Usuários

```sql
-- users.sql
CREATE TABLE users (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  email VARCHAR(255) NOT NULL UNIQUE,
  password_hash VARCHAR(255) NOT NULL,
  first_name VARCHAR(100) NOT NULL,
  last_name VARCHAR(100) NOT NULL,
  is_active BOOLEAN DEFAULT true,
  email_verified BOOLEAN DEFAULT false,
  created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
  updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Índices
CREATE INDEX idx_users_email ON users(email);
CREATE INDEX idx_users_created_at ON users(created_at);
CREATE INDEX idx_users_is_active ON users(is_active);

-- Trigger para updated_at
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
  NEW.updated_at = NOW();
  RETURN NEW;
END;
$$ language 'plpgsql';

CREATE TRIGGER update_users_updated_at
  BEFORE UPDATE ON users
  FOR EACH ROW
  EXECUTE FUNCTION update_updated_at_column();
```

### Tabela de Produtos

```sql
-- products.sql
CREATE TABLE products (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  name VARCHAR(255) NOT NULL,
  description TEXT,
  price DECIMAL(10,2) NOT NULL CHECK (price >= 0),
  stock_quantity INTEGER NOT NULL DEFAULT 0 CHECK (stock_quantity >= 0),
  category_id UUID REFERENCES categories(id),
  is_active BOOLEAN DEFAULT true,
  created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
  updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Índices
CREATE INDEX idx_products_category_id ON products(category_id);
CREATE INDEX idx_products_price ON products(price);
CREATE INDEX idx_products_stock_quantity ON products(stock_quantity);
CREATE INDEX idx_products_is_active ON products(is_active);

-- Trigger para updated_at
CREATE TRIGGER update_products_updated_at
  BEFORE UPDATE ON products
  FOR EACH ROW
  EXECUTE FUNCTION update_updated_at_column();
```

### Tabela de Pedidos

```sql
-- orders.sql
CREATE TABLE orders (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  user_id UUID NOT NULL REFERENCES users(id),
  status order_status NOT NULL DEFAULT 'pending',
  total_amount DECIMAL(10,2) NOT NULL CHECK (total_amount >= 0),
  shipping_address JSONB NOT NULL,
  billing_address JSONB NOT NULL,
  notes TEXT,
  created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
  updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Enum para status
CREATE TYPE order_status AS ENUM (
  'pending',
  'confirmed',
  'processing',
  'shipped',
  'delivered',
  'cancelled'
);

-- Índices
CREATE INDEX idx_orders_user_id ON orders(user_id);
CREATE INDEX idx_orders_status ON orders(status);
CREATE INDEX idx_orders_created_at ON orders(created_at);

-- Trigger para updated_at
CREATE TRIGGER update_orders_updated_at
  BEFORE UPDATE ON orders
  FOR EACH ROW
  EXECUTE FUNCTION update_updated_at_column();
```

## Padrões de Queries

### Repository Pattern

```typescript
// repositories/UserRepository.ts
import { Pool } from 'pg';
import { User } from '../types/User';
import { CreateUserDto } from '../types/CreateUserDto';

export class UserRepository {
  private pool: Pool;

  constructor(pool: Pool) {
    this.pool = pool;
  }

  async create(userData: CreateUserDto): Promise<User> {
    const query = `
      INSERT INTO users (email, password_hash, first_name, last_name)
      VALUES ($1, $2, $3, $4)
      RETURNING *
    `;

    const values = [
      userData.email,
      userData.passwordHash,
      userData.firstName,
      userData.lastName,
    ];

    const result = await this.pool.query(query, values);
    return result.rows[0];
  }

  async findById(id: string): Promise<User | null> {
    const query = `
      SELECT * FROM users 
      WHERE id = $1 AND is_active = true
    `;

    const result = await this.pool.query(query, [id]);
    return result.rows[0] || null;
  }

  async findByEmail(email: string): Promise<User | null> {
    const query = `
      SELECT * FROM users 
      WHERE email = $1 AND is_active = true
    `;

    const result = await this.pool.query(query, [email]);
    return result.rows[0] || null;
  }

  async update(id: string, updateData: Partial<User>): Promise<User> {
    const fields = Object.keys(updateData);
    const values = Object.values(updateData);

    const setClause = fields
      .map((field, index) => `${field} = $${index + 2}`)
      .join(', ');

    const query = `
      UPDATE users 
      SET ${setClause}, updated_at = NOW()
      WHERE id = $1 AND is_active = true
      RETURNING *
    `;

    const result = await this.pool.query(query, [id, ...values]);
    return result.rows[0];
  }

  async delete(id: string): Promise<void> {
    const query = `
      UPDATE users 
      SET is_active = false, updated_at = NOW()
      WHERE id = $1
    `;

    await this.pool.query(query, [id]);
  }

  async findAll(limit = 10, offset = 0): Promise<User[]> {
    const query = `
      SELECT * FROM users 
      WHERE is_active = true
      ORDER BY created_at DESC
      LIMIT $1 OFFSET $2
    `;

    const result = await this.pool.query(query, [limit, offset]);
    return result.rows;
  }
}
```

### Query Builder Pattern

```typescript
// utils/QueryBuilder.ts
export class QueryBuilder {
  private query: string = '';
  private values: any[] = [];
  private paramIndex: number = 1;

  select(fields: string[] = ['*']): QueryBuilder {
    this.query = `SELECT ${fields.join(', ')}`;
    return this;
  }

  from(table: string): QueryBuilder {
    this.query += ` FROM ${table}`;
    return this;
  }

  where(condition: string, value?: any): QueryBuilder {
    if (value !== undefined) {
      this.query += ` WHERE ${condition} = $${this.paramIndex}`;
      this.values.push(value);
      this.paramIndex++;
    } else {
      this.query += ` WHERE ${condition}`;
    }
    return this;
  }

  andWhere(condition: string, value?: any): QueryBuilder {
    if (value !== undefined) {
      this.query += ` AND ${condition} = $${this.paramIndex}`;
      this.values.push(value);
      this.paramIndex++;
    } else {
      this.query += ` AND ${condition}`;
    }
    return this;
  }

  orderBy(field: string, direction: 'ASC' | 'DESC' = 'ASC'): QueryBuilder {
    this.query += ` ORDER BY ${field} ${direction}`;
    return this;
  }

  limit(limit: number): QueryBuilder {
    this.query += ` LIMIT $${this.paramIndex}`;
    this.values.push(limit);
    this.paramIndex++;
    return this;
  }

  offset(offset: number): QueryBuilder {
    this.query += ` OFFSET $${this.paramIndex}`;
    this.values.push(offset);
    this.paramIndex++;
    return this;
  }

  build(): { query: string; values: any[] } {
    return {
      query: this.query,
      values: this.values,
    };
  }
}
```

## Padrões de Migração

### Migration Template

```typescript
// migrations/001_create_users_table.ts
import { Pool } from 'pg';

export async function up(pool: Pool): Promise<void> {
  await pool.query(`
    CREATE TABLE users (
      id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
      email VARCHAR(255) NOT NULL UNIQUE,
      password_hash VARCHAR(255) NOT NULL,
      first_name VARCHAR(100) NOT NULL,
      last_name VARCHAR(100) NOT NULL,
      is_active BOOLEAN DEFAULT true,
      email_verified BOOLEAN DEFAULT false,
      created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
      updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
    );

    CREATE INDEX idx_users_email ON users(email);
    CREATE INDEX idx_users_created_at ON users(created_at);
    CREATE INDEX idx_users_is_active ON users(is_active);

    CREATE OR REPLACE FUNCTION update_updated_at_column()
    RETURNS TRIGGER AS $$
    BEGIN
      NEW.updated_at = NOW();
      RETURN NEW;
    END;
    $$ language 'plpgsql';

    CREATE TRIGGER update_users_updated_at 
      BEFORE UPDATE ON users 
      FOR EACH ROW 
      EXECUTE FUNCTION update_updated_at_column();
  `);
}

export async function down(pool: Pool): Promise<void> {
  await pool.query(`
    DROP TABLE IF EXISTS users CASCADE;
  `);
}
```

### Migration Runner

```typescript
// utils/MigrationRunner.ts
import { Pool } from 'pg';
import fs from 'fs';
import path from 'path';

export class MigrationRunner {
  private pool: Pool;
  private migrationsPath: string;

  constructor(pool: Pool, migrationsPath: string) {
    this.pool = pool;
    this.migrationsPath = migrationsPath;
  }

  async runMigrations(): Promise<void> {
    const migrationFiles = fs
      .readdirSync(this.migrationsPath)
      .filter(file => file.endsWith('.ts'))
      .sort();

    for (const file of migrationFiles) {
      const migration = require(path.join(this.migrationsPath, file));

      try {
        console.log(`Running migration: ${file}`);
        await migration.up(this.pool);
        console.log(`✅ Migration completed: ${file}`);
      } catch (error) {
        console.error(`❌ Migration failed: ${file}`, error);
        throw error;
      }
    }
  }

  async rollbackMigrations(): Promise<void> {
    const migrationFiles = fs
      .readdirSync(this.migrationsPath)
      .filter(file => file.endsWith('.ts'))
      .sort()
      .reverse();

    for (const file of migrationFiles) {
      const migration = require(path.join(this.migrationsPath, file));

      try {
        console.log(`Rolling back migration: ${file}`);
        await migration.down(this.pool);
        console.log(`✅ Rollback completed: ${file}`);
      } catch (error) {
        console.error(`❌ Rollback failed: ${file}`, error);
        throw error;
      }
    }
  }
}
```

## Padrões de Performance

### Índices Estratégicos

```sql
-- Índices para consultas frequentes
CREATE INDEX idx_orders_user_status ON orders(user_id, status);
CREATE INDEX idx_products_category_price ON products(category_id, price);
CREATE INDEX idx_users_email_active ON users(email, is_active);

-- Índices para ordenação
CREATE INDEX idx_orders_created_desc ON orders(created_at DESC);
CREATE INDEX idx_products_name_asc ON products(name ASC);

-- Índices parciais
CREATE INDEX idx_active_products ON products(id) WHERE is_active = true;
CREATE INDEX idx_verified_users ON users(id) WHERE email_verified = true;
```

### Query Optimization

```typescript
// Otimização de queries com paginação
async findProductsWithPagination(
  categoryId?: string,
  minPrice?: number,
  maxPrice?: number,
  limit = 20,
  offset = 0
): Promise<{ products: Product[]; total: number }> {
  const conditions: string[] = ['is_active = true'];
  const values: any[] = [];
  let paramIndex = 1;

  if (categoryId) {
    conditions.push(`category_id = $${paramIndex}`);
    values.push(categoryId);
    paramIndex++;
  }

  if (minPrice !== undefined) {
    conditions.push(`price >= $${paramIndex}`);
    values.push(minPrice);
    paramIndex++;
  }

  if (maxPrice !== undefined) {
    conditions.push(`price <= $${paramIndex}`);
    values.push(maxPrice);
    paramIndex++;
  }

  const whereClause = conditions.join(' AND ');

  // Query para produtos
  const productsQuery = `
    SELECT * FROM products
    WHERE ${whereClause}
    ORDER BY created_at DESC
    LIMIT $${paramIndex} OFFSET $${paramIndex + 1}
  `;

  // Query para total
  const totalQuery = `
    SELECT COUNT(*) as total FROM products
    WHERE ${whereClause}
  `;

  const [productsResult, totalResult] = await Promise.all([
    this.pool.query(productsQuery, [...values, limit, offset]),
    this.pool.query(totalQuery, values)
  ]);

  return {
    products: productsResult.rows,
    total: parseInt(totalResult.rows[0].total)
  };
}
```

## Anti-Patterns (Proibidos)

### ❌ NÃO FAÇA

- **SELECT \***: Sempre especifique colunas
- **N+1 queries**: Use JOIN ou IN
- **Sem índices**: Indexe colunas frequentemente consultadas
- **Hardcoded values**: Use parâmetros
- **Sem transações**: Use transações para operações críticas
- **Sem constraints**: Sempre defina constraints
- **Sem backups**: Configure backups automáticos

### ✅ SEMPRE FAÇA

- **Especifique colunas**: SELECT id, name, email FROM users
- **Use índices**: Para colunas de busca e ordenação
- **Use parâmetros**: Evite SQL injection
- **Use transações**: Para operações que modificam múltiplas tabelas
- **Defina constraints**: NOT NULL, UNIQUE, CHECK
- **Configure backups**: Automatize backups
- **Monitore performance**: Use EXPLAIN ANALYZE
