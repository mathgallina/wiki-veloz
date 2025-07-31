module.exports = {
  env: {
    browser: true,
    es2021: true,
    node: true,
  },
  extends: ['eslint:recommended', 'plugin:@typescript-eslint/recommended'],
  parser: '@typescript-eslint/parser',
  parserOptions: {
    ecmaVersion: 'latest',
    sourceType: 'module',
  },
  plugins: ['@typescript-eslint'],
  rules: {
    // CDD v2.0 - Convenções de nomenclatura
    camelcase: ['error', { properties: 'always' }],
    'no-underscore-dangle': 'off',

    // CDD v2.0 - Imports obrigatórios
    'import/order': [
      'error',
      {
        groups: ['builtin', 'external', 'internal', 'parent', 'sibling', 'index'],
        'newlines-between': 'always',
        alphabetize: {
          order: 'asc',
          caseInsensitive: true,
        },
      },
    ],

    // CDD v2.0 - Anti-patterns proibidos
    'no-console': 'warn',
    'no-debugger': 'error',
    'no-alert': 'error',
    'no-eval': 'error',
    'no-implied-eval': 'error',
    'no-new-func': 'error',
    'no-script-url': 'error',

    // CDD v2.0 - Performance
    'no-unused-vars': 'error',
    'no-unused-expressions': 'error',
    'prefer-const': 'error',
    'no-var': 'error',

    // CDD v2.0 - Legibilidade
    'max-len': ['error', { code: 100 }],
    indent: ['error', 2],
    quotes: ['error', 'single'],
    semi: ['error', 'always'],
    'comma-dangle': ['error', 'always-multiline'],

    // CDD v2.0 - TypeScript específico
    '@typescript-eslint/no-unused-vars': 'error',
    '@typescript-eslint/explicit-function-return-type': 'warn',
    '@typescript-eslint/no-explicit-any': 'warn',
    '@typescript-eslint/prefer-interface': 'error',

    // CDD v2.0 - React patterns (se aplicável)
    'react/jsx-uses-react': 'off',
    'react/react-in-jsx-scope': 'off',
    'react/prop-types': 'off',

    // CDD v2.0 - Error handling
    'no-throw-literal': 'error',
    'prefer-promise-reject-errors': 'error',

    // CDD v2.0 - Security
    'no-implied-eval': 'error',
    'no-new-func': 'error',
    'no-script-url': 'error',
  },
  overrides: [
    {
      files: ['*.test.js', '*.test.ts', '*.test.tsx'],
      env: {
        jest: true,
      },
      rules: {
        '@typescript-eslint/no-explicit-any': 'off',
      },
    },
  ],
};
