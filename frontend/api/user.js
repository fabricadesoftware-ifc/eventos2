export function createUserAPIClient($axios) {
  return {
    list({ email }) {
      return $axios.$get(`api/v1/users/?email=${email}`)
    },
    create({ first_name, last_name, email, password }) {
      return $axios.$post('api/v1/users/', {
        first_name,
        last_name,
        email,
        password
      })
    },
    update({ first_name, last_name }) {
      return $axios.$put('api/v1/users/current/', {
        first_name,
        last_name
      })
    }
  }
}
