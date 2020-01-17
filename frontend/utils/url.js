export function parseEventSlug(host) {
  const names = host.split('.')
  if (names.length <= 2) {
    return null
  }
  return names[0]
}
