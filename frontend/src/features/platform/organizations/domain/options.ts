/**
 * Organization domain options.
 */

import {
  ORGANIZATION_TYPES,
} from "./types";

export const organizationTypeOptions =
  ORGANIZATION_TYPES.map((type) => ({
    value: type,
    label: type
      .replaceAll("_", " ")
      .toLowerCase()
      .replace(
        /\b\w/g,
        (char) => char.toUpperCase(),
      ),
  }));
