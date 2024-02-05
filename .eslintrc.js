module.exports = {
  env: {
    browser: true,
    es2021: true,
  },
  extends: ["eslint:recommended"],
  overrides: [
    {
      env: {
        node: true,
      },
      files: [".eslintrc.{js,cjs}"],
      parserOptions: {
        sourceType: "script",
      },
    },
  ],
  parserOptions: {
    ecmaVersion: "latest",
    sourceType: "module",
  },
  plugins: [],
  rules: {
    "no-unused-vars": ["error", { args: "after-used" }],
  },
  ignorePatterns: [
    "jupyter_remote_desktop_proxy/static/dist/**",
    "webpack.config.js",
  ],
};
