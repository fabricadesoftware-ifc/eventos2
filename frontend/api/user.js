import { handleAxiosError } from '~/api/utils'

export function createUserAPIClient($axios) {
  return {
    create({ first_name, last_name, email, password }) {
      return $axios
        .$post('api/v1/users/', {
          first_name,
          last_name,
          email,
          password
        })
        .catch(handleAxiosError)
    },
    update({ first_name, last_name }) {
      return $axios.$put('api/v1/users/current/', {
        first_name,
        last_name
      })
    }
  }
}
