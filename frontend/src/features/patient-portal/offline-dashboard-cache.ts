import Dexie, { type Table } from "dexie";

export type PatientDashboardSnapshot = {
  patient: { id: string; display_name: string };
  counts: {
    upcoming_appointments: number;
    active_prescriptions: number;
    lab_reports: number;
    documents: number;
  };
  upcoming_appointment: {
    provider_name: string;
    scheduled_start: string;
    appointment_type: string;
    status: string;
    is_virtual: boolean;
  } | null;
  health_updates: Array<{
    id: string;
    category: string;
    title: string;
    occurred_at: string;
  }>;
};

export type OfflineDashboardSnapshot = {
  data: PatientDashboardSnapshot;
  updatedAt: string;
};

type EncryptedDashboardRecord = {
  id: string;
  salt: string;
  iv: string;
  ciphertext: string;
  updatedAt: string;
  expiresAt: string;
};

type EncryptedDashboardPayload = {
  email: string;
  data: PatientDashboardSnapshot;
};

class PatientOfflineDatabase extends Dexie {
  snapshots!: Table<EncryptedDashboardRecord, string>;

  public constructor() {
    super("datavion-patient-offline");
    this.version(1).stores({
      snapshots: "id,updatedAt,expiresAt",
    });
  }
}

const CACHE_TTL_DAYS = 14;
const PBKDF2_ITERATIONS = 310_000;
const DEVICE_SNAPSHOT_ID = "patient-dashboard";
let database: PatientOfflineDatabase | undefined;
const unlockedKeys = new Map<string, CryptoKey>();

function getDatabase(): PatientOfflineDatabase {
  database ??= new PatientOfflineDatabase();
  return database;
}

function requireCrypto(): Crypto {
  if (typeof window === "undefined" || !window.crypto?.subtle) {
    throw new Error("Encrypted offline access requires a secure browser context.");
  }
  return window.crypto;
}

function encodeBase64(value: Uint8Array): string {
  let binary = "";
  for (const byte of value) binary += String.fromCharCode(byte);
  return window.btoa(binary);
}

function decodeBase64(value: string): Uint8Array<ArrayBuffer> {
  const binary = window.atob(value);
  const bytes = new Uint8Array(new ArrayBuffer(binary.length));
  for (let index = 0; index < binary.length; index += 1) {
    bytes[index] = binary.charCodeAt(index);
  }
  return bytes;
}

function cacheId(): string {
  return DEVICE_SNAPSHOT_ID;
}

async function deriveKey(passphrase: string, salt: Uint8Array<ArrayBuffer>): Promise<CryptoKey> {
  if (passphrase.trim().length < 10) {
    throw new Error("Choose an offline passphrase with at least 10 characters.");
  }
  const crypto = requireCrypto();
  const material = await crypto.subtle.importKey(
    "raw",
    new TextEncoder().encode(passphrase),
    "PBKDF2",
    false,
    ["deriveKey"],
  );
  return crypto.subtle.deriveKey(
    {
      name: "PBKDF2",
      salt,
      iterations: PBKDF2_ITERATIONS,
      hash: "SHA-256",
    },
    material,
    { name: "AES-GCM", length: 256 },
    false,
    ["encrypt", "decrypt"],
  );
}

async function encryptSnapshot(
  email: string,
  data: PatientDashboardSnapshot,
  key: CryptoKey,
): Promise<{ iv: string; ciphertext: string }> {
  const iv = requireCrypto().getRandomValues(new Uint8Array(12));
  const ciphertext = await requireCrypto().subtle.encrypt(
    { name: "AES-GCM", iv },
    key,
    new TextEncoder().encode(JSON.stringify({
      email: email.trim().toLocaleLowerCase(),
      data,
    } satisfies EncryptedDashboardPayload)),
  );
  return {
    iv: encodeBase64(iv),
    ciphertext: encodeBase64(new Uint8Array(ciphertext)),
  };
}

