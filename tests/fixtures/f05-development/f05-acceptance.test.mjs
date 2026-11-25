// Version: 0.1.0 | Fecha: 2026-11-24
// Aceptación protegida F05-C-DEV; no modificar para obtener PASS.
import test from 'node:test';
import assert from 'node:assert/strict';
import { createStore } from './f05-data.mjs';
import { reserveInventory } from './f05-service.mjs';
import { viewFor } from './f05-view.mjs';

const line = (sku, quantity) => ({ sku, locationId: 'L1', quantity });
const request = (idempotencyKey, lines) => ({ idempotencyKey, saleId: 'S1', lines });
const withStore = (fn) => {
  const store = createStore();
  try { fn(store); } finally { store.close(); }
};

test('validación: no llama almacenamiento con datos inválidos', () => {
  const store = { reserve() { assert.fail('No debe llamar store.reserve'); } };
  for (const req of [null, request('k', []), request('k', [line('A', 0)]),
    request('k', [line('A', 1.5)]), request('k', [line('A', 1), line('A', 2)]),
    request('', [line('A', 1)]), request('k', [line('A', Number.MAX_SAFE_INTEGER + 1)])]) {
    assert.deepEqual(reserveInventory(store, req), { ok: false, code: 'INVALID_REQUEST' });
  }
});

test('normalización: copia y orden determinista, una llamada', () => {
  const req = request('k', [line('B', 1), line('A', 1)]);
  const before = structuredClone(req);
  const result = { ok: true, reservationId: 'R1', saleId: 'S1', lines: [line('A', 1), line('B', 1)] };
  let calls = 0;
  const store = { reserve(normalized) {
    calls++;
    assert.deepEqual(normalized.lines, result.lines);
    return result;
  } };
  assert.deepEqual(reserveInventory(store, req), result);
  assert.equal(calls, 1);
  assert.deepEqual(req, before);
});

test('competencia secuencial y saldos', () => withStore(store => {
  const first = reserveInventory(store, request('k1', [line('A', 4)]));
  assert.equal(first.ok, true);
  assert.equal(typeof first.reservationId, 'string');
  assert.ok(first.reservationId.length > 0);
  const second = reserveInventory(store, request('k2', [line('A', 4)]));
  assert.deepEqual(second, { ok: false, code: 'INSUFFICIENT_STOCK', sku: 'A' });
  assert.deepEqual(store.getStock('A', 'L1'), { physical: 5, reserved: 4, available: 1 });
}));

test('idempotencia y conflicto de clave', () => withStore(store => {
  const req = request('k1', [line('A', 2)]);
  const first = reserveInventory(store, req);
  assert.equal(first.ok, true);
  assert.deepEqual(reserveInventory(store, req), first);
  assert.deepEqual(reserveInventory(store, request('k1', [line('A', 1)])),
    { ok: false, code: 'IDEMPOTENCY_KEY_REUSED' });
  assert.deepEqual(store.getStock('A', 'L1'), { physical: 5, reserved: 2, available: 3 });
}));

test('todo-o-nada y SKU no gestionado', () => withStore(store => {
  assert.deepEqual(reserveInventory(store, request('k1', [line('A', 1), line('B', 3)])),
    { ok: false, code: 'INSUFFICIENT_STOCK', sku: 'B' });
  assert.deepEqual(reserveInventory(store, request('k2', [line('A', 1), line('Z', 1)])),
    { ok: false, code: 'STOCK_NOT_MANAGED' });
  assert.deepEqual(store.getStock('A', 'L1'), { physical: 5, reserved: 0, available: 5 });
  assert.deepEqual(store.getStock('B', 'L1'), { physical: 2, reserved: 0, available: 2 });
  assert.equal(store.getStock('Z', 'L1'), null);
}));

test('estados de interfaz, sin confundir reserva con compra', () => {
  assert.deepEqual(viewFor('RESERVATION_PENDING'), {
    message: 'Solicitud de reserva enviada. Aún no se ha confirmado el resultado.', canSubmit: false
  });
  assert.deepEqual(viewFor('INSUFFICIENT_STOCK', 'A'), {
    message: 'No se reservó ningún producto porque no hay existencias suficientes de A.', canSubmit: true
  });
  assert.deepEqual(viewFor('RETRYABLE_CONFLICT'), {
    message: 'Conflicto técnico: no se pudo confirmar el resultado de la reserva.', canSubmit: false
  });
  assert.deepEqual(viewFor('RESERVED'), { message: 'Reserva confirmada.', canSubmit: false });
  assert.throws(() => viewFor('UNKNOWN'));
});
