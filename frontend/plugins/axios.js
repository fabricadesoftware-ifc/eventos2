import { handleAPIError } from '~/api/utils'

export default function({ $axios }) {
  $axios.onError(error => {
    if (error.response.config.url.startsWith('api/')) {
      handleAPIError(error)
    }
  })
}
