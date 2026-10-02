import type {
  EffectiveCapabilityContext,
} from "../types/capability";

export function hasCapability(
  context: EffectiveCapabilityContext | null,
  capability: string,
): boolean {
  if (!context) {
    return false;
  }

  if (context.capabilities?.[capability] === true) {
    return true;
  }

  if (context.features?.[capability] === true) {
    return true;
  }

  return false;
}

export function hasModule(
  context: EffectiveCapabilityContext | null,
  moduleKey: string,
): boolean {
  return context?.modules?.[moduleKey] === true;
}

export function hasPermission(
  context: EffectiveCapabilityContext | null,
  permission: string,
): boolean {
  return context?.permissions?.includes(permission) === true;
}

export function isPlatformUser(
  context: EffectiveCapabilityContext | null,
): boolean {
  return (
    context?.roles?.includes("platform_admin") === true ||
    context?.roles?.includes("platform_user") === true
  );
}

export function isOrganizationAdmin(
  context: EffectiveCapabilityContext | null,
): boolean {
  return (
    context?.roles?.includes("organization_admin") === true ||
    context?.roles?.includes("org_admin") === true
  );
}

/**
 * Resolve whether a capability is active in the effective
 * capability context returned by the backend.
 *
 * Supported backend representations:
 *
 * 1. Direct boolean
 *    {
 *      "pharmacy": true
 *    }
 *
 * 2. Capability map
 *    {
 *      "capabilities": {
 *        "pharmacy": true
 *      }
 *    }
 *
 * 3. Capability object
 *    {
 *      "capabilities": [
 *        {
 *          "key": "pharmacy",
 *          "enabled": true
 *        }
 *      ]
 *    }
 *
 * 4. Feature map
 *    {
 *      "features": {
 *        "pharmacy": true
 *      }
 *    }
 *
 * 5. Effective capability map
 *    {
 *      "effective_capabilities": {
 *        "pharmacy": true
 *      }
 *    }
 *
 * The frontend never becomes an authority. It only resolves the
 * effective capability context supplied by the backend.
 */
export function resolveCapability(
  context: unknown,
  capability: string,
): boolean {
  if (!context || !capability) {
    return false;
  }

  const root = context as Record<string, unknown>;

  const direct = root[capability];

  if (direct === true) {
    return true;
  }

  if (direct === false) {
    return false;
  }

  const containers: unknown[] = [
    root.capabilities,
    root.effective_capabilities,
    root.effectiveCapabilities,
    root.permissions,
    root.entitlements,
    root.features,
    root.modules,
  ];

  for (const container of containers) {
    if (Array.isArray(container)) {
      if (container.includes(capability)) {
        return true;
      }

      const match = container.find((item) => {
        if (typeof item === "string") {
          return item === capability;
        }

        if (!item || typeof item !== "object") {
          return false;
        }

        const record = item as Record<string, unknown>;

        const identityMatches =
          record.key === capability ||
          record.code === capability ||
          record.name === capability ||
          record.slug === capability ||
          record.module === capability ||
          record.module_key === capability ||
          record.moduleKey === capability ||
          record.capability === capability;

        if (!identityMatches) {
          return false;
        }

        if (record.enabled === false) {
          return false;
        }

        if (record.active === false) {
          return false;
        }

        if (record.is_enabled === false) {
          return false;
        }

        if (record.isEnabled === false) {
          return false;
        }

        return true;
      });

      if (match !== undefined) {
        return true;
      }
    }

    if (container && typeof container === "object") {
      const record = container as Record<string, unknown>;

      const value = record[capability];

      if (value === true) {
        return true;
      }

      if (value === false) {
        continue;
      }

      if (value && typeof value === "object") {
        const capabilityRecord = value as Record<string, unknown>;

        if (capabilityRecord.enabled === true) {
          return true;
        }

        if (capabilityRecord.active === true) {
          return true;
        }

        if (capabilityRecord.is_enabled === true) {
          return true;
        }

        if (capabilityRecord.isEnabled === true) {
          return true;
        }
      }
    }
  }

  return false;
}
