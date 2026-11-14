/**
 * VX Observer Light V4.4 — plugin exclusivamente global de Kilo Code.
 *
 * Metadatos permitidos: tipo de evento, franja horaria UTC y contador.
 * NO lee ni almacena prompts, respuestas, paths, codigo, errores completos,
 * herramientas, tokens, modelos o IDs de sesion.
 *
 * Auto-cargado por Kilo si el usuario opta por instalarlo; INERTE hasta
 * observer-mode light. No crea hooks de escritura ni modifica mensajes.
 * API: https://kilo.ai/docs/automate/extending/plugins
 */
import { existsSync } from "node:fs";
import { spawn } from "node:child_process";
import { homedir } from "node:os";
import { join } from "node:path";

const HOME = homedir();
const BASE = join(HOME, ".config", "kilo");
const FLAG = join(BASE, "vx-evolution", "observer-light.flag");
const CORE = join(BASE, "harness", "scripts", "vx_evolution_core.py");
const TYPES = Object.freeze({
  "session.idle": "session_idle",
  "session.error": "session_error",
  "session.compacted": "session_compacted",
});
const RATE_MS = 10_000;
const MAX_PLUGIN_EVENTS_PER_HOUR = 120;
const MAX_RECENT_KEYS = 256;
const recent = new Map();
let hourStart = 0;
let emittedThisHour = 0;

function safeSessionKey(event, type) {
  // Se usa SOLO en memoria para suprimir callbacks duplicados, no se transmite.
  const raw = event?.properties?.sessionID ?? event?.data?.sessionID;
  const id = typeof raw === "string" && raw.length <= 128 ? raw : "__unknown__";
  return type + ":" + id;
}

function minimumEnv() {
  const keep = ["PATH", "Path", "PATHEXT", "SystemRoot", "SYSTEMROOT",
    "WINDIR", "TEMP", "TMP", "HOME", "USERPROFILE", "LOCALAPPDATA"];
  const env = { PYTHONUTF8: "1", PYTHONDONTWRITEBYTECODE: "1" };
  for (const name of keep) {
    if (typeof process.env[name] === "string") env[name] = process.env[name];
  }
  return env;
}

export default {
  id: "vx-observer-light",
  server: async () => ({
    event: async ({ event }) => {
      // El hook se llama para MUCHOS eventos; no inspeccionar otros payloads.
      const kind = event?.type;
      const signal = typeof kind === "string" && Object.hasOwn(TYPES, kind)
        ? TYPES[kind] : undefined;
      if (!signal) return;
      if (!existsSync(FLAG) || !existsSync(CORE)) return;
      const now = Date.now();
      if (now - hourStart >= 3_600_000) {
        hourStart = now;
        emittedThisHour = 0;
        recent.clear();
      }
      if (emittedThisHour >= MAX_PLUGIN_EVENTS_PER_HOUR) return;
      const key = safeSessionKey(event, signal);
      const last = recent.get(key) ?? 0;
      if (last && now - last < RATE_MS) return;
      recent.set(key, now);
      if (recent.size > MAX_RECENT_KEYS) {
        // Limitar RAM de instancias largas; no exportar IDs ni registrar logs.
        recent.delete(recent.keys().next().value);
      }
      emittedThisHour++;
      try {
        // Sin shell; argumentos de lista blanca; no se pasan datos de sesion.
        const interpreter = process.platform === "win32" ? "python" : "python3";
        const child = spawn(interpreter,
          ["-I", CORE, "observer-event", "--event", signal], {
            cwd: HOME, env: minimumEnv(), shell: false, windowsHide: true,
            stdio: "ignore",
          });
        child.on("error", () => { /* sin logs sensibles; no bloquear Kilo */ });
        child.unref();
      } catch (_) {
        // Un fallo del observador NUNCA detiene la sesion ni el modelo.
      }
    },
  }),
};
