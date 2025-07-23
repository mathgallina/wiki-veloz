# Padrões Node.js - CDD v2.0

## Estrutura de Projeto

### Estrutura Obrigatória

```
src/
├── controllers/          # Controladores de API
├── services/            # Lógica de negócio
├── models/              # Modelos de dados
├── middleware/          # Middlewares customizados
├── routes/              # Definição de rotas
├── utils/               # Utilitários
├── types/               # Definições TypeScript
├── config/              # Configurações
└── tests/               # Testes
```

## Padrões de API

### Controller Pattern

```typescript
// controllers/UserController.ts
import { Request, Response } from 'express';
import { UserService } from '../services/UserService';
import { ApiResponse } from '../types/ApiResponse';

export class UserController {
  private userService: UserService;

  constructor() {
    this.userService = new UserService();
  }

  public async createUser(req: Request, res: Response): Promise<void> {
    try {
      const { name, email, password } = req.body;

      // Validação de entrada
      if (!name || !email || !password) {
        const response: ApiResponse = {
          success: false,
          message: 'Missing required fields',
          errors: ['name', 'email', 'password'],
        };
        res.status(400).json(response);
        return;
      }

      // Lógica de negócio
      const user = await this.userService.createUser({ name, email, password });

      const response: ApiResponse = {
        success: true,
        data: user,
        message: 'User created successfully',
      };

      res.status(201).json(response);
    } catch (error) {
      console.error('UserController.createUser error:', error);

      const response: ApiResponse = {
        success: false,
        message: 'Internal server error',
        error: error instanceof Error ? error.message : 'Unknown error',
      };

      res.status(500).json(response);
    }
  }

  public async getUserById(req: Request, res: Response): Promise<void> {
    try {
      const { id } = req.params;
      const user = await this.userService.getUserById(id);

      if (!user) {
        const response: ApiResponse = {
          success: false,
          message: 'User not found',
        };
        res.status(404).json(response);
        return;
      }

      const response: ApiResponse = {
        success: true,
        data: user,
      };

      res.status(200).json(response);
    } catch (error) {
      console.error('UserController.getUserById error:', error);

      const response: ApiResponse = {
        success: false,
        message: 'Internal server error',
        error: error instanceof Error ? error.message : 'Unknown error',
      };

      res.status(500).json(response);
    }
  }
}
```

### Service Pattern

```typescript
// services/UserService.ts
import { User } from '../models/User';
import { CreateUserDto } from '../types/CreateUserDto';
import { UserRepository } from '../repositories/UserRepository';
import { HashService } from './HashService';

export class UserService {
  private userRepository: UserRepository;
  private hashService: HashService;

  constructor() {
    this.userRepository = new UserRepository();
    this.hashService = new HashService();
  }

  public async createUser(userData: CreateUserDto): Promise<User> {
    // Validação de negócio
    const existingUser = await this.userRepository.findByEmail(userData.email);
    if (existingUser) {
      throw new Error('User with this email already exists');
    }

    // Hash da senha
    const hashedPassword = await this.hashService.hash(userData.password);

    // Criação do usuário
    const user = await this.userRepository.create({
      ...userData,
      password: hashedPassword,
    });

    // Remove senha do retorno
    const { password, ...userWithoutPassword } = user;
    return userWithoutPassword;
  }

  public async getUserById(id: string): Promise<User | null> {
    const user = await this.userRepository.findById(id);

    if (!user) {
      return null;
    }

    // Remove senha do retorno
    const { password, ...userWithoutPassword } = user;
    return userWithoutPassword;
  }

  public async updateUser(
    id: string,
    updateData: Partial<CreateUserDto>
  ): Promise<User> {
    const user = await this.userRepository.findById(id);
    if (!user) {
      throw new Error('User not found');
    }

    // Hash da senha se fornecida
    if (updateData.password) {
      updateData.password = await this.hashService.hash(updateData.password);
    }

    const updatedUser = await this.userRepository.update(id, updateData);

    // Remove senha do retorno
    const { password, ...userWithoutPassword } = updatedUser;
    return userWithoutPassword;
  }
}
```

