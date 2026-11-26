// Fixture F06-R2.1 | Version: 0.1.0 | Fecha: 2026-11-26
export function reserve(available, quantities) {
  if (!Number.isSafeInteger(available) || available < 0 ||
      !Array.isArray(quantities) || quantities.length === 0 ||
      quantities.some(q => !Number.isSafeInteger(q) || q <= 0)) {
    throw new TypeError('INVALID_INPUT');
  }
  if (quantities.some(q => q > available)) {
    return { ok: false, code: 'INSUFFICIENT_STOCK' };
  }
  const reserved = quantities.reduce((total, q) => total + q, 0);
  return { ok: true, reserved, remaining: available - reserved };
}
