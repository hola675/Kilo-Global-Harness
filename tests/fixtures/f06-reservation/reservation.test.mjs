// Fixture F06-R2.1 | Version: 0.1.0 | Fecha: 2026-11-26
import test from 'node:test';
import assert from 'node:assert/strict';
import { reserve } from './reservation.mjs';

test('reserva valida de varias lineas y conserva la entrada', () => {
  const quantities = Object.freeze([2, 3]);
  assert.deepEqual(reserve(8, quantities), { ok: true, reserved: 5, remaining: 3 });
  assert.deepEqual(quantities, [2, 3]);
});
test('consumo exacto del saldo', () => {
  assert.deepEqual(reserve(5, [2, 3]), { ok: true, reserved: 5, remaining: 0 });
});
test('rechazo por linea superior al saldo', () => {
  assert.deepEqual(reserve(5, [6]), { ok: false, code: 'INSUFFICIENT_STOCK' });
});
test('rechazo por suma superior al saldo', () => {
  assert.deepEqual(reserve(5, [3, 3]), { ok: false, code: 'INSUFFICIENT_STOCK' });
});
test('rechazo seguro con enteros grandes', () => {
  assert.deepEqual(reserve(Number.MAX_SAFE_INTEGER, [Number.MAX_SAFE_INTEGER, 1]),
    { ok: false, code: 'INSUFFICIENT_STOCK' });
});
test('entradas invalidas conservan el error contractual', () => {
  for (const [stock, lines] of [[-1, [1]], [1, []], [1, [0]], [1, [-1]], [1, [0.5]], [1, [NaN]], [1, ['1']], [1, null], [Infinity, [1]]]) {
    assert.throws(() => reserve(stock, lines), { name: 'TypeError', message: 'INVALID_INPUT' });
  }
});