## Padrões de Middleware

### Error Handling Middleware

```typescript
// middleware/errorHandler.ts
import { Request, Response, NextFunction } from 'express';
import { ApiError } from '../types/ApiError';

export const errorHandler = (
  error: Error,
  req: Request,
  res: Response,
  next: NextFunction
): void => {
  console.error('Error:', error);

  if (error instanceof ApiError) {
    res.status(error.statusCode).json({
      success: false,
      message: error.message,
      errors: error.errors,
    });
    return;
  }

  // Erro padrão
  res.status(500).json({
    success: false,
    message: 'Internal server error',
    error: process.env.NODE_ENV === 'development' ? error.message : 'Unknown error',
  });
};
```

### Authentication Middleware

```typescript
// middleware/auth.ts
import { Request, Response, NextFunction } from 'express';
import jwt from 'jsonwebtoken';
import { ApiError } from '../types/ApiError';

interface AuthenticatedRequest extends Request {
  user?: {
    id: string;
    email: string;
    role: string;
  };
}

export const authenticateToken = (
  req: AuthenticatedRequest,
  res: Response,
  next: NextFunction
): void => {
  const authHeader = req.headers.authorization;
  const token = authHeader && authHeader.split(' ')[1];

  if (!token) {
    throw new ApiError('Access token required', 401);
  }

  try {
    const decoded = jwt.verify(token, process.env.JWT_SECRET!) as any;
    req.user = {
      id: decoded.id,
      email: decoded.email,
      role: decoded.role,
    };
    next();
  } catch (error) {
    throw new ApiError('Invalid token', 401);
  }
};

export const requireRole = (roles: string[]) => {
  return (req: AuthenticatedRequest, res: Response, next: NextFunction): void => {
    if (!req.user) {
      throw new ApiError('Authentication required', 401);
    }

    if (!roles.includes(req.user.role)) {
      throw new ApiError('Insufficient permissions', 403);
    }

    next();
  };
};
```

### Validation Middleware

```typescript
// middleware/validation.ts
import { Request, Response, NextFunction } from 'express';
import { z } from 'zod';
import { ApiError } from '../types/ApiError';

export const validateRequest = (schema: z.ZodSchema) => {
  return (req: Request, res: Response, next: NextFunction): void => {
    try {
      const validatedData = schema.parse({
        body: req.body,
        query: req.query,
        params: req.params,
      });

      req.body = validatedData.body;
      req.query = validatedData.query;
      req.params = validatedData.params;

      next();
    } catch (error) {
      if (error instanceof z.ZodError) {
        throw new ApiError('Validation failed', 400, error.errors);
      }
      next(error);
    }
  };
};
```

## Padrões de Rotas

### Route Definition

```typescript
// routes/userRoutes.ts
import { Router } from 'express';
import { UserController } from '../controllers/UserController';
import { authenticateToken, requireRole } from '../middleware/auth';
import { validateRequest } from '../middleware/validation';
import { createUserSchema, updateUserSchema } from '../schemas/userSchemas';

const router = Router();
const userController = new UserController();

// Rotas públicas
router.post(
  '/register',
  validateRequest(createUserSchema),
  userController.createUser.bind(userController)
);

router.post('/login', userController.login.bind(userController));

// Rotas protegidas
router.get(
  '/profile',
  authenticateToken,
  userController.getProfile.bind(userController)
);

router.put(
  '/profile',
  authenticateToken,
  validateRequest(updateUserSchema),
  userController.updateProfile.bind(userController)
);

// Rotas administrativas
router.get(
  '/users',
  authenticateToken,
  requireRole(['admin']),
  userController.getAllUsers.bind(userController)
);

router.get(
  '/users/:id',
  authenticateToken,
  requireRole(['admin']),
  userController.getUserById.bind(userController)
);

export default router;
```