async function decryptSnapshot(
  record: EncryptedDashboardRecord,
  key: CryptoKey,
): Promise<EncryptedDashboardPayload> {
  try {
    const plaintext = await requireCrypto().subtle.decrypt(
      { name: "AES-GCM", iv: decodeBase64(record.iv) },
      key,
      decodeBase64(record.ciphertext),
    );
    return JSON.parse(new TextDecoder().decode(plaintext)) as EncryptedDashboardPayload;
  } catch {
    throw new Error("That offline passphrase did not unlock this patient’s saved data.");
  }
}

function expiresAtFrom(now: Date): string {
  const expiresAt = new Date(now);
  expiresAt.setDate(expiresAt.getDate() + CACHE_TTL_DAYS);
  return expiresAt.toISOString();
}

function assertSamePatient(
  existing: EncryptedDashboardPayload,
  email: string,
  incoming: PatientDashboardSnapshot,
): void {
  if (existing.email !== email.trim().toLocaleLowerCase() || existing.data.patient.id !== incoming.patient.id) {
    throw new Error("This email’s offline copy belongs to a different patient. Remove it before enabling a new copy.");
  }
}

export async function getOfflineDashboardCacheInfo(
): Promise<{ exists: boolean; updatedAt: string | null; expired: boolean }> {
  const id = await cacheId();
  const record = await getDatabase().snapshots.get(id);
  if (!record) return { exists: false, updatedAt: null, expired: false };
  return {
    exists: true,
    updatedAt: record.updatedAt,
    expired: Date.now() >= Date.parse(record.expiresAt),
  };
}

export async function saveOfflineDashboardSnapshot(
  email: string,
  passphrase: string,
  data: PatientDashboardSnapshot,
): Promise<OfflineDashboardSnapshot> {
  const id = await cacheId();
  const table = getDatabase().snapshots;
  const existing = await table.get(id);
  const now = new Date();
  const salt = existing
    ? decodeBase64(existing.salt)
    : requireCrypto().getRandomValues(new Uint8Array(16));
  const key = await deriveKey(passphrase, salt);

  if (existing) {
    const previousSnapshot = await decryptSnapshot(existing, key);
    assertSamePatient(previousSnapshot, email, data);
  }

  const encrypted = await encryptSnapshot(email, data, key);
  const record: EncryptedDashboardRecord = {
    id,
    salt: encodeBase64(salt),
    ...encrypted,
    updatedAt: now.toISOString(),
    expiresAt: expiresAtFrom(now),
  };
  await table.put(record);
  unlockedKeys.set(id, key);
  return { data, updatedAt: record.updatedAt };
}

export async function unlockOfflineDashboardSnapshot(
  passphrase: string,
): Promise<OfflineDashboardSnapshot> {
  const id = await cacheId();
  const record = await getDatabase().snapshots.get(id);
  if (!record) throw new Error("No offline copy is saved on this device.");
  if (Date.now() >= Date.parse(record.expiresAt)) {
    throw new Error("This offline copy has expired. Connect to the internet and sync again.");
  }

  const key = await deriveKey(passphrase, decodeBase64(record.salt));
  const payload = await decryptSnapshot(record, key);
  unlockedKeys.set(id, key);
  return { data: payload.data, updatedAt: record.updatedAt };
}

export async function refreshUnlockedOfflineDashboardSnapshot(
  email: string,
  data: PatientDashboardSnapshot,
): Promise<OfflineDashboardSnapshot | null> {
  const id = await cacheId();
  const key = unlockedKeys.get(id);
  if (!key) return null;
  const table = getDatabase().snapshots;
  const existing = await table.get(id);
  if (!existing) {
    unlockedKeys.delete(id);
    return null;
  }

  const previousSnapshot = await decryptSnapshot(existing, key);
  assertSamePatient(previousSnapshot, email, data);
  const now = new Date();
  const encrypted = await encryptSnapshot(email, data, key);
  const record: EncryptedDashboardRecord = {
    ...existing,
    ...encrypted,
    updatedAt: now.toISOString(),
    expiresAt: expiresAtFrom(now),
  };
  await table.put(record);
  return { data, updatedAt: record.updatedAt };
}

export async function deleteOfflineDashboardSnapshot(): Promise<void> {
  const id = await cacheId();
  await getDatabase().snapshots.delete(id);
  unlockedKeys.delete(id);
}

export function clearUnlockedOfflineDashboardKeys(): void {
  unlockedKeys.clear();
}
