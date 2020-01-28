export class APIError extends Error {
  constructor(cause, message) {
    super(message)
    this.name = 'APIError'
    this.cause = cause
  }
}

export class APIValidationError extends APIError {
  constructor(cause, message, fields) {
    super(cause, message)
    this.name = 'APIValidationError'
    this.fields = fields || {}
  }
}