## Padrões de Configuração

### Environment Configuration

```typescript
// config/environment.ts
import { z } from 'zod';

const envSchema = z.object({
  NODE_ENV: z.enum(['development', 'production', 'test']),
  PORT: z.string().transform(Number),
  DATABASE_URL: z.string(),
  JWT_SECRET: z.string(),
  JWT_EXPIRES_IN: z.string().default('1d'),
  CORS_ORIGIN: z.string().optional(),
  LOG_LEVEL: z.enum(['error', 'warn', 'info', 'debug']).default('info'),
});

export const config = envSchema.parse(process.env);

export type Config = typeof config;
```

### Database Configuration

```typescript
// config/database.ts
import { Pool } from 'pg';
import { config } from './environment';

export const pool = new Pool({
  connectionString: config.DATABASE_URL,
  ssl: config.NODE_ENV === 'production' ? { rejectUnauthorized: false } : false,
  max: 20,
  idleTimeoutMillis: 30000,
  connectionTimeoutMillis: 2000,
});

pool.on('error', err => {
  console.error('Unexpected error on idle client', err);
  process.exit(-1);
});
```

## Padrões de Teste

### Unit Test

```typescript
// tests/services/UserService.test.ts
import { UserService } from '../../services/UserService';
import { UserRepository } from '../../repositories/UserRepository';
import { HashService } from '../../services/HashService';

jest.mock('../../repositories/UserRepository');
jest.mock('../../services/HashService');

describe('UserService', () => {
  let userService: UserService;
  let mockUserRepository: jest.Mocked<UserRepository>;
  let mockHashService: jest.Mocked<HashService>;

  beforeEach(() => {
    mockUserRepository = new UserRepository() as jest.Mocked<UserRepository>;
    mockHashService = new HashService() as jest.Mocked<HashService>;
    userService = new UserService();
  });

  describe('createUser', () => {
    it('should create user successfully', async () => {
      const userData = {
        name: 'John Doe',
        email: 'john@example.com',
        password: 'password123',
      };

      const hashedPassword = 'hashedPassword123';
      const createdUser = {
        id: '1',
        ...userData,
        password: hashedPassword,
      };

      mockHashService.hash.mockResolvedValue(hashedPassword);
      mockUserRepository.findByEmail.mockResolvedValue(null);
      mockUserRepository.create.mockResolvedValue(createdUser);

      const result = await userService.createUser(userData);

      expect(mockHashService.hash).toHaveBeenCalledWith(userData.password);
      expect(mockUserRepository.findByEmail).toHaveBeenCalledWith(userData.email);
      expect(mockUserRepository.create).toHaveBeenCalledWith({
        ...userData,
        password: hashedPassword,
      });
      expect(result.password).toBeUndefined();
    });

    it('should throw error if user already exists', async () => {
      const userData = {
        name: 'John Doe',
        email: 'john@example.com',
        password: 'password123',
      };

      mockUserRepository.findByEmail.mockResolvedValue({ id: '1', ...userData });

      await expect(userService.createUser(userData)).rejects.toThrow(
        'User with this email already exists'
      );
    });
  });
});
```

## Anti-Patterns (Proibidos)

### ❌ NÃO FAÇA

- **Lógica de negócio em controllers**: Use services
- **Queries SQL em controllers**: Use repositories
- **Hardcoded secrets**: Use environment variables
- **Synchronous operations**: Use async/await
- **No error handling**: Sempre trate erros
- **No input validation**: Sempre valide entrada
- **No logging**: Sempre logue operações importantes

### ✅ SEMPRE FAÇA

- **Separation of concerns**: Controllers, services, repositories
- **Error handling**: Try/catch em todas as operações
- **Input validation**: Valide entrada com Zod
- **Environment configuration**: Use variáveis de ambiente
- **Logging**: Log operações importantes
- **TypeScript**: Use types para type safety
- **Testing**: Teste unitário para services
