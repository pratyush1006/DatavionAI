import {
  defineConfig,
  globalIgnores,
} from "eslint/config";

import nextVitals from "eslint-config-next/core-web-vitals";
import nextTs from "eslint-config-next/typescript";

const eslintConfig = defineConfig([
  ...nextVitals,
  ...nextTs,

  {
    files: [
      "src/components/common/table/entity-table.tsx",
    ],
    rules: {
      "react-hooks/incompatible-library": "off",
    },
  },

  // Override default ignores of eslint-config-next.
  globalIgnores([
    ".next/**",
    "out/**",
    "build/**",
    "next-env.d.ts",
    "node_modules/**",
    "playwright-report/**",
    "playwright-report-*/**",
    "test-results/**",
    ".datavion-backups/**",
    ".datavion-installer-backups/**",
    ".datavionos-backups/**",
    ".datavionos_auth_backups/**",
    ".datavionos_navigation_backups/**",
    ".datavionos_route_backups/**",
    ".datavionos_runtime_backups/**",
    ".datavionos_runtime_context_backups/**",
    ".datavionos_runtime_contract_backups/**",
    ".datavion_backups/**",
    ".datavion_installer_backups/**",
    ".datavionos_installer_backups/**",
    "e2e/**",
    "e2e-saas-business/**",
    "e2e-saas-business-runtime/**",
]),
]);

export default eslintConfig;
