module.exports = {
  root: true,
  env: {
    browser: true,
    node: true
  },
  parserOptions: {
    parser: '@babel/eslint-parser',
    requireConfigFile: false
  },
  extends: ['@nuxtjs', 'plugin:prettier/recommended'],
  plugins: ['vue'],
  rules: {
    // Disable camelcase
    // Makes it easier to work with API parameters and responses.
    camelcase: 'off',
    'no-console': 'warn',
    'no-debugger': 'warn',
    'vue/no-reserved-component-names': 'error',
    'vue/no-deprecated-scope-attribute': 'error',
    'vue/no-deprecated-slot-attribute': 'error',
    'vue/no-deprecated-slot-scope-attribute': 'error',
    'vue/multi-word-component-names': 'off'
  }
}
