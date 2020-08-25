import { handleAPIError } from '~/api/utils'

export default function ({ $axios }) {
  $axios.onError(error => {
    if (
      error.config &&
      error.config.url &&
      error.config.url.startsWith('api/')
    ) {
      handleAPIError(error)
    }
  })
}
