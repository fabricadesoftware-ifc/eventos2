import { APIError, APIValidationError } from '~/api/exceptions'

function isObjectEmpty(obj) {
  return Object.keys(obj).length === 0
}

function isValidResponse(response) {
  return response.data && response.status < 500
}

export function handleAPIError(error) {
  if (error.response && isValidResponse(error.response)) {
    const data = error.response.data
    if (isObjectEmpty(data)) {
      throw new APIError(error)
    }
    throw new APIValidationError(error, data.detail || '', data)
  }
  throw error
}
