/**
 * Serialize JSON-LD for an inline script safely.
 *
 * JSON is valid inside a script tag, but raw `<`, `>` and `&` characters can
 * still be interpreted as HTML by the browser. Escaping them preserves the
 * JSON value while preventing a data value from closing the script element.
 */
export function serializeJsonLd(value: unknown): string {
  const json = JSON.stringify(value);
  if (json === undefined) return '';

  return json
    .replace(/</g, '\\u003c')
    .replace(/>/g, '\\u003e')
    .replace(/&/g, '\\u0026')
    .replace(/\u2028/g, '\\u2028')
    .replace(/\u2029/g, '\\u2029');
}
